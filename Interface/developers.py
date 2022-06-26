from Controllers import *
from mysql.connector import MySQLConnection
from Interface import data_check
import os


def developers_print(result):
    try:
        for i in result:
            print(i["title"])
            print("______________")
    except TypeError as err:
        print(err)


def show_developers(conn: MySQLConnection):
    offset = 0
    count = 5
    while True:
        print("Developers")
        result = DeveloperController.get_all_developers(offset, count, conn)
        if result:
            developers_print(result)
        else:
            print("No developers found")

        print("Enter:")

        print("1 - previous page \n"
              "2 - next page \n"   
              "3 - to insert new developer \n"
              "4 - to delete developer \n"
              "5 - to update developer \n"
              "6 - exit \n")

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
            print("Enter developer title to insert:")
            title = input()
            if data_check.common_check(title):
                if data_check.common_check(DeveloperController.insert_developer(title, conn)):
                    print("Developer inserted\n")
        elif in_str == "4":
            os.system("cls")
            print("Enter developer title to delete:")
            title = input()
            if data_check.common_check(title):
                if data_check.common_check(DeveloperController.delete_developer(title, conn)):
                    print("Developer deleted\n")
        elif in_str == "5":
            os.system("cls")
            print("Enter developer title to update:")
            title = input()
            if data_check.common_check(title):
                print("Enter new developer title:")
                new_title = input()
                if data_check.common_check(new_title):
                    if data_check.common_check(DeveloperController.update_developer(new_title, title, conn)):
                        print("Developer updated\n")
        elif in_str == "6":
            return
        else:
            os.system("cls")
            print("Error: wrong input")
