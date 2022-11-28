import sys
from modules.cache import BdfsCache
from modules.caches.flat import FlatCache
from modules.caches.exception import NestedCacheException, FlatCacheException
from pprint import pprint
from collections import OrderedDict
from modules.decorators import debug, validate

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

    _storage: list[FlatCache] = []

    _locations = []

    # locations are the indexes for the FlatCache
    #   We will make sure that they are setup properly as the caches are built
    @debug
    @validate('locations', ['notNone'])
    @validate('data', ['notNone'])
    def __init__(self, locations, data):
        self.debug("__init__()")

        # # self.__validateData(data=locations, methodName="__init__()", dataName="locations")
        # # self.__validateData(data=data, methodName="__init__()")
        
        self._storage = []

        self.__setup(locations, data)


    ####
    #
    # Setup methods
    #
    ####
    @debug
    @validate('locations', ['notNone'])
    @validate('data', ['notNone'])
    def __setup(self, locations, data):
        self.__addLocations(locations)
        self.__addDataRowsWhereHeadersAreConfirmed(data)


    ####
    #
    # Locations functionality
    #
    ####
    @debug
    def __getLocations(self):
        return self._locations

    # create the available locations from a list
    @debug
    @validate('locations', ['notNone'])
    def __setLocations(self, locations):

        if [] != self.__getLocations():
            raise NestedCacheException("The locations are already set, we shoudn't reset them this way.")
        self._locations = locations


    # do we know about this location?
    @debug
    @validate('location', ['orExists:index', 'locationExists'])
    @validate('index', ['orExists:location'])
    def __locationExists(self, location=None, index=None):
        # self.debug("\t__locationExists(location={})".format(location))
        
        print(self.__getLocations())

        if None != location and location in self.__getLocations():
            return True
        elif None != index and index <= self.width() and None != self.__getLocations()[index]:
            return True
        return False

    @debug
    @validate('location', ['orExists:index', 'locationExists'])
    @validate('index', ['orExists:location'])
    def __getLocationIndex(self, location=None, index=None):
        # self.debug("\t__getLocationIndex(location={}, index={})", (location, index))
        # self.__validateLocationIndex(methodName="__getLocationIndex()", location=location, index=index)


        if None == location and None == index:
            raise NestedCacheException("__getLocationIndex() needs either location or index")

        if None == index:
            index = self.__getIndexFromLocation(location)

        if None == location:
            location = self.__getLocationFromIndex(index)

        self.debug("\t\tlocation={},index={}", (location, index))

        return location, index


    ####
    #
    # Rows
    #
    ####

    # check if the row exists already
    @debug
    @validate('row', ['notNone'])
    def __rowExists(self, row):
        # self.debug("\t__rowExists(row={})".format(row))
        # This method we are in exists to validate rows... so we are OK to check any row, to see if it exists
        #       # self.__validateRow(row=row, methodName="__rowExists()")
        return (0 <= row <= self.height())

    @debug
    @validate('locations', ['notNone'])
    # used in order to setup the locations row, so that we can check against it in the future
    def __addLocations(self, locations):
        # self.debug("\t__addLocations({})".format(locations))
        # self.__validateData(methodName="__addLocations()", data=locations, dataName="locations")

        newRow = self.__createLocationsRowItem(locations)
        self.debug("\t\tnewRow: {}".format(newRow))
        self.__setLocations(locations)
        self.appendRow(newRow)


    # formats the data for the locations row and returns a FlatCache item of that data
    @debug
    @validate('locations', ['notNone'])
    def __createLocationsRowItem(self, locations):
        # self.debug("\t__createLocationsRowItem({})".format(locations))
        # self.__validateData(methodName="__addLocations()", data=locations, dataName="locations")

        newRowData = {}
        for index, location in enumerate(locations):
            # we are going to overload this row with the location twice, so that we can pull it the same as the other
            #   data when we need it later, load up the location and index as indeces on the FlatCache - so we can look up and manage it from either direction
            #   now we can get to the data either way, regardless of which method we take to get there.
            rowDataItem = self.__createRowItemData(location=location, index=index, data=location)
            # merge the two dicts
            newRowData.update(rowDataItem)

        self.info("\t\tnewRowData: {}".format(newRowData))

        flatcache = self.__createRowObject(newRowData)

        self.debug("\t\tflatcache: {}".format(flatcache))

        return flatcache

    
    #Allows us to look up the location string by an index
    # this is used when we are looping through data and want to know what the header of the data is
    @debug
    @validate('index', ['notNone'])
    def __getLocationFromIndex(self, index):
        # self.debug("\t__getLocationFromIndex(index={})".format(index))
        # self.__validateLocationIndex(methodName="__setRow()", index=index, ignore="location")

        if not self.__locationExists(index=index):
            raise NestedCacheException("Index '{}' doesn't exist, to add it use addColumn(location=)".format(index))

        self.debug("\t\tlocations: {}".format(self.__getLocations()))
        return self.__getLocations()[index]

    # Looks into the locations array and then returns the index of the item in the array
    @debug
    @validate('location', ['notNone'])
    def __getIndexFromLocation(self, location):
        # self.debug("\t__getLocationFromIndex(location={})".format(location))
        # self.__validateLocationIndex(methodName="__getIndexFromLocation()", location=location, ignore="index")

        if not self.__locationExists(location=location):
            raise NestedCacheException("Location '{}' doesn't exist, to add it use addColumn(location={})".format(location, location))

        locationIndex = self.__getLocations().index(location)

        if None == locationIndex:
            raise NestedCacheException("The Location '{}' was not found".format(location))

        return locationIndex












' NEED TO FINISH decorators on these methods '
sys.exit()


















    # allows adding multiple rows of data at the same time.
    # do not use this unless you confirmed the headers match what is expected
    def __addDataRowsWhereHeadersAreConfirmed(self, data):
        self.debug("\t__addDataRowsWhereHeadersAreConfirmed({})".format(data))
        # self.__validateData(data=data, methodName="__addDataRowsWhereHeadersAreConfirmed()")
        for rowData in data:
            newRow = self.__createRowItem_FromData_WhereHeadersAreConfirmed(rowData)
            self.appendRow(newRow)


    # Adding a single row of data into the cache
    # cannot be accessed directly, because we want to guarantee that we have headers whenever data is added later
    # Only use this when you KNOW that the headers and the data match (like on an insert where headers are passed)
    def __createRowItem_FromData_WhereHeadersAreConfirmed(self, data):
        self.debug("\t__createRowItem_FromData_WhereHeadersAreConfirmed({})".format(data))
        # self.__validateData(data=data, methodName="__createRowItem_FromData_WhereHeadersAreConfirmed()")

        newRowData = {}
        for index, item in enumerate(data):
            # self.debug("__createRowItem_FromData_WhereHeadersAreConfirmed {}::{}".format(index, item))
            location, index = self.__getLocationIndex(index = index)
            # keeping the data in sync, whether we access by the location or the index
            rowDataItem = self.__createRowItemData(location=location, index=index, data=item)
            newRowData.update(rowDataItem)
        
        return self.__createRowObject(newRowData)


    # uses the dict get() to return None or the value if the item exists
    #   returns the FlatCache object in this location
    def getRow(self, row, asObj="list"):
        self.debug("getRow(row={})", row)
        # self.__validateRow(row=row, methodName="getRow()")

        if self.__rowExists(row):
            if asObj == "list":
                return self.__getRowAsList(row)
            elif asObj == "dict":
                return self.__getRowAsDict(row)
            else:
                raise NestedCacheException("Rows can be returned as list or dict, but not {}".format(asObj))
        else:
            return None

    def __getRowAsList(self, row):
        self.debug("__getRowAsList(row={})", row)
        # self.__validateRow(row=row, methodName="__getRowAsList()")
        obj = []
        row = self.__getRawRow(row)
        for location in self.__getLocations():
            positionalData = row.get(location)
            if None == positionalData:
                obj.append(None)
            else:
                obj.append(row.get(location)['data'])
        return obj

    def __getRowAsDict(self, row):
        self.debug("__getRowAsDict(row={})", row)
        # self.__validateRow(row=row, methodName="__getRowAsDict()")
        obj = {}
        row = self.__getRawRow(row)
        for location in self.__getLocations():
            positionalData = row.get(location)
            if None == positionalData:
                obj[location] = None
            else:
                obj[location] = row.get(location)['data']
        return obj


    def __getRawRow(self, row):
        self.debug("__getRawRow(row={})".format(row))
        # self.__validateRow(row=row, methodName="getRow()")

        if self.__rowExists(row):
            return self._storage[row]
        else:
            return None


    # assumes the row, location already exist in the data
    def set(self, row, location, data):
        self.debug("set(row={},location={},data={})", (row,location,data))

        # self.__validateRowLocationIndex(methodName="set()", row=row, location=location, ignore="index")
        
        # it is valid for data == None here
        # # self.__validateData(data=data, methodName="set()")

        if not self.__rowExists(row):
            raise NestedCacheException("Row [{}] doesn't exist, to add it use append(row,location,data)".format(row))
        if not self.__locationExists(location=location):
            raise NestedCacheException("Location '{}' doesn't exist, to add it use addLocation(location)".format(location))

        self.__setRow(row=row, location=location, data=data)


    def __setRow(self, row, index=None, location=None, data=None):
        self.debug("\t__setRow(row={}, index={}, location={}, data={})", (row, index, location, data))
        # self.__validateRowLocationIndex(methodName="__setRow()", row=row, location=location, index=index)
        # self.__validateData(data=data, methodName="__setRow()")
        
        location, index = self.__getLocationIndex(index = index, location=location)

        try:
            self._storage[row].set(location=index, data=data)
        except FlatCacheException:
            raise NestedCacheException("There is already data at row:{} location:{}/index:{}, to change this data use update(row, location/index, data)".format(row, location, index))
        
        try:
            self._storage[row].set(location=location, data=data)
        except FlatCacheException:
            raise NestedCacheException("There is already data at row:{} location:{}/index:{}, to change this data use update(row, location/index, data)".format(row, location, index))


    def appendRow(self, location=None, index=None, data=None):
        self.debug("appendRow(location={}, index={}, data={})", (location, index, data))

        # self.__validateLocationIndex(methodName="appendRow()", location=location, index=index)

        # self.__validateData(methodName="appendRow()", data=data)

        newRowData = self.__createRowItemData(location=location, index=index, data=data)
        flatCache = self.__createRowObject(newRowData)

        self.__appendRow(flatCache)


    def __appendRow(self, flatCacheItem:FlatCache):
        self.debug("__appendRow(flatCacheItem={})".format(flatCacheItem))
        # self.__validateData(methodName="__appendRow()", data=flatCacheItem, dataName="flatCacheItem")

        if type(flatCacheItem) != FlatCache:
            raise NestedCacheException("FlatCache item expected in __appendRow(), received ''".format(type(flatCacheItem)))

        self._storage.append(flatCacheItem)

        self.info("Height: {}".format(self.height()))
        self.__increaseHeight()
        self.info("Height: {}".format(self.height()))


    def __createRowObject(self, rowDataObj=None):
        self.debug("__createRowObject(rowDataObj={})".format(rowDataObj))

        flatcache = FlatCache.create(rowDataObj)

        return flatcache


    def __createRowItemData(self, location=None, index=None, data=None):
        self.debug("\t__createRowItemData(location={}, index={}, data={})", (location, index, data))
        
        # self.__validateLocationIndex(methodName="__createRowItemData()", location=location, index=index)

        # It is completely valid for data to be == None here, if there is no data in a specific location        
        # # self.__validateData(data=data, methodName="__createRowItemData()")

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


    def deleteRow(self, row):
        self.debug("deleteRow(row={})".format(row))
        # self.__validateRow(methodName="deleteRow()", row=row)

        self.info("deleting: {}".format(self._storage.pop(row)))
        self.__decreaseHeight()


    def unsetRow(self, row):
        self.debug("unsetRow(row={})".format(row))
        # self.__validateRow(methodName="unsetRow()", row=row)

        self.info("unsetting row: {}".format((row)))
        # call the flatCache unset method for this row
        self._storage[row] = self.__createRowObject(None)

    #### 
    #
    # Column Methods
    #
    ####

    # Delete the column, but first make sure we have all the correct data that we need in order to properly
    #   remove the column from every row in the dataset
    def deleteColumn(self, index=None, location=None):
        self.debug("deleteColumn(index={},location={})",(index, location))

        # self.__validateRowLocationIndex(methodName="()", row=row, location=location, index=index)

        location, index = self.__getLocationIndex(location=location, index = index)

        if not self.__locationExists(location=location):
            raise NestedCacheException("Location '{}' doesn't exist, to add it use addColumn(location={})".format(location, location))

        #finally, delete the header from storage
        self.__removeHeaderIndexes(index=index, location=location)


    # remove both the index and location from all rows in the sheetData
    def __removeHeaderIndexes(index, location):
        self.debug("\t__removeHeaderIndexes(index={},location={})", (index, location))
        # self.__validateRowLocationIndex(methodName="__removeHeaderIndexes()", row=row, location=location, ignore="index")

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
    def getData(self, row, location):
        self.debug("getData(row={},location={})", (row, location))
        # self.__validateRowLocationIndex(methodName="getData()", row=row, location=location, ignore="index")
        if self.__rowExists(row):
            data = self.__getItem(row=row, location=location)
            print(data)
            if None == data:
                return None
            return data['data']
        else:
            return None


    def __getItem(self, row, location):
        self.debug("\t__getItem(row={},location={})", (row, location))
        # self.__validateRowLocationIndex(methodName="__getItem()", row=row, location=location, ignore="index")
        if self.__rowExists(row):
            return self.__getRawRow(row).get(location)
        else:
            return None


    # wrapper for deleteItem
    def delete(self, row, location=None, index=None):
        self.debug("delete(row={}, location={}, index={})", (row, location, index))
        # self.__validateRowLocationIndex(methodName="delete()", row=row, location=location, index=index)
        self.deleteItem(row=row, location=location, index=index)


    def deleteItem(self, row, location=None, index=None):
        self.debug("deleteItem(row={}, location={}, index={})", (row, location, index))
        # self.__validateRowLocationIndex(methodName="deleteItem()", row=row, location=location, index=index)
        if 0 == row:
            raise NestedCacheException("You cannot delete from row[0], if you want to modify locations, use deleteColumn()")
        
        # if this is true, then we have index bc we passed validation. So, get the location
        if None == location:
            location == __getLocationFromIndex(index)

        self._storage[row].delete(location=location)


    def update(self, row, index=None, location=None, data=None):
        self.debug("update(row={}, index={}, location={}, data={})", (row, index, location, data))
        # self.__validateRowLocationIndex(methodName="__setRow()", row=row, location=location, index=index)
        
        # it is completely valid for data == None
        # # self.__validateData(data=data, methodName="__setRow()")

        location, index = self.__getLocationIndex(location=location, index = index)

        # create the data for the rows
        rowData = self.__createRowItemData(location=location, index=index, data=data)

        # do the manual update, we are not replacing the row, only the data in these locations
        self._storage[row].update(location=location, data=rowData[index])
        self._storage[row].update(location=index, data=rowData[location])

    def unset(self, **kwargs):
        raise NestedCacheException("unset() is not valid for NestedCache, use either unsetRow() or unsetData()")


    def unsetData(self, row, location=None, index=None):
        self.debug("unsetData(row={}, location={}, index={})", (row, location, index))

        # self.__validateRowLocationIndex(methodName="unsetData()", row=row, location=location, index=index)

        self._storage[row].unset(location=location)
        self._storage[row].unset(location=index)

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
        # decrement bc the user doesn't need to know we are overloading the 0th row
        return (self._height - 1)
    
    @debug
    @validate('increaseBy', ['notNone','gt:0'])
    def __increaseHeight(self, increaseBy = 1):
        self.debug("\t__increaseHeight(increaseBy={})".format(increaseBy))
        if 0 > increaseBy:
            raise NestedCacheException("You can only increase height by positive integers")
        self._height += increaseBy


    @debug
    @validate('decreaseBy', ['notNone','gt:0'])
    def __decreaseHeight(self, decreaseBy = 1):
        self.debug("\t__increaseHeight(decreaseBy={})".format(decreaseBy))
        if 0 > decreaseBy:
            raise NestedCacheException("You can only decrease height by positive integers")
        self._height -= decreaseBy


    def width(self):
        self.debug("width()")
        # in order to avoid getting yelled at by row(0) check validations, use the _locations arr for width
        return len(self.__getLocations())


    def __str__(self) -> str:
        self.debug("__str__()")
        output = "NestedCache: \n"
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

    # ####
    # #
    # # Validation Methods
    # #
    # ####

    # # lots of lines of code to cleanup the other methods in this class
    # # checks row, location, data, and allows for checking the row or location exists all with passing some basic config
    # #   e.g. # self.__setupMethod(methodName="someMethod()", validate=['location', 'row'], params=locals())
    # # copypaste version:
    # #       # self.__setupMethod(methodName="()", validate=[], params=locals())
    # def __setupMethod(self, methodName=None, validate=[], params=None):
    #     self.debug("__setupMethod(methodName={}, validate={}, params={}", (methodName, validate, params))

    #     ####
    #     #
    #     # Setup the methodName and send a Debug Message if we have it
    #     #
    #     ####
    #     if None == methodName:
    #         raise NestedCacheException("methodName is required for __setupMethod() it was not found") 
    #     else:
    #         if "__" in methodName:
    #             methodName += "\t"

    #     if [] != validate and None == params: # we have validations to run, but params are not passed
            
    #         raise NestedCacheException("'{}' validations are requested in __setupMethod(), but params were not passed".format(validate))
    #     elif [] == validate:  # there's nothing to validate
            
    #         return
    #     else: # validations and params are passed
    #         ####
    #         #
    #         # What are we going to check and setup params
    #         #
    #         ####

    #         #param          paramExistsInValidate       addToMethodName #return the updated validate object
    #         row,            rowInValidate,              rowMethod,      validate = self.__checkSetupMethodParams(paramName="row",            validate=validate, params=params)
    #         _,              rowExistsInValidate,        _,              validate = self.__checkSetupMethodParams(paramName="rowExists",      validate=validate, params=params)
    #         location,       locationInValidate,         locationMethod, validate = self.__checkSetupMethodParams(paramName="location",       validate=validate, params=params)
    #         _,              locationExistsInValidate,   _,              validate = self.__checkSetupMethodParams(paramName="locationExists", validate=validate, params=params)
    #         index,          indexInValidate,            indexMethod,    validate = self.__checkSetupMethodParams(paramName="index",          validate=validate, params=params)
    #         ignore,         _,                          ignoreMethod,   validate = self.__checkSetupMethodParams(paramName="ignore",         validate=validate, params=params)
    #         data,           dataInValidate,             dataMethod,     validate = self.__checkSetupMethodParams(paramName="data",           validate=validate, params=params)
    #         dataName,       _,                          dataNameMethod, validate = self.__checkSetupMethodParams(paramName="dataName",       validate=validate, params=params)

    #         for item in validate:
    #             if 'data:' in item:
    #                 #do some dynamic validation on this

    #         ####
    #         #
    #         # Set the debug string, now that we have all the params
    #         #
    #         ####
    #         extendedMethodString = rowMethod+locationMethod+indexMethod+ignoreMethod+dataMethod+dataNameMethod
    #         self.debug("{}({})".format(methodName, extendedMethodString))

    #         ####
    #         #
    #         # Do things with the information we have
    #         #
    #         ####

    #         if rowInValidate:
    #             # self.__validateRow(methodName=methodName, row=row, validateExists=rowExistsInValidate)

    #         if locationExistsInValidate:
    #             if not locationInValidate and indexInValidate:                
    #                 raise NestedCacheException("'locationExists' validation was requested, but no location or index was passed to __setupMethod()")

    #         if locationInValidate or indexInValidate:
    #             if None == index and None == location:
    #                 raise NestedCacheException("You must provide either location or index to {}, neither were found".format(methodName))

    #             if locationInValidate:
    #                 # self.__validateLocation(methodName=methodName, location=location, ignore=ignoreItems, validateExists=locationExistsInValidate)

    #             if indexInValidate:
    #                 # self.__validateIndex(methodName=methodName, index=index, ignore=ignoreItems, validateExists=locationExistsInValidate)

    #         if dataInValidate:
    #             # self.__validateData(methodName=methodName, data=data, dataName=dataName)


    # # dynamically checks if params are in validate, and if so are they in params?
    # # @return param, Whether item is in the validate list, an updated MethodString, and the validation
    # def __checkSetupMethodParams(self, paramName=None, validate=[], params={}):
    #     self.debug("__checkSetupMethodParams(paramname={}, validate={}, params={})", (paramName, validate, params))
    #     param = None
    #     inValidate = False
    #     methodString = ""
    #     inParams = True

    #     if paramName in params:
    #         param = params[paramName]
    #         methodString = "{}={}".format(paramName, param)
    #     else:
    #         inParams = False

    #     if paramName in validate:
    #         inValidate = True
    #         if not inParams:
    #             raise NestedCacheException("'{}' was requested as validation in __setupMethod(), but it was not passed in params to be validated".format(paramName))

    #     return param, inValidate, methodString, validate.remove(paramName)


    # def __validateRow(self, row=None, methodName=None, validateExists=False):
    #     self.debug("\t\t__validateRow(row={})".format(row))

    #     if None == row:
    #         raise NestedCacheException("You must provide a row number to {}".format(methodName))

    #     if 0 == row:
    #         raise NestedCacheException("Silly, you cannot directly access row 0 via {}".format(methodName))

    #     if validateExists and not self.__rowExists(row=row):
    #         raise NestedCacheException("Row [{}] doesn't exist, to add it use append(row,location,data)".format(row))

    @debug
    def validate_locationExists(self, methodName=None, location=None, ignore=None, validateExists=False):
        
        if not self.__locationExists(location=location):
            raise NestedCacheException("Location '{}' doesn't exist, to add it use addLocation(location)".format(location))

    # def __validateIndex(self, methodName=None, index=None, validateExists=False):

    #     self.debug("\t\t__validateIndex(index={}, ignore={}, validateExists={})", (index, ignore, validateExists))

    #     if validateExists and not self.__locationExists(index=index):
    #         raise NestedCacheException("Location '{}' doesn't exist, to add it use addLocation(location)".format(index))


    # def __validateData(self, data=None, methodName=None, dataName="data"):
    #     self.debug("\t\t__validateData(data={})".format(data))
        
    #     if None == data:
    #         raise NestedCacheException("{} shouldn't be None for  {}".format(dataName, methodName))

