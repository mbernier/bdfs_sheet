
import sys
from modules.base import BaseClass
from modules.caches.exception import CacheException


class BdfsCache(BaseClass):

    logger_name = "BdfsCache"

    def __init__(self):
        self._storage = {}
        pass

    def set(self):
        self.debug("bdfsCache.set()")
        pass

    def unset():
        self.debug("bdfsCache.unset()")
        pass

    def update(self):
        self.debug("bdfsCache.update()")
        pass

    def get(self):
        self.debug("bdfsCache.get()")
        pass

    def clear(self):
        self.debug("bdfsCache.clear()")
        pass

    def __write(self):
        self.debug("bdfsCache.__write()")
        pass

    def delete(self):
        self.debug("bdfsCache.delete()")
        pass