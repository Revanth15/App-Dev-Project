from tit.classes.logData import logData

class Archive(logData):
    def __init__(self, filetype, tags):
        super().__init__()
        self.__filename = logData.get_id(self)
        self.__filetype = filetype
        self.__tags = tags
        
    def get_filename(self):
        return self.__filename

    def get_filetype(self):
        return self.__filetype

    def get_tags(self):
        return self.__tags

    def set_filename(self, filename):
        self.set_Modified()
        self.__filename = filename

    def set_filetype(self, filetype):
        self.set_Modified()
        self.__filetype = filetype
    
    def set_tags(self, tags):
        self.set_Modified()
        self.__tags = tags
    