import sys
from collections import OrderedDict
from pprint import pprint

from modules.cache import BdfsCache
from modules.caches.flat import Flat_Cache
from modules.caches.nested_cache.rows.data import Nested_Cache_Rows_Data
from modules.caches.nested_cache.rows.location import Nested_Cache_Row_Location
from modules.caches.exception import Nested_Cache_Exception, Flat_Cache_Exception
from modules.config import config
from modules.decorator import debug_log, validate

# effectively a list of Flat Caches, allows for better control over the data and how it is stored/accessed
# Rules:
#    empty rows are None, not new Flat_Cache()
#    Flat_Cache items will be setup with the same headers every time, if data has unexpected headers:
    # options: 
    #     Fail hard
    #     return the unexpected headers
#   flat cache data is: location: {position: , data: } // index can be inferred from the position in the Flat_Cache item
#   locations flat cache is the same thing, it's the first row

class Nested_Cache(BdfsCache):

    logger_name = "Nested_Cache"

    _height = 0

    _storage: list = []

    _locations:list = None

    # locations are the indexes for the Flat_Cache
    #   We will make sure that they are setup properly as the caches are built
    @debug_log
    @validate()
    def __init__(self, locations: list = [], data:list = []):        
        self._debug = config("debug_validations") # get the debug level for validations
        self._storage = []
        self.__setup(locations, data)


    ####
    #
    # Setup methods
    #
    ####
    @debug_log
    @validate()
    def __setup(self, locations:list, data:list):
        self.__addLocations(locations)
        self.__addDataRowsWhereHeadersAreConfirmed(data)


    ####
    #
    # Location Row functionality
    #
    ####

    @debug_log
    @validate()
    # used in order to setup the locations row, so that we can check against it in the future
    def __addLocations(self, locations:list):
        locationRow = Nested_Cache_Row_Location(locations)

        self.__setLocationRow(locationRow)


    @debug_log
    @validate()
    def __getLocations(self) -> list:
        #_storage[0] is our locations Cache
        return self._storage[0].getLocationKeys()


    # create row[0] from the Locations Row, setup the OrderedDict for Location Headers
    @debug_log
    @validate()
    def __setLocationRow(self, locationRow:Nested_Cache_Row_Location):
        # set the storage Row
        if len(self._storage) == 0:
            self._storage.append(locationRow)
        else:
            self._storage[0] = locationRow

        # update the locations list with the locations
        self._locations = self.__getLocations()


    # do we know about this location?
    @debug_log
    @validate(position=['isType:int,str'])
    def __locationExists(self, position):
        locationData = self._storage[0].get(position)
        if None == locationData:
            return False
        return True


    @debug_log
    @validate(location=['oneIsNotNone:index'],
                index=['oneIsNotNone:location'])
    def __getLocationIndex(self, index:int=None, location:str=None):
        position = index if None == location else location
        return self._storage[0].getLocationIndex(position)


    ####
    #
    # Data Row Functionality
    #
    ####

    @debug_log
    @validate(location=['oneIsNotNone:index'], #we are just creating a data row, no need to validate location exists
                index=['oneIsNotNone:location']) #data can be anything, don't validate type
    def __createRowItemData(self, location:str=None, index:int=None, data=None):

        newRowData = {}

        # if we are doing anything after the first row, then we need to check.
        # the first row has no lookup because the first row is the lookup
        if 1 < self.height():
            # if we didn't get the location with the call then we need to look it up
            location, index = self.__getLocationIndex(index = index, location=location)

        newRowData[location] = {
            "position": index,
            "data": data
        }
        newRowData[index] = {
            "position": location,
            "data": data
        }

        return newRowData



    # check if the row exists already
    @debug_log
    @validate(row=['gte:0'])
    def __rowExists(self, row:int):
        # This method we are in exists to validate rows... so we are OK to check any row, to see if it exists
        return (0 <= row <= self.height())



    # allows adding multiple rows of data at the same time.
    # do not use this unless you confirmed the headers match what is expected
    @debug_log
    @validate()
    def __addDataRowsWhereHeadersAreConfirmed(self, data:list):

        for rowData in data:
            newRow = self.__createRowItem_FromData_WhereHeadersAreConfirmed(rowData)
            self.__appendRow(newRow)


    # Adding a single row of data into the cache
    # cannot be accessed directly, because we want to guarantee that we have headers whenever data is added later
    # Only use this when you KNOW that the headers and the data match (like on an insert where headers are passed)
    @debug_log
    @validate()
    def __createRowItem_FromData_WhereHeadersAreConfirmed(self, data:list):
        newRowData = {}
        for index, item in enumerate(data):

            location, index = self.__getLocationIndex(index = index)

            # keeping the data in sync, whether we access by the location or the index
            rowDataItem = self.__createRowItemData(location=location, index=index, data=item)
            newRowData.update(rowDataItem)
        return self.__createRowObject(newRowData)


    # uses the dict get() to return None or the value if the item exists
    #   returns the Flat_Cache object in this location
    @debug_log
    @validate( # row is not including rowExists, bc we want to return None if we don't have a row
                asObj=['contains:list,dict'])
    def getRow(self, row:int, asObj:str="list"):

        if self.__rowExists(row):
            if asObj == "list":
                return self.__getRowAsList(row)
            elif asObj == "dict":
                return self.__getRowAsDict(row)
            else:
                raise Nested_Cache_Exception("Rows can be returned as list or dict, but not {}".format(asObj))
        else:
            return None

    @debug_log
    @validate(row=['rowExists']) # overkill if only called by getRow, but not if called elsewhere
    def __getRowAsList(self, row:int):

        obj = []
        row = self.__getRawRow(row)
        for location in self.__getLocations():
            positionalData = row.get(location)
            if None == positionalData:
                obj.append(None)
            else:
                obj.append(row.get(location)['data'])
        return obj

    @debug_log
    @validate(row=['rowExists']) # overkill if only called by getRow, but not if called elsewhere
    def __getRowAsDict(self, row:int):

        obj = {}
        row = self.__getRawRow(row)
        for location in self.__getLocations():
            positionalData = row.get(location)
            if None == positionalData:
                obj[location] = None
            else:
                obj[location] = row.get(location)['data']
        return obj

    @debug_log
    @validate() #no rowExists is needed here
    def __getRawRow(self, row:int):

        if self.__rowExists(row):
            return self._storage[row]
        else:
            return None


    # assumes the row, location already exist in the data
    @debug_log
    @validate(row=['rowExists'],location=['locationExists']) # it is valid for data == None here, and data can be any type
    def set(self, row:int, location:str, data=None):
        self.__setRow(row=row, location=location, data=data)

    @debug_log
    @validate(row=['rowExists'],
                location=['oneIsNotNone:index', 'ifSet:locationExists'], 
                index=['oneIsNotNone:location', 'ifSet:indexExists']) #data can be anything, don't validate
    def __setRow(self, row:int, index:int=None, location:str=None, data=None):
        
        location, index = self.__getLocationIndex(index = index, location=location)

        try:
            self._storage[row].set(index, data)
        except Flat_Cache_Exception:
            raise Nested_Cache_Exception("There is already data at row:{} location:{}/index:{}, to change this data use update(row, location/index, data)".format(row, location, index))
        
        try:
            self._storage[row].set(location, data)
        except Flat_Cache_Exception:
            raise Nested_Cache_Exception("There is already data at row:{} location:{}/index:{}, to change this data use update(row, location/index, data)".format(row, location, index))

    @debug_log
    @validate(location=['oneIsNotNone:index', 'ifSet:locationExists'],
                index=['oneIsNotNone:location', 'ifSet:indexExists'])
                #data can be anything here, so don't validate the type
    def appendRow(self, location:str=None, index:int=None, data=None):
        newRowData = self.__createRowItemData(location=location, index=index, data=data)
        flatcache = self.__createRowObject(newRowData)
        self.__appendRow(flatcache)

    @debug_log
    @validate()
    def __appendRow(self, Flat_CacheItem:Flat_Cache):

        self._storage.append(Flat_CacheItem)

        self.info("Height: {}".format(self.height()))
        self.__increaseHeight()
        self.info("Height: {}".format(self.height()))


    @debug_log
    @validate() # can be None
    def __createRowObject(self, rowDataObj:dict=None):
        flatCache = Flat_Cache(rowDataObj)
        return flatCache

    @debug_log
    @validate(location=['oneIsNotNone:index'], #we are just creating a data row, no need to validate location exists
                index=['oneIsNotNone:location']) #data can be anything, don't validate type
    def __createRowItemData(self, location:str=None, index:int=None, data=None):

        newRowData = {}

        # if we didn't get the location with the call then we need to look it up
        location, index = self.__getLocationIndex(index = index, location=location)

        newRowData[location] = {
            "position": index,
            "data": data
        }
        newRowData[index] = {
            "position": location,
            "data": data
        }

        return newRowData


    @debug_log
    @validate(row=['rowExists'])
    def deleteRow(self, row:int):
        raise Exception("needs to be tested")
        row = self._storage.pop(row)
        self.info("deleting: {}".format(row))
        self.__decreaseHeight()


    @debug_log
    @validate(row=['rowExists'])
    def unsetRow(self, row:int):
        raise Exception("needs to be tested")
        self.info("unsetting row: {}".format((row)))
        # call the Flat_Cache unset method for this row
        self._storage[row] = self.__createRowObject(None)

    #### 
    #
    # Column Methods
    #
    ####

    # Delete the column, but first make sure we have all the correct data that we need in order to properly
    #   remove the column from every row in the dataset
    @debug_log
    @validate(location=['oneIsNotNone:index', 'ifSet:locationExists'],
                index=['oneIsNotNone:location', 'ifSet:indexExists'])
    def deleteColumn(self, index:int=None, location:str=None):
        raise Exception("needs to be tested")
        location, index = self.__getLocationIndex(location=location, index = index)

        if not self.__locationExists(location):
            raise Nested_Cache_Exception("Location '{}' doesn't exist, to add it use addColumn(location={})".format(location, location))

        #finally, delete the header from storage
        self.__removeHeaderIndexes(index=index, location=location)

    @debug_log
    @validate(location=['oneIsNotNone:index', 'ifSet:locationExists'],
                index=['oneIsNotNone:location', 'ifSet:indexExists'])
    # remove both the index and location from all rows in the sheetData
    def __removeHeaderIndexes(index:int, location:str):
        # delete the header from every single row in the storage
        for row in range(0, self.height()):
            self._storage[row].delete(index)
            self._storage[row].delete(location)


    ####
    #
    # Individual Item Methods
    #
    ####
    # uses the dict get() to return None or the value if the item exists
    @debug_log
    @validate() # no need to test location exists, return None if the data doesn't exist at row or location
    def getData(self, row:int, location:str):
        if self.__rowExists(row):
            data = self.__getItem(row=row, location=location)

            if None == data:
                return None
            return data['data']
        else:
            return None

    @debug_log
    @validate() #don't validate row or location, we want to return None if they don't exist
    def __getItem(self, row:int, location:str):

        if self.__rowExists(row):
            return self.__getRawRow(row).get(location)
        else:
            return None


    # wrapper for deleteItem
    @debug_log
    @validate(location=['oneIsNotNone:index','ifSet:locationExists'],
                index=['oneIsNotNone:location','ifSet:indexExists'])
    def delete(self, row:int, location:str=None, index:int=None):
        raise Exception("needs to be tested")
        self.deleteItem(row=row, location=location, index=index)

    @debug_log
    @validate(location=['oneIsNotNone:index','ifSet:locationExists'],
                index=['oneIsNotNone:location','ifSet:indexExists'])
    def deleteItem(self, row:int, location:str=None, index:int=None):
        raise Exception("needs to be tested")
        if 0 == row:
            raise Nested_Cache_Exception("You cannot delete from row[0], if you want to modify locations, use deleteColumn()")
        
        # if this is true, then we have index bc we passed validation. So, get the location
        if None == location:
            location, index == self.__getLocationIndex(index)

        self._storage[row].delete(location)
        self._storage[row].delete(index)


    @debug_log
    @validate(location=['oneIsNotNone:index','ifSet:locationExists'],
                index=['oneIsNotNone:location','ifSet:indexExists']) #data can be anything
    def update(self, row:int, index:int=None, location:str=None, data=None):

        location, index = self.__getLocationIndex(location=location, index = index)

        # create the data for the rows
        rowData = self.__createRowItemData(location=location, index=index, data=data)

        # do the manual update, we are not replacing the row, only the data in these locations
        self._storage[row].update(location=location, data=rowData[index])
        self._storage[row].update(location=index, data=rowData[location])

    @debug_log
    def unset(self, **kwargs):
        raise Nested_Cache_Exception("unset() is not valid for Nested_Cache, use either unsetRow() or unsetData()")

    @debug_log
    @validate(location=['oneIsNotNone:index','ifSet:locationExists'],
                index=['oneIsNotNone:location','ifSet:indexExists'])
    def unsetData(self, row, location:str=None, index:int=None):
        raise Exception("needs to be tested")
        self._storage[row].unset(location)
        self._storage[row].unset(index)

    ####
    #
    # Meta
    #
    ####

    # nuclear option
    @debug_log
    def clear(self):
        raise Exception("needs to be tested")
        self._storage = []

    @debug_log
    def height(self):
        # decrement bc the user doesn't need to know we are overloading the 0th row
        return self._height
    
    @debug_log
    @validate(increaseBy=['gt:0'])
    def __increaseHeight(self, increaseBy:int = 1):
        if 0 > increaseBy:
            raise Nested_Cache_Exception("You can only increase height by positive integers")
        self._height += increaseBy


    @debug_log
    @validate(decreaseBy=['gt:0'])
    def __decreaseHeight(self, decreaseBy:int = 1):
        if 0 > decreaseBy:
            raise Nested_Cache_Exception("You can only decrease height by positive integers")
        self._height -= decreaseBy

    @debug_log
    def width(self):
        # in order to avoid getting yelled at by row(0) check validations, use the _locations arr for width
        return len(self.__getLocations())

    @debug_log
    def __str__(self) -> str:
        output = "Nested_Cache: \n"
        return str(self.getAsListOfDicts())


    @debug_log
    def getAsListOfLists(self):
        data = self.getStorage()
        output = []
        for rowindex, row in enumerate(data):
            rowAsList = row.getAsList()
            rowData = []

            if 0 == rowindex: # this is the locations Row
                rowData = rowAsList
            else:
                for itemindex, rowItem in enumerate(rowAsList):
                    rowData.insert(itemindex, rowItem['data'])

            output.append(rowData)
        return output

    @debug_log
    def getAsListOfDicts(self):
        data = self.getStorage()
        output = []
        for index, row in enumerate(data):
            rowAsList = row.getAsDict()

            rowData = OrderedDict()
            for index in rowAsList:
                rowData[index] = rowAsList[index]['data']

            output.append(rowData)
        return output

    ####
    #
    # Validation Methods
    #
    ####

    @debug_log
    @validate()
    def validation_locationExists(self, param:str, paramValue:str=None):
        self.validation_method_debug("validation_locationExists", locals())
        if not self.__locationExists(paramValue):
            raise Nested_Cache_Exception("Location '{}' doesn't exist, to add it use addLocation(location)".format(paramValue))
        return True


    @debug_log
    @validate()
    def validation_indexExists(self, param:str, paramValue:int=None):
        self.validation_method_debug("validation_indexExists", locals())
        if not self.__locationExists(paramValue):
            raise Nested_Cache_Exception("Index '{}' doesn't exist, to add it use addLocation(location)".format(paramValue))
        return True


    @debug_log
    @validate()
    def validation_rowExists(self, param:str, paramValue=None):
        self.validation_method_debug("validation_rowExists", locals())
        if not self.__rowExists(row=paramValue):
            raise Nested_Cache_Exception("Row {} doesn't exist, to add it use appendRow()".format(paramValue))
        return True