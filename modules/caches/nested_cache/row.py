import sys
from collections import OrderedDict
from pprint import pprint

from modules.base import BaseClass
from modules.caches.flat import Flat_Cache
from modules.caches.exception import Nested_Cache_Row_Exception, Flat_Cache_Exception
from modules.config import config
from modules.decorator import debug_log, validate

# stores everything by index, so that we don't have to keep track of the headers
#   Header management can be handled by the Nested_Cache class
class Nested_Cache_Row(BaseClass):

    _storage = None

    @debug_log
    @validate()
    def __init__(self, data:list=None):
        self.load(data)


    @debug_log
    @validate()
    def load(self, data:list=None):
        data = self.__prepData(data)
        self._storage = Flat_Cache()
        for i in data: 
            self.append(data[i])


    @debug_log
    @validate()
    def __prepData(self, data:list=None):

        if None == data:
            return {}

        return {i: data[i] for i in range(0, len(data))}


    @debug_log
    @validate()
    def add(self, index:int, data=None):
        try:
            self._storage.set(index, data)
        except Flat_Cache_Exception as err:
            raise Nested_Cache_Row_Exception(str(err))

    @debug_log
    @validate()
    def append(self, data=None):
        self._storage.set(self.width(),data)


    @debug_log
    @validate() # can be an index or a location string
    def get(self, position:int):
        return self._storage.get(position)


    @debug_log
    @validate() # index and location must be passed for set, bc the data has to be the same
    def set(self, index:int, data=None):
        try:
            self._storage.set(index, data)

        except Flat_Cache_Exception as err:
            raise Nested_Cache_Row_Exception(str(err))

    @debug_log
    @validate()
    def width(self):
        return self._storage.size()

    @debug_log
    @validate()
    def update(self, index:int, data=None):
        try:
            self._storage.update(index, data)
        except Flat_Cache_Exception as err:
            raise Nested_Cache_Row_Exception(str(err))
