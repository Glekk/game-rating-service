from Controllers import *
from mysql.connector import MySQLConnection
from Interface import data_check
import os


def publishers_print(result):
    try:
        for i in result:
            print(i["title"])
            print("______________")
    except TypeError as err:
        print(err)


def show_publishers(conn: MySQLConnection):
    offset = 0
    count = 5
    while True:
        print("Publishers")
        result = PublisherController.get_all_publishers(offset, count, conn)
        if result:
            publishers_print(result)
        else:
            print("No publishers found")

        print("Enter:")

        print("1 - previous page \n"
              "2 - next page \n"   
              "3 - to insert new publisher \n"
              "4 - to delete publisher \n"
              "5 - to update publisher \n"
              "6 - exit \n")
        in_str = input()
        os.system("cls")

        if in_str == "1":
            if offset > 0:
                offset -= count
            else:
                print("You are on the first page\n")
        elif in_str == "2":
            if len(result) == count:
                offset += count
            else:
                print("No more pages\n")
        elif in_str == "3":
            os.system("cls")
            print("Enter publisher title to insert:")
            title = input()
            if data_check.common_check(title):
                if data_check.common_check(PublisherController.insert_publisher(title, conn)):
                    print("Publisher inserted\n")
        elif in_str == "4":
            os.system("cls")
            print("Enter publisher title to delete:")
            title = input()
            if data_check.common_check(title):
                if data_check.common_check(PublisherController.delete_publisher(title, conn)):
                    print("Publisher deleted\n")
        elif in_str == "5":
            os.system("cls")
            print("Enter publishers title to update:")
            title = input()
            if data_check.common_check(title):
                print("Enter new publisher title:")
                new_title = input()
                if data_check.common_check(new_title):
                    if data_check.common_check(PublisherController.update_publisher(new_title, title, conn)):
                        print("Publishers updated\n")
        elif in_str == "6":
            return
        else:
            os.system("cls")
            print("Error: wrong input")
