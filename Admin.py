import User

class Admin(User.User):
    count_id = 0

    # Admin
    def __init__(self, name, email, gender, phone_number, password, confirm_password):

    #   User
        super().__init__(name, email, phone_number, password)
        Admin.count_id += 1
        self.__admin_id = Admin.count_id
        self.__gender = gender
        self.__confirm_password = confirm_password


    def get_admin_id(self):
        return self.__admin_id

    def get_gender(self):
        return self.__gender
    
    def get_confirm_password(self):
        return self.__confirm_password

    def set_admin_id(self, admin_id):
        self.__admin_id = admin_id

    def set_gender(self, gender):
        self.__gender = gender

    def set_confirm_password(self, confirm_password):
        self.__confirm_password = confirm_password
