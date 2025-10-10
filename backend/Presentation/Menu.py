from Services.User_service import UserService
from Services.Availability_service import AvailabilityService
from Services.Appointment_service import AppointmentService
from Models.Role_enum import RoleEnum
from Models.Days_enum import DaysEnum
from Models.TimeFrame_enum import TimeFrameEnum

class Menu():
    
    def __init__(self, user_service: UserService, availability_service: AvailabilityService,
                 appointment_service: AppointmentService):
            self._user_service = user_service
            self._availability_service = availability_service
            self._appointment_service = appointment_service
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
            "11. Crear un horario disponibilidad (solo profesional médico). \n" 
            "12. Eliminar un horario disponibilidad (solo profesional médico). \n"
            "13. Editar tus horarios disponibilidad (solo profesional médico). \n"
            "14. Mostrar tus horario disponibilidad (solo profesional médico). \n"
            "15. Editar datos del profesional (solo profesional médico). \n"
            "16. Mostrar todos los turnos del usuario. \n"
            "17. Crear nuevo turno (solo pacientes). \n"
            "0. Salir. \n")

            if option == "1":
                name = input("Ingrese su nombre: ")
                surname = input("Ingrese su apellido: ")
                dni = int(input("Ingrese su DNI: "))
                phone_number = int(input("Ingrese su número de teléfono: "))
                date_of_birth = input("Ingrese su fecha de nacimiento (YYYY-MM-DD): ")
                email = input("Ingrese su email: ")
                password = input("Ingrese su contraseña (mínimo 6 caracteres, con letras y números): ")
                repeat_password = input("Repita su contraseña: ")

                if password != repeat_password:
                    print("Las contraseñas no coinciden. Vuelva a registrarse.\n")
                    continue
                
                role = None
                role_input = input("Ingrese su rol: 1) Paciente. 2) Profesional de salud. 3) Administrador: ")

                if role_input == "1":
                    role = RoleEnum.PATIENT
                elif role_input == "2":
                    role = RoleEnum.DOCTOR
                elif role_input == "3":
                    role = RoleEnum.ADMIN
                else:
                    print("Rol no reconocido. Ingrese un rol válido.\n")
                    continue
                
                specialty = None
                license_number = None
                accepts_medical_insurance = None

                if role == RoleEnum.DOCTOR:
                    specialty = input("Ingrese su especialidad médica: ")
                    license_number = int(input("Ingrese su número de matrícula: "))
                    accepts_input = input("¿Acepta obra social? (s/n): ").lower()
                    accepts_medical_insurance = accepts_input == "s"

                self._user_service.register(
                    name=name,
                    surname=surname,
                    dni=dni,
                    email=email,
                    password=password,
                    phone_number=phone_number,
                    role=role,
                    date_of_birth=date_of_birth,
                    specialty=specialty,
                    accepts_medical_insurance=accepts_medical_insurance,
                    license_number=license_number
                )

                print("Usuario creado exitosamente. Puede proceder a iniciar sesión.\n")


            elif option == "2":
                email = input("Ingrese su email: ")
                password = input("Ingrese su contraseña: ")
                self.current_user = self._user_service.login(email, password)

            #Solo admin (Fullstack requirement)
            elif option == "3":
                if (self.current_user == None):
                    print("Error, debe iniciar sesión primero! \n")
                    continue
                if (self.current_user.role != RoleEnum.ADMIN):
                    print("Error, acción solo accesible para admin! \n")
                    continue
                users = self._user_service.get_all_users()
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
                data = self._user_service.get_all_users_by_role(role)
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
                user_found = self._user_service.get_user_by_id(id)
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
                user_found = self._user_service.get_user_by_email(email)
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
                    updated_user = self._user_service.update_user(name=name, surname=surname, dni=dni, 
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
                self._user_service.change_user_role(user_email, role)

            elif option == "9":
                if (self.current_user == None):
                    print("Error, debe iniciar sesión primero! \n")
                    continue
                input_email = input("Ingrese su dirección de " \
                "email para confirmar la baja de la cuenta: ")
                if self.current_user.email != input_email:
                    print("El email solicitado no coincide con el de la cuenta activa. \n")
                else:
                    disabled_user = self._user_service.disable_account(input_email)
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
                deleted_user = self._user_service.delete_account(input_email)
                if (deleted_user):
                    print("La cuenta se eliminó exitosamente. \n")
                else:
                    print("No se pudo eliminar la cuenta. Verifique el email.")

            #Solo doctor (Fullstack requirement for sprint 2)
            elif option == "11":
                if (self.current_user == None):
                    print("Error, debe iniciar sesión primero! \n")
                    continue
                if (self.current_user.role != RoleEnum.DOCTOR):
                    print("Error, acción solo accesible para doctor! \n")
                    continue
                timeframe = None
                while (timeframe == None):
                    input_timeframe = input("Ingrese numero de acuerdo al horario, uno por vez. 1. MAÑANA. 2. TARDE. 3. NOCHE.: ")
                    if input_timeframe == "1":
                        timeframe = TimeFrameEnum.MAÑANA
                    elif input_timeframe == "2":
                        timeframe = TimeFrameEnum.TARDE
                    elif input_timeframe == "3":
                        timeframe = TimeFrameEnum.NOCHE
                    else:
                        print("Horario no reconocido. Ingrese un horario válido.\n")
                        continue
                days = None
                while (days == None):
                    input_days = input("Ingrese numero de acuerdo al día, uno por vez. " \
                "1. LUNES. 2. MARTES. 3. MIERCOLES. 4. JUEVES. 5. VIERNES. 6. SABADO. 7. DOMINGO.: ")
                    if input_days == "1":
                        days = DaysEnum.LUNES
                    elif input_days == "2":
                        days = DaysEnum.MARTES
                    elif input_days == "3":
                        days = DaysEnum.MIERCOLES
                    elif input_days == "4":
                        days = DaysEnum.JUEVES
                    elif input_days == "5":
                        days = DaysEnum.VIERNES
                    elif input_days == "6":
                        days = DaysEnum.SABADO
                    elif input_days == "7":
                        days = DaysEnum.DOMINGO
                    else:
                        print("Día no reconocido. Ingrese un día válido.\n")
                        continue

                new_timeframe = self._availability_service.add_availability(
                    self.current_user.user_id, timeframe, days)
                if (new_timeframe):
                    print("La disponibilidad se creó exitosamente. \n")
                else:
                    print("No se pudo elcrear la disponibilidad.")

            #Solo doctor (Fullstack requirement for sprint 2)
            elif option == "12":
                if (self.current_user == None):
                    print("Error, debe iniciar sesión primero! \n")
                    continue
                if (self.current_user.role != RoleEnum.DOCTOR):
                    print("Error, acción solo accesible para doctor! \n")
                    continue
                availability_list = self._availability_service.get_all_by_doctor_id(
                                                            self.current_user.user_id)
                if not availability_list:
                    print("No se encuentran horarios para el profesional. \n")
                else:
                    print(f"Lista de horarios: {availability_list} \n")
                availability_id = input("Ingrese el id del horario que desea borrar. \n")
                deleted_timeframe = self._availability_service.remove_availability(
                    availability_id)
                if (deleted_timeframe): 
                    print("El horario ha sido eliminado exitosamente. \n")
                else: 
                    print("No se pudo eliminar el horario. Confirme el id del mismo. \n")
            
            #Solo doctor (Fullstack requirement for sprint 2)
            elif option == "13":
                if (self.current_user == None):
                    print("Error, debe iniciar sesión primero! \n")
                    continue
                if (self.current_user.role != RoleEnum.DOCTOR):
                    print("Error, acción solo accesible para doctor! \n")
                    continue
                availability_list = self._availability_service.get_all_by_doctor_id(
                                                            self.current_user.user_id)
                if not availability_list:
                    print("No se encuentran horarios para el profesional. \n")
                else:
                    print(f"Lista de horarios: {availability_list} \n")
                availability_id = input("Ingrese el id del horario que desea editar. \n")
                timeframe = None
                while (timeframe == None):
                    input_timeframe = input("Ingrese numero de acuerdo al horario, uno por vez. 1. MAÑANA. 2. TARDE. 3. NOCHE.: ")
                    if input_timeframe == "1":
                        timeframe = TimeFrameEnum.MAÑANA
                    elif input_timeframe == "2":
                        timeframe = TimeFrameEnum.TARDE
                    elif input_timeframe == "3":
                        timeframe = TimeFrameEnum.NOCHE
                    else:
                        print("Horario no reconocido. Ingrese un horario válido.\n")
                        continue
                days = None
                while (days == None):
                    input_days = input("Ingrese numero de acuerdo al día, uno por vez. " \
                "1. LUNES. 2. MARTES. 3. MIERCOLES. 4. JUEVES. 5. VIERNES. 6. SABADO. 7. DOMINGO.: ")
                    if input_days == "1":
                        days = DaysEnum.LUNES
                    elif input_days == "2":
                        days = DaysEnum.MARTES
                    elif input_days == "3":
                        days = DaysEnum.MIERCOLES
                    elif input_days == "4":
                        days = DaysEnum.JUEVES
                    elif input_days == "5":
                        days = DaysEnum.VIERNES
                    elif input_days == "6":
                        days = DaysEnum.SABADO
                    elif input_days == "7":
                        days = DaysEnum.DOMINGO
                    else:
                        print("Día no reconocido. Ingrese un día válido.\n")
                        continue

                updated_timeframe = self._availability_service.update_availability(
                    availability_id, timeframe, days)
                if (updated_timeframe):
                    print("El horario se editó exitosamente. \n")
                else:
                    print("No se pudo editar el horario.")

            #Solo doctor (Fullstack requirement for sprint 2)
            elif option == "14":
                if (self.current_user == None):
                    print("Error, debe iniciar sesión primero! \n")
                    continue
                if (self.current_user.role != RoleEnum.DOCTOR):
                    print("Error, acción solo accesible para doctor! \n")
                    continue
                availability_list = self._availability_service.get_all_by_doctor_id(
                                                        self.current_user.user_id)
                if not availability_list:
                    print("No se encuentran horarios para el profesional. \n")
                else:
                    print(f"Lista de horarios: {availability_list} \n")
             
            #Solo doctor (Fullstack requirement for sprint 2)
            elif option == "15":
                if (self.current_user == None):
                    print("Error, debe iniciar sesión primero! \n")
                    continue
                if (self.current_user.role != RoleEnum.DOCTOR):
                    print("Error, acción solo accesible para doctor! \n")
                    continue
                specialty = input("Ingrese su especialidad médica: ")
                license_number = int(input("Ingrese su número de matrícula: "))
                accepts_input = input("¿Acepta obra social? (s/n): ").lower()
                accepts_medical_insurance = accepts_input == "s"

                self._user_service.update_doctor_profile(
                    doctor_id = self.current_user.user_id,
                    specialty = specialty,
                    accepts_medical_insurance = accepts_medical_insurance,
                    license_number = license_number
                )
                print("Datos profesionales editados exitosamente.\n")


            #Solo paciente (Fullstack requirement for sprint 2)
            elif option == "16":
                if (self.current_user == None):
                    print("Error, debe iniciar sesión primero! \n")
                    continue
                searched_id = None
                is_doctor = False
                if (self.current_user.role == RoleEnum.ADMIN):
                    searched_id = input("Ingrese id del usuario para ver sus turnos. \n")
                    is_doctor_input = input("¿Es profesional médico? (s/n): ").lower()
                    is_doctor = is_doctor_input == "s"
                else:
                    searched_id = self.current_user.user_id
                    if (self.current_user.role == RoleEnum.DOCTOR):
                        is_doctor = True
                data = self._appointment_service.get_all_appointments_by_user_id(searched_id, is_doctor)
                if not data:
                    print("No hay turnos registrados para el usuario. \n")
                else:
                    print(f"Lista de turnos del usuario: {data} \n")

            #Solo paciente (Fullstack requirement for sprint 2)
            elif option == "17":
                if (self.current_user == None):
                    print("Error, debe iniciar sesión primero! \n")
                    continue
            
                if (self.current_user.role != RoleEnum.PATIENT):
                    print("Error, solo los pacientes pueden crear turnos! \n")
                    continue
            
                
                print("=== CREAR NUEVO TURNO ===")
                doctor_id = input("Ingrese ID del doctor: ")
                medical_consultation_id = input("Ingrese ID de consulta médica: ")
                
                
                date_str = input("Ingrese fecha (YYYY-MM-DD): ")
                time_str = input("Ingrese hora (HH:MM): ")
                
                try:
                    from datetime import datetime
                    date_and_time = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
                    
                    
                    appointment = self._appointment_service.create_appointment(
                        date_and_time=date_and_time,
                        user_id=self.current_user.user_id,
                        doctor_id=doctor_id,
                        medical_consultation_id=medical_consultation_id
                    )
                    
                    if appointment:
                        print("✅ Turno creado exitosamente!")
                        print(f"ID del turno: {appointment.appointment_id}")
                    else:
                        print("❌ No se pudo crear el turno")
                        
                except ValueError:
                    print("❌ Formato de fecha/hora inválido")
                except Exception as e:
                    print(f"❌ Error: {e}")

            #Opcion 0
            elif option == "0":
                print("Saliendo de WappTurno...\n ")
                break
            
            else:
                print("Opción no válida. Por favor, vuelva a intentar.\n")