
import sys
from modules.base import BaseClass
from modules.caches.nested import Nested_Cache
from modules.logger import Logger
from modules.worksheets.exception import Bdfs_Worksheet_Data_Exception
from modules.decorator import Debugger
from pydantic import validate_arguments
from typing import Union


class Bdfs_Worksheet_Data(BaseClass):

    dataStore:Nested_Cache = None
    _emptyHeaderIndexes = []
    _uniqueHeaders = []
    _duplicateHeaders = [] 
    _headers = []
    _removedHeaders = []
    uniqueField = None
    uniques = []

    @Debugger
    @validate_arguments
    def __init__(self, sheetData:list=[], uniqueField = None):
        self.dataStore:Nested_Cache = None
        self.uniqueField = None
        self.uniques = []

        # allow identifying which field is a way to identify the row
        if None != uniqueField:
            self.uniqueField = uniqueField

        self.load(sheetData) 


    @Debugger
    @validate_arguments
    def load(self, sheetData:list=[]):
        headers = []
        if [] != sheetData:
            # store all the data in the data store
            headers = sheetData.pop(0)
            headers = self.__prepHeaders(headers)

        self.dataStore = Nested_Cache(locations=headers, data=sheetData, uniqueField=self.uniqueField)


    # replaces empty headers with "NoHeaderFound_{index}"
    @Debugger
    @validate_arguments
    def __prepHeaders(self, headers:list)->tuple[list]:
        uniqueHeaders = []
        duplicateHeaders = []
        emptyHeaderIndexes = []
        timestampHeaders = []
        
        for index, header in enumerate(headers):
            if "" == header:
                #replace the header with a placeholder name
                header = "NoHeaderFound_{}".format(index)
                
                #record the headers that are empty
                emptyHeaderIndexes.append(index)
            
            # add the header to the list
            headers[index] = header

            # check for duplication
            if header not in uniqueHeaders:
                uniqueHeaders.append(header)
                if header != "update_timestamp":
                    timestampHeaders.append(f"{header}_update_timestamp")
            else:
                duplicateHeaders.append(header)

        if 0 < len(duplicateHeaders):
            Logger.critical("There are duplicate headers in your spreadsheet with these names: {}".format(duplicateHeaders))

        return headers.copy()

    ####
    #
    # Column Methods
    #
    ####

    @Debugger
    def getHeaders(self)->list:
        return self.dataStore.getLocations()


    # add multiple headers to the data
    @Debugger
    @validate_arguments
    def addHeaders(self, headers:list[str]):
        for header in headers:
            # add to the end of the data
            self.addHeader(name=header)


    @Debugger
    @validate_arguments
    def addHeader(self, name:str, index:int=None):
        # add to the end of the data
        self.dataStore.insert_location(location=name, index=index)


    # fancy logic that just calls removeHeader(index)
    # returns the number of headers removed
    @Debugger
    @validate_arguments
    def removeHeaders(self, headers:list[str]):
        # call directly to the multi-delete on Nested Cache
        self.dataStore.deleteColumns(positions=headers)


    @Debugger
    @validate_arguments
    def removeHeader(self, header:str=None):        
        self.dataStore.deleteColumn(position=header)


    # set the data headers order to the order in this list
    @Debugger
    @validate_arguments
    def reorderHeaders(self, newHeaders:list[str]):
        # Make sure the order is correct
        self.dataStore.reorderColumns(newHeaders)


    @Debugger
    @validate_arguments
    def alignHeaders(self, newHeaders:list[str]):

        currentHeaders = self.getHeaders()

        # remove headers from the data that are not in the new Headers
        extraHeaders = list(set(currentHeaders) - set(newHeaders))

        self.removeHeaders(extraHeaders)

        # add headers in newHeaders that are not in currentHeaders
        missingHeaders = list(set(newHeaders) - set(currentHeaders)) 
        self.addHeaders(missingHeaders)

        # make sure the data is in the newHeaders order
        self.reorderHeaders(newHeaders)

    ####
    #
    # Row Methods
    # 
    ####
    @Debugger
    @validate_arguments
    def select(self, row:int, column:Union[int,str]=None, update_timestamp=True):
        return self.dataStore.select(row=row, position=column, update_timestamp=update_timestamp)


    #given some data, identify if we need to update or insert the data
    @Debugger
    @validate_arguments
    def putRow(self, rowData:list):
        self.dataStore.putRow(rowData=rowData)


    # add a new row to storage
    @Debugger
    @validate_arguments
    def insertRow(self, rowData:list=None):
        self.dataStore.insert(rowData)

    ####
    #
    # All Data
    #
    ###

    @Debugger
    @validate_arguments
    def deleteAllData(self):
        self.dataStore.deleteAllData()
        Logger.info("All data in Worksheet_Data has been deleted")
    
    @Debugger
    @validate_arguments
    def deleteRowWhere(self, column:str, value):
        self.dataStore.deleteRowWhere(column=column, value=value)

    ####
    #
    # Meta Methods
    #
    ####

    @Debugger
    def width(self) -> int:
        return len(self.getHeaders())

    @Debugger
    def height(self) -> int:
        return self.dataStore.height()

    @Debugger
    @validate_arguments
    def getAsListOfLists(self, update_timestamp:bool=True) -> list[list]:
        return self.dataStore.getAsListOfLists(update_timestamp=update_timestamp)
    
    @Debugger
    @validate_arguments
    def getAsListOfDicts(self, update_timestamp:bool=True) -> list[dict]:
        return self.dataStore.getAsListOfDicts(update_timestamp=update_timestamp)