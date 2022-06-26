
class UserModel:
    def __init__(self, user_id, login, password, email, roles, is_enable=1):
        self.__user_id = user_id
        self.__login = login
        self.__password = password
        self.__email = email
        self.__roles = roles
        self.__is_enable = is_enable

    def get_user_id(self):
        return self.__user_id

    def set_user_id(self, user_id):
        self.__user_id = user_id

    def get_login(self):
        return self.__login

    def set_login(self, login):
        self.__login = login

    def get_password(self):
        return self.__password

    def set_password(self, password):
        self.__password = password

    def get_email(self):
        return self.__email

    def set_email(self, email):
        self.__email = email

    def get_is_enable(self):
        return self.__is_enable

    def set_is_enable(self, is_enable):
        self.__is_enable = is_enable

    def get_roles(self):
        return self.__roles

    def set_roles(self, roles):
        self.__roles = roles

    # def show(self):
    #     print("Login: {}".format(self.get_login()))
    #     print("Password: {}".format(self.get_password()))
    #     print("Email: {}".format(self.get_email()))
    #     print("Roles: {}".format(self.get_roles()))
    #     print("Is enable: {}".format(self.get_is_enable()))