class CommentsModel:
    def __init__(self, comment_id, game_id, user_id, text, rating, create_date, edit_date, moderator_id, is_enabled):
        self.__comment_id = comment_id
        self.__game_id = game_id
        self.__user_id = user_id
        self.__text = text
        self.__rating = rating
        self.__create_date = create_date
        self.__edit_date = edit_date
        self.__moderator_id = moderator_id
        self.__is_enabled = is_enabled

    def get_comment_id(self):
        return self.__comment_id

    def set_comment_id(self, comment_id):
        self.__comment_id = comment_id

    def get_game_id(self):
        return self.__game_id

    def get_user_id(self):
        return self.__user_id

    def get_text(self):
        return self.__text

    def get_rating(self):
        return self.__rating

    def get_create_date(self):
        return self.__create_date

    def get_edit_date(self):
        return self.__edit_date

    def get_moderator_id(self):
        return self.__moderator_id

    def get_is_enabled(self):
        return self.__is_enabled

    def set_game_id(self, game_id):
        self.__game_id = game_id

    def set_user_id(self, user_id):
        self.__user_id = user_id

    def set_text(self, text):
        self.__text = text

    def set_rating(self, rating):
        self.__rating = rating

    def set_create_date(self, create_date):
        self.__create_date = create_date

    def set_edit_date(self, edit_date):
        self.__edit_date = edit_date

    def set_moderator_id(self, moderator_id):
        self.__moderator_id = moderator_id

    def set_is_enabled(self, is_enabled):
        self.__is_enabled = is_enabled
