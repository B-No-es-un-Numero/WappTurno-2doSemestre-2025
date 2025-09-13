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
            raise Exception(f"Error al insertar: {error}")
        finally: self.__connection.close()
        return created_user
        

    def get_user_by_id(self, user_id: str):
        user_exists = next(filter(lambda u: u.user_id == user_id
                                  and u.enabled == True, 
                                  self.__Users), None)
        return user_exists
        
    
    def get_user_by_email(self, user_email: str) -> User | None:
        try:
            with self.__connection.cursor(dictionary=True) as cursor:
                query= ("SELECT * FROM User WHERE email = %s AND enabled = TRUE")
                cursor.execute(query, (user_email,))
                row = cursor.fetchone()
                if row:
                    role_enum = RoleEnum(row["role"]) if "role" in row else None
                    user = User(
                        name=row["name"],
                        surname=row["surname"],
                        dni=row["dni"],
                        email=row["email"],
                        password=row["password"],
                        role=role_enum,
                        date_of_birth=row["date_of_birth"]
                    )
    
                    user.enabled = row.get("enabled", True)
                return user
            return None
        except mysql.connector.Error as error:
            raise Exception(f"Error al buscar por email: {error}")
        finally: 
            pass
 


    def get_all_users(self) -> list['User']:
        try:
            with self.__connection.cursor(dictionary=True) as cursor:
                query= ("SELECT * FROM User WHERE enabled = TRUE")
                cursor.execute(query, ())
                rows = cursor.fetchall()
                users = []

                for row in rows:
                    role_enum = RoleEnum(row["role"]) if "role" in row else None
                    user = User(
                        name=row["name"],
                        surname=row["surname"],
                        dni=row["dni"],
                        email=row["email"],
                        password=row["password"],
                        role=role_enum,
                        date_of_birth=row["date_of_birth"]
                    )
                    user.enabled = row.get("enabled", True)
                    users.append(user)
            return users
        except mysql.connector.Error as error:
            raise Exception(f"Error al buscar usuarios: {error}")
        finally: 
            pass


    def get_all_users_by_role(self, role: RoleEnum):
        user_list = list(filter(lambda u: u.enabled == True
                                  and u.role == role,
                                  self.__Users))
        return user_list

    def get_all_doctor(self,):
        try:
            with self.__connection.cursor(dictionary=True) as cursor:
                query= ("SELECT * FROM User WHERE role = 'doctor' AND enabled = TRUE")
                cursor.execute(query, ())
                rows = cursor.fetchall()
                users = []

                for row in rows:
                    role_enum = RoleEnum(row["role"]) if "role" in row else None
                    user = User(
                        name=row["name"],
                        surname=row["surname"],
                        dni=row["dni"],
                        email=row["email"],
                        password=row["password"],
                        role=role_enum,
                        date_of_birth=row["date_of_birth"]
                    )
                    user.enabled = row.get("enabled", True)
                    users.append(user)
            return users
        except mysql.connector.Error as error:
            raise Exception(f"Error al buscar doctores: {error}")
        finally: 
            pass
    
    
    def update_user(self, name: str, surname: str, email: str, password: str):
        try:
            with self.__connection.cursor() as cursor:
                query= ("UPDATE User SET name = %s, surname = %s, email = %s, password = %s WHERE email = %s")
                cursor.execute(query, (name, surname, email, password, email))
                self.__connection.commit()
        except mysql.connector.Error as error:
            raise Exception(f"Error al insertar: {error}")
        finally: 
            pass
    
    
    def change_user_role(self, user_id: str, role: RoleEnum):
        searched_user = self.get_user_by_id(user_id)
        searched_user.role = role
        return searched_user

    def disable_account(self, email: str,) -> bool:
        try:
            with self.__connection.cursor(dictionary=True) as cursor:
                query= ("UPDATE User SET enabled = FALSE WHERE email = %s")
                cursor.execute(query, (email,))
                self.__connection.commit()
                return cursor.rowcount > 0
        except mysql.connector.Error as error:
            raise Exception(f"Error al deshabilitar el usuario: {error}")
        finally: 
            pass
    
    