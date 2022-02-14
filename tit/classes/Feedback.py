from re import T
from pandas import NA
import tit.classes.logData as logData
class feedback(logData.logData):
    def __init__(self, Name, email,type = None, feedback = None ):
        super().__init__()
        self.__Name = Name
        self.email = email
        self.feedback = feedback
        self.type = type
        self.status = "Pending"


    def get_Name(self):
        return self.__Name
    def get_email(self):
        return self.email
    def get_feedback(self):
        return self.feedback
    def get_type(self):
        return self.type
    
    def get_status(self):
        return self.status


    def set_Name(self, Name):
        self.__Name = Name
       
    def set_email(self,email):
        self.email = email
    def set_feedback(self, feedback):
        self.feedback = feedback
    def set_type(self, type):
        self.type = type
    
    def set_status(self, status):
        self.status = status


    


