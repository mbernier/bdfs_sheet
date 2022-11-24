import sys
from modules.cache import BdfsCache
from modules.caches.exception import FlatCacheException


class FlatCache(BdfsCache):

    logger_name = "modules.caches.FlatCache"


    # put data in a location if it doesn't have that data, if it does, error out
    def set(self, location, data):
        self.debug("set(location={}, data={})", (location, data))
        if None == self.get(location):
            self.__write(location=location, data=data)
        else:
            raise FlatCacheException("FlatCache has {} at {}. To update data in the cache, use update()".format(self.get(location), location))


    # remove the data from the location, but keep the location index
    def unset(self, location):
        self.debug("unset(location={})", location)
        if self.get(location):
            self._storage[location] = None


    #change the data at the location
    def update(self, location, data):
        self.debug("update(location={}, data={})", (location, data))
        if None == self.get(location):
            raise FlatCacheException("There is nothing to update at {}".format(location))
        self.__write(location=location, data=data)


    # get the data at the location
    def get(self, location):
        self.debug("get(location={})", location)
        return self._storage.get(location)


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
        return self._storage