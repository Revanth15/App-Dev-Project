from tit.classes.logData import logData

class Notification(logData):
    def __init__(self, name, type, message, url, id):
        super().__init__()
        self.__name = name
        self.__type = type
        self.__message = message
        self.__url = url
        self.__objid = id
        self.__seenby = []

    def get_name(self):
        return self.__name

    def get_type(self):
        return self.__type

    def get_message(self):
        return self.__message

    def get_url(self):
        return self.__url

    def get_obj_id(self):
        return self.__objid

    def get_seenby(self):
        return self.__seenby

    def set_message(self, message):
        self.__message = message

    def update_seenby(self, user_id):
        self.__seenby.append(user_id)

    def delete_seenby(self, user_id):
        self.__seenby.pop(user_id)