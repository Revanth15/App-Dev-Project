from tit.classes.logData import logData


class Voucher(logData):
    count_id = 0

    def __init__(self, name, description, discount_code, spools, discount_amount, expiry_date, quantity, filename):
        super().__init__()
        Voucher.count_id += 1
        self.__voucher_id = Voucher.count_id
        self.__name = name
        self.__description = description
        self.__discount_code = discount_code
        self.__spools = spools
        self.__discount_amount = discount_amount
        self.__expiry_date = expiry_date
        self.__quantity = quantity
        self.__filename = filename


    def get_voucher_id(self):
        return self.__voucher_id

    def get_name(self):
        return self.__name

    def get_description(self):
        return self.__description

    def get_discount_code(self):
        return self.__discount_code

    def get_discount_amount(self):
        return self.__discount_amount

    def get_expiry_date(self):
        return self.__expiry_date

    def get_quantity(self):
        return self.__quantity

    def get_spools(self):
        return self.__spools

    def get_filename(self):
        return self.__filename


    def set_voucher_id(self, voucher_id):
        self.__voucher_id = voucher_id

    def set_name(self, name):
        self.__name = name

    def set_description(self, description):
        self.__description = description

    def set_discount_code(self, discount_code):
        self.__discount_code = discount_code

    def set_discount_amount(self, discount_amount):
        self.__discount_amount = discount_amount

    def set_expiry_date(self, expiry_date):
        self.__expiry_date = expiry_date

    def set_quantity(self, quantity):
        self.__quantity = quantity

    def set_spools(self, spools):
        self.__spools = spools

    def set_filename(self, filename):
        self.__filename = filename


