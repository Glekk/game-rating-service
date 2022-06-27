import mysql.connector
from Interface import *

if __name__ == '__main__':
    connection = mysql.connector.connect(
        host="localhost",
        user="someuser",
        password="password",
        database="game service"
    )
    interface.main_menu_guest(connection)

    connection.close()
