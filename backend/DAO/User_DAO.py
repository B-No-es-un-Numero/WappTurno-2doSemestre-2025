from Models.Role_enum import RoleEnum
from Models.Doctor import Doctor
from Models.User import User
from DAO.connection_mysql import connection_mysql
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
                query_user = (
                "INSERT INTO Users (id, name, surname, dni, email, password, phone_number, role, date_of_birth, enabled) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                )
                cursor.execute(
                query_user,
                (
                    created_user.user_id,
                    created_user.name,
                    created_user.surname,
                    created_user.dni,
                    created_user.email,
                    created_user.password,
                    created_user.phone_number,
                    created_user.role.name,
                    created_user.date_of_birth,
                    created_user.enabled,
                ),
            )   
                if (created_user.role.name == "DOCTOR"):
                    query_doctor = (
                        "INSERT INTO Doctors (user_id, specialty, accepts_medical_insurance, license_number) "
                        "VALUES (%s, %s, %s, %s)"
                    )
                    cursor.execute(
                    query_doctor,
                    (
                        created_user.user_id,
                        created_user.specialty,
                        created_user.accepts_medical_insurance,
                        created_user.license_number,
                    ),
                )   
            self.__connection.commit()  
        except mysql.connector.Error as error:
            self.__connection.rollback()
            raise Exception(f"Error al insertar en la base de datos: {error}") 
        finally:        
            self.__connection.close()  
        return created_user
        

    def get_user_by_id(self, user_id: str) -> User | None:
        try:
            self.open_connection()
            with self.__connection.cursor(dictionary=True) as cursor:
                query = "SELECT * FROM Users WHERE id = %s AND enabled = TRUE"
                cursor.execute(query, (user_id,))
                row = cursor.fetchone()
                if row:
                   return self.__create_user_dto(row)
                return None
        except mysql.connector.Error as error:
            raise Exception(f"Error al buscar usuario por ID: {error}")
        finally:
            self.__connection.close()


    def get_user_by_email(self, user_email: str, close: bool = True) -> User | None:
        try:
            self.open_connection()
            with self.__connection.cursor(dictionary=True) as cursor:
                query= ("SELECT * FROM Users WHERE email = %s AND enabled = TRUE")
                cursor.execute(query, (user_email,))
                row = cursor.fetchone()
                if row:
                    return self.__create_user_dto(row)    
                return None
        except mysql.connector.Error as error:
            raise Exception(f"Error al buscar por email: {error}")
        finally:
            if close:
                self.__connection.close()


    def get_all_users(self) -> list['User']:
        try:
            self.open_connection()
            with self.__connection.cursor(dictionary=True) as cursor:
                query= ("SELECT * FROM Users WHERE enabled = TRUE "
                "AND role != 'ADMIN'")
                cursor.execute(query, ())
                rows = cursor.fetchall()
                users = []

                for row in rows:
                    user = self.__create_user_dto(row) 
                    users.append(user)
            return users
        except mysql.connector.Error as error:
            raise Exception(f"Error al buscar usuarios: {error}")
        finally: self.__connection.close()

 
    def get_all_users_by_role(self, role: RoleEnum) -> list['User']:
        try:
            self.open_connection()
            with self.__connection.cursor(dictionary=True) as cursor:
                query = """
                    SELECT 
                        u.*,
                        d.specialty,
                        d.accepts_medical_insurance,
                        d.license_number
                    FROM Users u
                    LEFT JOIN Doctors d ON u.id = d.user_id
                    WHERE u.role = %s AND u.enabled = TRUE
                """
                cursor.execute(query, (role.value,))
                rows = cursor.fetchall()
                users = []
    
                for row in rows:
                    user = self.__create_user_dto(row) 
                    users.append(user)
                return users
            
        except mysql.connector.Error as error:
            raise Exception(f"Error al buscar usuarios por rol: {error}")
        finally:
            self.__connection.close()


    def update_user(self, name: str, surname: str, dni: int,
                    email: str, password: str, phone_number: int) -> User | None:
        try:
            self.open_connection()
            with self.__connection.cursor(dictionary=True) as cursor:
                query= ("UPDATE Users SET name = %s, surname = %s,  dni = %s,"
                "password = %s, phone_number = %s WHERE email = %s")
                cursor.execute(query, (name, surname, dni, password, phone_number, email))
                self.__connection.commit()
                if cursor.rowcount == 0:
                    return None
                
                cursor.execute("SELECT * FROM Users WHERE email = %s", (email,))
                row = cursor.fetchone()
                if row:
                    return self.__create_user_dto(row)
            
        except mysql.connector.Error as error:
            self.__connection.rollback()
            raise Exception(f"Error al insertar: {error}")
        finally: self.__connection.close()
    

    def change_user_role(self, user_email: str, role: RoleEnum) -> bool:
        try:
            self.open_connection()
            with self.__connection.cursor(dictionary=True) as cursor:
                query= ("UPDATE Users SET role = %s WHERE email = %s")
                cursor.execute(query, (role, user_email,))
                self.__connection.commit()
                return True
        except mysql.connector.Error as error:
            self.__connection.rollback()
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
            self.__connection.rollback()
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
            self.__connection.rollback()
            raise Exception(f"Error al eliminar permanentemente el usuario: {error}")
        finally: self.__connection.close()


    def update_doctor(self, doctor_id: str, specialty: str, accepts_medical_insurence: bool,
                              license_number: int) -> Doctor | None:
        try:
            self.open_connection()
            with self.__connection.cursor(dictionary=True) as cursor:
                query= ("UPDATE Doctors SET specialty = %s, accepts_medical_insurance = %s,"
                "license_number = %s WHERE user_id = %s")
                cursor.execute(query, (specialty, accepts_medical_insurence,
                                       license_number, doctor_id))
                self.__connection.commit()
                if cursor.rowcount == 0:
                    return None

                cursor.execute("SELECT * FROM Users " \
                "JOIN Doctors ON Users.id = Doctors.user_id " \
                "WHERE id = %s", (doctor_id,))
                row = cursor.fetchone()
                if row:
                    return self.__create_user_dto(row)
        except mysql.connector.Error as error:
            self.__connection.rollback()
            raise Exception(f"Error al insertar: {error}")
        finally: self.__connection.close()


    def __create_user_dto(self, data_row) -> User:
        role_enum = RoleEnum(data_row["role"]) if "role" in data_row else None
        if (role_enum.name == "DOCTOR" and data_row.get("specialty") is not None):
            doctor = Doctor(
                            name=data_row["name"],
                            surname=data_row["surname"],
                            dni=data_row["dni"],
                            email=data_row["email"],
                            password=data_row["password"],
                            phone_number=data_row["phone_number"],
                            date_of_birth=data_row["date_of_birth"],
                            specialty=data_row["specialty"],
                            accepts_medical_insurance=data_row["accepts_medical_insurance"],
                            license_number=data_row["license_number"]
                        )
            doctor.user_id = data_row["id"]
            doctor.enabled = data_row.get("enabled", True)
            return doctor           
        user = User(
            name=data_row["name"],
            surname=data_row["surname"],
            dni=data_row["dni"],
            email=data_row["email"],
            password=data_row["password"],
            phone_number=data_row["phone_number"],
            role=role_enum,
            date_of_birth=data_row["date_of_birth"]
        )
        user.user_id = data_row.get("id")
        user.enabled = data_row.get("enabled", True)
        return user
    


