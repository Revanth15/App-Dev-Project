from flask_login import UserMixin

class User(UserMixin):
    count_id = 0

# more, use this. User class
    def __init__(self, name, email, phone_number, password, role='Customer'):
        super().__init__()
        User.count_id += 1
        self.__user_id = User.count_id
        self.__name = name
        self.__email = email 
        self.__phone_number = phone_number
        self.__password = password
        self.__role = role


    def get_id(self):
        return self.__user_id

    def get_user_id(self):
        return self.__user_id

    def get_name(self):
        return self.__name

    def get_email(self):
        return self.__email

    def get_phone_number(self):
        return self.__phone_number

    def get_password(self):
        return self.__password

    def get_role(self):
        return self.__role

    def set_user_id(self, user_id):
        self.__user_id = user_id

    def set_name(self, name):
        self.__name = name

    def set_email(self, email):
        self.__email = email

    def set_phone_number(self, phone_number):
        self.__phone_number = phone_number
 
    def set_password(self, password):
        self.__password = password
    