
import sys
from modules.base import BaseClass
from modules.caches.exception import CacheException


class BdfsCache(BaseClass):

    logger_name = "BdfsCache"
    _storage = {}

    def set(self):
        self.debug("set()")
        pass

    def unset():
        self.debug("unset()")
        pass

    def update(self):
        self.debug("update()")
        pass

    def get(self):
        self.debug("get()")
        pass

    def clear(self):
        self.debug("clear()")
        pass

    def __write(self):
        self.debug("__write()")
        pass

    def delete(self):
        self.debug("delete()")
        pass

    def getStorage(self):
        self.debug("getStorage()")
        return self._storage