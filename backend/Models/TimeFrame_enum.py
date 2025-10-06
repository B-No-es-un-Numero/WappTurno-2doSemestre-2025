from enum import StrEnum

class TimeFrameEnum(StrEnum):
    MAÑANA = "MAÑANA"
    TARDE = "TARDE"
    NOCHE = "NOCHE"

    @classmethod
    def values(self):
        return [_.value for _ in list(self)]

    @classmethod
    def has(self, value):
        return value in self.values()