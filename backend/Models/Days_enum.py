from enum import StrEnum

class DaysEnum(StrEnum):
    LUNES = "LUNES"
    MARTES = "MARTES"
    MIERCOLES = "MIERCOLES"
    JUEVES = "JUEVES"
    VIERNES = "VIERNES"
    SABADO = "SABADO"
    DOMINGO = "DOMINGO"

    @classmethod
    def values(self):
        return [_.value for _ in list(self)]

    @classmethod
    def has(self, value):
        return value in self.values()