# super() =  function used to give access to the methods of a parent class.
#            Returns a temporary onject of a parent class when used

import tit.classes.Customer as Customer

class Admin(Customer.User):
    count_id = 0

    def __init__(self, first_name, last_name, email, phone_number, address, unit_number, postal_code, password,date_joined):
        super().__init__(first_name, last_name, email, phone_number, address, unit_number, postal_code, password)
        Admin.count_id += 1
        self.__admin_id = Admin.count_id
        self.__email = email
        self.__date_joined = date_joined
        self.__address = address

    def get_admin_id(self):
        return self.__admin_id

    def get_email(self):
        return self.__email

    def get_date_joined(self):
        return self.__date_joined

    def get_address(self):
        return self.__address

    def set_customer_id(self, customer_id):
        self.__customer_id = customer_id

    def set_email(self, email):
        self.__email = email

    def set_date_joined(self, date_joined):
        self.__date_joined = date_joined

    def set_address(self, address):
        self.__address = address
