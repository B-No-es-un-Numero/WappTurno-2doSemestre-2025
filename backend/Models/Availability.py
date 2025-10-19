import uuid
from Models.Days_enum import DaysEnum
from Models.TimeFrame_enum import TimeFrameEnum

class Availability:
    def __init__(
        self,
        doctor_id: str,
        time_frame: TimeFrameEnum,
        days: DaysEnum
    ):
        self.__id = str(uuid.uuid4())
        self.__doctor_id = doctor_id
        self.__time_frame = time_frame
        self.__days = days

    def __str__(self):
        return f"Availability(id={self.id}, doctor_id={self.doctor_id}, time_frame={self.time_frame}, days={self.days})"

    def __repr__(self):
        return f"Availability(id={self.id}, doctor_id={self.doctor_id}, time_frame={self.time_frame}, days={self.days})"

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value):
        self.__id = value

    @property
    def doctor_id(self):
        return self.__doctor_id

    @doctor_id.setter
    def doctor_id(self, value):
        self.__doctor_id = value

    @property
    def time_frame(self):
        return self.__time_frame

    @time_frame.setter
    def time_frame(self, value):
        self.__time_frame = value

    @property
    def days(self):
        return self.__days

    @days.setter
    def days(self, value):
        self.__days = value
