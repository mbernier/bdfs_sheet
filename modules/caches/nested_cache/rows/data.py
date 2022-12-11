import sys
from collections import OrderedDict
from pprint import pprint
from pydantic import validator, validate_arguments
from modules.caches.flat import Flat_Cache
from modules.caches.nested_cache.row import Nested_Cache_Row
from modules.caches.exception import Nested_Cache_Row_Exception, Flat_Cache_Exception
from modules.config import config
from modules.decorator import Debugger


# This is a wrapper for Nested_Cache on top of Flat Cache
#   in order to reduce the complexity in the Nested_Cache implementation
#   and to wrap Flat_Cache with the logic needed for Nested_Cache in a clean way.
#   A nested Cache Row can be created with values or not and can be written 
#   to the Flat Cache either way.
class Nested_Cache_Rows_Data(Flat_Cache):


    @Debugger
    @validate_arguments
    def createDataDicts(self, location, index, data):
        locationData = {
            "position": index,
            "data": data
        }

        indexData = {
            "position": location,
            "data": data
        }

        return locationData, indexData

    @Debugger
    @validate_arguments
    def add_at_location(self, location:str, index:int, data=None):
        
        locationData, indexData = self.createDataDicts()

        self.write(location=location, data=locationData)
        self.write(location=index, data=indexData)

    @Debugger
    @validate_arguments
    def set_at_location(self, location:str, index:int, data=None):
        locationData, indexData = self.createDataDicts()
        super().set_at_location(location, locationData)
        super().set_at_location(index, indexData)

    @Debugger
    @validate_arguments
    def remove_location(self, location:str, index:int):
        super().remove_location(location)
        super().remove_location(index)