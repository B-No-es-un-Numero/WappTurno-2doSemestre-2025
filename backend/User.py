from datetime import date
from Role_enum import RoleEnum
import uuid

class User:
    def __init__(
        self,
        name: str,
        surname: str,
        dni: int,
        email: str,
        password: str,
        phone_number: int,
        role: RoleEnum,
        date_of_birth: date
    ):
        self.user_id = str(uuid.uuid4())
        self.name = name
        self.surname = surname
        self.dni = dni
        self.email = email
        self.__password = password
        self.__phone_number = phone_number
        self.role = role
        self.date_of_birth = date_of_birth
        self.enabled = True

    def __str__(self):
        return f"User(id={self.user_id}, name={self.name}, surname={self.surname}, dni={self.dni}, email={self.email}, role={self.role}, date_of_birth={self.date_of_birth}, enabled={self.enabled})"

    def __repr__(self):
        return f"User(id={self.user_id}, name={self.name}, surname={self.surname}, dni={self.dni}, email={self.email}, role={self.role}, date_of_birth={self.date_of_birth}, enabled={self.enabled})"

    @property
    def user_id(self):
        return self.__user_id
    
    @user_id.setter
    def user_id(self, value):
        self.__user_id = value

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value

    @property
    def surname(self):
        return self.__surname

    @surname.setter
    def surname(self, value):
        self.__surname = value

    @property
    def dni(self):
        return self.__dni

    @dni.setter
    def dni(self, value):
        self.__dni = value

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, value):
        self.__email = value

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, value):
        self.__password = value

    @property
    def phone_number(self):
        return self.__phone_number

    @phone_number.setter
    def phone_number(self, value):
        self.__phone_number = value

    @property
    def role(self):
        return self.__role

    @role.setter
    def role(self, value):
        self.__role = value

    @property
    def date_of_birth(self):
        return self.__date_of_birth
    
    @date_of_birth.setter
    def date_of_birth(self, value):
        self.__date_of_birth = value

    @property
    def enabled(self):
        return self.__enabled

    @enabled.setter
    def enabled(self, value):
        self.__enabled = value