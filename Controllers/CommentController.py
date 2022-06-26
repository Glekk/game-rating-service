from mysql.connector import MySQLConnection, Error
from Models import *
from Controllers import GameController


def insert_comment(comment: CommentsModel, conn: MySQLConnection):
    try:
        cur = conn.cursor()

        query = "INSERT INTO comments (game_id, user_id, text, rating, create_date, edit_date, moderator_id," \
                " is_enabled) VALUES (%s, %s, %s, %s, sysdate(), sysdate(), NULL, 1)"
        cur.execute(query, (comment.get_game_id(), comment.get_user_id(), comment.get_text(), comment.get_rating()))
        conn.commit()
        cur.close()
        GameController.update_rating(comment.get_game_id(), conn)
        return comment
    except Error as err:
        print("Something went wrong: {}".format(err))
        return False


def update_comment(comment: CommentsModel, conn: MySQLConnection):
    try:
        cur = conn.cursor()

        query = "UPDATE comments SET text = %s, rating = %s, edit_date = sysdate(), moderator_id = NULL, " \
                " is_enabled = 1 WHERE comment_id = %s"
        cur.execute(query, (comment.get_text(), comment.get_rating(), comment.get_comment_id()))
        conn.commit()
        cur.close()
        GameController.update_rating(comment.get_game_id(), conn)
        return comment
    except Error as err:
        print("Something went wrong: {}".format(err))
        return False


def delete_comment(comment: CommentsModel, conn: MySQLConnection):
    try:
        cur = conn.cursor()

        query = "DELETE FROM comments WHERE comment_id = %s"
        cur.execute(query, (comment.get_comment_id(),))
        conn.commit()
        comment.set_comment_id(0)
        comment.set_text("")
        comment.set_rating(0)
        comment.set_create_date("")
        comment.set_edit_date("")
        comment.set_moderator_id(0)
        comment.set_is_enabled(0)
        cur.close()
        GameController.update_rating(comment.get_game_id(), conn)
        return comment
    except Error as err:
        print("Something went wrong: {}".format(err))
        return False


def disable_comment(user_id, game_id, moderator_id, conn: MySQLConnection):
    try:
        cur = conn.cursor()

        query = "UPDATE comments SET moderator_id = %s, is_enabled = %s WHERE user_id = %s and game_id = %s"
        cur.execute(query, (moderator_id, "0", user_id, game_id))
        conn.commit()
        cur.close()
        GameController.update_rating(game_id, conn)
        return True
    except Error as err:
        print("Something went wrong: {}".format(err))
        return False


def enable_comment(user_id, game_id, conn: MySQLConnection):
    try:
        cur = conn.cursor()

        query = "UPDATE comments SET moderator_id = NULL, is_enabled = %s WHERE user_id = %s and game_id = %s"
        cur.execute(query, ("1", user_id, game_id))
        conn.commit()
        cur.close()
        GameController.update_rating(game_id, conn)
        return True
    except Error as err:
        print("Something went wrong: {}".format(err))
        return False


def get_all_comments(is_all: bool, user_id: int, game_id: int, offset: int, count: int, conn: MySQLConnection):
    try:
        cur = conn.cursor(dictionary=True)
        if is_all:
            query = "SELECT g.title, u.login, c.text, c.rating, c.create_date, c.edit_date, c.is_enabled" \
                " FROM comments as c" \
                " join user_list as u using (user_id)"\
                " join game_list as g using (game_id)"\
                " WHERE u.user_id != %s and g.game_id = %s"\
                " LIMIT %s, %s"
        else:
            query = "SELECT g.title, u.login, c.text, c.rating, c.create_date, c.edit_date, c.is_enabled" \
                    " FROM comments as c" \
                    " join user_list as u using (user_id)"\
                    " join game_list as g using (game_id)"\
                    " WHERE c.is_enabled = 1 and u.user_id != %s and g.game_id = %s"\
                    " LIMIT %s, %s"
        cur.execute(query, (user_id, game_id, offset, count))
        result = cur.fetchall()
        cur.close()
        return result
    except Error as err:
        print("Something went wrong: {}".format(err))
        return False


def get_my_comment(comment: CommentsModel, conn: MySQLConnection):
    try:
        cur = conn.cursor(dictionary=True)

        query = "SELECT c.comment_id, g.title, u.login, c.text, c.rating, c.create_date, c.edit_date, c.moderator_id," \
                " c.is_enabled FROM comments as c" \
                " join user_list as u using (user_id)"\
                " join game_list as g using (game_id)" \
                " WHERE u.user_id = %s and g.game_id = %s"
        cur.execute(query, (comment.get_user_id(), comment.get_game_id()))
        result = cur.fetchall()
        cur.close()
        if result:
            comment.set_comment_id(result[0]['comment_id'])
            comment.set_text(result[0]['text'])
            comment.set_rating(result[0]['rating'])
            comment.set_create_date(result[0]['create_date'])
            comment.set_edit_date(result[0]['edit_date'])
            comment.set_moderator_id(result[0]['moderator_id'])
            comment.set_is_enabled(result[0]['is_enabled'])
        return result
    except Error as err:
        print("Something went wrong: {}".format(err))
        return False
