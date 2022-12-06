import sys
from modules.base import BaseClass
from modules.caches.exception import Cache_Exception


class BdfsCache(BaseClass):

    logger_name = "BdfsCache"
    _storage = {}

    def set(self):
        print("set")
        self.debug("set()")
        pass

    def unset():
        print("unset")
        self.debug("unset()")
        pass

    def update(self):
        print("update")
        self.debug("update()")
        pass

    def get(self):
        print("get")
        self.debug("get()")
        pass

    def clear(self):
        print("clear")
        self.debug("clear()")
        pass

    def __write(self):
        print("__write")
        self.debug("__write()")
        pass

    def delete(self):
        print("delete")
        self.debug("delete()")
        pass

    def getStorage(self):
        self.debug("getStorage()")
        return self._storage