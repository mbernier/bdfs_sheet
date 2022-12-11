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
        self._storage = Flat_Cache(data)

    @Debugger
    @validate_arguments
    def __prepData(self, data:list=None):

        if None == data:
            return {}

        return {i: data[i] for i in range(0, len(data))}


    @Debugger
    @validate_arguments
    def add_at(self, index:int, data=None):
        try:
            self._add_at_location(index, data)
        except Flat_Cache_Exception as err:
            raise Nested_Cache_Row_Exception(str(err))


    def add_at_location(*args, **kwargs):
        raise Nested_Cache_Row_Exception("add_at_location is not available for Nested_Cache_Row")


    def _add_at_location(self, location:Union[int,str], data=None):
        self._storage.add_at_location(location=location, data=data)


    @Debugger
    @validate_arguments
    def append(self, data=None):
        self._storage.set_at_location(self.width(),data)


    @Debugger
    @validate_arguments # can be an index or a location string
    def get_at(self, position:int):
        return self._get_at_location(position)


    def get_at_location(*args, **kwargs):
        raise Nested_Cache_Row_Exception("get_at_location is not available for Nested_Cache_Row")


    def _get_at_location(self, location:Union[int,str]):
        return self._storage.get_at_location(location=location)


    @Debugger
    @validate_arguments # index and location must be passed for set, bc the data has to be the same
    def set_at(self, index:int, data=None):
        try:
            self._set_at_location(location=index, data=data)

        except Flat_Cache_Exception as err:
            raise Nested_Cache_Row_Exception(str(err))


    def set_at_location(*args, **kwargs):
        raise Nested_Cache_Row_Exception("set_at_location is not available for Nested_Cache_Row")


    def _set_at_location(self, location:Union[int,str], data=None):
        self._storage.set_at_location(location=location, data=data)


    @Debugger
    @validate_arguments
    def width(self):
        return self._storage.size()

    @Debugger
    @validate_arguments
    def update_at(self, index:int, data=None):
        try:
            self._update_at_location(index, data)
        except Flat_Cache_Exception as err:
            raise Nested_Cache_Row_Exception(str(err))

    def update_at_location(*args, **kwargs):
        raise Nested_Cache_Row_Exception("update_at_location is not available for Nested_Cache_Row")

    def _update_at_location(self, location:Union[int,str], data=None):
        self._storage.update_at_location(location=location, data=data)

    def getAsList(self):
        return self._storage.getAsList()

    def getAsDict(self):
        return self._storage.getAsDict()