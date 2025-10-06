from Services.User_service import UserService
from Services.Availability_service import AvailabilityService
from DAO.User_DAO import UserDAO
from DAO.Availability_DAO import AvailabilityDAO
from Presentation.Menu import Menu

def main():
    menu = Menu(UserService(UserDAO()),
                AvailabilityService(AvailabilityDAO()))
    menu.run_menu()

if __name__ == "__main__":
    main()