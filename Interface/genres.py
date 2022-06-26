from Controllers import GenreController
from mysql.connector import MySQLConnection
from Interface import data_check
import os


def choose_genres(for_game_connect: bool, conn: MySQLConnection):
    cur = conn.cursor()
    offset = 0
    count = 5
    genres_arr = []
    while True:
        print(" ")
        result = GenreController.get_all_genres(offset, count, conn)

        for x in result:
            print(x[0])
            print("____________________")
        print(" ")
        print("Enter:")
        if for_game_connect:
            print("1-5 - check (repeat to uncheck))")

        print("6 - previous page\n"
              "7 - next page\n"
              "8 - to insert new genre\n"
              "9 - to delete genre\n"
              "10 - to update genre\n"
              "11 - to exit")
        if for_game_connect:
            print("Your choices{}".format(genres_arr))

        in_str = input()

        os.system("cls")
        if for_game_connect and in_str in ["1", "2", "3", "4", "5"] and int(in_str) <= len(result):
            if result[int(in_str) - 1][0] not in genres_arr:
                genres_arr.append(result[int(in_str) - 1][0])
                print("Genre added\n")
            else:
                genres_arr.remove(result[int(in_str) - 1][0])
                print("Genre deleted\n")
        elif in_str == "6":
            if offset > 0:
                os.system("cls")
                offset -= count
            else:
                os.system("cls")
                print("You are on the first page\n")
        elif in_str == "7":
            if len(result) == count:
                os.system("cls")
                offset += count
            else:
                os.system("cls")
                print("No more pages\n")
        elif in_str == "8":
            os.system("cls")
            print("Enter genre title to insert:")
            title = input()

            if data_check.common_check(title):
                if data_check.common_check(GenreController.insert_genre(title, conn)):
                    print("Genre inserted")

        elif in_str == "9":
            print("Enter genre title to delete:")
            title = input()
            if data_check.common_check(title):
                if data_check.common_check(GenreController.delete_genre(title, conn)):
                    print("Genre deleted\n")
        elif in_str == "10":
            print("Enter genre title to update:")
            title = input()
            if data_check.common_check(title):
                print("Enter new genre title:")
                new_title = input()
                if data_check.common_check(new_title):
                    if data_check.common_check(GenreController.update_genre(new_title, title, conn)):
                        print("Genre updated\n")
        elif in_str == "11":
            print("Exit")
            break
        else:
            os.system("cls")
            print("Error: wrong input\n")
    cur.close()
    return genres_arr
