import sys
from modules.cache import Bdfs_Cache
from modules.caches.flat import Flat_Cache, UPDATE_TIMESTAMP_KEY
from modules.caches.exception import Nested_Cache_Exception, Flat_Cache_Exception
from modules.decorator import Debugger
from modules.helper import Helper
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


class Nested_Cache(Bdfs_Cache):
    _height = 0

    _storage: list = []

    _locations:list = []
    uniques = []
    uniqueField = None
    uniqueFieldIndex = None
    headerRowOnly = False
    
    # locations are the indexes for the Flat_Cache
    #   We will make sure that they are setup properly as the caches are built
    @Debugger
    def __init__(self, data:list[dict]=None, uniqueField:str=None):        
        self._storage = []
        self.uniques = []
        self.uniqueField = None
        self.uniqueFieldIndex = None
        self.uniqueField = uniqueField
        self.headerRowOnly = False
        # set up the initial data
        self.__setup(data)
        
        # verify the unique field is in the locations list
        self.__setupUniqueIndex()
        

    ####
    #
    # Setup methods
    #
    ####
    @Debugger
    def __setup(self, data:list[dict]=None):
        if None != data:
            for rowData in data:
                self.insertRow(rowData=rowData)


    @Debugger
    def __setupUniqueIndex(self):
        if self.height() > 0:
            if None != self.uniqueField and 0 < len(self.getLocations()):
                self.uniqueFieldIndex = self.getLocations().index(self.uniqueField)

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
        return list(row.values())


    @Debugger
    @validate_arguments
    def getRowAsDict(self, row:Annotated[int, Field(gt=-1)]):
        self.validation_rowExists(row)
        obj = {}
        return self.select(row)


    # uses the dict get() to return None or the value if the item exists
    @Debugger
    @validate_arguments # no need to test location exists, return None if the data doesn't exist at row or location
    def select(self, row:Annotated[int,Field(gt=-1)]=None, position:Union[int,str]=None, unique=None, update_timestamp=True):
        if None != unique:
            if None != row:
                raise Nested_Cache_Exception("Passing row and unique together is poor form, pick one")
            # we want the row based on the unique value
            row = self.__getRowByUnique(uniqueData=unique)
            data = self._storage[row].select(position=position, update_timestamp=update_timestamp)
        else: 
            if None == row:
                # select all
                return self.getAsListOfDicts(update_timestamp=update_timestamp)
            else: 
                # a row was passed, validate it
                self.validation_rowExists(row)

            # if position is None, will return the row, if it's set it will return the data at that position
            data = self._storage[row].select(position=position, update_timestamp=update_timestamp)
        return data


    @Debugger
    @validate_arguments
    def update(self, row:Annotated[int, Field(gt=-1)], position:Union[int,str], data=None):

        self.__handleHeaderRowOnly(row)

        self.validation_rowExists(row)

        if position == self.uniqueField:
            self.__replaceUniqueItem(data, row)

        # do the manual update, we are not replacing the row, only the data in these locations
        self._storage[row].update(position=position, data=data)


    @Debugger
    @validate_arguments
    def insert(self):
        raise Nested_Cache_Exception("There is no Nested_Cache.insert() method, maybe you meant insertRow()?")
        
    ####
    #
    # Row Actions
    #
    ####

    @Debugger
    @validate_arguments
    def selectAll(self, update_timestamp=True):
        # select all
        return self.getAsListOfDicts(update_timestamp=update_timestamp)


    @Debugger
    @validate_arguments # no need to test location exists, return None if the data doesn't exist at row or location
    def selectRow(self, row:Annotated[int,Field(gt=-1)]=None, update_timestamp:bool=True):
        # a row was passed, validate it
        self.validation_rowExists(row)

        # if position is None, will return the row, if it's set it will return the data at that position
        data = self._storage[row].select(position=None, update_timestamp=update_timestamp)
        return data


    @Debugger
    @validate_arguments # no need to test location exists, return None if the data doesn't exist at row or location
    def selectRowByUnique(self, unique:str=None, update_timestamp:bool=True):
        # we want the row based on the unique value
        try:
            row = self.__getRowByUnique(uniqueData=unique)
            data = self._storage[row].select(position=None, update_timestamp=update_timestamp)
        except Nested_Cache_Exception as err:
            data = None # we didn't find a unique row
        
        return data

    # given some data, identify whether it should be inserted or updated, based on the uniqueField
    @Debugger
    @validate_arguments
    def putRow(self, rowData:dict):
        if None != self.uniqueField:
            uniqueData = rowData[self.uniqueField]
            if self.isUnique(uniqueData):
                # insert
                self.insertRow(rowData)
            else:
                row = self.__getRowByUnique(uniqueData)
                # update
                self.updateRow(row=row,rowData=rowData)
        else:
            # if there is no unique constraint, do an insert
            self.insertRow(rowData)


    @Debugger
    @validate_arguments
    def insertRow(self, rowData:dict=None):
        if rowData == {}: # we shouldn't insert anything, bc it's empty
            return

        if self.height() > 0:
            # only do this after the first row is set up, bc first row will have locations passed
            locations = self.getLocations() # returns only the locations, not the timestamps

            newRow = Flat_Cache(rowData)
            newRowLocations = newRow.getKeys(keyType=str) # will not return any timestamps, only raw keys

            newRowKeys = newRow.getAsDict().keys()

            # let's compare the raw keys to raw keys, ignoring timestamps that are handled by Flat_Cache
            if len(newRowLocations) == len(locations):
                # the keys are the same, now...do we have unique columns?
                self.__handleUniqueRowLogic(newRow)
            else:
                locationsHas = Helper.listDiff(locations, newRowKeys, ignoreWith=UPDATE_TIMESTAMP_KEY)
                rowDataHas = Helper.listDiff(newRowKeys, locations, ignoreWith=UPDATE_TIMESTAMP_KEY)

                if [] != locationsHas:
                    raise Nested_Cache_Exception(f"rowData is missing {locationsHas}")

                if [] != rowDataHas:
                    raise Nested_Cache_Exception(f"rowData contains extra locations: {rowDataHas}")
                
                raise Nested_Cache_Exception(f"rowData was expected to be of length {len(locations)} but {len(newRowKeys)} was passed")
        else:
            # we are in row one, whatever keys we are passed are what we're going to compare to going forward...
            newRow = Flat_Cache(rowData)
            
            self.__handleUniqueRowLogic(newRow)


    @Debugger
    @validate_arguments
    def __handleUniqueRowLogic(self, newRow):
        if None != self.uniqueField: #otherwise, we add the entire row to the uniques - not great
            # we never want None in uniques, bc that could be the header row and if it's not then we should catch this earlier
            if None != newRow.select(position=self.uniqueField):
                self.__updateUniques(newRow.select(position=self.uniqueField))
        
        if self.headerRowOnly == True:
            # we have a placeholder row in the header and we now have a suitable replacement row
            self._storage = [newRow] # first row
            
            if False == newRow.isEmpty(): # The new row has more than None stored
                self.headerRowOnly = False

        else:
            self._storage.append(newRow)
        
        self.__increaseHeight()


    @Debugger
    @validate_arguments
    def deleteRow(self, row:Annotated[int, Field(gt=-1)]):
        self.validation_rowExists(row)
        if self.headerRowOnly == True:
            raise Nested_Cache_Exception("There is only an empty header row, you shouldn't delete that")

        row = self._storage.pop(row)
        Logger.info("Row {} deleted".format(row))

        self.__removeUnique(row.select(self.uniqueField))        
        self.__decreaseHeight()
    

    @Debugger
    @validate_arguments
    def deleteRowWhere(self, column:str, value):
        for row in reversed(range(0, self.height())):
            if value == self._storage[row].select(position=column):
                self.deleteRow(row)


    # replace the current row with different data
    @Debugger
    @validate_arguments
    def updateRow(self, row:Annotated[int, Field(gt=-1)], rowData:dict):
        self.validation_rowExists(row)
        self.__handleHeaderRowOnly(row)

        locations = self.getLocations()

        if type(rowData) is list:
            rowData = Helper.listsToDict(self.getLocations(), rowData)
        
        newRow = Flat_Cache(rowData)

        # let's let Flat_Cache do it's thing, handling the keys and the timestamps, then let's ask how many columns we have
        if len(newRow.getKeys(keyType=str)) != len(locations):
            raise Nested_Cache_Exception(f"rowData was expected to be of length {len(locations)} but {len(newRow.getKeys(keyType=str))} was passed")
        
        newRowUnique = newRow.select(position=self.uniqueField)

        # if we care about unique Fields check that the new uniqueField hasn't already been entered
        if None != self.uniqueField:
            self.__replaceUniqueItem(newRowUnique, index=row)
        
        self._storage[row] = newRow

    #### 
    #
    # Column Methods
    #
    ####

    @Debugger
    def getLocations(self, update_timestamp=False) -> list:
        locations = []
        if 0 < self.height():
            locations = self._storage[0].getKeys()
            if True == update_timestamp:
                timestamps = self._storage[0].getTimestampKeys()
                locations += timestamps
        # all of the methods keep the Flat_Cache storages aligned, so this will be the same for all of them
        return locations


    # do we know about this location?
    @Debugger
    @validate_arguments
    def locationExists(self, position: Union[int,str]) -> bool:
        return (position in self.getLocations())


    @Debugger
    @validate_arguments
    def insert_location(self, location:str, index:int=None):
        
        # we have our first location, so we need to add it
        if self.height() == 0:
            # this inserts a new row with only this location, it calls __setupUniqueIndex() so we don't 
            #   need to call it here
            self.headerRowOnly = True

            self.insertRow({location: None})
            
        elif self.height() > 0:
            for row in range(0, self.height()):
                self._storage[row].insert_location(position=location, index=index)
        
            # things might have moved around, go get the index of the unique field just in case
            self.__setupUniqueIndex()


    # ask Flat Cache to delete the column
    @Debugger
    @validate_arguments
    def deleteColumn(self, position:StrictStr):
        if position == self.uniqueField:
            raise Nested_Cache_Exception(f"You cannot delete the unique column '{self.uniqueField}'")

        if 0 == self.height():
            raise Nested_Cache_Exception(f"Cannot delete a column from an empty Row")

        for row in range(0, self.height()):
            self._storage[row].delete_location(position) 


    # ask Flat Cache to delete each column
    @Debugger
    @validate_arguments
    def deleteColumns(self, positions:list[StrictStr]):

        if self.uniqueField in positions:
            raise Nested_Cache_Exception(f"Unique column '{self.uniqueField}' was passed to deleteColumns but it cannot be deleted")

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

        # get each row of data and recreate it, using the new location order
        for row in range(0, self.height()):
            rowData = self._storage[row] # get the old row, so we can fetch the data

            # rather than try to move the data around, just recreate it
            dataToLoad = []
            #load the data into dataToLoad in the same order as the columns
            for column in newColumns:
                if rowData.positionIsTimestamp(column):
                    # get the specific column's timestamp
                    dataToLoad.append(rowData.getUpdateTimestamp(column))
                else:
                    # get the data from the old row and order it in the new list
                    dataToLoad.append(rowData.select(column))
                

            # load all the data at once, so we can add the timestamps in
            self._storage[row] = Flat_Cache(Helper.listsToDict(newColumns, dataToLoad))
        
        # make sure we reset the uniqueIndex, just in case it moved
        self.__setupUniqueIndex()



    ####
    #
    # Meta Methods
    #
    ####

    # nuclear option
    @Debugger
    def clear_all(self):
        for row in range(0, self.height()):
            self._storage[row].clear_all()
        self.uniques = [] # no data, no uniques
    
    # reset all the data to nothing
    @Debugger
    def deleteAllData(self):
        # if we had a headerRowOnly, we don't any longer
        self.headerRowOnly = False
        self._storage = []
        self._height = 0
        Logger.info("All data in Nested_Cache has been deleted")


    @Debugger
    def height(self):
        # decrement bc the user doesn't need to know we are overloading the 0th row
        return self._height


    @Debugger
    @validate_arguments
    def __handleHeaderRowOnly(self, row:Annotated[int, Field(gt=-1)]):
        if self.headerRowOnly == True and row ==0:
            self.headerRowOnly == False

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
    @validate_arguments
    def __updateUniques(self, uniqueData, index:int=None):
        if None == uniqueData:
            raise Nested_Cache_Exception("None is not a valid value for uniques in Nested_Cache")
        
        if True == self.isUnique(uniqueData):
            if None != index:
                # we have this at a specific index, so add it
                self.uniques.insert(index, uniqueData)
            else:
                # we are adding it to the end
                self.uniques.append(uniqueData)
            return True
        raise Nested_Cache_Exception(f"'{uniqueData}' for position '{self.uniqueField}' violates uniqueness")
    

    @Debugger
    @validate_arguments
    def __replaceUniqueItem(self, uniqueData, index:int):
        # get the old uniqueValue
        oldUnique = self.select(position=self.uniqueField, row=index)

        if oldUnique != uniqueData:

            if True == self.isUnique(uniqueData):
                
                # fail if the data is different and the data is already in the uniques list
                self.__removeUnique(oldUnique)
                
                self.uniques.insert(index, uniqueData)
                return True
            else:
                raise Nested_Cache_Exception(f"'{uniqueData}' for position '{self.uniqueField}' violates uniqueness")        


    @Debugger
    @validate_arguments
    def __removeUnique(self, uniqueData):
        if None != self.uniqueField and uniqueData in self.uniques:
            self.uniques.remove(uniqueData)


    @Debugger
    @validate_arguments
    def __getRowByUnique(self, uniqueData):
        if None == self.uniqueField:
            raise Nested_Cache_Exception("No unique Field is set, so you cannot select a row by uniqueField")
        if uniqueData in self.uniques:
            return self.uniques.index(uniqueData)
        raise Nested_Cache_Exception(f"'{uniqueData}' is not in the uniques list, you should try...except this error and handle it accordingly")


    @Debugger
    @validate_arguments
    def isUnique(self, uniqueData):
        if None == self.uniqueField: # we don't have a uniqueness constraint
            return True

        if uniqueData in self.uniques:
            return False
        return True

    @Debugger
    def width(self) -> int:
        return self._storage[0].size()


    @Debugger
    @validate_arguments
    def __str__(self, update_timestamp:bool=True) -> str:
        output = "Nested_Cache: \n"
        return str(self.getAsListOfDicts(update_timestamp=update_timestamp))


    @Debugger
    def getUniques(self) -> list:
        return self.uniques.copy()


    @Debugger
    @validate_arguments
    def getAsListOfLists(self,update_timestamp:bool=True) -> list[list]:
        output = []
        for rowindex, row in enumerate(self._storage):
            rowAsList = row.getAsList(update_timestamp=update_timestamp)
            output.append(rowAsList)
        return output


    @Debugger
    @validate_arguments
    def getAsListOfDicts(self,update_timestamp:bool=True) -> list[dict]:
        output = []
        for index, row in enumerate(self._storage):
            rowAsDict = row.getAsDict(update_timestamp=update_timestamp)
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
            raise Nested_Cache_Exception("Row {} doesn't exist, to add it use insertRow(rowData)".format(row))
        return True