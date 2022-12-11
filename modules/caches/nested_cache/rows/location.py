import sys, pydantic
from pydantic import Field
from pydantic import validate_arguments
from collections import OrderedDict
from pprint import pprint
from typing import Union
from modules.caches.flat import Flat_Cache
from modules.caches.nested_cache.row import Nested_Cache_Row
from modules.caches.exception import Nested_Cache_Rows_Location_Exception
from modules.config import config
from modules.decorator import Debugger


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

        # take in a list of locations that we care about if they are there and setup the row
        if None != locations:
            self.load(locations)


    # allows setting many locations at once
    @Debugger
    @validate_arguments
    def load(self, locations:list):
        for location in locations:
            self.add(location)


    @Debugger
    @validate_arguments # no reason to check if one exists, they must both exist
    def add(self, location:str):

        try:
            # set the location with width as index
            self.set_at_location(location, self.width()) # handles both location and index setting
            self._width += 1
        except Nested_Cache_Row_Exception as err:
            raise Nested_Cache_Rows_Location_Exception(str(err))

    def remove(self, location):
        raise Exception("remove() is not implemented")
        # @todo:
            # decrement width
            # modify the indexes after the one that was removed

    # This will return the index if location is given, or the location if index is given
    #   if it is set, the item must exist in the Row
    @Debugger
    @validate_arguments
    def get_at_location(self, position: Union[int, str]):
        return self._storage.get_at_location(position)


    # gets both index and location, then returns them in the correct order based on type
    @Debugger
    @validate_arguments
    def getLocationIndex(self, position: Union[int, str]):

        if type(position) is int: # we have the index
            return self.get_at_location(position), position
    
        else: # we have the location
            return position, self.get_at_location(position)



    # this overrides the Nested_Cache_Row default of setting data to the same thing
    #   for both index and location, so that we have the ability to reference in either
    #   direction
    @Debugger
    @validate_arguments
    def set_at_location(self, position: Union[int, str], otherPosition=None):
        if None == otherPosition:
            otherPosition = self.get_at_location(position)

        # then set the data, because Nested_Cache_Row sets the data for both Index/Location at the same time
        # we want the location row to have index point to location and location point to index
        try:
            self._storage.set_at_location(position, data=otherPosition)
            self._storage.set_at_location(otherPosition, data=position)
        except Flat_Cache_Exception as err:
            raise Nested_Cache_Rows_Location_Exception(str(err))



    # Change the index of a location
    @Debugger
    @validate_arguments
    def update(self, position: Union[int, str]):
        raise Exception("double check that the indexes get updated correctly if an index changes, also add tests")
        currentIndex = self.get_at_location(location)
        self._storage.update(currentIndex, None) # reset the current index to None

        try:
            self._storage.set_at_location(index, data=location) # add the new index
            self._storage.update(location, data=index) # update location to have the new index
        except Nested_Cache_Row_Exception as err:
            raise Nested_Cache_Rows_Location_Exception(str(err))



    # return only the string keys from the storage
    @Debugger
    def getLocationKeys(self) -> list:
        keys = [] 

        for index in range(0,self.width()):
            # will get the location name for each index, in the correct order
            keys.append(self._storage.get_at_location(index))
        
        return keys

    @Debugger
    def width(self) -> int:
        return self._width


    @Debugger
    @validate_arguments
    def move(self, location:str, newIndex:int):
        raise Nested_Cache_Rows_Location_Exception("move is not implemented yet")
        # consider using self.update() where possible?
        # add testing!!
        # start:
                    # Storage: 1:one, 2:two, 3:three, 4:four, 5:five, one:1, two:2, three:3, four:4, five:5
                    # Memory: None
                    # StorageCopy: 1:one, 2:two, 3:three, 4:four, 5:five, one:1, two:2, three:3, four:4, five:5
        # move from 2 to 5
        #   pull the index to move and the location out of the row, store the data in memory
                    # Storage: 1:one, 3:three, 4:four, 5:five, one:1, three:3, four:4, five:5
                    # Memory: 2:two, two:2
                    # StorageCopy: 1:one, 2:two, 3:three, 4:four, 5:five, one:1, two:2, three:3, four:4, five:5
        #   in between 2 and 5:
        #       indexes > 2 get decremented & locations get the new index
                    # Storage: 1:one, 2:three, 3:four, 4:five, one:1, three:2, four:3, five:4
                    # Memory: 2:two, two:2
                    # StorageCopy: 1:one, 2:two, 3:three, 4:four, 5:five, one:1, two:2, three:3, four:4, five:5
        #   !! change notiong < 2 or > 5
        #   insert the index and location into the new position
                    # Storage: 1:one, 2:three, 3:four, 4:five, one:1, three:2, four:3, five:4, 5:two, two:5
                    # Memory: 
                    # StorageCopy: 1:one, 2:two, 3:three, 4:four, 5:five, one:1, two:2, three:3, four:4, five:5
        #   if everything went OK, delete StorageCopy, if not - throw exception


    @Debugger
    def getAsList(self):
        return self._storage.getAsList()


    @Debugger
    def getAsDict(self):
        return self._storage.getAsDict()