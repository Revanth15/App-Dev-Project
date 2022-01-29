class Importfile():
    def __init__(self,xlsx_file):
        self.__xlsx_file = xlsx_file

    def get_xlsx_file(self,xlsx_file):
        return self.__xlsx_file

    def set_xlsx_file(self,xlsx_file):
        self.__xlsx_file = xlsx_file