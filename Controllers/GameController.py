from mysql.connector import MySQLConnection, Error
from Models import *
from Interface import genres


def get_all_games(offset, count, conn: MySQLConnection):
    try:
        cur = conn.cursor(dictionary=True)
        query = "SELECT g.title, d.title as developer, p.title as publisher, g.release_date," \
                " g.rating FROM game_list as g"\
                " join developer_list as d using (developer_id)"\
                " join publisher_list as p using (publisher_id)"\
                " LIMIT %s, %s"
        cur.execute(query, (offset, count))
        result = cur.fetchall()
        cur.close()
        return result
    except Error as err:
        print("Something went wrong: {}".format(err))
        return False


def connect_game_genre(game: GameModel, update: bool, conn: MySQLConnection):
    try:
        cur = conn.cursor()
        query = "SELECT game_id FROM game_list WHERE title = %s"
        cur.execute(query, (game.get_title(),))
        game_id = cur.fetchall()[0][0]

        genres_arr = genres.choose_genres(True, conn)
        if not update and len(genres_arr) == 0:
            print("No genres selected")
            return False
        elif update and len(genres_arr) == 0:
            print("No genres selected")
            return True
        else:
            for i in genres_arr:
                query = "SELECT genre_id FROM genre_list WHERE title = %s"
                cur.execute(query, (i,))
                genre_id = cur.fetchall()[0][0]

                query = "INSERT INTO game_genre (`game_id`, `genre_id`) VALUES (%s, %s)"
                cur.execute(query, (game_id, genre_id))
            cur.close()
            return True
    except Error as err:
        print("Something went wrong: {}".format(err))
        return False


def insert_game(game: GameModel, conn: MySQLConnection):
    try:
        cur = conn.cursor()
        developer_id = game.get_developer_id()
        publisher_id = game.get_publisher_id()
        if not developer_id or not publisher_id:
            return False
        query = "INSERT INTO game_list (title, developer_id, publisher_id, release_date) VALUES (%s, %s, %s, %s)"
        cur.execute(query, (game.get_title(), developer_id, publisher_id, game.get_release_date()))
        if connect_game_genre(game, False, conn):
            conn.commit()
            cur.close()
            return game
        else:
            conn.commit()
            cur.close()
            return False
    except Error as err:
        print("Something went wrong: {}".format(err))
        conn.rollback()
        return False


def delete_game(game: GameModel, conn: MySQLConnection):
    try:
        cur = conn.cursor()
        query = "DELETE FROM game_list WHERE title = %s"
        cur.execute(query, (game.get_title(),))
        cur.close()
        conn.commit()
        return True
    except Error as err:
        print("Something went wrong: {}".format(err))
        return False


def find_games(title, offset, count, conn: MySQLConnection):
    try:
        cur = conn.cursor(dictionary=True)
        query = "SELECT g.title, d.title as developer, p.title as publisher, g.release_date," \
                " g.rating FROM game_list as g"\
                " join developer_list as d using (developer_id)"\
                " join publisher_list as p using (publisher_id)"\
                " where LOWER(g.title) LIKE LOWER(%s)"\
                " LIMIT %s, %s"
        cur.execute(query, ("%"+title+"%", offset, count))
        result = cur.fetchall()
        cur.close()
        return result
    except Error as err:
        print("Something went wrong: {}".format(err))
        return False


def get_game_by_title(title: str, conn: MySQLConnection):
    try:
        cur = conn.cursor(dictionary=True)
        query = "SELECT * FROM game_list WHERE title = %s"
        cur.execute(query, (title,))
        result = cur.fetchall()
        if result:
            game = GameModel(result[0]['game_id'], result[0]['title'], result[0]['developer_id'],
                             result[0]['publisher_id'], result[0]['release_date'], result[0]['rating'])
            game.set_game_id(result[0]['game_id'])
            cur.close()
            return game
        else:
            cur.close()
            return False
    except Error as err:
        print("Something went wrong: {}".format(err))
        return False


def update_rating(game_id: int, conn: MySQLConnection):
    try:
        cur = conn.cursor()
        query = "UPDATE game_list SET rating = (SELECT ROUND(AVG(comments.rating),2) FROM comments WHERE game_id = %s"\
                " and comments.is_enabled = 1) where game_id = %s"
        cur.execute(query, (game_id, game_id))
        conn.commit()
        cur.close()
        return True
    except Error as err:
        print("Something went wrong: {}".format(err))
        return False
