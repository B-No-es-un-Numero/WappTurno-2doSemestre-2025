from Models.Role_enum import RoleEnum
from Models.Appointment_state_enum import AppointmentStateEnum
from Services.Appointment_service import AppointmentService

class BaseUserMenu:
    def __init__(self, user_service, user, appointment_service: AppointmentService):
        self._appointment_service = appointment_service
        self._user_service = user_service
        self.user = user


    def show_common_options(self):
        print("1. Editar datos personales")
        print("2. Dar de baja mi cuenta")
        print("3. Editar frecuencia de un turno")
        print("4. Editar estado de un turno")


    def handle_common_options(self, option):
        if option == "1":
            self.update_profile()
            return True
        elif option == "2":
            self.disable_account()
            return True
        elif option == "3":
            self.update_frequency()
            return True
        elif option == "4":
            self.update_state()
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


    def update_frequency(self):
        if(self.user.role == RoleEnum.ADMIN):
            searched_id = input("Ingrese id del usuario para ver sus turnos. \n")
            data = self._appointment_service.get_all_appointments_by_user_id(searched_id, False)
        elif(self.user.role == RoleEnum.DOCTOR):        
             data = self._appointment_service.get_all_appointments_by_user_id(self.user.user_id, False)
        else:
            data = self._appointment_service.get_all_appointments_by_user_id(self.user.user_id, False)
        
        if not data:
            print("No hay turnos registrados.\n")
        else:
            for appointment in data:
                print(f"- {appointment}")
        
        appointment_id = input("Ingrese el ID del turno: ")
        frequency = input("Ingrese nueva frecuencia (semanal/mensual/quincenal): ")
        self._appointment_service.update_frequency(appointment_id, frequency)

    def update_state(self):
        if(self.user.role == RoleEnum.ADMIN):
            searched_id = input("Ingrese id del usuario para ver sus turnos. \n")
            data = self._appointment_service.get_all_appointments_by_user_id(searched_id, False)
        elif(self.user.role == RoleEnum.DOCTOR):        
             data = self._appointment_service.get_all_appointments_by_user_id(self.user.user_id, False)
        else:
            data = self._appointment_service.get_all_appointments_by_user_id(self.user.user_id, False)
        
        if not data:
            print("No hay turnos registrados.\n")
        else:
            for appointment in data:
                print(f"- {appointment}")

        appointment_id = input("Ingrese el ID del turno: ")
        print("Seleccione nuevo estado:")
        print(" 1. Confirmado\n 2. Reprogramado\n 3. Cancelado\n 4. Finalizado")
        option = input("Opción: ")
        state_map = {
            "1": AppointmentStateEnum.CONFIRMED,
            "2": AppointmentStateEnum.RESCHEDULED,
            "3": AppointmentStateEnum.CANCELLED,
            "4": AppointmentStateEnum.COMPLETED   
        }
        new_state = state_map.get(option)
        if new_state:
            self._appointment_service.update_state(appointment_id, new_state)
        else:
            print("Opción inválida.\n")