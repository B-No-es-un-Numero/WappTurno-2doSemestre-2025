from DAO.connection_mysql import connection_mysql
import mysql.connector
from Models.Availability import Availability
from Models.Days_enum import DaysEnum
from Models.TimeFrame_enum import TimeFrameEnum

class AvailabilityDAO: 

    def __init__(self):
       pass


    def open_connection(self):
        if hasattr(self, "__connection") and self.__connection.is_connected(): 
            pass
        self.__connection = connection_mysql().create_connection()


    def add(self, new_availability: Availability) -> Availability:
        try:
            self.open_connection()
            cursor = self.__connection.cursor()
            query_availability = (
            "INSERT INTO Availability (id, doctor_id, time_frame, days) "
            "VALUES (%s, %s, %s, %s)"
            )
            cursor.execute(
            query_availability,
            (
                new_availability.id,
                new_availability.doctor_id,
                new_availability.time_frame,
                new_availability.days
            ),
            )    
            self.__connection.commit()
            return new_availability  
        except mysql.connector.Error as error:
            self.__connection.rollback()
            raise Exception(f"Error al insertar en la base de datos: {error}") 
        finally:        
            cursor.close()
            self.__connection.close()  
    

    def delete(self, availability_id: str) -> bool:
        try:
            self.open_connection()
            cursor = self.__connection.cursor()
            query = "DELETE FROM Availability WHERE id = %s"
            cursor.execute(query, (availability_id,))
            self.__connection.commit()
            return cursor.rowcount > 0
        except mysql.connector.Error as error:
            self.__connection.rollback()
            raise Exception(f"Error al eliminar el horario: {error}")
        finally: 
            cursor.close()
            self.__connection.close()


    def update(self, availability_id: str, time_frame: TimeFrameEnum, days: DaysEnum) -> bool:    
        try:
            self.open_connection()
            cursor = self.__connection.cursor()
            query_availability = (
            "UPDATE Availability SET time_frame=%s, days=%s "
            "WHERE id=%s"
            )
            cursor.execute(
            query_availability,
            (time_frame,days,availability_id,),
            )    
            self.__connection.commit()
            return True  
        except mysql.connector.Error as error:
            self.__connection.rollback()
            raise Exception(f"Error al insertar en la base de datos: {error}") 
        finally:        
            cursor.close()
            self.__connection.close()  
        

    def get_all_by_doctor_id(self, doctor_id: str) -> list['Availability']:
        try:
            self.open_connection()
            with self.__connection.cursor(dictionary=True) as cursor:
                query = "SELECT * FROM Availability WHERE doctor_id = %s"
                cursor.execute(query, (doctor_id,))
                rows = cursor.fetchall()
                data_list = []
                for row in rows:
                    availability = Availability(         
                        doctor_id=row["doctor_id"],
                        time_frame=row["time_frame"],
                        days=row["days"]
                    )
                    availability.id = row["id"]
                    data_list.append(availability)
            return data_list
        except mysql.connector.Error as error:
            raise Exception(f"Error al buscar horarios por doctor: {error}")
        finally:
            self.__connection.close()
    
        
    def get_availability_by_id(self, availability_id: str) -> Availability:
        try:
            self.open_connection()
            with self.__connection.cursor(dictionary=True) as cursor:
                query = "SELECT * FROM Availability WHERE id = %s"
                cursor.execute(query, (availability_id,))
                row = cursor.fetchone()
                if row:
                    availability = Availability(
                        doctor_id=row["doctor_id"],
                        time_frame=row["time_frame"],
                        days=row["days"]
                    )
                    availability.id = row["id"]
                    return availability
                else:
                    return None

        except mysql.connector.Error as error:
            raise Exception(f"Error al buscar horarios por id: {error}")

        finally:
            self.__connection.close()
