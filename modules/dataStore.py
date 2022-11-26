# All of the methods for handling the caches and lookups within the data
# This class should never be used directly, it should be wrapped by a class that
# will translate it into the formats that the end result system needs
# e.g. WorksheetData should use Data and do any translations to a worksheet from the data we have stored
# This creates a nice layer differentiation and allows for replacing the data class with another data storage engine in the future

# All methods and return data are in terms of the data here, there is NO translation done for the system that is using this data store

import sys
from modules.base import BaseClass
from modules.caches.flat import FlatCache
from modules.caches.nested import NestedCache


class DataStore(BaseClass):

    logger_name = "Data"

    def __init__(self, sheetData = None):
        
        # _headersList
        #   ['header1', 'header2']
        self._headersList: list = []

        # _headersFlatCache
        #   [{header1:location, header2:location}]
        self._headersFlatCache = FlatCache()
        
        # is a NestedCache Object [RowCache,RowCache]
        self._dataCache: NestedCache = NestedCache()

        # This is the entire data of the spreadsheet
        # [[],[],[]]
        self._data = None

        # a place to keep track of empty headers
        #   These are only the ones within the data values
        #   trailing empty headers will be ignored for this
        self._emptyHeaderIndexes = []

        self.debug("init()")

        # don't do things if nothing was passed
        if None != sheetData:
            self.__setData(sheetData)

    ####
    #
    # _data meta methods
    #
    ####
    def height(self):
        self.debug("height()")
        return len(self.getData())

    def width(self):
        self.debug("width()")
        return len(self.getHeaders())

    def size(self):
        self.debug("range()")
        return (self.__getDataHeight(), self.__getDataWidth())

    ####
    #
    # _data retrieval methods
    #
    ####

    #public accessor to retrive the sheet Data
    def getData(self):
        self.debug("getData()")
        return self._data


    ####
    #
    # _data Writing Methods
    #
    ####
    # the _data is the source of truth
    #   If we want to update our sheet, we will do this from data
    #   If we change anything about the rows, columns, we need to update our other caches
    def __setData(self, data):
        self.debug("__setData(data={})".format(data))
        self._data = data
        self.__setupCache()


    ####
    #
    # Cache Setup Methods - creates the data objects and stores things the way we want it stored
    #
    ####

    def __setupCache(self):
        self.debug("setupCache()")
        data = self.getData()

        for index, rowData in enumerate(data):
            if 0 == index:
                self.__setupHeadersCaches(rowData)
            else:
                self.__appendDataCacheRow(data=rowData)

        print("\n\n\n")
        self.debug("headersList: {}".format(self._headersList))
        self.debug("headersFlatCache: {}".format(self._headersFlatCache))
        self.debug("data: {}".format(self._dataCache))
        self.debug("Empty Headers: {}".format(self.getEmptyHeaders()))


    # NestedCache of the data 
    def __appendDataCacheRow(self, data):
        self.debug("__appendDataCacheRow(data={})", data)
        headers = self.getHeaders()

        rowFlatCache = FlatCache()

        # [1,"some text", "$4.50"]
        # go through the headers and setup the data object for the data cache
        for index, headerValue in enumerate(headers):
            cellData = {"value": headerValue, "position": index}

            rowFlatCache.set(location=headerValue, data=cellData)
        
        # add the row to the data store
        self.__appendCacheRow(rowFlatCache)

        self.debug("Data Cache Rows: {}".format(self._dataCache.totalSize()))


    ####
    #
    # Header Management
    #
    ####

    #
    def __setupHeadersCaches(self, headers):
        self.debug("__setupHeaderCaches(headers={})".format(headers))
        cache = FlatCache()

        emptyCol = 1

        for index, headerName in enumerate(headers):
            # build the lookup table
            # {"headerOne": 1, "headerTwo": 2}
            if "" == headerName:
                headerName = "NoHeaderFound_{}".format(emptyCol)
                
                # replace that one empty header
                headers[index] = headerName

                # add the index to the empty header storage
                self.__appendEmptyHeaderIndex(index)

                emptyCol+=1

            cache.set(location=headerName, data=index)

        self.__setHeadersFlatCache(cache)

        # Build the HeadersList
        # ['headerOne', 'headerTwo']
        self._setHeadersList(headers)

    def __setHeadersList(self, headers):
        self.debug("__setHeadersList(headers={})", headers)
        self._headersList = headers
        return self._headersList

    def __setHeadersFlatCache(self, data):
        self.debug("__setHeadersFlatCache({})".format(data))
        self._headersFlatCache = cache

    def __appendEmptyHeaderIndex(self, index):
        self.debug("__appendEmptyHeaderIndex({})".format(index))
        self._emptyHeaderIndexes.append(index)

    def getHeaders(self):
        self.debug("getHeadersList()")
        return self._headersList

    def getHeaderByIndex(self, index):
        self.debug("getHeaderByIndex(index={})", index)
        return self._headersList[index]

    def getIndexByHeader(self, header):
        self.debug("getIndexByHeader(header={})", header)
        return self._headersFlatCache.get(header)

    def getEmptyHeaders(self):
        self.debug("getEmptyHeaders()")
        return self._emptyHeaderIndexes

    ####
    #
    # Cache Writing Methods
    #
    ####
    def __appendCacheRow(self, flatCacheObject):
        self.debug("__appendCacheRow({})".format(flatCacheObject))
        self._dataCache.append(rowFlatCache)
