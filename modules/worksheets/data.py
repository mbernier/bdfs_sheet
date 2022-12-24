
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

    @Debugger
    @validate_arguments
    def __init__(self, sheetData:list=[]):
        
        self.load(sheetData)

    @Debugger
    @validate_arguments
    def load(self, sheetData:list=[]):
        headers = []
        if None != sheetData and [] != sheetData:
            # store all the data in the data store
            headers = sheetData.pop(0)

            headers, uniqueHeaders, duplicateHeaders, emptyHeaderIndexes = self.__prepHeaders(headers)

        self._headers = headers

        self.dataStore = Nested_Cache(self._headers, sheetData)


    # replaces empty headers with "NoHeaderFound_{index}"
    @Debugger
    @validate_arguments
    def __prepHeaders(self, headers):
        uniqueHeaders = []
        duplicateHeaders = []
        emptyHeaderIndexes = []

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
            else:
                duplicateHeaders.append(header)

        if 0 < len(duplicateHeaders):
            Logger.critical("There are duplicate headers in your spreadsheet with these names: {}".format(duplicateHeaders))

        return headers, uniqueHeaders, duplicateHeaders, emptyHeaderIndexes

    ####
    #
    # Column Methods
    #
    ####

    @Debugger
    def getHeaders(self):
        return self._headers


    # add multiple headers to the data
    @Debugger
    @validate_arguments
    def addHeaders(self, headers:list[str]):
        for header in headers:
            # add to the end of the data
            self.dataStore.insert_location(location=header)


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
        self._headers = list(set(self._headers) - set(headers))


    @Debugger
    @validate_arguments
    def removeHeader(self, header:str=None):    
        self.dataStore.deleteColumn(position=header)
        # do a double check for whether this was removed by reference
        #   it is possible that the headers list in NestedCache is referencing the headers list here
        #   so when we deleteColumn() and remove from that list, we remove it here, too
        if header in self._headers:
            self._headers.remove(header)


    # set the data headers order to the order in this list
    @Debugger
    @validate_arguments
    def reorderHeaders(self, newHeaders:list[str]):
        # Make sure the order is correct
        self.dataStore.reorderColumns(newHeaders)

        # make sure to update the list of locations in the correct order
        self._headers = self.dataStore.getLocations()


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
    def select(self, row, column:Union[int,str]=None):
        return self.dataStore.select(row=row, position=column)

    @Debugger
    @validate_arguments
    def insertRow(self, rowData:list=None):
        self.dataStore.insert(rowData)

    ####
    #
    # Meta Methods
    #
    ####

    @Debugger
    def width(self):
        return len(self.getHeaders())

    @Debugger
    def height(self):
        return self.dataStore.height()

    @Debugger
    def getAsListOfLists(self):
        return self.dataStore.getAsListOfLists()
    
    @Debugger
    def getAsListOfDicts(self):
        return self.dataStore.getAsListOfDicts()