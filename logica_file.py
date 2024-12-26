import main as ui
import re


class logica():
    def __init__(self, app_instance):
        self.numero_cuenta = []
        self.titular_cuenta = []
        self.password = []
        self.saldo_disponible = []
        self.usuario_actual = None
        self.ui = app_instance  # Guarda la referencia de la instancia de App

    def registro_usuario(self):
        # Validar que todos los campos estén rellenados
        if not all([
            self.ui.usuario_entry.get().strip(),
            self.ui.contraseña_entry.get().strip(),
            self.ui.monto_inicial_entry.get().strip()
        ]):
            self.ui.mostrar_info("ERROR", "Por favor, rellene todos los campos.")
            return  # Salir de la función si hay campos vacíos

        # Validar que la contraseña cumple con los requisitos
        patron_contraseña = r"^(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{8,}$"
        if not re.fullmatch(patron_contraseña, self.ui.contraseña_entry.get()):
            self.ui.mostrar_info(
                "ERROR",
                "La contraseña debe tener al menos 8 caracteres, una letra mayúscula y un número."
            )
            return  # Salir de la función si la contraseña no es válida

        if self.ui.usuario_entry.get() in self.titular_cuenta:
            self.ui.mostrar_info(
                "ERROR",
                "Nombre de usuario ya registrado"
            )
            return

        if self.ui.contraseña_entry.get() != self.ui.contraseña_entryCC.get():
            self.ui.mostrar_info(
                "ERROR",
                "Contraseñas no coinciden"
            )
            return

        try:
            # Validar que el monto inicial sea un número entero
            monto_inicial = int(self.ui.monto_inicial_entry.get().strip())
        except ValueError:
            self.ui.mostrar_info("ERROR", "El monto inicial debe ser un número entero.")
            return  # Salir de la función si la validación falla

        # Si todas las validaciones son correctas, registrar los datos
        self.ui.mostrar_info("REGISTRADO", "Registro realizado con éxito.")
        self.titular_cuenta.append(self.ui.usuario_entry.get().strip())  # Guardar usuario
        self.password.append(self.ui.contraseña_entry.get().strip())  # Guardar contraseña
        self.saldo_disponible.append(monto_inicial)  # Guardar el monto inicial como entero
        self.numero_cuenta.append(self.ui.numero_cuenta_entry.cget("text"))  # Obtener número de cuenta
        print(f"Número de cuenta registrado: {self.numero_cuenta[-1]}")

        # Redirigir a la interfaz de inicio de sesión
        self.ui.iniciar_sesion()

        # Imprimir en consola para verificar los datos
        print(f"Primer titular registrado: {self.titular_cuenta[0]}")

    def iniciar_sesion(self):
        usuario_login = self.ui.usuario_login_entry.get()
        password_login = self.ui.password_login_entry.get()

        # Recorremos las listas de usuarios y contraseñas
        for index, (titular, password) in enumerate(zip(self.titular_cuenta, self.password)):
            if usuario_login == titular and password_login == password:
                self.usuario_actual = index  # Guardar el índice del usuario activo
                self.ui.frame_principal()  # Usuario válido, cambiamos a la interfaz principal
                return

        # Si no encuentra coincidencias
        self.ui.mostrar_info("ERROR", "Usuario o contraseña incorrectos")

    def depositar(self):
        monto_deposito = int(self.ui.deposito_entry.get())
        saldo_actual = int(self.saldo_disponible[self.usuario_actual])
        self.saldo_disponible[self.usuario_actual] = saldo_actual + monto_deposito
        self.ui.frame_principal()

    def retirar(self):
        monto_retiro = int(self.ui.retiro_entry.get())
        saldo_actual = int(self.saldo_disponible[self.usuario_actual])
        if monto_retiro <= saldo_actual:
            self.saldo_disponible[self.usuario_actual] = saldo_actual - monto_retiro
            self.ui.mostrar_info("ÉXITO", "Retiro realizado con éxito")
            self.ui.frame_principal()
        else:
            self.ui.mostrar_info("ERROR", "El monto a retirar es superior al saldo disponible")

    def transferir(self):
        cuenta_transferir = self.ui.transferencia_cuenta_entry.get()
        monto = int(self.ui.transferencia_monto_entry.get())
        saldo_actual = int(self.saldo_disponible[self.usuario_actual])

        # Validar transferencia
        cuenta_valida = cuenta_transferir in self.numero_cuenta
        saldo_suficiente = monto <= saldo_actual
        cuenta_distinta = cuenta_transferir != self.numero_cuenta[self.usuario_actual]

        if cuenta_valida and saldo_suficiente and cuenta_distinta:
            # Obtener índice del destinatario
            indice_destinatario = self.numero_cuenta.index(cuenta_transferir)

            # Restar saldo del remitente
            self.saldo_disponible[self.usuario_actual] = saldo_actual - monto

            # Añadir saldo al destinatario
            saldo_destinatario = int(self.saldo_disponible[indice_destinatario])
            self.saldo_disponible[indice_destinatario] = saldo_destinatario + monto

            # Mostrar mensaje de éxito
            self.ui.mostrar_info("Éxito", "Transferencia realizada con éxito")
            self.ui.frame_principal()
        else:
            # Mostrar mensaje de error
            if not cuenta_valida:
                self.ui.mostrar_info("Error", "La cuenta de destino no es válida")
            elif not saldo_suficiente:
                self.ui.mostrar_info("Error", "Saldo insuficiente para la transferencia")
            elif not cuenta_distinta:
                self.ui.mostrar_info("Error", "No puedes transferir a tu propia cuenta")


    #En el registro corregir que la cuenta no se añada cuando estan los campos vacios
    #Poner un limite para los caracteres del usuario
    #Validar una contraseña segura
    #Validar que no se repita el usuario

