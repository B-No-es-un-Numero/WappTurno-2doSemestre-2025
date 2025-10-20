import uuid

class Medical_consultation:
    def __init__(self, name: str, code: str, id: str = None):
        self.__id = id if id is not None else str(uuid.uuid4())
        self.__name = name
        self.__code = code


    def __str__(self):
        return f"Medical_consultation(id={self.id}, name={self.name}, code={self.code})"

    def __repr__(self):
        return f"Medical_consultation(id={self.id}, name={self.name}, code={self.code})"

    
    @property
    def id(self):
        return self.__id
    
    @id.setter
    def id(self, value):
        self.__id = value

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value

    @property
    def code(self):
        return self.__code

    @code.setter
    def code(self, value):
        self.__code = value