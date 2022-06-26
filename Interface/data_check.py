import re
import os

# def check_user_data(user: UserModel):
#     if " " not in user.get_login() and " " not in user.get_password() and (
#             re.search(r"^[a-z0-9]+[._]?[a-z0-9]+[@]\w+[.]\w{2,3}$", user.get_email())) and user.get_login() and\
#             user.get_password():
#
#         return True
#     else:
#         print("Error: data entered incorrectly")
#         return False


def check_login(login):
    if " " not in login and login:
        return True
    os.system("cls")
    print("Error: login entered incorrectly\n")
    return False


def check_password(password):
    if " " not in password and password:
        return True
    os.system("cls")
    print("Error: password entered incorrectly\n")
    return False


def check_email(email):
    if re.search(r"^[\w.-]+@[\w.-]+[.]+\w+$", email):
        return True
    os.system("cls")
    print("Error: email entered incorrectly\n")
    return False


def check_date(date):
    if re.search(r"^(20|19)[0-9]{2}-((0[1-9])|(1[0-2]))-([1-2][0-9]|[0-2][1-9]|3[0-1])$", date):
        return True
    os.system("cls")
    print("Error: wrong date\n")
    return False


def common_check(data):
    if data:
        return True
    os.system("cls")
    print("Error: wrong input\n")
    return False
