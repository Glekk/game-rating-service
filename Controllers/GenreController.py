from mysql.connector import MySQLConnection, Error


def insert_genre(title: str, conn: MySQLConnection):
    try:
        cur = conn.cursor()

        query = "INSERT INTO genre_list (title) VALUES (%s)"
        cur.execute(query, (title,))
        conn.commit()
        cur.close()
        print("Insert completed")
        return True
    except Error as err:
        print("Something went wrong: {}".format(err))
        return False


def delete_genre(title: str, conn: MySQLConnection):
    try:
        cur = conn.cursor()

        query = "DELETE FROM genre_list WHERE title = %s"
        cur.execute(query, (title,))
        conn.commit()
        cur.close()
        return True
    except Error as err:
        print("Something went wrong: {}".format(err))
        return False


def update_genre(new_title: str, old_title: str, conn: MySQLConnection):
    try:
        cur = conn.cursor()

        query = "UPDATE genre_list SET title = %s WHERE title = %s"
        cur.execute(query, (new_title, old_title))
        conn.commit()
        cur.close()
        return True
    except Error as err:
        print("Something went wrong: {}".format(err))
        return False


def get_all_genres(offset: int, count: int, conn: MySQLConnection):
    try:
        cur = conn.cursor()
        query = "SELECT title FROM genre_list LIMIT  %s,  %s"
        cur.execute(query, (offset, count))
        result = cur.fetchall()
        cur.close()
        return result
    except Error as err:
        print("Something went wrong: {}".format(err))
        return False


def get_genres(game_title: str, conn: MySQLConnection):
    try:
        cur = conn.cursor(dictionary=True)
        query = "SELECT gl.title FROM game_list as g"\
                " join game_genre as gg using (game_id)"\
                " join genre_list as gl using (genre_id)"\
                " where LOWER(g.title) = LOWER(%s)"
        cur.execute(query, (game_title,))
        result = cur.fetchall()
        cur.close()
        return result
    except Error as err:
        print("Something went wrong: {}".format(err))
        return False
