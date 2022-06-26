from Controllers import *
from Models import *
from mysql.connector import MySQLConnection
import Interface.data_check as data_check
import Interface.games as games
import Interface.users as users
import Interface.genres as genres
import Interface.developers as developers
import Interface.publishers as publishers

import os


def main_menu_logged(user: UserModel, conn: MySQLConnection):
    while True:
        print("Main menu, enter:\n"
              "1 - show games\n"
              "2 - log out\n"
              "3 - change password")
        if "Admin" in user.get_roles():
            print("4 - work with users\n"
                  "5 - work with developers\n"
                  "6 - work with publishers\n"
                  "7 - work with genres")

        in_str = input()
        if in_str == "1":
            os.system("cls")
            games.show_games(user, conn)

        elif in_str == "2":
            os.system("cls")
            UserController.log_out(user)
            return

        elif in_str == "3":
            os.system("cls")
            old_password = input("Enter old password: ")
            if UserController.hash_password(user.get_login(), old_password) == user.get_password():
                new_password = input("Enter new password: ")
                if data_check.check_password(new_password):
                    if UserController.change_password(user, new_password, conn):
                        print("Password changed")
            else:
                print("Error: old password entered incorrectly")

        elif in_str == "4" and "Admin" in user.get_roles():
            os.system("cls")
            users.show_users(conn)

        elif in_str == "5" and "Admin" in user.get_roles():
            os.system("cls")
            developers.show_developers(conn)

        elif in_str == "6" and "Admin" in user.get_roles():
            os.system("cls")
            publishers.show_publishers(conn)

        elif in_str == "7" and "Admin" in user.get_roles():
            os.system("cls")
            genres.choose_genres(False, conn)
        else:
            os.system("cls")
            print("Error: wrong input")


def main_menu_guest(conn: MySQLConnection):
    while True:
        user = UserModel(0, "", "", "", [""], 0)
        print("Main menu, enter:\n"
              "1 - log in\n"
              "2 - register\n"
              "3 - show games\n"
              "4 - exit\n"
              )
        in_str = input()
        if in_str == "1":
            os.system("cls")
            user = log_in(conn)
            if user:
                main_menu_logged(user, conn)
        elif in_str == "2":
            os.system("cls")
            user = registration(conn)
            if user:
                main_menu_logged(user, conn)
        elif in_str == "3":
            os.system("cls")
            games.show_games(user, conn)
        elif in_str == "4":
            return
        else:
            os.system("cls")
            print("Error: wrong input")


def registration(conn: MySQLConnection):
    while True:
        print("Registration, enter: \n"
              "1 - enter data \n"
              "2 - exit \n")
        in_str = input()
        if in_str == "1":
            password = email = ""
            os.system("cls")
            correct = True
            print("Enter login: ")
            login = input()
            if not data_check.check_login(login):
                correct = False

            if correct:
                print("Enter password: ")
                password = input()
                if not data_check.check_password(password):
                    correct = False

            if correct:
                print("Enter email: ")
                email = input()
                if not data_check.check_email(email):
                    correct = False
            if correct:
                user = UserModel(0, login, password, email, ["User"])
                if UserController.insert_user(user, conn):
                    user = UserController.get_user_by_login(user.get_login(), conn)
                    os.system("cls")
                    print("Registration completed\n")
                    return user
        elif in_str == "2":
            return False
        else:
            os.system("cls")
            print("Error: wrong input")


def log_in(conn: MySQLConnection):
    while True:
        in_str = input("Logging in, enter\n"
                       "1 - enter login and password \n"
                       "2 - exit: \n")

        print()
        os.system("cls")
        if in_str == "1":
            login = input("Enter login: ")
            password = input("Enter password: ")
            print()
            user = UserModel(0, login, password, "", ["User"])
            if UserController.log_in_db(user, conn):
                if user.get_is_enable():
                    return user
                else:
                    print("You are banned")
            else:
                os.system("cls")
                print("Error: data entered incorrectly")
        elif in_str == "2":
            return False
        else:
            os.system("cls")
            print("Error: wrong input")
