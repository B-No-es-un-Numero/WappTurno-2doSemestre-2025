from User_service import UserService
from User_DAO import UserDAO
from Menu import Menu

def main():
    menu = Menu(UserService(UserDAO()))
    menu.run_menu()

if __name__ == "__main__":
    main()