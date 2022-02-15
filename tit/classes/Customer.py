from tit.classes.User import User
import datetime
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
        self.__cartStatus = ['Empty', datetime.datetime.now()]

    def get_customer_id(self):
        return self.__customer_id

    def get_gender(self):
        return self.__gender
    
    def get_confirm_password(self):
        return self.__confirm_password
    
    def get_spools(self):
        return self.__spools

    def get_cartStatus(self, index):
        if self.__cartStatus[0] == 'Purchased':
            if self.__cartStatus[1]-datetime.datetime.now() < datetime.timedelta(days=30):
                self.__cartStatus[0] = 'Empty'
            return self.__cartStatus[index]
        else:
            return self.__cartStatus[index]

    def set_customer_id(self, customer_id):
        self.__customer_id = customer_id

    def set_gender(self, gender):
        self.__gender = gender

    def set_confirm_password(self, confirm_password):
        self.__confirm_password = confirm_password
    
    def set_spools(self, spools):
        self.__spools = spools

    def set_cartStatus(self, status):
        print(status)
        self.__cartStatus[0] = status
        print(self.__cartStatus)
