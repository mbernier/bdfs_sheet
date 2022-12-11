import sys, pydantic
from collections import OrderedDict
from enum import Enum, IntEnum
from modules.cache import BdfsCache
from modules.caches.flat import Flat_Cache
from modules.caches.nested_cache.rows.data import Nested_Cache_Rows_Data
from modules.caches.nested_cache.rows.location import Nested_Cache_Rows_Location
from modules.caches.exception import Nested_Cache_Exception, Flat_Cache_Exception
from modules.config import config
from modules.decorator import Debugger
from modules.logger import Logger
from modules.validation import Validation
from typing import Union
from pprint import pprint
from pydantic import Field, validator, validate_arguments
from pydantic.typing import Annotated


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
        for rowData in data:
            self.appendRow(rowData)


    ####
    #
    # Location Row functionality
    #
    ####

    @Debugger
    # used in order to setup the locations row, so that we can check against it in the future
    def __addLocations(self, locations:list):
        locationRow = Nested_Cache_Rows_Location(locations)

        self.__setLocationRow(locationRow)


    @Debugger
    def __getLocations(self) -> list:
        #_storage[0] is our locations Cache
        return self._storage[0].getLocationKeys()


    # create row[0] from the Locations Row, setup the OrderedDict for Location Headers
    @Debugger
    def __setLocationRow(self, locationRow:Nested_Cache_Rows_Location):
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
        locationData = self._storage[0].get_at(position)
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



    # uses the dict get() to return None or the value if the item exists
    #   returns the Flat_Cache object in this location
    @Debugger
    def getRow(self, row:Annotated[int, Field(gt=0)], asObj:str_list="list"):
        if self.rowExists(row):
            return self._storage[row]
        else:
            return None

    @Debugger
    @validate_arguments
    def getRowAsList(self, row:Annotated[int, Field(gt=0)]):
        self.validation_rowExists(row)
        obj = []
        row = self.getRow(row)
        for location in self.__getLocations():
            positionalData = row.getAsList(position=location)
            obj.append(positionalData)
        return obj

    @Debugger
    @validate_arguments
    def getRowAsDict(self, row:Annotated[int, Field(gt=0)]):
        self.validation_rowExists(row)
        obj = {}
        row = self.getRow(row)
        for location in self.__getLocations():
            positionalData = row.getAsDict(location)
            obj.update(positionalData)
        return obj


    # assumes the row, location already exist in the data
    @Debugger
    @validate_arguments # it is valid for data == None here, and data can be any type
    def set_row_item(self, row:Annotated[int, Field(gt=0)], position:str, data=None):
        self.validation_rowExists(row)
        self.validation_locationExists(position)
        self.__setRow(row=row, position=position, data=data)


    @Debugger
    @validate_arguments #data can be anything, don't validate
    def __setRow(self, row:Annotated[int, Field(gt=0)], position:Union[int,str], data=None):

        self.validation_rowExists(row)

        try:
            self._storage[row].set_at(position=position, data=data)
        except Flat_Cache_Exception:
            raise Nested_Cache_Exception("There is already data at row:{} position:{}, to change this data use update(row, location/index, data)".format(row, position))


    @Debugger
    @validate_arguments
    def appendRow(self, rowData:list=None):

        newRow = self.createRowFromData(rowData)
        self.__appendRow(newRow)

    # created outside of appendRow, so it could be used in unsetRow as well
    @Debugger
    @validate_arguments
    def createRowFromData(self, rowData:list=None):
        newRow = Nested_Cache_Rows_Data()
        
        locations = self.__getLocations()

        for index, location in enumerate(locations):
            cellData = None
            if None != rowData:
                if index in rowData:
                    cellData = rowData[index]
            # add based on the index, bc
            newRow.add_at(location=location, index=index, data=cellData)

        return newRow


    @Debugger
    @validate_arguments(config=dict(arbitrary_types_allowed=True))
    def __appendRow(self, row_data_obj:Nested_Cache_Rows_Data):

        self._storage.append(row_data_obj)

        Logger.info("Height: {}".format(self.height()))
        self.__increaseHeight()
        Logger.info("Height: {}".format(self.height()))


    @Debugger
    @validate_arguments
    def deleteRow(self, row:Annotated[int, Field(gt=0)]):
        self.validation_rowExists(row)
        
        raise Exception("needs to be tested")
        row = self._storage.pop(row)
        Logger.info("deleting: {}".format(row))
        self.__decreaseHeight()


    @Debugger
    @validate_arguments
    def unsetRow(self, row:Annotated[int, Field(gt=0)]):
        self.validation_rowExists(row)
        
        raise Exception("needs to be tested")
        
        Logger.info("unsetting row: {}".format((row)))

        # call the Flat_Cache unset method for this row
        self._storage[row] = self.createRowFromData()

    #### 
    #
    # Column Methods
    #
    ####

    # Delete the column, but first make sure we have all the correct data that we need in order to properly
    #   remove the column from every row in the dataset
    @Debugger
    @validate_arguments
    def deleteColumn(self, position:Union[int,str]):
        raise Exception("needs to be tested")

        location, index = self.__getLocationIndex(position=position)

        if not self.locationExists(position):
            raise Nested_Cache_Exception("Location '{}' doesn't exist, to add it use addColumn(location={})".format(location, location))

        #finally, delete the header from storage
        self.__removeHeaderIndexes(position)


    @Debugger
    @validate_arguments
    # remove both the index and location from all rows in the sheetData
    def __removeHeaderIndexes(position:Union[int,str]):

        raise Exception("needs to be tested")
        
        # delete the header from every single row in the storage
        for row in range(0, self.height()):
            self._storage[row].remove_position(position=position)


    ####
    #
    # Individual Item Methods
    #
    ####
    # uses the dict get() to return None or the value if the item exists
    @Debugger
    @validate_arguments # no need to test location exists, return None if the data doesn't exist at row or location
    def get_row_item(self, row:Annotated[int, Field(gt=0)], position:Union[int,str]):
        if self.rowExists(row):
            data = self.__getItem(row=row, position=position)

            if None == data:
                return None
            return data['data']
        else:
            return None


    @Debugger
    @validate_arguments #don't validate row or location, we want to return None if they don't exist
    def __getItem(self, row:Annotated[int, Field(gt=0)], position:Union[int,str]):

        if self.rowExists(row):
            return self.getRow(row).get_at(position)
        else:
            return None


    @Debugger
    @validate_arguments
    def unset_row_item(self, row:Annotated[int, Field(gt=0)], position:Union[int,str]):

        self.validation_rowExists(row)

        self._storage[row].unset_at(position)


    @Debugger
    @validate_arguments #data can be anything, forcing
    def update_row_item(self, row:Annotated[int, Field(gt=0)], position:Union[int,str], data):

        self.validation_rowExists(row)

        # do the manual update, we are not replacing the row, only the data in these locations
        self._storage[row].update_at(position=position, data=data)

    ####
    #
    # Meta
    #
    ####

    # nuclear option
    @Debugger
    def clear_all(self):
        self._storage[row].clear_all()


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
        output = []
        for rowindex, row in enumerate(self._storage):
            rowAsList = row.getAsList()
            output.append(rowAsList)
        return output

    @Debugger
    def getAsListOfDicts(self):
        output = []
        for index, row in enumerate(self._storage):
            rowAsDict = row.getAsDict()
            output.append(rowAsDict)
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
    def validation_rowExists(self, row:Annotated[int, Field(gt=0)]):
        Logger.validation_method_debug("validation_rowExists", locals())
        if not self.rowExists(row):
            raise Nested_Cache_Exception("Row {} doesn't exist, to add it use appendRow()".format(row))
        return True