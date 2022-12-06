import sys
from collections import OrderedDict
from pprint import pprint

from modules.caches.nested_cache.rows.row import Nested_Cache_Row
from modules.caches.exception import Nested_Cache_Row_Exception, Flat_Cache_Exception
from modules.config import config
from modules.decorator import debug_log, validate

class Nested_Cache_Row(Flat_Cache):

    @debug_log
    @validate() 
    def __init__(self, data:dict=None):
        self.load(data)


    @debug_log
    def load(self, data:dict=None):
        self._storage = Flat_Cache.create(data)


    @debug_log
    @validate()
    def add(self, index:int, location:str, data=None):
        try:
            self._storage.set(index, data)
            self._storage.set(location, data)
        except(Flat_Cache_Exception as err):
            raise Nested_Cache_Row_Exception(err)

    @debug_log
    @validate(position=['isType:int,str']) # can be an index or a location string
    def get(self, position):
        return self._storage.get(position)


    @debug_log
    @validate(data=None) # index and location must be passed for set, bc the data has to be the same
    def set(self, index:int, location:str, data=None):
        try:
            self._storage.set(index, data)
            self._storage.set(location, data)
        except(Flat_Cache_Exception as err):
            raise Nested_Cache_Row_Exception(err)

    def update():
        raise Exception("not implmented yet, need to consider capturing Excpetions and rewriting here")
