from Models.Appointment import Appointment
from Models.Appointment_state_enum import AppointmentStateEnum
from DAO.connection_mysql import connection_mysql
import mysql.connector
from datetime import datetime

class AppointmentDAO:

    def __init__(self):
        pass

    def open_connection(self):
        if hasattr(self, "__connection") and self.__connection.is_connected(): 
            pass
        else:
            self.__connection = connection_mysql().create_connection()

    def create_appointment(self, appointment: Appointment):
        
        try:
            self.open_connection()
            with self.__connection.cursor() as cursor:
                query = (
                    "INSERT INTO Appointments (id, date_and_time, user_id, doctor_id, medical_consultation_id, frequency, state, enabled) "
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                )
                cursor.execute(query, (
                    appointment.appointment_id,
                    appointment.date_and_time,
                    appointment.user_id,
                    appointment.doctor_id,
                    appointment.medical_consultation_id,
                    appointment.frequency,
                    appointment.state.value,
                    appointment.enabled
                ))
                self.__connection.commit()
                return True
                
        except mysql.connector.Error as err:
            print(f"Error al crear appointment: {err}")
            return None
        finally:
            if hasattr(self, "__connection") and self.__connection.is_connected():
                self.__connection.close()

    def reschedule_appointment(self, appointment_id: str, date_and_time: datetime):
        
        try:
            self.open_connection()
            with self.__connection.cursor() as cursor:
                query = "UPDATE Appointments SET date_and_time = %s WHERE id = %s AND enabled = TRUE"
                cursor.execute(query, (date_and_time, appointment_id))
                self.__connection.commit()
                return cursor.rowcount > 0
        except mysql.connector.Error as err:
            print(f"Error al reprogramar appointment: {err}")
            return False
        finally:
            if hasattr(self, "__connection") and self.__connection.is_connected():
                self.__connection.close()

    def delete_appointment(self, appointment_id: str):
        
        try:
            self.open_connection()
            with self.__connection.cursor() as cursor:
                query = "UPDATE Appointments SET enabled = FALSE WHERE id = %s"
                cursor.execute(query, (appointment_id,))
                self.__connection.commit()
                return cursor.rowcount > 0
        except mysql.connector.Error as err:
            print(f"Error al eliminar appointment: {err}")
            return False
        finally:
            if hasattr(self, "__connection") and self.__connection.is_connected():
                self.__connection.close()

    def update_frequency(self, appointment_id: str, frequency: str):
        
        try:
            self.open_connection()
            with self.__connection.cursor() as cursor:
                query = (
                    "UPDATE Appointments SET frequency = %s "
                    "WHERE id = %s AND enabled = TRUE"
                )
                cursor.execute(query, (frequency, appointment_id))
                self.__connection.commit()
                return cursor.rowcount > 0
                
        except mysql.connector.Error as err:
            print(f"Error al actualizar frecuencia: {err}")
            return False
        finally:
            if hasattr(self, "__connection") and self.__connection.is_connected():
                self.__connection.close()

    def update_state(self, appointment_id: str, appointment_state_enum: AppointmentStateEnum) -> bool:
        
        try:
            self.open_connection()
            with self.__connection.cursor() as cursor:
                query = (
                    "UPDATE Appointments SET state = %s "
                    "WHERE id = %s AND enabled = TRUE"
                )
                cursor.execute(query, (appointment_state_enum.value, appointment_id))
                self.__connection.commit()
                return cursor.rowcount > 0
                
        except mysql.connector.Error as err:
            print(f"Error al actualizar estado: {err}")
            return False
        finally:
            if hasattr(self, "__connection") and self.__connection.is_connected():
                self.__connection.close()