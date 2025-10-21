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
    def get_spanish_value(self, value):
        match value:
            case AppointmentStateEnum.SCHEDULED.value:
              return "programado"
            case AppointmentStateEnum.RESCHEDULED.value:
              return "reprogramado"
            case AppointmentStateEnum.CONFIRMED.value:
              return "confirmado"
            case AppointmentStateEnum.CANCELLED.value:
              return "cancelado"
            case AppointmentStateEnum.COMPLETED.value:
              return "finalizado"
    
    @classmethod
    def has(self, value):
        return value in self.values()