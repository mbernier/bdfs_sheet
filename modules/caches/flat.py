import sys
from modules.cache import BdfsCache
from modules.caches.exception import Flat_Cache_Exception
from collections import OrderedDict
from pprint import pprint

# @todo add a toString method

class Flat_Cache(BdfsCache):

    logger_name = "modules.caches.Flat_Cache"

    _storage = {}

    def __init__(self):
        self._storage = {}

    # put data in a location if it doesn't have that data, if it does, error out
    def set(self, location, data):
        self.debug("set(location={}, data={})", (location, data))
        if None == self.get(location):
            self.__write(location=location, data=data)
        else:
            raise Flat_Cache_Exception("Flat_Cache has {} at {}. To update data in the cache, use update()".format(self.get(location), location))


    # remove the data from the location, but keep the location index
    def unset(self, location):
        self.debug("unset(location={})", location)
        if self.get(location):
            self._storage[location] = None


    #change the data at the location
    def update(self, location, data):
        self.debug("update(location={}, data={})", (location, data))
        if None == self.get(location):
            raise Flat_Cache_Exception("There is nothing to update at position '{}'".format(location))
        self.__write(location=location, data=data)


    # get the data at the location
    def get(self, location):
        self.debug("get(location={})", location)
        return self._storage.get(location)

    # returns a list of keys from the storage dict
    def getKeys(self):
        self._storage.keys()


    # write data to the cache location
    def __write(self, location, data):
        self.debug("__write(location={}, data={})", (location, data))
        self._storage[location] = data


    # clears the entire cache
    def clear(self):
        self.debug("clear()")
        self._storage.clear()


    # delete the location from the cache completely
    def delete(self, location):
        self.debug("delete(location={})",location)
        if self.get(location):
            del self._storage[location]


    # give us everything
    def value(self):
        return self.getStorage()


    def size(self):
        return len(self.getStorage())


    # creates a new Flat_Cache item from some data
    @staticmethod
    def create(data=None):
        flatCache = Flat_Cache()
        if not None == data:
            for index in data:
                flatCache.set(index, data[index])
        return flatCache

    def __str__(self) -> str:
        output = "Flat_Cache: \n\t"
        for item in self.getStorage():
            output += "\t{}: {}\n".format(item, self.get(item))
        return output

    def getAsList(self):
        self.debug("getAsList()")
        data = self.getStorage()
        output = []
        for index in data:
            if int == type(index):
                output.insert(index, data[index])
        return output

    def getAsDict(self):
        self.debug("getAsDict()")
        data = self.getStorage()
        output = OrderedDict()
        for index in data:
            if int != type(index):
                output[index] = data[index]
        return output


    def validate_locationExists(self, location):
        if location in self._storage.keys():
            return True
        return False