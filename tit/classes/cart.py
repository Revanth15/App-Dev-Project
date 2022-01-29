import tit.classes.product as product

class Cart(product.Product):
    def __init__(self, product_name="", sku="", product_price=0.0, quantity=1, filename="", total_price=0.0):
        super().__init__(product_name, sku, product_price, quantity, filename)
        self.__total_price = total_price

    def set_total_price(self,total_price):
        self.__total_price = total_price

    def get_total_price(self):
        return self.__total_price
