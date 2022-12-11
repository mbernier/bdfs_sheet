import sys, pydantic
from pydantic import Field
from pydantic import validate_arguments

from collections import OrderedDict
from pprint import pprint

from modules.base import BaseClass
from modules.caches.flat import Flat_Cache
from modules.caches.exception import Nested_Cache_Row_Exception, Flat_Cache_Exception
from modules.config import config
from modules.decorator import Debugger

# stores everything by index, so that we don't have to keep track of the headers
#   Header management can be handled by the Nested_Cache class
class Nested_Cache_Row(BaseClass):

    _storage = None

    @Debugger
    @validate_arguments
    def __init__(self, data:list=None):
        self.load(data)


    @Debugger
    @validate_arguments
    def load(self, data:list=None):
        data = self.__prepData(data)
        self._storage = Flat_Cache()
        for i in data: 
            self.append(data[i])


    @Debugger
    @validate_arguments
    def __prepData(self, data:list=None):

        if None == data:
            return {}

        return {i: data[i] for i in range(0, len(data))}


    @Debugger
    @validate_arguments
    def add(self, index:int, data=None):
        try:
            self._storage.setData(index, data)
        except Flat_Cache_Exception as err:
            raise Nested_Cache_Row_Exception(str(err))

    @Debugger
    @validate_arguments
    def append(self, data=None):
        self._storage.setData(self.width(),data)


    @Debugger
    @validate_arguments # can be an index or a location string
    def get(self, position:int):
        return self._storage.get(position)


    @Debugger
    @validate_arguments # index and location must be passed for set, bc the data has to be the same
    def setData(self, index:int, data=None):
        try:
            self._storage.setData(index, data)

        except Flat_Cache_Exception as err:
            raise Nested_Cache_Row_Exception(str(err))

    @Debugger
    @validate_arguments
    def width(self):
        return self._storage.size()

    @Debugger
    @validate_arguments
    def updateData(self, index:int, data=None):
        try:
            self._storage.updateData(index, data)
        except Flat_Cache_Exception as err:
            raise Nested_Cache_Row_Exception(str(err))
