from enum import Enum

class AppointmentStateEnum(Enum):

    SCHEDULED = "scheduled"
    RESCHEDULED = "rescheduled"      
    CONFIRMED = "confirmed"     
    CANCELLED = "cancelled"      
    COMPLETED = "completed"      
    
    
    @classmethod
    def values(self):
        return [_.value for _ in list(self)]

    @classmethod
    def has(self, value):
        return value in self.values()