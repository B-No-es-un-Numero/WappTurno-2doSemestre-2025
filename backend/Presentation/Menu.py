from Services.User_service import UserService
from Services.Availability_service import AvailabilityService
from Services.Appointment_service import AppointmentService
from Models.Role_enum import RoleEnum
from Presentation.Patient_menu import PatientMenu
from Presentation.Doctor_menu import DoctorMenu
from Presentation.Admin_menu import AdminMenu

class Menu:
    def __init__(self, user_service: UserService, availability_service: AvailabilityService,
                 appointment_service: AppointmentService):
        self._user_service = user_service
        self._availability_service = availability_service
        self._appointment_service = appointment_service
        self.current_user = None

    def run_menu(self):
        while True:
            if self.current_user:
                print(f"\n Usuario conectado: {self.current_user.email} ({self.current_user.role.value})\n")
                self.run_role_menu()
            else:
                self.show_guest_menu()

    def show_guest_menu(self):
        option = input(
            "Elija una opción:\n"
            "1. Registrarse\n"
            "2. Ingresar\n"
            "0. Salir\n"
        )

        if option == "1":
            self.register_user()
        elif option == "2":
            self.login()
        elif option == "0":
            print("Saliendo de WappTurno...\n")
            exit()
        else:
            print("Opción no válida.\n")

    def register_user(self):
        name = input("Nombre: ")
        surname = input("Apellido: ")
        dni = int(input("DNI: "))
        phone_number = int(input("Teléfono: "))
        date_of_birth = input("Fecha de nacimiento (YYYY-MM-DD): ")
        email = input("Email: ")
        password = input("Contraseña: ")
        repeat_password = input("Repetir contraseña: ")

        if password != repeat_password:
            print("Las contraseñas no coinciden.\n")
            return

        role_input = input("Rol: 1) Paciente 2) Profesional 3) Administrador: ")
        role = {
            "1": RoleEnum.PATIENT,
            "2": RoleEnum.DOCTOR,
            "3": RoleEnum.ADMIN
        }.get(role_input)
        if not role:
            print("Rol inválido.\n")
            return

        specialty = license_number = accepts_medical_insurance = None
        if role == RoleEnum.DOCTOR:
            specialty = input("Especialidad médica: ")
            license_number = int(input("Número de matrícula: "))
            accepts_medical_insurance = input("¿Acepta obra social? (s/n): ").lower() == "s"

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
        print("Usuario registrado exitosamente.\n")

    def login(self):
        email = input("Email: ")
        password = input("Contraseña: ")
        self.current_user = self._user_service.login(email, password)
        if not self.current_user:
            print("\nEmail o contraseña incorrectos. Intente nuevamente.\n")
            return

    def run_role_menu(self):
        role = self.current_user.role
        if role == RoleEnum.PATIENT:
            PatientMenu(self._user_service, self._appointment_service, 
                        self.current_user).run()
        elif role == RoleEnum.DOCTOR:
            DoctorMenu(self._user_service, self._availability_service,
                       self._appointment_service, self.current_user).run()
        elif role == RoleEnum.ADMIN:
            AdminMenu(self._user_service, self._appointment_service, 
                      self.current_user).run()
        self.current_user = None  
