from mysql.connector import MySQLConnection, Error


def give_role(login: str, role: str, conn: MySQLConnection):
    try:
        cur = conn.cursor()
        query = "SELECT role_id FROM role_list WHERE title = %s"
        cur.execute(query, (role,))
        role_id = cur.fetchall()[0][0]
        query = "SELECT user_id FROM user_list WHERE login = %s"
        cur.execute(query, (login,))
        user_id = cur.fetchall()[0][0]
        query = "INSERT INTO user_role (user_id, role_id) VALUES (%s, %s)"
        cur.execute(query, (user_id, role_id))
        conn.commit()
        cur.close()
        return True
    except Error as err:
        print("Something went wrong: {}".format(err))
        conn.rollback()
        return False


def delete_role(login: str, role: str, conn: MySQLConnection):
    try:
        cur = conn.cursor()
        query = "SELECT role_id FROM role_list WHERE title = %s"
        cur.execute(query, (role,))
        role_id = cur.fetchall()[0][0]
        query = "SELECT user_id FROM user_list WHERE login = %s"
        cur.execute(query, (login,))
        user_id = cur.fetchall()[0][0]
        query = "DELETE FROM user_role where user_id = %s and role_id = %s"
        cur.execute(query, (user_id, role_id))
        conn.commit()
        cur.close()
        return True
    except Error as err:
        print("Something went wrong: {}".format(err))
        conn.rollback()
        return False


def get_roles(login: str, conn: MySQLConnection):
    try:
        cur = conn.cursor(dictionary=True)
        query = """SELECT role_list.title FROM role_list
        join user_role using (role_id)
        join user_list using (user_id)
        where user_list.login = %s"""
        cur.execute(query, (login,))
        result = cur.fetchall()
        roles_arr = []
        for i in result:
            roles_arr.append(i["title"])
        return roles_arr
    except Error as err:
        print("Something went wrong: {}".format(err))
        return False
