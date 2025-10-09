from datetime import datetime
from Models.Appointment_state_enum import AppointmentStateEnum
import uuid

class Appointment:
    def __init__(
        self,
        date_and_time: datetime,
        user_id: str,
        doctor_id: str,
        frequency: str,
        medical_consultation_id: str
    ):
        self.appointment_id = str(uuid.uuid4())
        self.date_and_time = date_and_time
        self.user_id = user_id
        self.doctor_id = doctor_id
        self.medical_consultation_id = medical_consultation_id
        self.frequency = frequency
        self.state = AppointmentStateEnum.SCHEDULED
        self.enabled = True

    def __str__(self):
        return f"Appointment(id={self.appointment_id}, date_and_time={self.date_and_time}, user_id={self.user_id}, doctor_id={self.doctor_id}, state={self.state}, enabled={self.enabled})"

    def __repr__(self):
        return f"Appointment(id={self.appointment_id}, date_and_time={self.date_and_time}, user_id={self.user_id}, doctor_id={self.doctor_id}, medical_consultation_id={self.medical_consultation_id}, frequency={self.frequency}, state={self.state}, enabled={self.enabled})"

    
    @property
    def appointment_id(self):
        return self.__appointment_id
    
    @appointment_id.setter
    def appointment_id(self, value):
        self.__appointment_id = value

    @property
    def date_and_time(self):
        return self.__date_and_time
    
    @date_and_time.setter
    def date_and_time(self, value):
        self.__date_and_time = value

    @property
    def user_id(self):
        return self.__user_id
    
    @user_id.setter
    def user_id(self, value):
        self.__user_id = value

    @property
    def doctor_id(self):
        return self.__doctor_id
    
    @doctor_id.setter
    def doctor_id(self, value):
        self.__doctor_id = value

    @property
    def medical_consultation_id(self):
        return self.__medical_consultation_id
    
    @medical_consultation_id.setter
    def medical_consultation_id(self, value):
        self.__medical_consultation_id = value

    @property
    def frequency(self):
        return self.__frequency
    
    @frequency.setter
    def frequency(self, value):
        self.__frequency = value

    @property
    def state(self):
        return self.__state
    
    @state.setter
    def state(self, value):
        self.__state = value

    @property
    def enabled(self):
        return self.__enabled
    
    @enabled.setter
    def enabled(self, value):
        self.__enabled = value

