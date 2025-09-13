from Role_enum import RoleEnum
from User import User
from connection_mysql import connection_mysql
import mysql.connector

class UserDAO: 

    def __init__(self):
       pass

    def open_connection(self):
        if hasattr(self, "__connection") and self.__connection.is_connected(): 
            pass
        self.__connection = connection_mysql().create_connection()

    def register_user(self, created_user: User):
        try:
            self.open_connection()
            with self.__connection.cursor() as cursor:
                query= ("INSERT INTO Users (user_id, name, surname, "
                    "dni, email, password, phone_number, role, date_of_birth, enabled) "
                    "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
                cursor.execute(query, (created_user.user_id, 
                                       created_user.name, 
                                       created_user.surname,
                                       created_user.dni,
                                       created_user.email,
                                       created_user.password,
                                       created_user.phone_number,
                                       created_user.role,
                                       created_user.date_of_birth,
                                       created_user.enabled))
                self.__connection.commit()
        except mysql.connector.Error as error:
            raise Exception(f"Error al insertar: {error}")
        finally: self.__connection.close()
        return created_user
        
    #TODO!!
    def get_user_by_id(self, user_id: str) -> User | None:
        try:
            self.open_connection()
            with self.__connection.cursor(dictionary=True) as cursor:
                query = "SELECT * FROM Users WHERE user_id = %s AND enabled = TRUE"
                cursor.execute(query, (user_id,))
                row = cursor.fetchone()
                if row:
                    role_enum = RoleEnum(row["role"]) if "role" in row else None
                    user = User(
                        name=row["name"],
                        surname=row["surname"],
                        dni=row["dni"],
                        email=row["email"],
                        password=row["password"],
                        phone_number=row["phone_number"],
                        role=role_enum,
                        date_of_birth=row["date_of_birth"]
                    )
                    user.enabled = row.get("enabled", True)
                    return user
                return None
        except mysql.connector.Error as error:
            raise Exception(f"Error al buscar usuario por ID: {error}")
        finally:
            self.__connection.close()
        
    
    def get_user_by_email(self, user_email: str) -> User | None:
        try:
            self.open_connection()
            with self.__connection.cursor(dictionary=True) as cursor:
                query= ("SELECT * FROM Users WHERE email = %s AND enabled = TRUE")
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
                        phone_number=row["phone_number"],
                        role=role_enum,
                        date_of_birth=row["date_of_birth"]
                    )
                    user.enabled = row.get("enabled", True)
                    return user
            return None
        except mysql.connector.Error as error:
            raise Exception(f"Error al buscar por email: {error}")

    def get_all_users(self) -> list['User']:
        try:
            self.open_connection()
            with self.__connection.cursor(dictionary=True) as cursor:
                query= ("SELECT * FROM Users WHERE enabled = TRUE")
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
                        phone_number=row["phone_number"],
                        role=role_enum,
                        date_of_birth=row["date_of_birth"]
                    )
                    user.enabled = row.get("enabled", True)
                    users.append(user)
            return users
        except mysql.connector.Error as error:
            raise Exception(f"Error al buscar usuarios: {error}")

    #TODO!!
    def get_all_users_by_role(self, role: RoleEnum) -> list['User']:
        try:
            self.open_connection()
            with self.__connection.cursor(dictionary=True) as cursor:
                query = "SELECT * FROM Users WHERE role = %s AND enabled = TRUE"
                cursor.execute(query, (role.value,))
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
                        phone_number=row["phone_number"],
                        role=role_enum,
                        date_of_birth=row["date_of_birth"]
                    )
                    user.enabled = row.get("enabled", True)
                    users.append(user)
            return users
        except mysql.connector.Error as error:
            raise Exception(f"Error al buscar usuarios por rol: {error}")
        finally:
            self.__connection.close()

    #No usado hasta que no agreguemos las otras clases y services.
    def get_all_doctor(self,):
        try:
            self.open_connection()
            with self.__connection.cursor(dictionary=True) as cursor:
                query= ("SELECT * FROM Users WHERE role = 'doctor' AND enabled = TRUE")
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
                        phone_number=row["phone_number"],
                        role=role_enum,
                        date_of_birth=row["date_of_birth"]
                    )
                    user.enabled = row.get("enabled", True)
                    users.append(user)
            return users
        except mysql.connector.Error as error:
            raise Exception(f"Error al buscar doctores: {error}")
    

    def update_user(self, name: str, surname: str, dni: int,
                    email: str, password: str, phone_number: int):
        try:
            self.open_connection()
            with self.__connection.cursor() as cursor:
                query= ("UPDATE Users SET name = %s, surname = %s, email = %s, dni = %s,"
                "password = %s, phone_number = %s WHERE email = %s")
                cursor.execute(query, (name, surname, dni, email, password, phone_number, email))
                self.__connection.commit()
                return True
        except mysql.connector.Error as error:
            raise Exception(f"Error al insertar: {error}")
        finally: self.__connection.close()
        
    
    def change_user_role(self, user_id: str, role: RoleEnum) -> bool:
        try:
            self.open_connection()
            with self.__connection.cursor(dictionary=True) as cursor:
                query= ("UPDATE Users SET role = %s WHERE user_id = %s")
                cursor.execute(query, (role, user_id,))
                self.__connection.commit()
                return True
        except mysql.connector.Error as error:
            raise Exception(f"Error al cambiar el rol del usuario: {error}")
        finally: self.__connection.close()


    def disable_account(self, email: str,) -> bool:
        try:
            self.open_connection()
            with self.__connection.cursor(dictionary=True) as cursor:
                query= ("UPDATE Users SET enabled = FALSE WHERE email = %s")
                cursor.execute(query, (email,))
                self.__connection.commit()
                return cursor.rowcount > 0
        except mysql.connector.Error as error:
            raise Exception(f"Error al deshabilitar el usuario: {error}")
        finally: self.__connection.close()
    
    def delete_account(self, email: str) -> bool:
        try:
            self.open_connection()
            with self.__connection.cursor(dictionary=True) as cursor:
                query = "DELETE FROM Users WHERE email = %s"
                cursor.execute(query, (email,))
                self.__connection.commit()
                return cursor.rowcount > 0
        except mysql.connector.Error as error:
            raise Exception(f"Error al eliminar permanentemente el usuario: {error}")
        finally: self.__connection.close()
