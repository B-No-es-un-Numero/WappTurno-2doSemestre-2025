from Models.Appointment import Appointment
from Models.Medical_consultation import Medical_consultation
from Models.Appointment_state_enum import AppointmentStateEnum
from Models.Days_enum import DaysEnum
from Models.TimeFrame_enum import TimeFrameEnum
from DAO.Appointment_DAO import AppointmentDAO
from DAO.Availability_DAO import AvailabilityDAO
from datetime import datetime

class AppointmentService:
    
    def __init__(self, appointment_dao: AppointmentDAO, availability_dao: AvailabilityDAO):
        self._appointment_dao = appointment_dao
        self._availability_dao = availability_dao


    def create_appointment(self, date_and_time: datetime, user_id: str, doctor_id: str, 
                          medical_consultation_id: str, frequency: str = None) -> Appointment:
       
        try:
            
            if not self._validate_appointment_data(date_and_time, user_id, doctor_id, medical_consultation_id):
                return None
            
            new_appointment = Appointment(
                date_and_time=date_and_time,
                user_id=user_id,
                doctor_id=doctor_id,
                medical_consultation_id=medical_consultation_id,
                frequency=frequency
            )
            
            if self._appointment_dao.create_appointment(new_appointment):
                return new_appointment
            else:
                return None
                
        except Exception as e:
            print(f"Error en create_appointment: {e}")
            return None
        

    def reschedule_appointment(self, appointment_id: str, new_date: datetime):
            previous_appointment = self._appointment_dao.get_appointment_by_id(appointment_id)

            if not self._validate_appointment_data(new_date, previous_appointment.user_id, 
                        previous_appointment.doctor_id,
                        previous_appointment.medical_consultation_id):
                return None
                 
            if not self._appointment_dao.reschedule_appointment(appointment_id, new_date):
                print(f"Error al reprogramar turno.")
                return False
            
            return self.update_state(appointment_id, AppointmentStateEnum.RESCHEDULED)


    def delete_appointment(self, appointment_id: str) -> bool:
        appointment = self._appointment_dao.get_appointment_by_id(appointment_id)

        if (appointment.state != AppointmentStateEnum.CANCELLED):
            return False
            
        self._appointment_dao.delete_appointment(appointment_id)
        return True   
    

    def update_frequency(self, appointment_id: str, frequency: str):
       
        if not appointment_id:
            print("Error: ID de turno requerido.")
            return False
        
        if frequency and frequency not in ["unico","semanal", "mensual", "quincenal"]:
            print("Error: Frecuencia inválida. Use: unico, semanal, mensual o quincenal")
            return False
        
        success = self._appointment_dao.update_frequency(appointment_id, frequency)
        if success:
            print("Frecuencia actualizada exitosamente.")
        else:
            print("Error: No se pudo actualizar la frecuencia.")
        
        return success


    def update_state(self, appointment_id: str, appointment_state_enum: AppointmentStateEnum):
        
        if not appointment_id:
            print("Error: ID de turno requerido.")
            return False
        
        if not AppointmentStateEnum.has(appointment_state_enum.value):
            print("Error: Estado de turno inválido.")
            return False
        
        success = self._appointment_dao.update_state(appointment_id, appointment_state_enum)
        if success:
            print(f"Turno actualizado a: {appointment_state_enum.value}")
        else:
            print("Error: No se pudo actualizar el estado del turno.")
        
        return success


    def get_appointment_by_id(self, appointment_id: str) -> Appointment:
        appointment = self._appointment_dao.get_appointment_by_id(appointment_id, False)
        if appointment is None:
            print("No se encontró el turno buscado. \n")
            return None
        return appointment
    
    
    def get_all_appointments_by_user_id(self, user_id: str, close: bool = True) -> list['Appointment']:
        appointment_list = self._appointment_dao.get_all_appointments_by_user_id(user_id, close)
        if not appointment_list:
            print("No se encontraron turnos para este usuario. \n")
            return None
        return appointment_list
    
    
    def get_all_medical_consultations(self) -> list['Medical_consultation']:
        medical_consultation_list = self._appointment_dao.get_all_medical_consultations()
        if not medical_consultation_list:
            print("Error: No se encontraron prestaciones médicas. \n")
            return None
        return medical_consultation_list


    def _validate_appointment_data(self, date_and_time: datetime, user_id: str, 
                                  doctor_id: str, medical_consultation_id: str):
        
        if date_and_time < datetime.now():
            print("Error: No se puede agendar turno en fecha y hora pasada")
            return False
        
        if not user_id or not doctor_id or not medical_consultation_id:
            print("Error: Todos los campos son requeridos")
            return False
        
        if self._appointment_dao.check_time_conflict(user_id, doctor_id, date_and_time):
            print(f"""Error: Uno de los usuarios ya tiene un turno a las {date_and_time.strftime('%H:%M')}.
                  Recuerde que los turnos son de 1 hora.""")
            return False
        
        self._validate_date_with_doctor_availability(doctor_id, date_and_time)

        return True
    
        
    def _validate_date_with_doctor_availability(self, doctor_id: str, date_and_time: datetime):  
        availability_list = self._availability_dao.get_all_by_doctor_id(doctor_id)
        for availability in availability_list:
            if (date_and_time.weekday() == 0 and availability.days == DaysEnum.LUNES) or \
            (date_and_time.weekday() == 1 and availability.days == DaysEnum.MARTES) or \
            (date_and_time.weekday() == 2 and availability.days == DaysEnum.MIERCOLES) or \
            (date_and_time.weekday() == 3 and availability.days == DaysEnum.JUEVES) or \
            (date_and_time.weekday() == 4 and availability.days == DaysEnum.VIERNES) or \
            (date_and_time.weekday() == 5 and availability.days == DaysEnum.SABADO) or \
            (date_and_time.weekday() == 6 and availability.days == DaysEnum.DOMINGO):
                hour = date_and_time.hour
                timeframe = availability.time_frame
                if timeframe == TimeFrameEnum.MAÑANA and 6 <= hour < 12:
                    return True
                elif timeframe == TimeFrameEnum.TARDE and 12 <= hour < 18:
                    return True
                elif timeframe == TimeFrameEnum.NOCHE and 18 <= hour <= 23:
                    return True
        
        return False
    