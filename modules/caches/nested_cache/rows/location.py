import sys
from collections import OrderedDict
from pprint import pprint

from modules.caches.nested_cache.rows.row import Nested_Cache_Row
from modules.caches.exception import Nested_Cache_Row_Exception, Flat_Cache_Exception
from modules.config import config
from modules.decorator import debug_log, validate


# This is a wrapper for Nested_Cache on top of Flat Cache
#   in order to reduce the complexity in the Nested_Cache implementation
#   and to wrap Flat_Cache with the logic needed for Nested_Cache in a clean way.
#   A nested Cache Row can be created with values or not and can be written 
#   to the Flat Cache either way.
class Nested_Cache_Row_Location(Nested_Cache_Row):

    @debug_log
    @validate()
    def __init__(self, locations:list=None):

        self._storage = Flat_Cache()

        # take in a list of locations that we care about if they are there and setup the row
        if None != locations:
            self.load(locations)


    # allows setting many locations at once
    @debug_log
    @validate()
    def load(self, locations:list):
        for location in locations:
            self.add(location)


    @debug_log
    @validate() # no reason to check if one exists, they must both exist
    def add(self, location:str):
        width = self.width()

        try:
            # try to create the location in the cache
            self.set(location, width)
            self.set(width, location)
        except(Nested_Cache_Row_Exception as err):
            raise Nested_Cache_Row_Location_Exception(err)



    # This will return the index if location is given, or the location if index is given
    #   if it is set, the item must exist in the Row
    @debug_log
    @validate(position=['isType:int,str'])
    def get(self, position):
        return super().get(position)



    # gets both index and location, then returns them in the correct order based on type
    @debug_log
    @validate(position=['isType:int,str'])
    def getLocationIndex(self, position)

        if type(position) is int: # we have the index
            return self.get(position), position
    
        else: # we have the location
            return position, self.get(position)



    # this overrides the Nested_Cache_Row default of setting data to the same thing
    #   for both index and location, so that we have the ability to reference in either
    #   direction
    @debug_log
    @validate(position=['ifType:int,str'])
    def set(position):
        otherPosition = self.get(position)

        # then set the data, because Nested_Cache_Row sets the data for both Index/Location at the same time
        # we want the location row to have index point to location and location point to index
        try:
            super().set(position, data=otherPosition)
            super().set(otherPosition, data=position)
        except(Nested_Cache_Row_Exception as err):
            raise Nested_Cache_Row_Location_Exception(err)



    # Change the index of a location
    @debug_log
    @validate(index=['locationEmpty'])
    def update(location:str, index:int):

        currentIndex = self.get(location)
        super().update(currentIndex, None) # reset the current index to None

        try:
            super().set(index, data=location) # add the new index
            super().update(location, data=index) # update location to have the new index
        except(Nested_Cache_Row_Exception as err):
            raise Nested_Cache_Row_Location_Exception(err)



    # return only the string keys from the storage
    def getLocationKeys(self) -> OrderedDict:
        keys = OrderedDict()
        
        for index in range(0,self.width()):
            # will get the location name for each index, in the correct order
            keys.append(self._storage.get(index))
        
        return keys


    def width(self) -> int:
        return self._storage.size() / 2


    def move(location:str, newIndex:int):
        raise Nested_Cache_Row_Location_Exception("move is not implemented yet")
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