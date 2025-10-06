from DAO.connection_mysql import connection_mysql
import mysql.connector
from Models.Availability import Availability

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
            with self.__connection.cursor() as cursor:
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
        except mysql.connector.Error as error:
            self.__connection.rollback()
            raise Exception(f"Error al insertar en la base de datos: {error}") 
        finally:        
            self.__connection.close()  
        return new_availability