import customtkinter
from customtkinter import CTkImage
from PIL import Image
from tkinter import messagebox
import os
import sys
import random

import logica_file

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

#Ruta para empaquetar
#pyinstaller --onefile --noconsole --add-data "consulta_saldo.png;." --add-data "deposito.png;." --add-data "retiro.png;." --add-data "transferencia.png;." --add-data "images.ico;." main.py

class App:
    def __init__(self):
        self.ventana = customtkinter.CTk()
        self.ventana.title("Tu Banco")
        self.ventana.iconbitmap(self.obtener_ruta_recurso("images.ico"))
        # self.ventana.geometry("500x400")


        # Declarar los atributos para los campos de entrada
        self.usuario_entry = None
        self.contraseña_entry = None
        self.numero_cuenta_entry = None
        self.monto_inicial_entry = None

        #Atributos campos de entrada login
        self.usuario_login_entry = None
        self.password_login_entry = None

        #Atributo campo de entrada deposito y retiro
        self.deposito_entry = None
        self.retiro_entry = None

        #Atributo campo de transferencia
        self.transferencia_cuenta_entry = None
        self.transferencia_monto_entry = None

        # Frame principal con scrollbar
        self.scrollable_frame = customtkinter.CTkScrollableFrame(master=self.ventana, corner_radius=15)
        self.scrollable_frame.pack(pady=20, padx=60, fill="both", expand=True)

        # Título general
        self.titulo = customtkinter.CTkLabel(self.scrollable_frame, text="", font=("Montserrat", 22))
        self.titulo.pack(pady=12, padx=10)

        # Mostrar ventana de inicio de sesión
        self.iniciar_sesion()

        self.logica = logica_file.logica(self)

        self.ventana.mainloop()

    def centrar_ventana(self):
        pantalla_ancho = self.ventana.winfo_screenwidth()
        pantalla_alto = self.ventana.winfo_screenheight()
        x = (pantalla_ancho // 2) - (400 // 2)
        y = (pantalla_alto // 2) - (300 // 2)
        self.ventana.geometry(f"{750}x{450}+{x}+{y}")
    def limpiar_frame(self):
        for widget in self.scrollable_frame.winfo_children():
            if widget != self.titulo:
                widget.destroy()

    def mostrar_info(self, titulo, texto):
        messagebox.showinfo(titulo, texto)

    def cargar_imagen(self, ruta_relativa, tamaño=(200, 200)):
        # Construir la ruta absoluta considerando sys._MEIPASS
        def resource_path(relative_path):
            try:
                base_path = sys._MEIPASS  # Directorio temporal al empaquetar
            except AttributeError:
                base_path = os.path.abspath(".")  # Ruta actual en desarrollo
            return os.path.join(base_path, relative_path)

        # Crear la ruta absoluta y cargar la imagen
        ruta = resource_path(ruta_relativa)
        return CTkImage(Image.open(ruta), size=tamaño)

    def obtener_ruta_recurso(self, relative_path):
        """Obtiene la ruta del recurso para desarrollo o ejecución empaquetada."""
        try:
            base_path = sys._MEIPASS  # Carpeta temporal al ejecutar con PyInstaller
        except AttributeError:
            base_path = os.path.abspath(".")  # Carpeta actual en desarrollo
        return os.path.join(base_path, relative_path)

    def crear_boton(self, frame, texto, img, color, comando):
        customtkinter.CTkButton(
            master=frame,
            text=texto,
            fg_color=color,
            corner_radius=15,
            image=self.cargar_imagen(img, tamaño=(100, 100)),
            command=comando
        ).pack(side="left", padx=20)

    def frame_principal(self):
        self.limpiar_frame()
        self.centrar_ventana()
        self.titulo.configure(text="BIENVENIDO A TU BANCA VIRTUAL")

        customtkinter.CTkLabel(self.scrollable_frame, text="Selecciona la acción que deseas realizar",
                               font=("Helvetica Neue", 14)).pack(pady=12)

        # Crear botones agrupados
        botones_frame1 = customtkinter.CTkFrame(self.scrollable_frame, fg_color="gray15", corner_radius=15)
        botones_frame1.pack(pady=10, padx=10)
        botones_frame2 = customtkinter.CTkFrame(self.scrollable_frame, fg_color="gray15", corner_radius=15)
        botones_frame2.pack(pady=10, padx=10)

        botones = [
            ("Consultar Saldo", "consulta_saldo.png", "green", self.saldo),
            ("Realizar un depósito", "deposito.png", None, self.deposito),
            ("Realizar un retiro", "retiro.png", "green", self.retiro),
            ("Realizar una transferencia", "transferencia.png", None, self.transferencia)
        ]

        for i, (texto, img, color, comando) in enumerate(botones):
            self.crear_boton(botones_frame1 if i < 2 else botones_frame2, texto, img, color, comando)

        customtkinter.CTkButton(master=self.scrollable_frame, text="Cerrar Sesión", fg_color="black",
                                text_color="white", command=self.iniciar_sesion).pack(pady=12, padx=10)

    def saldo(self):
        self.limpiar_frame()
        self.titulo.configure(text="CONSULTA DE SALDO", font=("Arial", 30))

        saldo_usuario = self.logica.saldo_disponible[self.logica.usuario_actual]

        # Imagen y mensaje de saldo
        customtkinter.CTkLabel(self.scrollable_frame, text="", image=self.cargar_imagen("consulta_saldo.png")).pack(pady=20)
        customtkinter.CTkLabel(self.scrollable_frame, text="Tu saldo actual es:", font=("Roboto", 22)).pack(pady=10)
        saldo_label = customtkinter.CTkLabel(self.scrollable_frame, text=f"${saldo_usuario}", font=("Arial", 28, "bold"),
                                             text_color="green")
        saldo_label.pack(pady=10)

        # Botón para regresar al menú principal
        customtkinter.CTkButton(self.scrollable_frame, text="Menú Principal", fg_color="blue",
                                command=self.frame_principal).pack(pady=20)

    def deposito(self):
        self.limpiar_frame()
        self.titulo.configure(text="DEPOSITOS", font=("Arial", 30))
        customtkinter.CTkLabel(self.scrollable_frame, text="", image=self.cargar_imagen("deposito.png")).pack(pady=20)
        customtkinter.CTkLabel(self.scrollable_frame, text="Ingrese el monto a depositar", font=("Roboto", 22)).pack(pady=10)

        self.deposito_entry = customtkinter.CTkEntry(self.scrollable_frame, placeholder_text="$$$$", height=30, width=250)
        self.deposito_entry.pack(pady=10)
        customtkinter.CTkButton(self.scrollable_frame, text="Depositar", fg_color="green",
                                command=self.logica.depositar).pack(pady=10)
        customtkinter.CTkButton(self.scrollable_frame, text="Menú Principal", fg_color="blue",
                                command=self.frame_principal).pack(pady=10)

    def retiro(self):
        self.limpiar_frame()
        self.titulo.configure(text="RETIROS", font=("Arial", 30))
        customtkinter.CTkLabel(self.scrollable_frame, text="", image=self.cargar_imagen("retiro.png")).pack(pady=20)
        customtkinter.CTkLabel(self.scrollable_frame, text="Ingrese el monto que desea retirar", font=("Roboto", 22)).pack(
            pady=10)
        self.retiro_entry = customtkinter.CTkEntry(self.scrollable_frame, placeholder_text="$$$$", height=30, width=250)
        self.retiro_entry.pack(pady=10)
        customtkinter.CTkButton(self.scrollable_frame, text="Retirar", fg_color="green",
                                command=self.logica.retirar).pack(pady=10)
        customtkinter.CTkButton(self.scrollable_frame, text="Menú Principal", fg_color="blue",
                                command=self.frame_principal).pack(pady=10)
    def transferencia(self):
        self.limpiar_frame()
        self.titulo.configure(text="TRANSFERENCIAS", font=("Arial", 30))
        customtkinter.CTkLabel(self.scrollable_frame, text="", image=self.cargar_imagen("transferencia.png")).pack(pady=20)

        # Campos
        self.crear_campo("Ingresa la cuenta destino")
        self.transferencia_cuenta_entry = customtkinter.CTkEntry(self.scrollable_frame, placeholder_text="###",
                                                                 height=30, width=250)
        self.transferencia_cuenta_entry.pack(pady=5)

        self.crear_campo("Ingresa el monto")
        self.transferencia_monto_entry = customtkinter.CTkEntry(self.scrollable_frame, placeholder_text="$$$",
                                                                height=30, width=250)
        self.transferencia_monto_entry.pack(pady=5)

        # Botones
        customtkinter.CTkButton(self.scrollable_frame, text="Transferir", fg_color="green",
                                command=self.logica.transferir).pack(pady=12, padx=10)
        customtkinter.CTkButton(self.scrollable_frame, text="Menú Principal", fg_color="blue",
                                command=self.frame_principal).pack(pady=5, padx=10)

    def crear_campo(self, texto):
        customtkinter.CTkLabel(self.scrollable_frame, text=texto, font=("Roboto", 18)).pack(pady=5)

    def iniciar_sesion(self):
        self.limpiar_frame()
        self.centrar_ventana()
        self.titulo.configure(text="Iniciar Sesión")

        self.usuario_login_entry = customtkinter.CTkEntry(self.scrollable_frame, placeholder_text="Username", width=250)
        self.usuario_login_entry.pack(pady=12, padx=10)

        self.password_login_entry = customtkinter.CTkEntry(self.scrollable_frame, placeholder_text="Contraseña", width=250, show="*")
        self.password_login_entry.pack(pady=12, padx=10)

        customtkinter.CTkButton(self.scrollable_frame, text="Iniciar Sesión", fg_color="green", width=250,
                                command=self.boton_iniciar_sesion).pack(pady=12, padx=10)
        customtkinter.CTkButton(self.scrollable_frame, text="Crear una cuenta", fg_color="blue", width=250,
                                command=self.crear_cuenta).pack(pady=12, padx=10)

    def boton_iniciar_sesion(self):
        self.logica.iniciar_sesion()


    def crear_cuenta(self):
        self.limpiar_frame()
        self.titulo.configure(text="Registro de Usuario")

        # Asignar los campos de entrada
        customtkinter.CTkLabel(self.scrollable_frame, text="", font=("Roboto", 18)).pack(pady=5)
        self.usuario_entry = customtkinter.CTkEntry(self.scrollable_frame, placeholder_text="Crea un usuario",
                                                    height=30, width=250)
        self.usuario_entry.pack(pady=5)

        self.contraseña_entry = customtkinter.CTkEntry(self.scrollable_frame, placeholder_text="Crea una contraseña", show="*",
                                                       height=30, width=250)
        self.contraseña_entry.pack(pady=5)

        self.contraseña_entryCC = customtkinter.CTkEntry(self.scrollable_frame,
                                                             placeholder_text="Confirmar Contraseña", width=250,
                                                             show="*")
        self.contraseña_entryCC.pack(pady=5)

        customtkinter.CTkLabel(master=self.scrollable_frame, text="No. de Cuenta:").pack(pady=0)
        self.numero_cuenta_entry = customtkinter.CTkLabel(master=self.scrollable_frame,
                                                          text=f"{random.randint(1000000000, 9999999999)}")
        self.numero_cuenta_entry.pack(pady=0)

        self.monto_inicial_entry = customtkinter.CTkEntry(self.scrollable_frame, placeholder_text="Monto inicial ($$$)",
                                                          height=30, width=250)
        self.monto_inicial_entry.pack(pady=5)

        customtkinter.CTkButton(self.scrollable_frame, text="Registrar", fg_color="green", command=self.registrar_usuario).pack(pady=10)
        customtkinter.CTkButton(self.scrollable_frame, text="Volver", fg_color="blue",
                                command=self.iniciar_sesion).pack(pady=5)

    def registrar_usuario(self):
        # Usar la clase logica para obtener los datos de los campos
        self.logica.registro_usuario()


if __name__ == "__main__":
    App()
