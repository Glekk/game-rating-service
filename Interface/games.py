from Controllers import *
from Models import *
from mysql.connector import MySQLConnection
import Interface.data_check as data_check
import Interface.comments as comments
import os


def games_print(result, conn: MySQLConnection):
    try:
        print("title"+" | "+"developer"+" | "+"publisher"+" genres"+" | "+"release date"+" | "+"rating")
        for i in result:
            genres = GenreController.get_genres(i["title"], conn)
            str_genres = ""
            for a in genres:
                str_genres += a["title"] + " "
            print(i["title"] + " | " + i["developer"] + " | " + i["publisher"] + " | " + str_genres + " | " +
                  i["release_date"].strftime("%Y-%m-%d") + " | " + str(i["rating"]))
            print("___________________________________________________________________________________________________")
    except TypeError as err:
        print(err)


def find_game(user: UserModel, conn: MySQLConnection):
    offset = 0
    count = 5
    while True:
        print("Print game title:")
        title = input()
        if title:
            while True:
                result = GameController.find_games(title, offset, count, conn)
                if result:
                    games_print(result, conn)
                else:
                    print("No games found")
                print("Enter:")
                if user.get_is_enable():
                    print("1-5 - choose game")

                print("6 - enter again \n"
                      "7 - previous page \n"
                      "8 - next page \n"
                      "9 - exit \n")
                in_str = input()
                os.system("cls")

                if in_str in ["1", "2", "3", "4", "5"] and int(in_str) <= len(result):
                    game = GameController.get_game_by_title(result[int(in_str) - 1]["title"], conn)
                    comments.show_comments(user, game, conn)
                elif in_str == "6":
                    break
                elif in_str == "7":
                    if offset > 0:
                        offset -= count
                    else:
                        print("You are on the first page\n")
                elif in_str == "8":
                    if len(result) == count:
                        offset += count
                    else:
                        print("No more pages\n")
                elif in_str == "9":
                    return
                else:
                    os.system("cls")
                    print("Error: wrong input\n")
        else:
            print("Error: wrong input\n")


def show_games(user: UserModel, conn: MySQLConnection):
    offset = 0
    count = 5
    while True:
        print("Games")
        result = GameController.get_all_games(offset, count, conn)
        if result:
            games_print(result, conn)
        else:
            print("No games found")

        print("Enter:")

        print("1-5 - choose game")
        print("6 - previous page \n"
              "7 - next page \n"
              "8 - find games \n"                 
              "9 - exit")
        if "Admin" in user.get_roles():
            print("10 - insert game \n"
                  "11 - delete game \n")
        in_str = input()
        os.system("cls")

        if in_str in ["1", "2", "3", "4", "5"] and int(in_str) <= len(result):
            game = GameController.get_game_by_title(result[int(in_str) - 1]["title"], conn)
            comments.show_comments(user, game, conn)
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
            find_game(user, conn)
        elif in_str == "9":
            return

        elif in_str == "10" and "Admin" in user.get_roles():
            os.system("cls")
            enter_data_for_game(conn)

        elif in_str == "11" and "Admin" in user.get_roles():
            os.system("cls")
            print("Enter game title to delete:")
            title = input()
            if data_check.common_check(title):
                game = GameModel(0, title, "", "", "", "")
                if data_check.common_check(GameController.delete_game(game, conn)):
                    print("Game deleted\n")
        else:
            print("Error: wrong input")


def enter_data_for_game(conn: MySQLConnection):
    while True:
        print("Insert")
        print("Enter game title:")
        title = input()
        if data_check.common_check(title):
            print("Enter developer title:")
            dev_title = input()
            dev_id = DeveloperController.get_developer_id(dev_title, conn)
            if data_check.common_check(dev_id):
                print("Enter publisher title:")
                pub_title = input()
                pub_id = PublisherController.get_publisher_id(pub_title, conn)
                if data_check.common_check(pub_id):
                    print("Enter release date (yyyy-mm-dd):")
                    release_date = input()
                    if data_check.check_date(release_date):
                        game = GameModel(0, title, dev_id, pub_id, release_date)
                        if data_check.common_check(GameController.insert_game(game, conn)):
                            print("Game inserted\n")
                            return True
        print("Enter:")
        print("1 - enter again\n"
              "2 - exit")
        in_str = input()
        os.system("cls")
        if in_str == "1":
            continue
        elif in_str == "2":
            return False
