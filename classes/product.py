class Product:

    def __init__(self, product_name, sku, product_price, quantity, sale_price, picture_name):
        self.__product_name = product_name
        self.__sku = sku
        self.__product_price = product_price
        self.__quantity = quantity
        self.__sale_price = sale_price
        self.__picture_name = picture_name

    def get_product_name(self):
        return self.__product_name

    def get_sku(self):
        return self.__sku

    def get_product_price(self):
        return self.__product_price

    def get_quantity(self):
        return self.__quantity

    def get_sale_price(self):
        return self.__sale_price

    def get_picture_name(self):
        return self.__picture_name

    def set_prodcut_name(self, product_name):
        self.__product_name = product_name

    def set_sku(self, sku):
        self.__sku = sku

    def set_product_price(self, product_price):
        self.__product_price = product_price
    
    def set_quantity(self, quantity):
        self.__quantity = quantity

    def set_sale_price(self, sale_price):
        self.__sale_price = sale_price

    def set_picture_name(self, picture_name):
        self.__picture_name = picture_name
    


    

