import sys, pydantic
from collections import OrderedDict
from pprint import pprint
from typing import Union
from pydantic import Field
from pydantic.typing import Annotated
from pydantic import validator, validate_arguments
from modules.cache import BdfsCache
from modules.caches.flat import Flat_Cache
from modules.caches.nested_cache.rows.data import Nested_Cache_Rows_Data
from modules.caches.nested_cache.rows.location import Nested_Cache_Row_Location
from modules.caches.exception import Nested_Cache_Exception, Flat_Cache_Exception
from modules.config import config
from modules.decorator import Debugger
from modules.logger import Logger
from modules.validation import Validation
from enum import Enum, IntEnum

# for validating items that can be either int/str
class str_list(str, Enum):
    str="str"
    list="list"

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
    @Debugger
    def __init__(self, locations: list = [], data:list = []):        
        self._storage = []
        self.__setup(locations, data)


    ####
    #
    # Setup methods
    #
    ####
    @Debugger
    def __setup(self, locations:list, data:list):
        self.__addLocations(locations)
        self.__addDataRowsWhereHeadersAreConfirmed(data)


    ####
    #
    # Location Row functionality
    #
    ####

    @Debugger
    # used in order to setup the locations row, so that we can check against it in the future
    def __addLocations(self, locations:list):
        locationRow = Nested_Cache_Row_Location(locations)

        self.__setLocationRow(locationRow)


    @Debugger
    def __getLocations(self) -> list:
        #_storage[0] is our locations Cache
        return self._storage[0].getLocationKeys()


    # create row[0] from the Locations Row, setup the OrderedDict for Location Headers
    @Debugger
    def __setLocationRow(self, locationRow:Nested_Cache_Row_Location):
        # set the storage Row
        if len(self._storage) == 0:
            self._storage.append(locationRow)
        else:
            self._storage[0] = locationRow

        # update the locations list with the locations
        self._locations = self.__getLocations()


    # do we know about this location?
    @Debugger
    def locationExists(self, position: Union[int,str]):
        locationData = self._storage[0].get_at_location(position)
        if None == locationData:
            return False
        return True

    @Debugger
    def __getLocationIndex(self, position: Union[int, str]):
         
        return self._storage[0].getLocationIndex(position)


    ####
    #
    # Data Row Functionality
    #
    ####

    # check if the row exists already
    @Debugger
    @validate_arguments
    def rowExists(self, row:Annotated[int, Field(gt=0)]):
        # This method we are in exists to validate rows... so we are OK to check any row, to see if it exists
        return (0 <= row <= self.height())

    # allows adding multiple rows of data at the same time.
    # do not use this unless you confirmed the headers match what is expected
    @Debugger
    @validate_arguments
    def __addDataRowsWhereHeadersAreConfirmed(self, data:list):

        for rowData in data:
            for index, item in enumerate(data):

                location, index = self.__getLocationIndex(index = index)

                row = Nested_Cache_Rows_Data()
                row.add(location=location, index=index, data=data)
            self.__appendRow(newRow)


    @Debugger
    @validate_arguments # can be None
    def __createRowObject(self, position, data):

        location, index = self.__getLocationIndex(position)

        flatCache = Nested_Cache_Rows_Data(location=location, index=index, data=data)
        return flatCache


    # uses the dict get() to return None or the value if the item exists
    #   returns the Flat_Cache object in this location
    @Debugger
    def getRow(self, row:int, asObj:str_list="list"):
        if self.validation_rowExists(row):
            if asObj == "list":
                return self.__getRowAsList(row)
            elif asObj == "dict":
                return self.__getRowAsDict(row)
            else:
                raise Nested_Cache_Exception("Rows can be returned as list or dict, but not {}".format(asObj))
        else:
            return None

    @Debugger
    @validate_arguments
    def __getRowAsList(self, row:int):
        self.validation_rowExists(row)
        obj = []
        row = self.__getRawRow(row)
        for location in self.__getLocations():
            positionalData = row.get_at_location(location)
            if None == positionalData:
                obj.append(None)
            else:
                obj.append(row.get_at_location(location)['data'])
        return obj

    @Debugger
    @validate_arguments
    def __getRowAsDict(self, row:int):
        self.validation_rowExists(row)
        obj = {}
        row = self.__getRawRow(row)
        for location in self.__getLocations():
            positionalData = row.get_at_location(location)
            if None == positionalData:
                obj[location] = None
            else:
                obj[location] = row.get_at_location(location)['data']
        return obj

    @Debugger
    @validate_arguments #no validation_rowExists is needed here, bc we can return None
    def __getRawRow(self, row:int):

        if self.rowExists(row):
            return self._storage[row]
        else:
            return None


    # assumes the row, location already exist in the data
    @Debugger
    @validate_arguments # it is valid for data == None here, and data can be any type
    def set_row_item(self, row:int, location:str, data=None):
        self.validation_rowExists(row)
        self.validation_locationExists(location)
        self.__setRow(row=row, location=location, data=data)

    @Debugger
    @validate_arguments #data can be anything, don't validate
    def __setRow(self, row:int, index:int=None, location:str=None, data=None):

        self.validation_rowExists(row)
        Validation.validation_oneIsNotNone(index, location)

        location, index = self.__getLocationIndex(index = index, location=location)

        try:
            self._storage[row].set_at_location(index, data)
        except Flat_Cache_Exception:
            raise Nested_Cache_Exception("There is already data at row:{} location:{}/index:{}, to change this data use update(row, location/index, data)".format(row, location, index))
        
        try:
            self._storage[row].set_at_location(location, data)
        except Flat_Cache_Exception:
            raise Nested_Cache_Exception("There is already data at row:{} location:{}/index:{}, to change this data use update(row, location/index, data)".format(row, location, index))

    @Debugger
    @validate_arguments #data can be anything here, so don't validate the type
    def appendRow(self, location:str=None, index:int=None, data=None):
        Validation.validation_oneIsNotNone(index, location)

        newRowData = self.__createRowItemData(location=location, index=index, data=data)
        flatcache = self.__createRowObject(newRowData)
        self.__appendRow(flatcache)

    @Debugger
    @validate_arguments(config=dict(arbitrary_types_allowed=True))
    def __appendRow(self, Flat_CacheItem:Flat_Cache):

        self._storage.append(Flat_CacheItem)

        Logger.info("Height: {}".format(self.height()))
        self.__increaseHeight()
        Logger.info("Height: {}".format(self.height()))

    @Debugger
    @validate_arguments #data can be anything, don't validate type
    def __createRowItemData(self, location:str=None, index:int=None, data=None):
        
        Validation.validation_oneIsNotNone(index, location)

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


    @Debugger
    @validate_arguments
    def deleteRow(self, row:int):
        self.validation_rowExists(row)
        
        raise Exception("needs to be tested")
        row = self._storage.pop(row)
        Logger.info("deleting: {}".format(row))
        self.__decreaseHeight()


    @Debugger
    @validate_arguments
    def unsetRow(self, row:int):
        self.validation_rowExists(row)
        raise Exception("needs to be tested")
        Logger.info("unsetting row: {}".format((row)))
        # call the Flat_Cache unset method for this row
        self._storage[row] = self.__createRowObject(None)

    #### 
    #
    # Column Methods
    #
    ####

    # Delete the column, but first make sure we have all the correct data that we need in order to properly
    #   remove the column from every row in the dataset
    @Debugger
    @validate_arguments
    def deleteColumn(self, index:int=None, location:str=None):
        raise Exception("needs to be tested")

        Validation.validation_oneIsNotNone(index, location)

        location, index = self.__getLocationIndex(location=location, index = index)

        if not self.locationExists(location):
            raise Nested_Cache_Exception("Location '{}' doesn't exist, to add it use addColumn(location={})".format(location, location))

        #finally, delete the header from storage
        self.__removeHeaderIndexes(index=index, location=location)

    @Debugger
    @validate_arguments
    # remove both the index and location from all rows in the sheetData
    def __removeHeaderIndexes(index:int, location:str):

        Validation.validation_oneIsNotNone(index, location)
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
    @Debugger
    @validate_arguments # no need to test location exists, return None if the data doesn't exist at row or location
    def get_row_item(self, row:Annotated[int, Field(gt=0)], location:str):
        if self.rowExists(row):
            data = self.__getItem(row=row, location=location)

            if None == data:
                return None
            return data['data']
        else:
            return None

    @Debugger
    @validate_arguments #don't validate row or location, we want to return None if they don't exist
    def __getItem(self, row:int, location:str):

        if self.rowExists(row):
            return self.__getRawRow(row).get_at_location(location)
        else:
            return None


    @Debugger
    @validate_arguments
    def deleteItem(self, row:Annotated[int, Field(gt=0)], location:str=None, index:int=None):
        raise Exception("needs to be tested")

        self.validation_rowExists(row)
        Validation.validation_oneIsNotNone(index, location)

        if 0 == row:
            raise Nested_Cache_Exception("You cannot delete from row[0], if you want to modify locations, use deleteColumn()")
        
        # if this is true, then we have index bc we passed validation. So, get the location
        if None == location:
            location, index == self.__getLocationIndex(index)

        self._storage[row].delete_at_location(location)
        self._storage[row].delete_at_location(index)


    @Debugger
    @validate_arguments #data can be anything
    def update_row_item(self, row:int, index:int=None, location:str=None, data=None):
        self.validation_rowExists(row)
        Validation.validation_oneIsNotNone(index, location)

        location, index = self.__getLocationIndex(location=location, index = index)

        # create the data for the rows
        rowData = self.__createRowItemData(location=location, index=index, data=data)

        # do the manual update, we are not replacing the row, only the data in these locations
        self._storage[row].update_at_location(location=location, data=rowData[index])
        self._storage[row].update_at_location(location=index, data=rowData[location])


    @Debugger
    @validate_arguments
    def unset_row_item(self, row, location:str=None, index:int=None):
        raise Exception("needs to be tested")
        
        self.validation_rowExists(row)
        Validation.validation_oneIsNotNone(index, location)

        self._storage[row].unset_at_location(location)
        self._storage[row].unset_at_location(index)

    ####
    #
    # Meta
    #
    ####

    # nuclear option
    @Debugger
    def clear_all(self):
        raise Exception("needs to be tested")
        self._storage = []

    @Debugger
    def height(self):
        # decrement bc the user doesn't need to know we are overloading the 0th row
        return self._height
    
    @Debugger
    @validate_arguments
    def __increaseHeight(self, increaseBy:Annotated[int, Field(gt=0)] = 1):
        if 0 > increaseBy:
            raise Nested_Cache_Exception("You can only increase height by positive integers")
        self._height += increaseBy


    @Debugger
    @validate_arguments
    def __decreaseHeight(self, decreaseBy:Annotated[int, Field(gt=0)] = 1):
        if 0 > decreaseBy:
            raise Nested_Cache_Exception("You can only decrease height by positive integers")
        self._height -= decreaseBy

    @Debugger
    def width(self):
        # in order to avoid getting yelled at by row(0) check validations, use the _locations arr for width
        return len(self.__getLocations())

    @Debugger
    def __str__(self) -> str:
        output = "Nested_Cache: \n"
        return str(self.getAsListOfDicts())


    @Debugger
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

    @Debugger
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

    @Debugger
    @validate_arguments
    def validation_locationExists(self, location:str):
        Logger.validation_method_debug("validation_locationExists", locals())
        if not self.locationExists(location):
            raise Nested_Cache_Exception("Location '{}' doesn't exist, to add it use addLocation(location)".format(location))
        return True


    @Debugger
    @validate_arguments
    def validation_indexExists(self, index:int):
        Logger.validation_method_debug("validation_indexExists", locals())
        if not self.locationExists(index):
            raise Nested_Cache_Exception("Index '{}' doesn't exist, to add it use addLocation(location)".format(index))
        return True


    @Debugger
    @validate_arguments
    def validation_rowExists(self, row:int):
        Logger.validation_method_debug("validation_rowExists", locals())
        if not self.rowExists(row):
            raise Nested_Cache_Exception("Row {} doesn't exist, to add it use appendRow()".format(row))
        return True