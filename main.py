import mysql.connector
from Interface import *
from Controllers import *

if __name__ == '__main__':
    connection = mysql.connector.connect(
        host="localhost",
        user="someuser",
        password="p4ssword",
        database="game_service"
    )
    interface.main_menu_guest(connection)

    connection.close()
