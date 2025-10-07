from Models.Availability import Availability
from DAO.Availability_DAO import AvailabilityDAO

class AvailabilityService:
    def __init__(self, dao: AvailabilityDAO):
        self.__dao = dao


    def add_availability(self, doctor_id, time_frame, days) -> Availability:
        new_availability = Availability(doctor_id= doctor_id,
                            time_frame= time_frame, days= days)
        self.__dao.add(new_availability)
        return new_availability


    def remove_availability(self, availability_id) -> bool:
        searched_availability = self.__dao.get_availability_by_id(availability_id)
        if not searched_availability:
            print("No se encontró el horario buscado. \n")
            return False
        else:
            self.__dao.delete(availability_id)
            return True

    def update_availability(self, availability_id, time_frame, days) -> Availability | None:
        searched_availability = self.__dao.get_availability_by_id(availability_id)
        if not searched_availability:
            print("No se encontró el horario buscado. \n")
            return None
        else:
            updated_availability = self.__dao.update(availability_id, time_frame, days)
            return updated_availability

    def get_all_by_doctor_id(self, doctor_id) -> list['Availability']:
        data = self.__dao.get_all_by_doctor_id(doctor_id)
        if not data:
            return None
        else:
            return data