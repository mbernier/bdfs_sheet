import sys
from modules.cache import BdfsCache
from modules.caches.flat import FlatCache
from modules.caches.exception import NestedCacheException
from pprint import pprint
from collections import OrderedDict

# @todo add a toString method

# effectively a list of Flat Caches, allows for better control over the data and how it is stored/accessed
# Rules:
#    empty rows are None, not new FlatCache()
#    flatCache items will be setup with the same headers every time, if data has unexpected headers:
    # options: 
    #     Fail hard
    #     return the unexpected headers
#   flat cache data is: location: {position: , data: } // index can be inferred from the position in the flatCache item
#   locations flat cache is the same thing, it's the first row

class NestedCache(BdfsCache):

    logger_name = "NestedCache"

    _height = 0

    # locations are the indexes for the FlatCache
    #   We will make sure that they are setup properly as the caches are built
    def __init__(self, locations, data):
        self._storage: list[FlatCache] = []

        self.__setup(locations, data)


    def __setup(self, locations, data):
        self.__addLocations(locations)
        self.__addDataRowsWhereHeadersAreConfirmed(data)




    ####
    #
    # Locations functionality
    #
    ####

    def __setLocations(self, locations):
        self.debug("__setLocations(locations={})".format(locations))
        self._locations = locations


    ####
    #
    # Rows
    #
    ####

    # check if the row exists already
    def __rowExists(self, row):
        self.debug("__rowExists(row={})".format(row))
        return (0 <= row < self.height())


    # used in order to setup the locations row, so that we can check against it in the future
    def __addLocations(self, locations):
        self.debug("__addLocations({})".format(locations))
        newRow = self.__createLocationsRowItem(locations)
        self.appendRow(newRow)


    # formats the data for the locations row and returns a FlatCache item of that data
    def __createLocationsRowItem(self, locations):
        self.debug("__createLocationsRowItem({})".format(locations))
        newRow = FlatCache()
        for index, location in enumerate(locations):
            # we are going to overload this row with the location twice, so that we can pull it the same as the other
            #   data when we need it later, load up the location and index as indeces on the FlatCache - so we can look up and manage it from either direction
            #   now we can get to the data either way, regardless of which method we take to get there.
            newRow.set(location, {
                    "position": index,
                    "data": location
                })
            newRow.set(index, {
                        "position": location,
                        "data":location
                })
        return newRow
    
    #Allows us to look up the location string by an index
    # this is used when we are looping through data and want to know what the header of the data is
    def __getLocationFromIndex(self, index):
        self.debug("__getLocationFromIndex(index={})".format(index))
        return self.getItem(0, index)['position']

    # allows adding multiple rows of data at the same time.
    # do not use this unless you confirmed the headers match what is expected
    def __addDataRowsWhereHeadersAreConfirmed(self, data):
        self.debug("__addDataRowsWhereHeadersAreConfirmed({})".format(data))
        for row in data:
            newRow = self.__createRowItem_FromData_WhereHeadersAreConfirmed(row)
            self.appendRow(newRow)

    # Adding a single row of data into the cache
    # cannot be accessed directly, because we want to guarantee that we have headers whenever data is added later
    # Only use this when you KNOW that the headers and the data match (like on an insert where headers are passed)
    def __createRowItem_FromData_WhereHeadersAreConfirmed(self, data):
        self.debug("__createRowItem_FromData_WhereHeadersAreConfirmed({})".format(data))
        newRowData = {}
        for index, item in enumerate(data):
            location = self.__getLocationFromIndex(index)
            # keeping the data in sync, whether we access by the location or the index
            newRowData[location] = {
                    "position": index,
                    "data": item
                }
            newRowData[index] = {
                "position": location,
                "data": item
            }
        return FlatCache.create(newRowData)


    # uses the dict get() to return None or the value if the item exists
    #   returns the FlatCache object in this location
    def getRow(self, row):
        self.debug("getRow(row={})", row)
        if self.__rowExists(row):
            return self._storage[row]
        else:
            return None

    def appendRow(self, flatCacheItem):
        self.debug("append({})", flatCacheItem)
        self._storage.insert(len(self._storage),flatCacheItem)
        self.__increaseHeight()







    # # allows inserting a new row into the cache
    # def X_insertRow(self, row, rowItem, updateCache = True):
    #     if type(rowItem) != Flatcache:
    #         raise NestedCacheException("When inserting a Row, FlatCache was expected {} was found".format(type(rowItem)))

    #     height = self.height()

    #     if height < row-1:
    #         diff = row - height
    #         newRows = [data]
    #         for i in range(diff):
    #             new.insert(0, None)
    #         self.extend(newRows)
    #     else:
    #         self._storage.insert(row, rowItem)

    #     self.__increaseHeight()

    #     return list





    ####
    #
    # Column Methods
    #
    ####

    def deleteColumns(self, index, header):
        # if both header and index, check that they point to eachother in the data store - otherwise raise Exception

        # if they are not both there, get the index or the header thats missing from data store

        # remove the header and index from each row of the data store
            #How does this affect the indexes that are stored -- do we need to decrement them?
        raise Exception("deleteColumsn is not implented yet")


    ####
    #
    # Individual Item Methods
    #
    ####
    # uses the dict get() to return None or the value if the item exists
    def getItem(self, row, location):
        self.debug("get(row={},location={})", (row, location))
        if self.__rowExists(row):
            return self.getRow(row).get(location)
        else:
            return None



    ####
    #
    # Meta
    #
    ####

    # nuclear option   
    def clear(self):
        self.debug("clear()")
        self._storage = []

    def height(self):
        self.debug("height()")
        return len(self._storage)

    def __increaseHeight(self, increaseBy = 1):
        self.debug("__increaseHeight(increaseBy={})".format(increaseBy))
        if 0 > increaseBy:
            raise NestedCacheException("You can only increase height by positive integers")
        self._height += increaseBy

    def __decreaseHeight(self, decreaseBy = 1):
        self.debug("__increaseHeight(decreaseBy={})".format(increaseBy))
        if 0 > decreaseBy:
            raise NestedCacheException("You can only decrease height by positive integers")
        self._height -= decreaseBy


    def width(self):
        self.debug("width()")
        return self.getRow(0).size()



    def __str__(self) -> str:
        self.debug("__str__()")
        output = "NestedCache: \n"
        for item in self.getStorage():
            output += "\t"+str(item) + "\n"

        return output

    def getAsListOfLists(self):
        self.debug("getAsLists()")
        data = self.getStorage()
        output = []
        for index, row in enumerate(data):
            rowAsList = row.getAsList()

            rowData = []
            for index, rowItem in enumerate(rowAsList):
                rowData.insert(index,rowItem['data'])

            output.append(rowData)
        return output


    def getAsListOfDicts(self):
        self.debug("getAsListOfDicts()")
        data = self.getStorage()
        output = []
        for index, row in enumerate(data):
            rowAsList = row.getAsDict()

            rowData = OrderedDict()
            for index in rowAsList:
                rowData[index] = rowAsList[index]['data']

            output.append(rowData)
        return output