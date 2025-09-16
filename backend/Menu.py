from User_service import UserService
from Role_enum import RoleEnum

class Menu():
    
    def __init__(self, service: UserService):
            self.__service = service
            self.current_user = None

    def run_menu(self):
        while True:
            if (self.current_user != None):
                print(f"Usuario conectado: {self.current_user.email} \n")
            option = input("Elija una opción: \n1. Registrarse. \n" \
            "2. Ingresar a la app. \n3. Ver listado de usuarios (solo admin). \n"
            "4. Ver listado de usuarios por rol (solo admin). \n5. Buscar usuario por id (solo admin). \n"
            "6. Buscar usuario por email (solo admin). \n"
            "7. Editar datos de usuario (solo propia cuenta). \n8. Cambiar rol de usuario (solo admin). \n"
            "9. Dar de baja la cuenta (solo propia cuenta). \n10. Eliminar definitivamente la cuenta (solo admin). \n"
            "0. Salir. \n")
            if option == "1":
                name = input("Ingrese su nombre: ")
                surname = input("Ingrese su apellido: ")
                dni = int(input("Ingrese su dni: "))
                phone_number = int(input("Ingrese su número de teléfono: "))
                email = input("Ingrese su email: ")
                password = input("Ingrese su contraseña. " \
                "Recuerde que debe tener mínimo 6 caracteres e incluir números y letras: ")
                repeat_password = input("Ingrese nuevamente su contraseña: ")
                if (password != repeat_password):
                    print("Las contraseñas no coinciden. Vuelva a registrarse. \n")
                    continue
                role = None
                roleInput = input("Ingrese su rol. 1) Paciente. 2) Profesional de salud. 3) Administrador: ")
                if roleInput == "1":
                    role = RoleEnum.PATIENT
                elif roleInput == "2":
                    role = RoleEnum.DOCTOR
                elif roleInput == "3":
                    role = RoleEnum.ADMIN
                else:
                    print("Rol no reconocido. Ingrese un rol válido.\n")
                    continue
                date_of_birth = input("Ingrese su fecha de nacimiento: ")
                created_user = self.__service.register(name=name, surname=surname, dni=dni,
                                                       email=email, password=password, phone_number=phone_number,
                                                       role=role, date_of_birth=date_of_birth)
                if (created_user):
                    print("Usuario creado exitosamente. Puede proceder a iniciar sesión. \n")

            elif option == "2":
                email = input("Ingrese su email: ")
                password = input("Ingrese su contraseña: ")
                self.current_user = self.__service.login(email, password)

            #Solo admin (Fullstack requirement)
            elif option == "3":
                if (self.current_user == None):
                    print("Error, debe iniciar sesión primero! \n")
                    continue
                if (self.current_user.role != RoleEnum.ADMIN):
                    print("Error, acción solo accesible para admin! \n")
                    continue
                users = self.__service.get_all_users()
                if not users:
                    print("No se encuentran usuarios activos en sistema! \n")
                else:
                    print(f"Lista de usuarios activos: {users} \n")
                    for user in users:
                        print(f"- {user.name} {user.surname}")
                    print()

            #Solo admin (Fullstack requirement)    
            elif option == "4":
                if (self.current_user == None):
                    print("Error, debe iniciar sesión primero! \n")
                    continue
                if (self.current_user.role != RoleEnum.ADMIN):
                    print("Error, acción solo accesible para admin! \n")
                    continue
                role = None
                while (role == None):
                    roleInput = input("Ingrese su rol. 1) Paciente. 2) Profesional de salud. 3) Administrador: ")
                    if roleInput == "1":
                        role = RoleEnum.PATIENT
                    elif roleInput == "2":
                        role = RoleEnum.DOCTOR
                    elif roleInput == "3":
                        role = RoleEnum.ADMIN
                    else:
                        print("Rol no reconocido. Ingrese un rol válido.\n")
                        continue
                data = self.__service.get_all_users_by_role(role)
                if not data:
                    print("No se encuentran usuarios que cumplan la condición buscada. \n")
                else:
                    print(f"Lista de usuarios con rol seleccionado: {data} \n")


            #Solo admin (Fullstack requirement)
            elif option == "5":
                if (self.current_user == None):
                    print("Error, debe iniciar sesión primero! \n")
                    continue
                if (self.current_user.role != RoleEnum.ADMIN):
                    print("Error, acción solo accesible para admin! \n")
                    continue
                id = input("Ingrese el id del usuario que desea buscar.")
                user_found = self.__service.get_user_by_id(id)
                if (user_found == None):
                    print("No se encontró el usuario buscado.")
                else:
                    print(f"El usuario encontrado es: {user_found} \n")

            #Solo admin (Fullstack requirement)
            elif option == "6":
                if (self.current_user == None):
                    print("Error, debe iniciar sesión primero! \n")
                    continue
                if (self.current_user.role != RoleEnum.ADMIN):
                    print("Error, acción solo accesible para admin! \n")
                    continue
                email = input("Ingrese el email del usuario que desea buscar: ")
                user_found = self.__service.get_user_by_email(email)
                if (user_found == None):
                    print("No se encontró el usuario buscado.")
                else:
                    print(f"El usuario encontrado es: {user_found} \n")

            elif option == "7":
                if (self.current_user == None):
                    print("Error, debe iniciar sesión primero! \n")
                    continue
                input_email = input("Ingrese su dirección de " \
                "email para confirmar la modificación de la cuenta: ")
                if self.current_user.email != input_email:
                    print("El email solicitado no coincide con el de la cuenta activa. \n")
                else:
                    print("Reingrese los valores para cada campo.")
                    name = input("Ingrese su nombre: ")
                    surname = input("Ingrese su apellido: ")
                    dni = int(input("Ingrese su dni: "))
                    phone_number = int(input("Ingrese su número telefónico: "))
                    password = input("Ingrese su contraseña. " \
                    "Recuerde que debe tener mínimo 6 caracteres e incluir números y letras: ")
                    repeat_password = input("Ingrese nuevamente su contraseña: ")
                    if (password != repeat_password):
                        print("Las contraseñas no coinciden. Por favor, vuelva a intentarlo. \n")
                        continue
                    updated_user = self.__service.update_user(name=name, surname=surname, dni=dni, 
                                                email=input_email, phone_number=phone_number, password=password)
                    if (updated_user):
                        print(f"Usuario modificado exitosamente! \n") 

            #Solo admin (Fullstack requirement)
            elif option == "8":
                if (self.current_user == None):
                    print("Error, debe iniciar sesión primero! \n")
                    continue
                if (self.current_user.role != RoleEnum.ADMIN):
                    print("Error, acción solo accesible para admin! \n")
                    continue
                role = None
                while (role == None):
                    roleInput = input("Ingrese su rol. 1) Paciente. 2) Profesional de salud. 3) Administrador: ")
                    if roleInput == "1":
                        role = RoleEnum.PATIENT
                    elif roleInput == "2":
                        role = RoleEnum.DOCTOR
                    elif roleInput == "3":
                        role = RoleEnum.ADMIN
                    else:
                        print("Rol no reconocido. Ingrese un rol válido.\n")
                        continue
                user_email = input("Ingrese el email del usuario para modificarle el rol: ")
                self.__service.change_user_role(user_email, role)

            elif option == "9":
                if (self.current_user == None):
                    print("Error, debe iniciar sesión primero! \n")
                    continue
                input_email = input("Ingrese su dirección de " \
                "email para confirmar la baja de la cuenta: ")
                if self.current_user.email != input_email:
                    print("El email solicitado no coincide con el de la cuenta activa. \n")
                else:
                    disabled_user = self.__service.disable_account(input_email)
                    if (disabled_user):
                        self.current_user = None
                        print("La cuenta se dio de baja exitosamente. Presione 0 para salir "
                        "o presione 2 para ingresar con otra cuenta. \n")
                    else:
                        print("No se pudo eliminar la cuenta. Verifique el email.")

            #Solo admin (Fullstack requirement)
            elif option == "10":
                if (self.current_user == None):
                    print("Error, debe iniciar sesión primero! \n")
                    continue
                if (self.current_user.role != RoleEnum.ADMIN):
                    print("Error, acción solo accesible para admin! \n")
                    continue
                input_email = input("Ingrese la dirección de " \
                "email para eliminar definitivamente la cuenta: ")
                deleted_user = self.__service.delete_account(input_email)
                if (deleted_user):
                    print("La cuenta se eliminó exitosamente. \n")
                else:
                    print("No se pudo eliminar la cuenta. Verifique el email.")

            elif option == "0":
                print("Saliendo de WappTurno...\n ")
                break
            
            else:
                print("Opción no válida. Por favor, vuelva a intentar.\n")

