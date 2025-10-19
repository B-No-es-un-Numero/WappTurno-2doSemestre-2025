from datetime import date
from Models.User import User
from Models.Role_enum import RoleEnum

class Doctor(User):
    def __init__(
        self,
        name: str,
        surname: str,
        dni: int,
        email: str,
        password: str,
        phone_number: int,
        date_of_birth: date,
        specialty: str,
        accepts_medical_insurance: bool,
        license_number: int
    ):
        super().__init__(
            name=name,
            surname=surname,
            dni=dni,
            email=email,
            password=password,
            phone_number=phone_number,
            role=RoleEnum.DOCTOR,
            date_of_birth=date_of_birth
        )
        self.__specialty = specialty
        self.__accepts_medical_insurance = accepts_medical_insurance
        self.__license_number = license_number

    def __str__(self):
        return (f"Doctor {self.name} {self.surname} - "
                f"Especialidad: {self.specialty}, "
                f"Matrícula: {self.license_number}")

    def __repr__(self):
        return (f"Doctor(name={self.name!r}, surname={self.surname!r}, "
                f"dni={self.dni!r}, email={self.email!r}, "
                f"specialty={self.specialty!r}, "
                f"accepts_medical_insurance={self.accepts_medical_insurance!r}, "
                f"license_number={self.license_number!r})")

    @property
    def specialty(self):
        return self.__specialty

    @specialty.setter
    def specialty(self, value: str):
        self.__specialty = value
        
    @property
    def accepts_medical_insurance(self):
        return self.__accepts_medical_insurance

    @accepts_medical_insurance.setter
    def accepts_medical_insurance(self, value: bool):
        self.__accepts_medical_insurance = value

    @property
    def license_number(self):
        return self.__license_number

    @license_number.setter
    def license_number(self, value: int):
        self.__license_number = value
