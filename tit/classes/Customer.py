from tit.classes.User import User
class Customer(User):
    count_id = 0

    # Customer
    def __init__(self, name, email, gender, phone_number, password, confirm_password):

    #   User
        super().__init__(name, email, phone_number, password)
        Customer.count_id += 1
        self.__customer_id = Customer.count_id
        self.__gender = gender
        self.__confirm_password = confirm_password
        self.__spools = 0

    def get_customer_id(self):
        return self.__customer_id

    def get_gender(self):
        return self.__gender
    
    def get_confirm_password(self):
        return self.__confirm_password
    
    def get_spools(self):
        return self.__spools

    def set_customer_id(self, customer_id):
        self.__customer_id = customer_id

    def set_gender(self, gender):
        self.__gender = gender

    def set_confirm_password(self, confirm_password):
        self.__confirm_password = confirm_password
    
    def set_spools(self, spools):
        self.__spools = spools
