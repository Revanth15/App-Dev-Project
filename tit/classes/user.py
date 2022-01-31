class User:
    count_id = 0

    def __init__(self, first_name, last_name, email, gender, phone_number, address, unit_number, postal_code, password):
        self.__first_name = first_name
        self.__last_name = last_name
        self.__email = email
        self.__gender = gender
        self.__phone_number = phone_number
        self.__address = address
        self.__unit_number = unit_number
        self.__postal_code = postal_code
        self.__password = password


    def get_first_name(self):
        return self.__first_name

    def get_last_name(self):
        return self.__last_name

    def get_email(self):
        return self.__email

    def get_gender(self):
        return self.__gender

    def get_phone_number(self):
        return self.__phone_number

    def get_address(self):
        return self.__address
    
    def get_unit_number(self):
        return self.__unit_number
    
    def get_postal_code(self):
        return self.__postal_code

    def get_password(self):
        return self.__password


    def set_first_name(self, first_name):
        self.__first_name = first_name

    def set_last_name(self, last_name):
        self.__last_name = last_name

    def set_email(self, email):
        self.__email = email

    def set_gender(self, gender):
        self.__gender = gender

    def set_phone_number(self, phone_number):
        self.__phone_number = phone_number

    def set_unit_number(self, unit_number):
        self.__unit_number = unit_number
    
    def set_postal_code(self, postal_code):
        self.__postal_code= postal_code

    def set_password(self, password):
        self.__password = password



    

