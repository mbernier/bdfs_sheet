
import sys
from modules.base import BaseClass
from modules.caches.nested import NestedCache
from pprint import pprint

class WorksheetData(BaseClass):

    dataStore = None
    logger_name = "WorksheetData"
    _emptyHeaderIndexes = []
    _uniqueHeaders = []
    _duplicateHeaders = []
    _headers = []
    _removedHeaders = []

    def __init__(self, sheetData = None):

        # store all the data in the data store
        headers = sheetData.pop(0)

        headers, uniqueHeaders, duplicateHeaders, emptyHeaderIndexes = self.__prepHeaders(headers)

        self.__setHeaders(headers)
        self.__setUniqueHeaders(uniqueHeaders)
        self.__setDuplicateHeaders(duplicateHeaders)
        self.__setEmptyHeaderIndexes(emptyHeaderIndexes)

        self.dataStore = NestedCache(headers, sheetData)

    # replaces empty headers with "NoHeaderFound_{index}"
    def __prepHeaders(self, headers):
        self.debug("__prepHeaders(headers={})".format(headers))
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
            self.critical("There are duplicate headers in your spreadsheet with these names: {}".format(duplicateHeaders))

        return headers, uniqueHeaders, duplicateHeaders, emptyHeaderIndexes

    ####
    #
    # Header Methods
    #
    ####

    def getHeaders(self):
        self.debug("getHeaders()")
        return self._headers

    def __setHeaders(self, headers):
        self.debug("__setHeaders(headers={})".format(headers))
        self._headers = headers

    def __getUniqueHeaders(self):
        self.debug("__getUniqueHeaders()")
        return self._uniqueHeaders

    def __setUniqueHeaders(self, headers):
        self.debug("__setUniqueHeaders(headers={})".format(headers))
        self._uniqueHeaders = headers

    def __appendUniqueHeader(self, header):
        self.debug("__appendUniqueHeader(header={})".format(header))
        self._uniqueHeaders.append(header)


    def __getDuplicateHeaders(self):
        self.debug("__getDuplicateHeaders()")
        return self._duplicateHeaders

    def __setDuplicateHeaders(self, headers):
        self.debug("__setDuplicateHeaders(headers={})".format(headers))
        self._duplicateHeaders = headers


    def __appendDuplicateeHeader(self, header):
        self.debug("__appendDuplicateHeader(header={})".format(header))
        self._uniqueHeaders.append(header)

    def __getEmptyHeaderIndexes(self):
        self.debug("__getEmptyHeaderIndexes()")
        return self._emptyHeaderIndexes

    def __setEmptyHeaderIndexes(self, headers):
        self.debug("__setEmptyHeaders(headers={})".format(headers))
        self._emptyHeaderIndexes = headers

    def __appendEmptyHeaderIndex(self, index):
        self.debug("__appendEmptyHeader(index={})".format(index))
        self._emptyHeaderIndexes.append(index)


    ####
    #
    # Column Methods
    #
    ####

    # fancy logic that just calls removeHeader(index)
    # returns the number of headers removed
    def removeHeaders(self, start, end):
        self.debug("removeColumns(start={}, end={})", (start, end))
        currentWidth = self.width()

        if start > self.width:
            return 0

        if end > self.width:
            end = self.width()

        if start == end:
            self.removeHeader(start)
            return 1

        for index in range(start, end)
            self.removeHeader(index)
            return end-start


    def removeHeader(self, index):
        self.debug("removeHeader(index={})".format(index))
        # get the header name
        headerName = self.__removeFrom_headers_byIndex(index)

        # remove the name from all the places
        self.__removeFrom_uniqueHeaders_byName(headerName)
        self.__removeFrom_duplicateHeaders_byName(headerName)
        self.__removeFrom_emptyHeaders_byIndex(index)

        # store the removed name in the removedHeaders array
        self.__appendRemovedHeader(headerName)

    def __removeFrom_headers_byIndex(self, index):
        self.debug("__removeFromHeaderByIndex(index={})".format(index))
        return self._headers.pop(index)


    ####
    #
    # Meta Methods
    #
    ####




    def width(self):
        self.debug("width()")
        return len(self.getHeaders())

    def height(self):
        self.debug("height()")
        return self.dataStore.height()