import datetime

class logData:
    def __init__(self):
        self.__id = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        self.__datetimeCreated = datetime.datetime.now()
        self.__datetimeModified = datetime.datetime.now()


    def get_Created(self, period='datetime'):
        if period == 'time':
            return self.__datetimeCreated.strftime("%H:%M:%S")

        elif period == 'date':
            return self.__datetimeCreated.strftime("%Y-%m-%d")

        elif period == 'datetime':
            return self.__datetimeCreated.strftime("%Y-%m-%d %H:%M:%S")

        else:
            return self.__datetimeCreated.strftime(period)

    def get_id(self):
        return self.__id

    def get_Modified(self, period):
        if period == 'time':
            return self.__datetimeModified.strftime("%H:%M:%S")

        elif period == 'date':
            return self.__datetimeModified.strptime("%Y-%M-%D")
        
        return self.__datetimeModified.strptime("%Y-%M-%D %H:%M:%S")

    def set_Modified(self):
        self.__datetimeModified = datetime.datetime.now()

    # def log_event(event):
        