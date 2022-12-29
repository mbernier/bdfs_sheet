import sys
from modules.base import Base_Class

class Bdfs_Cache(Base_Class):

    _storage = {}

    def setData(self):
        print("setData")
        pass

    def unsetData(self):
        print("unsetData")
        pass

    def update(self):
        print("update")
        pass

    def get(self):
        print("get")
        pass

    def insert(self):
        print("insert")
        self.__write()
        pass

    def clear(self):
        print("clear")
        pass

    def __write(self):
        print("__write")
        pass

    def delete(self):
        print("delete")
        pass

    def getStorage(self):
        return self._storage