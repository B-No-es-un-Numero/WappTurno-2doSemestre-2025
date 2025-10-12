import mysql.connector
import os
from dotenv import load_dotenv

class connection_mysql:

    def __init__(self):
        load_dotenv()
        self.__db_user = os.getenv('DB_USER')
        self.__db_password = os.getenv('DB_PASSWORD')
        self.__db_host = os.getenv('DB_HOST')
        self.__db_name = os.getenv('DB_NAME')
        self.__db_port = os.getenv('DB_PORT')

    def create_connection(self):
        return mysql.connector.connect(user=self.__db_user, 
                              password=self.__db_password,
                              host=self.__db_host,
                              database=self.__db_name,
                              port=self.__db_port)
    

    