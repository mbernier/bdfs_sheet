import sys
from modules.cache import BdfsCache
from modules.caches.exception import Flat_Cache_Exception
from modules.decorator import debug_log,validate
from collections import OrderedDict
from pprint import pprint

# @todo add a toString method

class Flat_Cache(BdfsCache):

    logger_name = "modules.caches.Flat_Cache"

    _storage = {}

    @debug_log
    def __init__(self, data=None):
        self._storage = {}
        self.load(data)

    @debug_log
    @validate()
    def load(self, data=None):
        if None != data:
            for index in data:
                self.set(index, data[index])

    # put data in a location if it doesn't have that data, if it does, error out
    @debug_log
    @validate(location=['isType:int,str'])
    def set(self, location, data=None):
        if None == self.get(location):
            self.__write(location=location, data=data)
        else:
            raise Flat_Cache_Exception("Flat_Cache has '{}' at location: {}. To update data in the cache, use update()".format(self.get(location), location))


    # remove the data from the location, but keep the location index
    @debug_log
    @validate(location=['isType:int,str'])
    def unset(self, location):
        if self.get(location):
            self._storage[location] = None


    #change the data at the location
    @debug_log
    @validate(location=['isType:int,str'])
    def update(self, location, data=None):
        if None == self.get(location):
            raise Flat_Cache_Exception("There is nothing to update at position '{}' consider using set".format(location))
        self.__write(location=location, data=data)


    # get the data at the location
    @debug_log
    @validate(location=['isType:int,str'])
    def get(self, location):
        return self._storage.get(location)


    # returns a list of keys from the storage dict
    @debug_log
    def getKeys(self):
        self._storage.keys()


    # write data to the cache location
    @debug_log
    @validate(location=['isType:int,str'])
    def __write(self, location, data=None):
        self._storage[location] = data


    # clears the entire cache
    @debug_log
    def clear(self):
        self._storage.clear()


    # delete the location from the cache completely
    @debug_log
    @validate(location=['isType:int,str'])
    def delete(self, location):
        if self.get(location):
            del self._storage[location]


    # give us everything
    @debug_log
    def value(self):
        return self.getStorage()

    @debug_log
    def size(self):
        return len(self.getStorage())


    @debug_log
    def __str__(self) -> str:
        output = "Flat_Cache: \n"
        for item in self.getStorage():
            output += "\t{}: {}\n".format(item, self.get(item))
        return output

    @debug_log
    def getAsList(self):
        data = self.getStorage()
        output = []
        for index in data:
            if int == type(index):
                output.insert(index, data[index])
        return output


    @debug_log
    def getAsDict(self):
        data = self.getStorage()
        output = OrderedDict()
        for index in data:
            if int != type(index):
                output[index] = data[index]
        return output

    @debug_log
    @validate(location=['isType:int,str'])
    def validate_locationExists(self, location):
        if location in self._storage.keys():
            return True
        return False