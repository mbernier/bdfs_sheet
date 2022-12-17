import sys, pydantic
from collections import OrderedDict
from modules.caches.flat import Flat_Cache
from modules.caches.nested_cache.row import Nested_Cache_Row
from modules.caches.exception import Flat_Cache_Exception, Nested_Cache_Row_Exception, Nested_Cache_Rows_Location_Exception
from modules.config import config
from modules.decorator import Debugger
from pprint import pprint
from pydantic import Field, validate_arguments
from typing import Union

# This is a wrapper for Nested_Cache on top of Flat Cache
#   in order to reduce the complexity in the Nested_Cache implementation
#   and to wrap Flat_Cache with the logic needed for Nested_Cache in a clean way.
#   A nested Cache Row can be created with values or not and can be written 
#   to the Flat Cache either way.
class Nested_Cache_Rows_Location(Nested_Cache_Row):

    _width = 0

    @Debugger
    @validate_arguments
    def __init__(self, locations:list=None):

        self._storage = Flat_Cache()

        # take in a list of locations
        if None != locations:
            self.load_locations(locations)

    def load(self):
        raise Nested_Cache_Rows_Location_Exception("There is no load() for Nested_Cache_Rows_Location class")

    @Debugger
    @validate_arguments # no reason to check if one exists, they must both exist
    def insert(self, position:Union[int,str]):
        raise Nested_Cache_Rows_Location_Exception("There is no insert() for Nested_Cache_Rows_Location class, use add_location()")

    # This will return the index if location is given, or the location if index is given
    #   if it is set, the item must exist in the Row
    @Debugger
    @validate_arguments
    def select(self, position: Union[int, str]):
        return super().select(position)['position']


    # this is the same as the select method, for locations row
    @Debugger
    @validate_arguments
    def getLocationIndex(self, position: Union[int, str]):
        return self.select(position)


    # this overrides the Nested_Cache_Row default of setting data to the same thing
    #   for both index and location, so that we have the ability to reference in either
    #   direction
    @Debugger
    @validate_arguments
    def update(self, position: Union[int, str], otherPosition:Union[int,str]=None):
        raise Nested_Cache_Rows_Location_Exception("There is no update() for Nested_Cache_Rows_Location class, use update_location()")

    def 

    @Debugger
    def getAsList(self):
        return super().getAsList()


    @Debugger
    def getAsDict(self):
        return super().getAsDict()