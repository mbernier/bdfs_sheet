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

        # take in a list of locations that we care about if they are there and setup the row
        if None != locations:
            self.load(locations)


    # allows setting many locations at once
    @Debugger
    @validate_arguments
    def load(self, locations:list=None):
        for location in locations:
            self.add_at(location)


    @Debugger
    @validate_arguments # no reason to check if one exists, they must both exist
    def add_at(self, position:Union[int,str]):

        try:
            # set the location with width as index
            super()._set_at_location(self.width(), position)
            super()._set_at_location(position, self.width()) # handles both location and index setting
            self._width += 1
        except Flat_Cache_Exception as err:
            raise Nested_Cache_Rows_Location_Exception(str(err))
        except Nested_Cache_Row_Exception as err:
            raise Nested_Cache_Rows_Location_Exception(str(err))

    @Debugger
    @validate_arguments
    def remove(self, position:Union[int,str]):
        raise Exception("remove() is not implemented")
        # @todo:
            # decrement width
            # modify the indexes after the one that was removed


    # This will return the index if location is given, or the location if index is given
    #   if it is set, the item must exist in the Row
    @Debugger
    @validate_arguments
    def get_at(self, position: Union[int, str]):
        return super()._get_at_location(position)


    # gets both index and location, then returns them in the correct order based on type
    @Debugger
    @validate_arguments
    def getLocationIndex(self, position: Union[int, str]):

        if type(position) is int: # we have the index
            return (super()._get_at_location(position), position)
    
        else: # we have the location
            return (position, super()._get_at_location(position))



    # this overrides the Nested_Cache_Row default of setting data to the same thing
    #   for both index and location, so that we have the ability to reference in either
    #   direction
    @Debugger
    @validate_arguments
    def set_at(self, position: Union[int, str], otherPosition:Union[int,str]=None):
        if None == otherPosition:
            otherPosition = super()._get_at_location(position)

        # then set the data, because Nested_Cache_Row sets the data for both Index/Location at the same time
        # we want the location row to have index point to location and location point to index
        try:
            super()._set_at_location(position, data=otherPosition)
            super()._set_at_location(otherPosition, data=position)
        except Flat_Cache_Exception as err:
            raise Nested_Cache_Rows_Location_Exception(str(err))



    # Change the index of a location
    @Debugger
    @validate_arguments
    def update_at(self, position: Union[int, str], otherPosition:Union[int,str]):
        raise Exception("double check that the indexes get updated correctly if an index changes, also add tests")
        currentIndex = self.get_at_location(position)
        super()._update_at_location(currentIndex, None) # reset the current index to None

        try:
            super()._set_at_location(index, data=position) # add the new index
            super()._update_at_location(position, data=index) # update location to have the new index
        except Nested_Cache_Row_Exception as err:
            raise Nested_Cache_Rows_Location_Exception(str(err))



    # return only the string keys from the storage
    @Debugger
    def getLocationKeys(self) -> list:
        keys = []
        for index in range(0,self.width()):
            # will get the location name for each index, in the correct order
            keys.append(super()._get_at_location(index))
        
        return keys

    @Debugger
    def width(self) -> int:
        return self._width


    @Debugger
    @validate_arguments
    def move(self, position:Union[int,str], new:Union[int,str]):
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
        return super().getAsList()


    @Debugger
    def getAsDict(self):
        return super().getAsDict()