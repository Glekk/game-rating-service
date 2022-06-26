from Controllers import *
from Models import *
import Interface.data_check as data_check
from mysql.connector import MySQLConnection
import os


def comments_print(is_my, is_moder, result, conn):
    try:
        print("title" + " | " + "login" + " | " + "create_date" + " | ""edit_date")
        for i in result:
            print(i["title"]+" | "+i["login"]+" | "+i["create_date"].strftime("%Y-%m-%d %H:%M:%S")+" | "
                  + i["edit_date"].strftime("%Y-%m-%d %H:%M:%S"))
            print("Rating: "+str(i["rating"]))
            print("Text: "+i["text"])
            if is_moder or is_my:
                enabled = "Yes" if i["is_enabled"] else "No"
                print("Enabled: " + enabled)
            if is_my:
                moder = UserController.get_login_by_id(i["moderator_id"], conn)
                if moder:
                    print("Moderator: " + moder[0]["login"])
            print("_______________________")
    except TypeError as err:
        print(err)


def show_comments(user: UserModel, game: GameModel, conn: MySQLConnection):
    offset = 0
    count = 5
    while True:
        print("My comment\n")
        is_moder = 0
        comment = CommentsModel(0, game.get_game_id(), user.get_user_id(), "", 0, 0, 0, 0, 0)
        my_comm = CommentController.get_my_comment(comment, conn)
        if len(my_comm):
            comments_print(1, is_moder, my_comm, conn)
        else:
            print("You have no comment")

        print("Comments:\n")

        if "Moderator" in user.get_roles():
            all_comm = CommentController.get_all_comments(True, user.get_user_id(), game.get_game_id(), offset, count,
                                                          conn)
            is_moder = 1
        else:
            all_comm = CommentController.get_all_comments(False, user.get_user_id(), game.get_game_id(), offset, count,
                                                          conn)
        if all_comm:
            comments_print(0, is_moder, all_comm, conn)
        else:
            print("No comments found")

        print("Enter:")

        print("1 - previous page\n"
              "2 - next page")
        if "User" in user.get_roles() and not comment.get_create_date():
            print("3 - to write new comment")
        if comment.get_create_date():
            print("4 - to delete comment")
        if len(my_comm):
            print("5 - to update comment")
        if "Moderator" in user.get_roles():
            print("6 - to disable comment \n"
                  "7 - to enable comment ")
        print("8 - exit \n")

        in_str = input()
        os.system("cls")

        if in_str == "1":
            if offset > 0:
                offset -= count
            else:
                os.system("cls")
                print("You are on the first page\n")
        elif in_str == "2":
            if len(all_comm) == count:
                os.system("cls")
                offset += count
            else:
                os.system("cls")
                print("No more pages\n")
        elif in_str == "3" and "User" in user.get_roles() and not comment.get_create_date():
            os.system("cls")
            print("Enter comment text: ")
            text = input()
            if data_check.common_check(text):
                print("Enter comment rating (0 - 10): ")
                rating = input()
                if int(rating) in range(0, 11):
                    comment = CommentsModel(0, game.get_game_id(), user.get_user_id(), text, rating, 0, 0, 0, 0)
                    CommentController.insert_comment(comment, conn)
                    print("Comment added")
                else:
                    os.system("cls")
                    print("Error: wrong rating")

        elif in_str == "4" and comment.get_create_date():
            os.system("cls")
            print("Are you sure, that you want to delete comment? (y/n)")
            text = input()
            if text == "y":
                CommentController.delete_comment(comment, conn)
            else:
                os.system("cls")
                print("Comment not deleted")
        elif in_str == "5" and len(my_comm):
            os.system("cls")
            print("Enter comment text: ")
            text = input()
            if data_check.common_check(text):
                print("Enter comment rating (0 - 10): ")
                rating = input()
                if int(rating) in range(0, 11):
                    comment.set_text(text)
                    comment.set_rating(rating)
                    CommentController.update_comment(comment, conn)
                    print("Comment updated")
                else:
                    os.system("cls")
                    print("Error: wrong rating")
        elif in_str == "6" and "Moderator" in user.get_roles():
            os.system("cls")
            print("Enter user login: ")
            text = input()
            user_comm = UserController.get_user_by_login(text, conn)
            if data_check.common_check(user_comm):
                if data_check.common_check(CommentController.disable_comment(user_comm.get_user_id(),
                                                                             game.get_game_id(), user.get_user_id(),
                                                                             conn)):
                    print("Comment disabled")
        elif in_str == "7" and "Moderator" in user.get_roles():
            os.system("cls")
            print("Enter user login: ")
            text = input()
            user_comm = UserController.get_user_by_login(text, conn)
            if data_check.common_check(user_comm):
                if data_check.common_check(CommentController.enable_comment(user_comm.get_user_id(), game.get_game_id(),
                                                                            conn)):
                    print("Comment enabled")
        elif in_str == "8":
            os.system("cls")
            return
        else:
            os.system("cls")
            print("Error: wrong input")
