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
    def __init__(self, location=None, index=None, data=None):

        self._storage = Flat_Cache()

        # take in a list of locations that we care about if they are there and setup the row
        if None != data && None != location && None != index:
            self.set_at_location(location=index, data=data[index])
        else: 
            raise Nested_Cache_Rows_Data_Exception("Either location, index, and data need to be set or need to all be None")


    @Debugger
    @validate_arguments
    def add(self, location:str, index:int, data=None):
        
        locationData = {
            "position": index,
            "data": data
        }
        self.set_at_location(index, locationData)

        indexData = {
            "position": location,
            "data": data
        }
        self.set_at_location(index, indeData)

