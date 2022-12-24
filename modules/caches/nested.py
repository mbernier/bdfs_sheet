import sys
from modules.cache import BdfsCache
from modules.caches.flat import Flat_Cache
from modules.caches.exception import Nested_Cache_Exception, Flat_Cache_Exception
from modules.decorator import Debugger
from modules.logger import Logger
from typing import Union
from pydantic import Field, validate_arguments, StrictStr,ConstrainedStr
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


class Nested_Cache(BdfsCache):
    _height = 0

    _storage: list = []

    _locations:list = []

    # locations are the indexes for the Flat_Cache
    #   We will make sure that they are setup properly as the caches are built
    @Debugger
    def __init__(self, locations: list = [], data:list = []):        
        self._storage = []
        self._locations = locations
        if 0 == len(locations):
            if 0 < len(data): # we have data, but we don't have headers
                raise Nested_Cache_Exception(f"Data {data} was sent with no headers")
        else:
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

    # replace the current row with different data
    @Debugger
    @validate_arguments
    def updateRow(self, row:Annotated[int, Field(gt=-1)], rowData:list):
        self.validation_rowExists(row)
        self._storage[row] = Flat_Cache(self.getLocations(), rowData)

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


    # ask Flat Cache to delete the column
    @Debugger
    @validate_arguments
    def deleteColumn(self, position:StrictStr):
        for row in range(0, self.height()):
            self._storage[row].delete_location(position)
        
        # remove it from the locations cache
        self._locations.remove(position)


    # ask Flat Cache to delete each column
    @Debugger
    @validate_arguments
    def deleteColumns(self, positions:list[StrictStr]):
        #this will make sure that if we have int values, we remove them in reverse order
            #  taking the highest ones first
        positions.sort()
        positions.reverse() #cannot be chained in sort, bc sort returns nothing
        for position in positions:
            self.deleteColumn(position)
    
    # this will cause Flat Cache to adjust indexes to the order of the locations passed
        # it does assume that the columns passed in the list already exist
    @Debugger
    @validate_arguments
    def reorderColumns(self, newColumns:list[str]):
        # we are going to override the current locations list
        self._locations = newColumns

        # get each row of data and recreate it, using the new location order
        for row in range(0, self.height()):
            rowData = self._storage[row] # get the old row, so we can fetch the data

            newData = [] # temp storage for the old row's data

            for column in newColumns:
                # get the data from the old row and order it in the new list
                newData.append(rowData.select(column))
            
            self.updateRow(row, newData)


    ####
    #
    # Individual Item Methods
    #
    ####
    # uses the dict get() to return None or the value if the item exists
    @Debugger
    @validate_arguments # no need to test location exists, return None if the data doesn't exist at row or location
    def select(self, row:Annotated[int, Field(gt=-1)]=None, position:Union[int,str] = None, updated_timestamp=False):
        self.validation_rowExists(row)

        if None == row:
            # select all
            return self.getAsListOfDicts(updated_timestamp=updated_timestamp)
        
        # if position is None, will return the row, if it's set it will return the data at that position
        data = self._storage[row].select(position=position, updated_timestamp=updated_timestamp)
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
    def __str__(self,updated_timestamp=False) -> str:
        output = "Nested_Cache: \n"
        return str(self.getAsListOfDicts(updated_timestamp=updated_timestamp))


    @Debugger
    def getAsListOfLists(self,updated_timestamp=False) -> list:
        output = []
        for rowindex, row in enumerate(self._storage):
            rowAsList = row.getAsList(updated_timestamp=updated_timestamp)
            output.append(rowAsList)
        return output


    @Debugger
    def getAsListOfDicts(self,updated_timestamp=False) -> list[dict]:
        output = []
        for index, row in enumerate(self._storage):
            rowAsDict = row.getAsDict(updated_timestamp=updated_timestamp)
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