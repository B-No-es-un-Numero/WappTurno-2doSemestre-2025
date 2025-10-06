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


    def remove_availability(self, availability_id) -> True:
       pass

    def update_availability(self, availability_id, time_frame, days) -> Availability:
       pass

    def get_all_by_doctor_id(self, doctor_id) -> list['Availability']:
       pass