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
        accepts_medical_ensurance: bool,
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
        self.specialty = specialty
        self.accepts_medical_ensurance = accepts_medical_ensurance
        self.license_number = license_number

    def __str__(self):
        return (f"Doctor {self.name} {self.surname} - "
                f"Especialidad: {self.specialty}, "
                f"Matrícula: {self.license_number}")

    def __repr__(self):
        return (f"Doctor(name={self.name!r}, surname={self.surname!r}, "
                f"dni={self.dni!r}, email={self.email!r}, "
                f"specialty={self.specialty!r}, "
                f"accepts_medical_ensurance={self.accepts_medical_ensurance!r}, "
                f"license_number={self.license_number!r})")

    def get_specialty(self):
        return self.specialty

    def set_specialty(self, specialty: str):
        self.specialty = specialty

    def get_accepts_medical_ensurance(self):
        return self.accepts_medical_ensurance

    def set_accepts_medical_ensurance(self, accepts_medical_ensurance: bool):
        self.accepts_medical_ensurance = accepts_medical_ensurance

    def get_license_number(self):
        return self.license_number

    def set_license_number(self, license_number: int):
        self.license_number = license_number