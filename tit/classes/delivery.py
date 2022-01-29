import tit.classes.logData as logData

class Delivery(logData.logData):
    def __init__(self, sku, delivery_date, restock_quantity, restock_price):
        super().__init__()
        self.__sku = sku
        self.__restock_price = restock_price
        self.__delivery_date = delivery_date
        self.__restock_quantity = restock_quantity

    def get_restock_price(self):
        return self.__restock_price
    
    def get_delivery_date(self):
        return self.__delivery_date

    def get_restock_quantity(self):
        return self.__restock_quantity
        
    def get_sku(self):
        return self.__sku

    
    def set_restock_price(self, restock_price):
        self.__restock_price = restock_price
    
    def set_delivery_date(self, delivery_date):
        self.__delivery_date = delivery_date

    def set_restock_quantity(self,restock_quantity):
        self.__restock_quantity = restock_quantity
    
    def set_sku(self,sku):
        self.__sku = sku