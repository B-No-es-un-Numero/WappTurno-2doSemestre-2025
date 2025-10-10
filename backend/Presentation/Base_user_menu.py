class BaseUserMenu:
    def __init__(self, user_service, user):
        self._user_service = user_service
        self.user = user


    def show_common_options(self):
        print("1. Editar datos personales")
        print("2. Dar de baja mi cuenta")


    def handle_common_options(self, option):
        if option == "1":
            self.update_profile()
            return True
        elif option == "2":
            self.disable_account()
            return True
        return False


    def update_profile(self):
        email = input("Confirme su email: ")
        if email != self.user.email:
            print("El email no coincide.")
            return
        name = input("Nuevo nombre: ")
        surname = input("Nuevo apellido: ")
        dni = int(input("Nuevo DNI: "))
        phone = int(input("Nuevo teléfono: "))
        password = input("Nueva contraseña: ")
        repeat = input("Repetir contraseña: ")
        if password != repeat:
            print("Las contraseñas no coinciden.\n")
            return
        self._user_service.update_user(name, surname, dni, email, phone, password)
        print("Datos actualizados.\n")


    def disable_account(self):
        email = input("Confirme su email para dar de baja: ")
        if email == self.user.email:
            self._user_service.disable_account(email)
            print("Cuenta dada de baja.\n")
            exit()
        else:
            print("Email incorrecto.\n")
