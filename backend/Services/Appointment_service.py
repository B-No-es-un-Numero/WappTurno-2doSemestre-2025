from Models.Appointment import Appointment
from Models.Appointment_state_enum import AppointmentStateEnum
from DAO.Appointment_DAO import AppointmentDAO
from datetime import datetime

class AppointmentService:
    
    def __init__(self):
        self.appointment_dao = AppointmentDAO()

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
            
            
            if self.appointment_dao.create_appointment(new_appointment):
                return new_appointment
            else:
                return None
                
        except Exception as e:
            print(f"Error en create_appointment: {e}")
            return None
    
    def _validate_appointment_data(self, date_and_time: datetime, user_id: str, 
                                  doctor_id: str, medical_consultation_id: str):
        
        if date_and_time < datetime.now():
            print("Error: No se puede crear un appointment en el pasado")
            return False
        
        if not all([user_id, doctor_id, medical_consultation_id]):
            print("Error: Faltan campos obligatorios")
            return False
        
        return True

    def reschedule_appointment(self, appointment_id: str, new_date: datetime):
    
        try:
            if new_date < datetime.now():
                print("Error: No se puede reprogramar a una fecha pasada")
                return False
                 
            if not self.appointment_dao.reschedule_appointment(appointment_id, new_date):
                return False
            
            return self.update_state(appointment_id, AppointmentStateEnum.RESCHEDULED)
            
        except Exception as e:
            print(f"Error al reprogramar appointment: {e}")
            return False

    def delete_appointment(self, appointment_id: str):
        
        try:
            if not self.update_state(appointment_id, AppointmentStateEnum.CANCELLED):
             return False
            
            return self.appointment_dao.delete_appointment(appointment_id)    
        except Exception as e:
            print(f"Error al cancelar appointment: {e}")
            return False

    def update_frequency(self, appointment_id: str, frequency: str):
       
        if not appointment_id:
            print("Error: ID de appointment requerido.")
            return False
        
        if frequency and frequency not in ["semanal", "mensual", "quincenal"]:
            print("Error: Frecuencia inválida. Use: semanal, mensual, quincenal")
            return False
        
        success = self.appointment_dao.update_frequency(appointment_id, frequency)
        if success:
            print("Frecuencia actualizada exitosamente.")
        else:
            print("Error: No se pudo actualizar la frecuencia.")
        
        return success

    def update_state(self, appointment_id: str, appointment_state_enum: AppointmentStateEnum):
        
        if not appointment_id:
            print("Error: ID de appointment requerido.")
            return False
        
        if not AppointmentStateEnum.has(appointment_state_enum.value):
            print("Error: Estado inválido.")
            return False
        
        success = self.appointment_dao.update_state(appointment_id, appointment_state_enum)
        if success:
            print(f"Estado actualizado a: {appointment_state_enum.value}")
        else:
            print("Error: No se pudo actualizar el estado.")
        
        return success


    