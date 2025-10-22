from Models.Appointment_state_enum import AppointmentStateEnum
from Presentation.Base_user_menu import BaseUserMenu
from Models.Days_enum import DaysEnum
from Models.TimeFrame_enum import TimeFrameEnum


class DoctorMenu(BaseUserMenu):


    def __init__(self, user_service, availability_service, appointment_service, user):
        super().__init__(user_service, user, appointment_service)
        self._availability_service = availability_service


    def run(self):
        while True:
            print("\n--- MENÚ DOCTOR ---")
            self.show_common_options()
            print("5. Ver mi turnero")
            print("6. Crear horario de disponibilidad")
            print("7. Editar horario")
            print("8. Eliminar horario")
            print("9. Mostrar horarios")
            print("10. Editar datos profesionales")
            print("0. Cerrar sesión")

            option = input("Opción: ")

            if self.handle_common_options(option):
                continue
            elif option == "5":
                self.show_appointments()
            elif option == "6":
                self.add_availability()
            elif option == "7":
                self.edit_availability()
            elif option == "8":
                self.remove_availability()
            elif option == "9":
                self.list_availability()
            elif option == "10":
                self.update_doctor_data()
            elif option == "0":
                print("Sesión cerrada.\n")
                break
            else:
                print("Opción no válida.\n")


    def show_appointments(self):
        data = self._appointment_service.get_all_appointments_by_user_id(self.user.user_id, True)
        if not data:
            print("No hay turnos registrados.\n")
            return
        print("\n=== TURNERO DEL PROFESIONAL DE SALUD ===\n")
        for idx, appointment in enumerate(data, start=1):
            print(f"Turno #{idx}")
            print(f"ID Turno:         {appointment.appointment_id}")
            print(f"Fecha y hora:     {appointment.date_and_time}")
            print(f"Estado:           {AppointmentStateEnum.get_spanish_value(appointment.state.value)}")
            print(f"Frecuencia:       {appointment.frequency if appointment.frequency else 'única'}")
            print(f"Paciente:         {appointment.patient_info}")
            print(f"Consulta:         {appointment.consultation_name}")
            print("-" * 50)


    def add_availability(self):
        tf_map = {"1": TimeFrameEnum.MAÑANA, "2": TimeFrameEnum.TARDE, "3": TimeFrameEnum.NOCHE}
        day_map = {
            "1": DaysEnum.LUNES, "2": DaysEnum.MARTES, "3": DaysEnum.MIERCOLES,
            "4": DaysEnum.JUEVES, "5": DaysEnum.VIERNES, "6": DaysEnum.SABADO, 
            "7": DaysEnum.DOMINGO
        }
        timeframe = tf_map.get(input("Elija Horario: 1) Mañana 2) Tarde 3) Noche: "))
        days = day_map.get(input("Elija Día: 1) Lunes 2) Martes 3) Miércoles 4) Jueves 5) " \
                                "Viernes 6) Sábado 7) Domingo: "))
        if timeframe and days:
            self._availability_service.add_availability(self.user.user_id, timeframe, days)
            print("Disponibilidad creada exitosamente.\n")


    def edit_availability(self):
        self.list_availability()
        availability_id = input("Seleccione ID del horario a editar: ")
        tf_map = {"1": TimeFrameEnum.MAÑANA, "2": TimeFrameEnum.TARDE, "3": TimeFrameEnum.NOCHE}
        day_map = {
            "1": DaysEnum.LUNES, "2": DaysEnum.MARTES, "3": DaysEnum.MIERCOLES,
            "4": DaysEnum.JUEVES, "5": DaysEnum.VIERNES, "6": DaysEnum.SABADO, 
            "7": DaysEnum.DOMINGO
        }
        timeframe = tf_map.get(input("Elija Horario: 1) Mañana 2) Tarde 3) Noche: "))
        days = day_map.get(input("Elija Día: 1) Lunes 2) Martes 3) Miércoles 4) Jueves 5) " \
                                "Viernes 6) Sábado 7) Domingo: "))
        if timeframe and days:
            self._availability_service.update_availability(availability_id, timeframe, days)
            print("Disponibilidad actualizada exitosamente.\n")


    def remove_availability(self):
        self.list_availability()
        availability_id = input("Seleccione ID del horario a eliminar: ")
        self._availability_service.remove_availability(availability_id)
        print("Disponibilidad eliminada exitosamente.\n")


    def list_availability(self):
        data = self._availability_service.get_all_by_doctor_id(self.user.user_id)
        if not data:
            print("No hay horarios para el profesional.\n")

        days_order = ["LUNES", "MARTES", "MIERCOLES", "JUEVES", "VIERNES",
                       "SABADO", "DOMINGO"]
        timeframes_order = ["MAÑANA", "TARDE", "NOCHE"]

        data.sort(
        key=lambda a: (
            days_order.index(a.days),
            timeframes_order.index(a.time_frame)
            )
        )   

        print(f"Horarios laborales del profesional: {self.user.name} {self.user.surname}.\n")
        for a in data:
            print(f"ID: {a.id} | Día: {a.days} | Horario: {a.time_frame}")


    def update_doctor_data(self):
        specialty = input("Especialidad: ")
        license_number = int(input("Matrícula: "))
        accepts = input("¿Acepta obra social? (s/n): ").lower() == "s"
        self._user_service.update_doctor_profile(
            doctor_id=self.user.user_id,
            specialty=specialty,
            accepts_medical_insurance=accepts,
            license_number=license_number
        )
        print("Datos actualizados exitosamente.\n")
