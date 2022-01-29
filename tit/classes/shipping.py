# import tit.classes.user as User
from uuid import uuid4

class Shipping():
    uuid = "#" + str(uuid4())[:8]
    def __init__(self,order_id,phone_number, address, unit_number, postal_code,first_name, last_name, email):
        super().__init__(phone_number, address, unit_number, postal_code,first_name, last_name, email)
        self.__order_id = Shipping.uuid

    def get_order_id(self):
        return self.__order_id

    def set_order_id(self,order_id):
        self.__order_id = order_id
