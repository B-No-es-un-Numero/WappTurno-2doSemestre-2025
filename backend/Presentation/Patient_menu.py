from Presentation.Base_user_menu import BaseUserMenu


class PatientMenu(BaseUserMenu):
    def __init__(self, user_service, appointment_service, user):
        super().__init__(user_service, user)
        self._appointment_service = appointment_service


    def run(self):
        while True:
            print("\n--- MENÚ PACIENTE ---")
            self.show_common_options()
            print("3. Ver mis turnos")
            print("4. Solicitar nuevo turno")
            # TODO, falta reprogramar turno, cancelarlo, etc.
            print("0. Cerrar sesión")

            option = input("Opción: ")

            if self.handle_common_options(option):
                continue
            elif option == "3":
                self.show_appointments()
            elif option == "4":
                self.create_appointment()
            elif option == "0":
                print("Sesión cerrada.\n")
                break
            else:
                print("Opción no válida.\n")


    def show_appointments(self):
        data = self._appointment_service.get_all_appointments_by_user_id(self.user.user_id, False)
        if not data:
            print("No hay turnos registrados.\n")
        else:
            for appointment in data:
                print(f"- {appointment}")


    def create_appointment(self):
        from datetime import datetime
        doctor_id = input("ID del doctor: ")
        consultation_id = input("ID de la consulta médica: ")
        date = input("Fecha (YYYY-MM-DD): ")
        time = input("Hora (HH:MM): ")
        try:
            dt = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
            self._appointment_service.create_appointment(
                date_and_time=dt,
                user_id=self.user.user_id,
                doctor_id=doctor_id,
                medical_consultation_id=consultation_id
            )
            print("Turno creado exitosamente.\n")
        except Exception as e:
            print(f"Error al crear turno: {e}")
