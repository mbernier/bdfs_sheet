
import sys
from modules.base import BaseClass
from modules.caches.nested import Nested_Cache
from modules.logger import Logger, logger_name
from modules.worksheets.exception import Bdfs_Worksheet_Data_Exception
from pprint import pprint
from modules.decorator import Debugger
from pydantic import validate_arguments

logger_name.name = "WorksheetData"

class Bdfs_Worksheet_Data(BaseClass):

    dataStore:Nested_Cache = None
    _emptyHeaderIndexes = []
    _uniqueHeaders = []
    _duplicateHeaders = [] 
    _headers = []
    _removedHeaders = []

    @Debugger
    @validate_arguments
    def __init__(self, sheetData = None):
        if None != sheetData:
            self.load(sheetData)

    @Debugger
    @validate_arguments
    def load(self, sheetData=None):
        # store all the data in the data store
        headers = sheetData.pop(0)

        headers, uniqueHeaders, duplicateHeaders, emptyHeaderIndexes = self.__prepHeaders(headers)

        self.__setHeaders(headers)
        self.__setUniqueHeaders(uniqueHeaders)
        self.__setDuplicateHeaders(duplicateHeaders)
        self.__setEmptyHeaderIndexes(emptyHeaderIndexes)

        self.dataStore = Nested_Cache(headers, sheetData)


    # replaces empty headers with "NoHeaderFound_{index}"
    @Debugger
    @validate_arguments
    def __prepHeaders(self, headers):
        uniqueHeaders = []
        duplicateHeaders = []
        emptyHeaderIndexes = []

        for index, header in enumerate(headers):
            if "" == header:
                header = "NoHeaderFound_{}".format(index)
                #replace the header with a placeholder name
                headers[index] = header
                
                #record the headers that are empty
                emptyHeaderIndexes.append(index)

            # check for duplication
            if header not in self.__getUniqueHeaders():
                uniqueHeaders.append(header)
            else:
                duplicateHeaders.append(header)

        if 0 < len(duplicateHeaders):
            Logger.critical("There are duplicate headers in your spreadsheet with these names: {}".format(duplicateHeaders))

        return headers, uniqueHeaders, duplicateHeaders, emptyHeaderIndexes

    ####
    #
    # Header Methods
    #
    ####

    @Debugger
    def getHeaders(self):
        return self._headers


    @Debugger
    @validate_arguments
    def __setHeaders(self, headers):
        self._headers = headers

    @Debugger
    def __getUniqueHeaders(self):
        return self._uniqueHeaders

    @Debugger
    @validate_arguments
    def __setUniqueHeaders(self, headers):
        self._uniqueHeaders = headers

    @Debugger
    @validate_arguments
    def __appendUniqueHeader(self, header):
        self._uniqueHeaders.append(header)

    @Debugger
    def __getDuplicateHeaders(self):
        return self._duplicateHeaders

    @Debugger
    @validate_arguments
    def __setDuplicateHeaders(self, headers):
        self._duplicateHeaders = headers

    @Debugger
    @validate_arguments
    def __appendDuplicateeHeader(self, header):
        self._uniqueHeaders.append(header)

    @Debugger
    def __getEmptyHeaderIndexes(self):
        return self._emptyHeaderIndexes

    @Debugger
    @validate_arguments
    def __setEmptyHeaderIndexes(self, headers):
        self._emptyHeaderIndexes = headers

    @Debugger
    @validate_arguments
    def __appendEmptyHeaderIndex(self, index):
        self._emptyHeaderIndexes.append(index)


    ####
    #
    # Column Methods
    #
    ####

    @Debugger
    @validate_arguments
    def addHeader(self, name:str, index:int=None):
        # add to the end of the data
        self.dataStore.insert_location(location=name, index=index)


    # fancy logic that just calls removeHeader(index)
    # returns the number of headers removed
    @Debugger
    @validate_arguments
    def removeHeaders(self, start, end):
        currentWidth = self.width()

        if start > self.width:
            return 0

        if end > self.width:
            end = self.width()

        if start == end:
            self.removeHeader(start)
            return 1

        for index in range(start, end):
            self.removeHeader(index)
            return end-start


    @Debugger
    @validate_arguments
    def removeHeader(self, index=None, header=None):

        # causes lookup of the name from the index
        if None != index:
            # get the header name
            header = self.__removeHeader_byIndex(index)
        elif None != header:
            self.__removeHeader_byName(header)
        else:
            raise Bdfs_Worksheet_Data_Exception("You must pass either an index or a header to removeHeader()")


    # removed the header from the headers list
    # @return the value from the headers list that was removed
    @Debugger
    @validate_arguments
    def __removeHeader_byIndex(self, index):
        header = self._headers.pop(index)

        self.__removeHeader(index=index, header=header)
        return header

    @Debugger
    @validate_arguments
    def __removeHeader_byName(self, header):
        index = self._headers.index(header)
        self._headers.pop(index)

        self.__removeHeader(index=index, header=header)
        return header


    @Debugger
    @validate_arguments
    def __removeHeader(self, index, header):

        # remove the name from all the places
        self.__removeHeaderFrom_uniqueHeaders_byName(header=header)
        
        # remove from duplicateHeaders
        self.__removeHeaderFrom_duplicateHeaders_byName(header=header)

        # remove from emptyHeaders
        self.__removeHeaderFrom_emptyHeaders_byIndex(index=index)
        
        # store the removed name in the removedHeaders array
        self.__appendRemovedHeader(header)

        # make sure to clean up the location storage
        self.__removeHeaderFrom_sheetData(index=index, name=headerName)

    @Debugger
    @validate_arguments
    def __removeHeaderFrom_sheetData(self, index, name):
        self._sheetData.deleteColumn(index=index, location=name)


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