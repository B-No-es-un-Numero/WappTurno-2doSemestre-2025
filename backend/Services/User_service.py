from datetime import datetime
from Models.Doctor import Doctor
from Models.User import User
from Models.Role_enum import RoleEnum
from DAO.User_DAO import UserDAO

class UserService:
    def __init__(self, dao: UserDAO):
        self._dao = dao

    def register( self, name: str, surname: str, dni: int, email: str, password: str,
        phone_number: int, role: RoleEnum, date_of_birth: str, specialty: str = None,
        accepts_medical_insurance: bool = None, license_number: int = None
    ) -> User:
        if not all([name, surname, dni, email, password, phone_number, date_of_birth]):
            print("Error! No se permiten campos vacíos.\n")
            return None

        already_exists = self._dao.get_user_by_email(email, close=False)
        if already_exists:
            print("Error! Este usuario ya se encuentra registrado. Proceda a iniciar sesión.\n")
            return None

        if len(password) < 6 or not any(c.isalpha() for c in password) or not any(c.isdigit() for c in password):
            print("Contraseña inválida. Debe tener al menos 6 caracteres e incluir letras y números.\n")
            return None

        try:
            date_of_birth_formatted = datetime.strptime(date_of_birth, "%Y-%m-%d").date()
        except ValueError:
            print("Fecha inválida. Use el formato YYYY-MM-DD.\n")
            return None

        if role == RoleEnum.DOCTOR:
            if not all([specialty is not None, license_number is not None, accepts_medical_insurance is not None]):
                print("Faltan datos obligatorios para registrar un profesional de salud.\n")
                return None

            created_user = Doctor(
                name=name,
                surname=surname,
                dni=dni,
                email=email,
                password=password,
                phone_number=phone_number,
                date_of_birth=date_of_birth_formatted,
                specialty=specialty,
                accepts_medical_insurance=accepts_medical_insurance,
                license_number=license_number
            )
        else:
            created_user = User(
                name=name,
                surname=surname,
                dni=dni,
                email=email,
                password=password,
                phone_number=phone_number,
                role=role,
                date_of_birth=date_of_birth_formatted
            )

        self._dao.register_user(created_user)

        return created_user
        
    def login(self, user_email: str, password: str) -> User:
        data = self._dao.get_user_by_email(user_email, close=False)
        if data is None:
            return None
        if data.password == password:
            return data
        else:
            return None

    def get_user_by_id(self, user_id: str) -> 'User':
        user = self._dao.get_user_by_id(user_id)
        if user is None:
            print("No se encontró el usuario buscado. \n")
            return None
        return user

    def get_user_by_email(self, user_email: str) -> 'User':
        user = self._dao.get_user_by_email(user_email)
        if user is None:
            return None
        return user
    
    #Solo para admin
    def get_all_users(self) -> list['User']:
        users = self._dao.get_all_users()
        return users
   
    def get_all_users_by_role(self, role: RoleEnum) -> list['User']:
        users = self._dao.get_all_users_by_role(role)
        return users

    #Solo para propio user
    def update_user(self, name: str, surname: str, dni: int, 
                       email: str, phone_number: int, password: str) -> 'User':
        
        if not all([name, surname, dni, email, password, phone_number]):
            print("Error! No se permiten campos vacíos. \n")
            return None

        if len(password) < 6 or not any(c.isalpha() for c in password) or not any(c.isdigit() for c in password):
            print("Contraseña inválida. Recuerde que debe tener" \
            "longitud de 6 caracteres mínimo e incluir letras y números. \n")
            return None
        
        user = self._dao.update_user(name, surname, dni, email, password, phone_number)

        return user

    #Solo para admin
    def change_user_role(self, user_email: str, role: RoleEnum) -> bool:
        searched_user = self._dao.get_user_by_email(user_email, close=False)
        if searched_user is None:
            return False
        self._dao.change_user_role(user_email, role)
        return True

    #Solo para propio user
    def disable_account(self, user_email: str,) -> 'User':
        user = self._dao.disable_account(user_email,)
        return user
    
    #Solo para admin
    def delete_account(self, user_email: str,) -> 'User':
        user = self._dao.delete_account(user_email,)
        return user

    #Solo para doctor
    def update_doctor_profile(self, doctor_id: str, specialty: str,
        accepts_medical_insurance: bool, license_number: int) -> Doctor:
        doctor = self._dao.get_user_by_id(doctor_id)
        if doctor is None:
            print("No se encontró el usuario buscado. \n")
            return None
        else:
            return self._dao.update_doctor(doctor_id, specialty, accepts_medical_insurance,
                                     license_number)