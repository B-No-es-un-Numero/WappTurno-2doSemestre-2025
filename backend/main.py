from Services.User_service import UserService
from DAO.User_DAO import UserDAO
from Presentation.Menu import Menu

def main():
    menu = Menu(UserService(UserDAO()))
    menu.run_menu()

if __name__ == "__main__":
    main()