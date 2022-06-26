from mysql.connector import MySQLConnection, Error


def insert_developer(title, conn: MySQLConnection):
    try:
        cur = conn.cursor()

        query = "INSERT INTO developer_list (title) VALUES (%s)"
        cur.execute(query, (title,))
        conn.commit()
        cur.close()
        return True
    except Error as err:
        print("Something went wrong: {}".format(err))
        return False


def delete_developer(title, conn: MySQLConnection):
    try:
        cur = conn.cursor()

        query = "DELETE FROM developer_list WHERE title = %s"
        cur.execute(query, (title,))
        conn.commit()
        cur.close()
        return True
    except Error as err:
        print("Something went wrong: {}".format(err))


def update_developer(new_title, old_title, conn: MySQLConnection):
    try:
        cur = conn.cursor()

        query = "UPDATE developer_list SET title = %s WHERE title = %s"
        cur.execute(query, (new_title, old_title))
        conn.commit()
        cur.close()
        return True
    except Error as err:
        print("Something went wrong: {}".format(err))


def get_all_developers(offset: int, count: int, conn: MySQLConnection):
    try:
        cur = conn.cursor(dictionary=True)

        query = "SELECT title FROM developer_list LIMIT %s, %s"
        cur.execute(query, (offset, count))
        result = cur.fetchall()
        cur.close()
        return result
    except Error as err:
        print("Something went wrong: {}".format(err))
        return False


def get_developer_id(title, conn: MySQLConnection):
    try:
        cur = conn.cursor()

        query = "SELECT developer_id FROM developer_list WHERE title = %s"
        cur.execute(query, (title,))
        result = cur.fetchall()
        if result:
            cur.close()
            return result[0][0]
        else:
            cur.close()
            return False
    except Error as err:
        print("Something went wrong: {}".format(err))
        return False
