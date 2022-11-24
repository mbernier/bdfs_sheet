import sys
from modules.cache import BdfsCache
from modules.caches.flat import FlatCache
from modules.caches.exception import NestedCacheException

# effectively a list of Flat Caches, allows for better control over the data and how it is stored/accessed
class NestedCache(BdfsCache):

    logger_name = "NestedCache"

    def __init__(self):
        self._storage: list[FlatCache] = []

    # check if the row exists already
    def _rowExists(self, row):
        return (0 <= row < len(self._storage))


    # Set some data into the flat cache at the row specified, if it's empty, otherwise error out
    def set(self, row, location, data):
        self.debug("set(row={}, location={}, data={})", (row, location, data))

        if None == self.get(row=row, location=location):
            self.__write(row=row, location=location, data=data)
        else:
            raise NestedCacheException("Cache has {} at {}:{}. To update data in the cache, use update()".format(self.get(row, location), row, location))

    def append(self, flatCacheItem):
        self.debug("append({})", flatCacheItem)
        self._storage.insert(len(self._storage),flatCacheItem)

    # Replace some data into the flat cache at the row specified
    def update(self, row, location, data):
        self.debug("update(row={}, location={}, data={})", (row, location, data))
        self._storage[row].update(location=location, data=data)


    # uses the dict get() to return None or the value if the item exists
    def get(self, row, location):
        self.debug("get(row={},location={})", (row, location))
        if self._rowExists(row):
            return self._storage[row].get(location)
        else:
            return None


    # uses the dict get() to return None or the value if the item exists
    #   returns the FlatCache object in this location
    def getRow(self, row):
        self.debug("getRow(row={})", row)
        if self._rowExists(row):
            return self._storage[row]
        else:
            return None


    def size(self):
        return len(self._storage)

    # use the flatCache.set() method on the data in this cache's row
    def __write(self, row, location, data):
        self.debug("__write(row={}, location={}, data={})", (row, location, data))
        print(self._storage)
        for rowIndex in range(0, row+1):
            self.debug("On Row {}", rowIndex)
            # check this row, if it exists, do nothing
            #   if it isn't set, but isn't our row, then set to None. Otherwise. create a Flat Cache there
            if None == self.getRow(rowIndex):
                if row != rowIndex:
                    self.debug("Appending an empty row to storage at row {}",rowIndex)
                    self._storage.insert(rowIndex,{})
                else:
                    self.debug("Appending a FlatCache obj to storage at row {}",rowIndex)
                    self._storage.insert(rowIndex,FlatCache())
        
        print(self._storage)

        # give the data to the flatCache to handle
        self._storage[row].set(location=location, data=data)


    # set the data in the row and location to None
    def unset(self, row, location):
        self.debug("unset(row={}. location={})", (row, location))
        if self.get(row=row, location=location):
            self._storage[row].unset(location)


    # set the data in the row and location to None
    def unsetRow(self, row):
        self.debug("unset(row={})", row)
        if self.getRow(row=row):
            self._storage[row] = FlatCache()


    # nuclear option   
    def clear(self):
        self.debug("clear()")
        self._storage = []


    def delete(self, row, location):
        self.debug("delete(row={},location={})", (row,location))
        self._storage[row].delete(location=location)


    def deleteRow(self, row):
        self.debug("deleteRow(row={})", row)
        del self._storage[row]

    # will return only the count of the data, will not include the header row
    #   This will create an off by one confusion at some point...
    def dataSize(self):
        return len(self._storage)

    def totalSize(self):
        return self.dataSize() + 1


