class Product:

    def __init__(self, product_name="", sku="", product_price=0.0, quantity=0, product_description="", filename="", category=""):
        self.__product_name = product_name
        self.__sku = sku
        self.__product_price = product_price
        self.__quantity = quantity
        self.__product_description = product_description
        self.__filename = filename
        self.__category = category

    def get_product_name(self):
        return self.__product_name

    def get_sku(self):
        return self.__sku

    def get_product_price(self):
        return self.__product_price

    def get_quantity(self):
        return self.__quantity
    
    def get_product_description(self):
        return self.__product_description

    def get_filename(self):
        return self.__filename

    def get_category(self):
        return self.__category
    
    
    def set_product_name(self, product_name):
        self.__product_name = product_name

    def set_sku(self, sku):
        self.__sku = sku

    def set_product_price(self, product_price):
        self.__product_price = product_price
    
    def set_quantity(self, quantity):
        self.__quantity = quantity

    def set_product_description(self, product_description):
        self.__product_description = product_description

    def set_filename(self, filename):
        self.__filename = filename

    def set_category(self,category):
        self.__category = category

    def __str__(self):
        return f'{self.get_product_name()} ({self.get_sku()})'
    

