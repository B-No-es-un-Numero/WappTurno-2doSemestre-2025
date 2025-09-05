from Role_enum import RoleEnum
from User import User
from connection_mysql import connection_mysql
import mysql.connector

class UserDAO: 

    def __init__(self):
        self.__connection = connection_mysql().create_connection()
        
    def register_user(self, created_user: User):
        try:
            with self.__connection.cursor() as cursor:
                query= ("INSERT INTO User (user_id, name, surname, "
                    "dni, email, password, role, date_of_birth, enabled) "
                    "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)")
                cursor.execute(query, (created_user.user_id, 
                                       created_user.name, 
                                       created_user.surname,
                                       created_user.dni,
                                       created_user.email,
                                       created_user.password,
                                       created_user.role,
                                       created_user.date_of_birth,
                                       created_user.enabled))
                self.__connection.commit()
        except mysql.connector.Error as error:
            raise f"Error al insertar, {error}"
        return created_user
        

    def get_user_by_id(self, user_id: str):
        user_exists = next(filter(lambda u: u.user_id == user_id
                                  and u.enabled == True, 
                                  self.__Users), None)
        return user_exists
        
    
    def get_user_by_email(self, user_email: str):
        user_exists = next(filter(lambda u: u.email == user_email
                                  and u.enabled == True,  
                                  self.__Users), None)
        return user_exists

    def get_all_users(self):
        user_list = list(filter(lambda u: u.enabled == True, 
                                  self.__Users))
        return user_list

    def get_all_users_by_role(self, role: RoleEnum):
        user_list = list(filter(lambda u: u.enabled == True
                                  and u.role == role,
                                  self.__Users))
        return user_list
    
    def update_user(self, name: str, surname: str, email: str, password: str):
        searched_user = self.get_user_by_email(email)
        searched_user.name = name
        searched_user.surname = surname
        searched_user.password = password
        return searched_user
    
    def change_user_role(self, user_id: str, role: RoleEnum):
        searched_user = self.get_user_by_id(user_id)
        searched_user.role = role
        return searched_user

    def disable_account(self, user_email: str):
        searched_user = self.get_user_by_email(user_email)
        searched_user.enabled = False
        return searched_user