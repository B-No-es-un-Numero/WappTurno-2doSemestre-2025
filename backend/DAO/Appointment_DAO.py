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
            print(f"Error al crear el turno: {err}")
            return None
        finally:
            if hasattr(self, "__connection") and self.__connection.is_connected():
                self.__connection.close()

    def reschedule_appointment(self, appointment_id: str, date_and_time: datetime):
        
        try:
            self.open_connection()
            with self.__connection.cursor() as cursor:
                query = "UPDATE Appointments SET date_and_time = %s " \
                        "WHERE id = %s AND enabled = TRUE"
                cursor.execute(query, (date_and_time, appointment_id))
                self.__connection.commit()
                return cursor.rowcount > 0
        except mysql.connector.Error as err:
            print(f"Error al reprogramar turno: {err}")
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
            print(f"Error al eliminar turno: {err}")
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

    def get_appointment_by_id(self, appointment_id: str,
                              close: bool = True) -> Appointment | None:
        try:
            self.open_connection()
            with self.__connection.cursor(dictionary=True) as cursor:
                query= ("SELECT * FROM Appointments WHERE id = %s AND enabled = TRUE")
                cursor.execute(query, (appointment_id,))
                row = cursor.fetchone()
                if row:
                    state_enum = AppointmentStateEnum(row["state"]) if "state" in row else AppointmentStateEnum.SCHEDULED
                    appointment = Appointment(
                        date_and_time=row["date_and_time"],
                        user_id=row["user_id"],
                        doctor_id=row["doctor_id"],
                        medical_consultation_id=row["medical_consultation_id"],
                        frequency=row["frequency"],
                        state=state_enum,
                    )
                    appointment.appointment_id = row.get("id")
                    appointment.enabled = row.get("enabled", True)
                    return appointment
            return None
        except mysql.connector.Error as error:
            raise Exception(f"Error al buscar turno por id: {error}")
        finally:
            if close:
                self.__connection.close()

    def get_all_appointments_by_user_id(self, user_id, is_doctor):
        try:
            self.open_connection()
            with self.__connection.cursor(dictionary=True) as cursor:
                
                if is_doctor:
                    
                    query = """
                    SELECT 
                        a.id, a.date_and_time, a.state, a.frequency, a.enabled,
                        a.user_id, a.doctor_id, a.medical_consultation_id,
                        u.name as patient_name, u.surname as patient_surname,
                        mc.name as consultation_name
                    FROM Appointments a
                    JOIN Users u ON a.user_id = u.id
                    JOIN Medical_consultations mc ON a.medical_consultation_id = mc.id
                    WHERE a.doctor_id = %s AND a.enabled = TRUE
                    ORDER BY a.date_and_time
                    """
                else:
                    
                    query = """
                    SELECT 
                        a.id, a.date_and_time, a.state, a.frequency, a.enabled,
                        a.user_id, a.doctor_id, a.medical_consultation_id,
                        d.name as doctor_name, d.surname as doctor_surname,
                        doc.specialty, mc.name as consultation_name
                    FROM Appointments a
                    JOIN Users d ON a.doctor_id = d.id
                    JOIN Doctors doc ON a.doctor_id = doc.user_id
                    JOIN Medical_consultations mc ON a.medical_consultation_id = mc.id
                    WHERE a.user_id = %s AND a.enabled = TRUE
                    ORDER BY a.date_and_time
                    """
                
                cursor.execute(query, (user_id,))
                rows = cursor.fetchall()
                appointments = []
                
                for row in rows:
                    state_enum = AppointmentStateEnum(row["state"].lower()) if "state" in row else AppointmentStateEnum.SCHEDULED
                    appointment = Appointment(
                        date_and_time=row["date_and_time"],
                        user_id=row["user_id"],
                        doctor_id=row["doctor_id"],
                        medical_consultation_id=row["medical_consultation_id"],
                        frequency=row["frequency"],
                    )
                    appointment.appointment_id = row.get("id")
                    appointment.enabled = row.get("enabled", True)
                    appointment.state = state_enum
                    
                    
                    if is_doctor:
                        
                        appointment.patient_info = f"{row.get('patient_name')} {row.get('patient_surname')}"
                    else:
                        
                        appointment.doctor_info = f"Dr. {row.get('doctor_name')} {row.get('doctor_surname')}"
                        appointment.specialty = row.get("specialty")
                    
                    # Info de la consulta (para ambos)
                    appointment.consultation_name = row.get("consultation_name")
                    
                    appointments.append(appointment)
                    
            return appointments
        except mysql.connector.Error as error:
            raise Exception(f"Error al buscar turnos del usuario: {error}")
        finally:
            self.__connection.close()

    def check_time_conflict(self, doctor_id: str, date_and_time: datetime):
        
        try:
            self.open_connection()
            
            query = """
            SELECT COUNT(*) as conflicts
            FROM Appointments 
            WHERE doctor_id = %s 
            AND date_and_time = %s
            AND state IN ('SCHEDULED', 'RESCHEDULED')
            AND enabled = 1
            """
            
            cursor = self.__connection.cursor()
            cursor.execute(query, (doctor_id, date_and_time))
            result = cursor.fetchone()
            conflicts_count = result[0]  
            
            return conflicts_count > 0
            
        except Exception as e:
            print(f"Error al verificar conflictos: {e}")
            return True  
        finally:
            self.__connection.close()

    

