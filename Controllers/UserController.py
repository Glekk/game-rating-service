import hashlib
from Models import *
import Controllers.RolesController as RolesController
from mysql.connector import MySQLConnection, Error


def hash_password(salt: str, password: str):
    return hashlib.sha256((salt + password).encode()).hexdigest()


def insert_user(user: UserModel, conn: MySQLConnection):
    try:
        cur = conn.cursor()
        query = "INSERT INTO user_list (login, `password`, email) VALUES (%s, %s, %s)"
        cur.execute(query, (user.get_login(), hash_password(user.get_login(), user.get_password()),
                            user.get_email()))
        query = "SELECT user_id FROM user_list WHERE login = %s"
        cur.execute(query, (user.get_login(),))
        user_id = cur.fetchall()[0][0]
        query = "SELECT role_id FROM role_list WHERE title = %s"
        cur.execute(query, ("User",))
        role_id = cur.fetchall()[0][0]
        query = "INSERT INTO user_role (user_id, role_id) VALUES (%s, %s)"
        cur.execute(query, (user_id, role_id))
        conn.commit()
        cur.close()
        return user
    except Error as err:
        print("Something went wrong: {}".format(err))
        conn.rollback()
        return False


def ban_user(user: UserModel, conn: MySQLConnection):
    try:
        cur = conn.cursor()
        query = "UPDATE user_list SET is_enable = 0 WHERE login = %s"
        cur.execute(query, (user.get_login(),))
        conn.commit()
        cur.close()
        return
    except Error as err:
        print("Something went wrong: {}".format(err))
        conn.rollback()
        return


def unban_user(user: UserModel, conn: MySQLConnection):
    try:
        cur = conn.cursor()
        query = "UPDATE user_list SET is_enable = 1 WHERE login = %s"
        cur.execute(query, (user.get_login(),))
        conn.commit()
        cur.close()
        return
    except Error as err:
        print("Something went wrong: {}".format(err))
        conn.rollback()
        return


def change_password(user: UserModel, new_password: str, conn: MySQLConnection):
    try:
        cur = conn.cursor()
        query = "UPDATE user_list SET password = %s WHERE login = %s"
        cur.execute(query, (hash_password(user.get_login(), new_password), user.get_login()))
        user.set_password(new_password)
        conn.commit()
        cur.close()
        return True
    except Error as err:
        print("Something went wrong: {}".format(err))
        conn.rollback()
        return False


def log_in_db(user: UserModel, conn: MySQLConnection):
    try:
        cur = conn.cursor(dictionary=True)
        query = "SELECT * FROM user_list WHERE login = %s and password = %s"
        cur.execute(query, (user.get_login(), hash_password(user.get_login(), user.get_password())))
        result = cur.fetchall()
        if not result:
            cur.close()
            return False
        roles = RolesController.get_roles(user.get_login(), conn)
        cur.close()
        user.set_user_id(result[0]["user_id"])
        user.set_email(result[0]["email"])
        user.set_password(result[0]["password"])
        user.set_is_enable(result[0]["is_enable"])
        user.set_roles(roles)
        return user
    except Error as err:
        print("Something went wrong: {}".format(err))
        return False


def log_out(user: UserModel):
    user.set_login("")
    user.set_password("")
    user.set_email("")
    user.set_roles([""])
    user.set_is_enable(0)
    return user


def get_all_users(offset, count, conn: MySQLConnection):
    try:
        cur = conn.cursor(dictionary=True)
        query = "SELECT u.login, u.email, u.is_enable FROM user_list as u LIMIT %s, %s"
        cur.execute(query, (offset, count))
        result = cur.fetchall()
        user_arr = []
        for i in result:
            roles = RolesController.get_roles(i["login"], conn)
            user = UserModel(0, i["login"], "", i["email"], roles, i["is_enable"])
            user_arr.append(user)
        cur.close()
        return user_arr
    except Error as err:
        print("Something went wrong: {}".format(err))
        return False


def get_user_by_login(login, conn: MySQLConnection):
    try:
        cur = conn.cursor(dictionary=True)
        query = "SELECT * FROM user_list WHERE login = %s"
        cur.execute(query, (login,))
        result = cur.fetchall()
        if not result:
            cur.close()
            return False
        else:
            roles = RolesController.get_roles(login, conn)
            cur.close()
            user = UserModel(result[0]["user_id"], result[0]["login"], result[0]["password"], result[0]["email"], roles,
                             result[0]["is_enable"])
            return user
    except Error as err:
        print("Something went wrong: {}".format(err))
        return False


def get_login_by_id(user_id, conn: MySQLConnection):
    try:
        cur = conn.cursor(dictionary=True)
        query = "SELECT login FROM user_list WHERE user_id = %s"
        cur.execute(query, (user_id,))
        result = cur.fetchall()
        if not result:
            cur.close()
            return False
        else:
            return result
    except Error as err:
        print("Something went wrong: {}".format(err))
        return False
