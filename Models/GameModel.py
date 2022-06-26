class GameModel:
    def __init__(self, game_id, title, developer_id, publisher_id, release_date, rating=0):
        self.__game_id = game_id
        self.__title = title
        self.__developer_id = developer_id
        self.__publisher_id = publisher_id
        self.__release_date = release_date
        self.__rating = rating

    def get_game_id(self):
        return self.__game_id

    def set_game_id(self, game_id):
        self.__game_id = game_id

    def get_title(self):
        return self.__title

    def set_title(self, title):
        self.__title = title

    def set_release_date(self, release_date):
        self.__release_date = release_date

    def get_release_date(self):
        return self.__release_date

    def get_developer_id(self):
        return self.__developer_id

    def set_developer_id(self, developer_id):
        self.__developer_id = developer_id

    def get_publisher_id(self):
        return self.__publisher_id

    def set_publisher_id(self, publisher_id):
        self.__publisher_id = publisher_id

    def set_rating(self, rating):
        self.__rating = rating

    def get_rating(self):
        return self.__rating
