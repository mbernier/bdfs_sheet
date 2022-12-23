import sys
from modules.base import BaseClass

class BdfsCache(BaseClass):

    _storage = {}

    def setData(self):
        print("setData")
        pass

    def unsetData():
        print("unsetData")
        pass

    def update(self):
        print("update")
        pass

    def get(self):
        print("get")
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