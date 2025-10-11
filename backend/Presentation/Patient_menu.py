from Presentation.Base_user_menu import BaseUserMenu
from datetime import datetime

class PatientMenu(BaseUserMenu):
    def __init__(self, user_service, appointment_service, user):
        super().__init__(user_service, user, appointment_service)

    def run(self):
        while True:
            print("\n--- MENÚ PACIENTE ---")
            self.show_common_options()
            print("5. Ver mis turnos")
            print("6. Solicitar nuevo turno")
            print("7. Reprogramar turno existente")
            print("0. Cerrar sesión")

            option = input("Opción: ")

            if self.handle_common_options(option):
                continue
            elif option == "5":
                self.show_appointments()
            elif option == "6":
                self.create_appointment()
            elif option == "7":
                self.reschedule_appointment()
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
        doctor_id = input("ID del doctor: ")
        consultation_id = input("ID de la consulta médica: ")
        date = input("Fecha (YYYY-MM-DD): ")
        time = input("Hora (HH:MM): ")
        dt = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
        success = self._appointment_service.create_appointment(
            date_and_time=dt,
            user_id=self.user.user_id,
            doctor_id=doctor_id,
            medical_consultation_id=consultation_id
        )
        if not success:
            print("Error al crear el turno")
        else:
            print("Turno creado exitosamente.\n")

    def reschedule_appointment(self):
        data = self._appointment_service.get_all_appointments_by_user_id(self.user.user_id, False)
        if not data:
            print("No hay turnos registrados.\n")
        else:
            for appointment in data:
                print(f"- {appointment}")
        appointment_id = input("Ingrese el ID del turno a reprogramar: ")
        new_date = input("Ingrese la nueva fecha (YYYY-MM-DD): ")
        new_time = input("Ingrese la nueva hora (HH:MM): ")

        try:
            new_datetime = datetime.strptime(f"{new_date} {new_time}", "%Y-%m-%d %H:%M")
            result = self._appointment_service.reschedule_appointment(appointment_id, new_datetime)
            if result:
                print("Turno reprogramado exitosamente.\n")
            else:
                print("No se pudo reprogramar el turno.\n")
        except ValueError:
            print("Formato de fecha u hora inválido.\n")
