from Services.User_service import UserService
from Services.Availability_service import AvailabilityService
from Services.Appointment_service import AppointmentService
from DAO.User_DAO import UserDAO
from DAO.Availability_DAO import AvailabilityDAO
from DAO.Appointment_DAO import AppointmentDAO
from Presentation.Menu2 import Menu2

def main():
    menu = Menu2(UserService(UserDAO()),
                AvailabilityService(AvailabilityDAO()),
                AppointmentService(AppointmentDAO(), AvailabilityDAO()))
    menu.run_menu()

if __name__ == "__main__":
    main()
