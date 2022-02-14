ouimport tit.classes.User as User 

class account(User.User):
    def __init__(self, first_name, last_name, email, remarks, account_name):
        super().__init__(first_name, last_name,email, remarks)
        self.__account_name = account_name
        
        
        
    def get_account_name(self):
        return self.__account_name

    def set_account_name(self, account_name):
        self.__account_name = account_name
        


    


