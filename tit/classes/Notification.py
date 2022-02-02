from tit.classes.logData import logData

class Notification(logData):
    def __init__(self, name, type, message):
        super().__init__()
        self.__name = name
        self.__type = type
        self.__message = message
        self.__seenby = []

    def get_name(self):
        return self.__name

    def get_type(self):
        return self.__type

    def get_message(self):
        return self.__message

    def get_seenby(self):
        return self.__seenby

    def set_message(self, message):
        self.__message = message

    def update_message(self, user_id):
        self.__seenby.append(user_id)