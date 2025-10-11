from Presentation.Base_user_menu import BaseUserMenu
from Models.Role_enum import RoleEnum


class AdminMenu(BaseUserMenu):
    def __init__(self, user_service, appointment_service, user):
        super().__init__(user_service, user, appointment_service)
        self._user_service = user_service


    def run(self):
        while True:
            print("\n--- MENÚ ADMIN ---")
            self.show_common_options()
            print("5. Listar usuarios")
            print("6. Listar usuarios por rol")
            print("7. Buscar usuario por ID")
            print("8. Buscar usuario por email")
            print("9. Cambiar rol de usuario")
            print("10. Eliminar usuario definitivamente")
            print("11. Mostrar turnos de un usuario")
            print("12. Eliminar turno de un usuario")
            print("0. Cerrar sesión")

            option = input("Opción: ")

            if self.handle_common_options(option):
                continue
            elif option == "5":
                self.list_users()
            elif option == "6":
                self.list_users_by_role()
            elif option == "7":
                self.find_user_by_id()
            elif option == "8":
                self.find_user_by_email()
            elif option == "9":
                self.change_role()
            elif option == "10":
                self.delete_user()
            elif option == "11":
                self.show_appointments()
            elif option == "12":
                self.delete_appointment()
            elif option == "0":
                print("Sesión cerrada.\n")
                break
            else:
                print("Opción no válida.\n")


    def list_users(self):
        users = self._user_service.get_all_users()
        for u in users or []:
            print(f"- {u.user_id} {u.name} {u.surname} ({u.role.value})")


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
        users = self._user_service.get_all_users()
        for u in users or []:
            print(f"- {u.user_id} {u.name} {u.surname} ({u.role.value})")
        searched_id = input("Ingrese id del usuario para ver sus turnos. \n")
        data = self._appointment_service.get_all_appointments_by_user_id(searched_id, False)
        if not data:
            print("No hay turnos registrados.\n")
            return
        print("\n=== TURNOS ===\n")
        for idx, appointment in enumerate(data, start=1):
            print(f"Turno #{idx}")
            print(f"ID Turno:         {appointment.appointment_id}")
            print(f"Fecha y hora:     {appointment.date_and_time}")
            print(f"Estado:           {appointment.state.value}")
            print(f"Frecuencia:       {appointment.frequency if appointment.frequency else 'única'}")
            print(f"Paciente:         {appointment.patient_info}")
            print(f"Médico:           {appointment.doctor_info}")
            print(f"Especialidad:     {appointment.specialty}")
            print(f"Consulta:         {appointment.consultation_name}")
            print(f"Habilitado:       {'Sí' if appointment.enabled else 'No'}")
            print("-" * 50)


    def delete_appointment(self):
        users = self._user_service.get_all_users()
        for u in users or []:
            print(f"- {u.user_id} {u.name} {u.surname} ({u.role.value})")
        searched_id = input("Ingrese id del usuario para ver sus turnos. \n")
        data = self._appointment_service.get_all_appointments_by_user_id(searched_id, False)
        if not data:
            print("No hay turnos registrados.\n")
            return False
        else:
            print("\n=== TURNOS ===\n")
            for idx, appointment in enumerate(data, start=1):
                print(f"Turno #{idx}")
                print(f"ID Turno:         {appointment.appointment_id}")
                print(f"Fecha y hora:     {appointment.date_and_time}")
                print(f"Estado:           {appointment.state.value}")
                print(f"Frecuencia:       {appointment.frequency if appointment.frequency else 'única'}")
                print(f"Paciente:         {appointment.patient_info}")
                print(f"Médico:           {appointment.doctor_info}")
                print(f"Especialidad:     {appointment.specialty}")
                print(f"Consulta:         {appointment.consultation_name}")
                print(f"Habilitado:       {'Sí' if appointment.enabled else 'No'}")
                print("-" * 50)
        appointment_id = input("Ingrese el ID del turno a eliminar: ")
        
        confirm = input("Confirma eliminación definitiva del turno? (s/n): ").lower()
        if confirm == "s":
            success = self._appointment_service.delete_appointment(appointment_id)
            if success:
                print("Turno eliminado exitosamente.\n")
            else:
                print("No se pudo eliminar el turno. Recuerde cancelarlo previamente.\n")
        else:
            print("Operación cancelada.\n")