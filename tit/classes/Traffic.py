import datetime

class Session():
    def __init__(self, userip, session, country=None, continent=None, city=None):
        self.__userIP = userip
        self.__sessionID = session
        self.__time = datetime.datetime.now().replace(microsecond=0)
        self.__userCountry = country
        self.__userContinent = continent
        self.__userCity = city
        self.__viewList = []

    def get_ip(self):
        return self.__userIP

    def get_session(self):
        return self.__sessionID

    def get_time(self):
        return self.__time

    def get_country(self):
        return self.__userCountry
    
    def get_continent(self):
        return self.__userContinent

    def get_city(self):
        return self.__userCity

    def get_views(self):
        return self.__viewList


    def set_country(self, country):
        self.__userCountry = country
    
    def set_continent(self, continent):
        self.__userContinent = continent

    def set_city(self, city):
        self.__userCity = city

    def update_views(self, view):
        self.__viewList.append(view)
