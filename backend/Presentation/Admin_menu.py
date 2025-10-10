from Presentation.Base_user_menu import BaseUserMenu
from Models.Role_enum import RoleEnum


class AdminMenu(BaseUserMenu):
    def __init__(self, user_service, appointment_service, user):
        super().__init__(user_service, user)
        self._user_service = user_service
        self._appointment_service = appointment_service


    def run(self):
        while True:
            print("\n--- MENÚ ADMIN ---")
            self.show_common_options()
            print("3. Listar usuarios")
            print("4. Listar usuarios por rol")
            print("5. Buscar usuario por ID")
            print("6. Buscar usuario por email")
            print("7. Cambiar rol de usuario")
            print("8. Eliminar usuario definitivamente")
            print("9. Mostrar turnos de un usuario")
            print("0. Cerrar sesión")

            option = input("Opción: ")

            if self.handle_common_options(option):
                continue
            elif option == "3":
                self.list_users()
            elif option == "4":
                self.list_users_by_role()
            elif option == "5":
                self.find_user_by_id()
            elif option == "6":
                self.find_user_by_email()
            elif option == "7":
                self.change_role()
            elif option == "8":
                self.delete_user()
            elif option == "9":
                self.show_appointments()
            elif option == "0":
                print("Sesión cerrada.\n")
                break
            else:
                print("Opción no válida.\n")


    def list_users(self):
        users = self._user_service.get_all_users()
        for u in users or []:
            print(f"- {u.name} {u.surname} ({u.role.value})")


    def list_users_by_role(self):
        role_map = {"1": RoleEnum.PATIENT, "2": RoleEnum.DOCTOR, "3": RoleEnum.ADMIN}
        role = role_map.get(input("Elija Rol: 1) Paciente 2) Doctor 3) Admin: "))
        if role:
            users = self._user_service.get_all_users_by_role(role)
            for u in users or []:
                print(f"- {u.name} {u.surname}")
        else:
            print("Error: Rol inválido.")


    def find_user_by_id(self):
        uid = input("ID del usuario: ")
        user = self._user_service.get_user_by_id(uid)
        print(user or "Usuario no encontrado. Corrobore el Id.")


    def find_user_by_email(self):
        email = input("Email: ")
        user = self._user_service.get_user_by_email(email)
        print(user or "Usuario no encontrado. Corrobore el email.")


    def change_role(self):
        email = input("Ingrese el email del usuario cuyo rol desea cambiar: ")
        role_map = {"1": RoleEnum.PATIENT, "2": RoleEnum.DOCTOR, "3": RoleEnum.ADMIN}
        role = role_map.get(input("Seleccione nuevo rol: 1) Paciente 2) Doctor 3) Admin: "))
        if role:
            self._user_service.change_user_role(email, role)
            print("Rol actualizado exitosamente.\n")


    def delete_user(self):
        email = input("Ingrese el email del usuario a eliminar: ")
        self._user_service.delete_account(email)
        print("Usuario eliminado exitosamente.\n")


    def show_appointments(self):
        searched_id = input("Ingrese id del usuario para ver sus turnos. \n")
        is_doctor_input = input("¿Es profesional médico? (s/n): ").lower()
        is_doctor = is_doctor_input == "s"
        data = self._appointment_service.get_all_appointments_by_user_id(searched_id, is_doctor)
        if not data:
            print("No hay turnos registrados.\n")
        else:
            for appointment in data:
                print(f"- {appointment}")