from datetime import datetime
from User import User
from Role_enum import RoleEnum
from User_DAO import UserDAO

class UserService:
    def __init__(self, dao: UserDAO):
        self.__dao = dao

    def register(self, name: str, surname: str, dni: int, email: str,
                 password: str, phone_number: int, role: RoleEnum, date_of_birth: str) -> User:
        if not all([name, surname, dni, email, password, phone_number, date_of_birth]):
            print("Error! No se permiten campos vacíos. \n")
            return None

        already_exists = self.get_user_by_email(email)
        if already_exists:
            print("Error! Este usuario ya se encuentra registrado! Proceda a iniciar sesión. \n")
            return None

        if len(password) < 6 or not any(c.isalpha() for c in password) or not any(c.isdigit() for c in password):
            print("Contraseña inválida. Recuerde que debe tener" \
            " longitud de 6 caracteres mínimo e incluir letras y números. \n")
            return None

        try:
            date_of_birth_formatted = datetime.strptime(date_of_birth, "%d-%m-%Y")
        except ValueError:
            print("Fecha inválida. Use el formato DD-MM-AAAA.\n")
            return None
        
        created_user = User(name, surname, dni, email, password, phone_number, role, date_of_birth_formatted)

        self.__dao.register_user(created_user)

        return created_user
        
    def login(self, user_email: str, password: str) -> User:
        data = self.get_user_by_email(user_email)
        if data is None:
            return None
        if data.password == password:
            print(f"Acceso permitido! Hola {data.name}! \n")
            return data
        else:
            print("Acceso denegado, contraseña incorrecta. \n")
            return None

    def get_user_by_id(self, user_id: str) -> 'User':
        user = self.__dao.get_user_by_id(user_id)
        if user is None:
            print("No se encontró el usuario buscado. \n")
            return None
        return user

    def get_user_by_email(self, user_email: str) -> 'User':
        user = self.__dao.get_user_by_email(user_email)
        if user is None:
            return None
        return user
    
    #Solo para admin
    def get_all_users(self) -> list['User']:
        users = self.__dao.get_all_users()
        return users
   
   #Solo para admin
    def get_all_users_by_role(self, role: RoleEnum) -> list['User']:
        users = self.__dao.get_all_users_by_role(role)
        return users

    def update_user(self, name: str, surname: str, dni: int, 
                       email: str, password: str, phone_number: int) -> 'User':
        
        if not all([name, surname, dni, email, password, phone_number]):
            print("Error! No se permiten campos vacíos. \n")
            return None

        if len(password) < 6 or not any(c.isalpha() for c in password) or not any(c.isdigit() for c in password):
            print("Contraseña inválida. Recuerde que debe tener" \
            "longitud de 6 caracteres mínimo e incluir letras y números. \n")
            return None
        
        user = self.__dao.update_user(name, surname, dni, password, email, phone_number)

        return user

    #Solo para admin
    def change_user_role(self, user_id: str, role: RoleEnum) -> bool:
        searched_user = self.get_user_by_id(user_id)
        if searched_user is None:
            return False
        self.__dao.change_user_role(user_id, role)
        return True

    def disable_account(self, user_email: str,) -> 'User':
        user = self.__dao.disable_account(user_email,)
        return user
    
    #Solo para admin
    def delete_account(self, user_email: str,) -> 'User':
        user = self.__dao.delete_account(user_email,)
        return user
