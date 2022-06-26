from Controllers import *
import Interface.data_check as data_check
from mysql.connector import MySQLConnection
import os


def users_print(result):
    try:
        for i in result:
            roles_arr = ""
            for k in i.get_roles():
                roles_arr += k + " "
            print(i.get_login() + " | " + i.get_email() + " | " + str(i.get_is_enable()) + " | " + roles_arr)
            print("______________________________________________________")
    except TypeError as err:
        print(err)


def show_users(conn: MySQLConnection):
    offset = 0
    count = 5
    while True:
        print("Users")
        result = UserController.get_all_users(offset, count, conn)
        if result:
            users_print(result)
        else:
            print("No users found")

        print("Enter:")

        print("1 - previous page \n"
              "2 - next page \n"   
              "3 - ban user \n" 
              "4 - unban user \n"
              "5 - add moder role to user \n"
              "6 - delete moder role from user \n"
              "7 - exit \n")
        in_str = input()
        os.system("cls")

        if in_str == "1":
            if offset > 0:
                os.system("cls")
                offset -= count
            else:
                os.system("cls")
                print("You are on the first page\n")
        elif in_str == "2":
            if len(result) == count:
                os.system("cls")
                offset += count
            else:
                os.system("cls")
                print("No more pages\n")
        elif in_str == "3":
            os.system("cls")
            print("Enter login:")
            login = input()
            if login:
                user_for_ban = UserController.get_user_by_login(login, conn)
                if not user_for_ban or user_for_ban.get_is_enable() == 0 or "Admin" in user_for_ban.get_roles():
                    print("No such user or you can't ban this user")
                else:
                    UserController.ban_user(user_for_ban, conn)
                    print("User banned")
            else:
                print("Error: wrong input\n")
        elif in_str == "4":
            os.system("cls")
            print("Enter login:")
            login = input()
            if login:
                user_for_ban = UserController.get_user_by_login(login, conn)
                if data_check.common_check(user_for_ban):
                    if user_for_ban.get_is_enable() == 1:
                        print("You can't unban this user")
                    else:
                        UserController.unban_user(user_for_ban, conn)
                        print("User unbanned")
            else:
                print("Error: wrong input\n")
        elif in_str == "5":
            os.system("cls")
            print("Enter login:")
            login = input()
            if login:
                user_for_ban = UserController.get_user_by_login(login, conn)
                if not user_for_ban or user_for_ban.get_is_enable() == 0 or "Admin" in user_for_ban.get_roles() \
                        or "Moder" in user_for_ban.get_roles():
                    print("No such user or you can't add role to this user")
                else:
                    if data_check.common_check(RolesController.give_role(user_for_ban.get_login(), "Moderator", conn)):
                        print("Role added")
            else:
                print("Error: wrong input")
        elif in_str == "6":
            os.system("cls")
            print("Enter login:")
            login = input()
            if login:
                user_for_ban = UserController.get_user_by_login(login, conn)
                if not user_for_ban or "Admin" in user_for_ban.get_roles():
                    print("No such user or you can't delete role from this user")
                else:
                    if data_check.common_check(RolesController.delete_role(user_for_ban.get_login(), "Moderator",
                                                                           conn)):
                        print("Role deleted")
            else:
                print("Error: wrong input")
        elif in_str == "7":
            return
        else:
            os.system("cls")
            print("Error: wrong input")
