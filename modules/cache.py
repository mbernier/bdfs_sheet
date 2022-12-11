import sys
from modules.base import BaseClass
from modules.caches.exception import Cache_Exception


class BdfsCache(BaseClass):

    logger_name = "BdfsCache"
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