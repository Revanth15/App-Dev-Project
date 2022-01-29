class Payment():
    def __init__(self, card_number, card_holder, exp_mm, exp_yy, cvv):
        self.__card_number = card_number
        self.__card_holder = card_holder
        self.__exp_mm = exp_mm
        self.__exp_yy = exp_yy
        self.__cvv = cvv
    
    def get_card_number(self):
        return self.__card_number

    def get_card_holder(self):
        return self.__card_holder

    def get_exp_mm(self):
        return self.__exp_mm

    def get_exp_yy(self):
        return self.__exp_yy

    def get_cvv(self):
        return self.__cvv

    
    def set_card_number(self, card_number):
        self.__card_number = card_number

    def set_card_holder(self, card_holder):
        self.__card_holder = card_holder

    def set_exp_mm(self, exp_mm):
        self.__exp_mm = exp_mm

    def set_exp_yy(self, exp_yy):
        self.__exp_yy = exp_yy

    def set_cvv(self, cvv):
        self.__cvv = cvv