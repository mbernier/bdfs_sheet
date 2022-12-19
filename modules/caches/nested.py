from modules.cache import BdfsCache
from modules.caches.flat import Flat_Cache
from modules.caches.exception import Nested_Cache_Exception, Flat_Cache_Exception
from modules.decorator import Debugger
from modules.logger import Logger, logger_name
from typing import Union
from pydantic import Field, validate_arguments
from pydantic.typing import Annotated


# effectively a list of Flat Caches, allows for better control over the data and how it is stored/accessed
# Rules:
#    empty rows are None, not new Flat_Cache()
#    Flat_Cache items will be setup with the same headers every time, if data has unexpected headers:
    # options: 
    #     Fail hard
    #     return the unexpected headers
#   flat cache data is: location: {position: , data: } // index can be inferred from the position in the Flat_Cache item
#   locations flat cache is the same thing, it's the first row

logger_name.name = "Nested_Cache"

class Nested_Cache(BdfsCache):
    _height = 0

    _storage: list = []

    _locations:list = None

    # locations are the indexes for the Flat_Cache
    #   We will make sure that they are setup properly as the caches are built
    @Debugger
    def __init__(self, locations: list = [], data:list = []):        
        self._storage = []
        self._locations = locations
        self.__setup(locations, data)


    ####
    #
    # Setup methods
    #
    ####
    @Debugger
    def __setup(self, locations:list, data:list):
        for rowData in data:
            self.insert(rowData)

    ####
    #
    # Data Row Functionality
    #
    ####

    # check if the row exists already
    @Debugger
    @validate_arguments
    def rowExists(self, row:Annotated[int, Field(gt=-1)]):
        # This method we are in exists to validate rows... so we are OK to check any row, to see if it exists
        return (0 <= row < self.height())


    @Debugger
    @validate_arguments
    def getRowAsList(self, row:Annotated[int, Field(gt=-1)]):
        self.validation_rowExists(row)
        obj = []
        row = self.select(row)
        return row.getAsList()


    @Debugger
    @validate_arguments
    def getRowAsDict(self, row:Annotated[int, Field(gt=-1)]):
        self.validation_rowExists(row)
        obj = {}
        row = self.select(row)
        return row.getAsDict()


    # assumes the row, location already exist in the data
    @Debugger
    @validate_arguments # it is valid for data == None here, and data can be any type
    def update(self, row:Annotated[int, Field(gt=-1)], position:Union[int,str], data=None):
        self.validation_rowExists(row)
        self.validation_locationExists(position)

        try:
            self._storage[row].update(position=position, data=data)
        except Flat_Cache_Exception:
            raise Nested_Cache_Exception("There is already data at row:{} position:{}, to change this data use update(row, location/index, data)".format(row, position))

        

    @Debugger
    @validate_arguments
    def insert(self, rowData:list=None):
        newRow = Flat_Cache(self.getLocations(), rowData)
        self._storage.append(newRow)
        Logger.info("Height: {}".format(self.height()))
        self.__increaseHeight()


    @Debugger
    @validate_arguments
    def deleteRow(self, row:Annotated[int, Field(gt=-1)]):
        self.validation_rowExists(row)
        row = self._storage.pop(row)
        Logger.info("deleting Row: {}".format(row))
        self.__decreaseHeight()

    #### 
    #
    # Column Methods
    #
    ####

    @Debugger
    def getLocations(self) -> list:
        return self._locations


    # do we know about this location?
    @Debugger
    @validate_arguments
    def locationExists(self, position: Union[int,str])->Union[int,str]:
        return position in self._locations


    @Debugger
    @validate_arguments
    def insert_location(self, location:str, index:int=None):
        if self.locationExists(location):
            raise Nested_Cache_Exception(f"Column Name: '{location}' already exists")

        if self.height() > 0:
            for row in range(0, self.height()):
                self._storage[row].insert_location(position=location, index=index)

        # Update the _locations list
        if None == index:
            #put it at the end
            self._locations.append(location)
        else:
            #put it at the right location
            self._locations.insert(index, location)


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
    def select(self, row:Annotated[int, Field(gt=-1)]=None, position:Union[int,str] = None):
        self.validation_rowExists(row)

        if None == row:
            # select all
            return self.getAsListOfDicts()
        
        # if position is None, will return the row, if it's set it will return the data at that position
        data = self._storage[row].select(position=position)
        return data


    @Debugger
    @validate_arguments #data can be anything, forcing
    def update(self, row:Annotated[int, Field(gt=-1)], position:Union[int,str], data=None):
        self.validation_rowExists(row)

        # do the manual update, we are not replacing the row, only the data in these locations
        self._storage[row].update(position=position, data=data)

    ####
    #
    # Meta
    #
    ####

    # nuclear option
    @Debugger
    def clear_all(self):
        for row in range(0, self.height()):
            self._storage[row].clear_all()


    @Debugger
    def height(self):
        # decrement bc the user doesn't need to know we are overloading the 0th row
        return self._height


    @Debugger
    @validate_arguments
    def __increaseHeight(self, increaseBy:Annotated[int, Field(gt=-1)] = 1):
        if 0 > increaseBy:
            raise Nested_Cache_Exception("You can only increase height by positive integers")
        self._height += increaseBy


    @Debugger
    @validate_arguments
    def __decreaseHeight(self, decreaseBy:Annotated[int, Field(gt=-1)] = 1):
        if 0 > decreaseBy:
            raise Nested_Cache_Exception("You can only decrease height by positive integers")
        self._height -= decreaseBy


    @Debugger
    def width(self) -> int:
        return self._storage[0].size()


    @Debugger
    def __str__(self) -> str:
        output = "Nested_Cache: \n"
        return str(self.getAsListOfDicts())


    @Debugger
    def getAsListOfLists(self) -> list:
        output = []
        for rowindex, row in enumerate(self._storage):
            rowAsList = row.getAsList()
            output.append(rowAsList)
        return output


    @Debugger
    def getAsListOfDicts(self) -> list[dict]:
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
    def validation_locationExists(self, location:str) -> bool:
        Logger.validation_method_debug("validation_locationExists", locals())
        if not self.locationExists(location):
            raise Nested_Cache_Exception("Location '{}' doesn't exist, to add it use addLocation(location)".format(location))
        return True


    @Debugger
    @validate_arguments
    def validation_indexExists(self, index:int) -> bool:
        Logger.validation_method_debug("validation_indexExists", locals())
        if not self.locationExists(index):
            raise Nested_Cache_Exception("Index '{}' doesn't exist, to add it use addLocation(location)".format(index))
        return True


    @Debugger
    @validate_arguments
    def validation_rowExists(self, row:Annotated[int, Field(gt=-1)]) -> bool:
        Logger.validation_method_debug("validation_rowExists", locals())
        if not self.rowExists(row):
            raise Nested_Cache_Exception("Row {} doesn't exist, to add it use insert(rowData)".format(row))
        return True