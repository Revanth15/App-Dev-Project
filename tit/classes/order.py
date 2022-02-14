from uuid import uuid4
from tit.classes.logData import logData

class Order(logData):
    uuid = ("#" + str(uuid4())[-12:]).upper()
    def __init__(self,total_price,order,status):
        super().__init__()
        self.__order_id = Order.uuid
        self.__total_price = total_price
        self.__order = order
        self.__status = status

    def get_status(self):
        return self.__status
    
    def get_total_price(self):
        return self.__total_price

    def get_order(self):
        return self.__order

    def get_order_id(self):
        return self.__order_id

    def set_status(self,status):
        self.__status = status

