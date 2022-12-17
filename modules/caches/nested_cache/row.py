import sys, pydantic
from collections import OrderedDict
from modules.base import BaseClass
from modules.caches.flat import Flat_Cache
from modules.caches.exception import Nested_Cache_Row_Exception, Flat_Cache_Exception
from modules.config import config
from modules.decorator import Debugger
from pprint import pprint
from pydantic import Field, validate_arguments
from typing import Union

# stores everything by index, so that we don't have to keep track of the headers
#   Header management can be handled by the Nested_Cache class
class Nested_Cache_Row(Flat_Cache):

    _storage = None

    @Debugger
    @validate_arguments
    def __init__(self, headers:list=None, data:list=None):
        self.load(headers, data)


    @Debugger
    @validate_arguments
    def load(self, headers:list=None, data:list=None):
        self._storage = Flat_Cache(headers, data)


    #insert with index=None is the same as appending to the end
    @Debugger
    @validate_arguments
    def insert(self, position:Union[int,str]=None, data=None):
        try:
            self._storage.insert(position=position, data=data)
        except Flat_Cache_Exception as err:
            raise Nested_Cache_Row_Exception(str(err))


    #index=None means get all
    @Debugger
    @validate_arguments # can be an index or a location string
    def select(self, position:Union[int,str]=None):
        data = self._storage.select(position=position)
        return data


    @Debugger
    @validate_arguments # index and location must be passed for set, bc the data has to be the same
    def update(self, position:Union[int,str], data=None):
        try:
            self._storage.update(position=position, data=data)
        except Flat_Cache_Exception as err:
            raise Nested_Cache_Row_Exception(str(err))


    @Debugger
    @validate_arguments
    def width(self):
        return self._storage.size()


    def getAsList(self):
        return self._storage.getAsList()


    def getAsDict(self):
        return self._storage.getAsDict()