# All of the methods for handling the caches and lookups within the data
# This class should never be used directly, it should be wrapped by a class that
# will translate it into the formats that the end result system needs
# e.g. WorksheetData should use Data and do any translations to a worksheet from the data we have stored
# This creates a nice layer differentiation and allows for replacing the data class with another data storage engine in the future

# All methods and return data are in terms of the data here, there is NO translation done for the system that is using this data store

import sys
from modules.base import BaseClass
from modules.caches.flat import Flat_Cache
from modules.caches.nested import Nested_Cache


class DataStore(BaseClass):

    logger_name = "Data"

    def __init__(self, sheetData = None):
        
        # _headersList
        #   ['header1', 'header2']
        self._headersList: list = []

        # _headersFlat_Cache
        #   [{header1:location, header2:location}]
        self._headersFlat_Cache = Flat_Cache()
        
        # is a Nested_Cache Object [RowCache,RowCache]
        self._dataCache: Nested_Cache = Nested_Cache()

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
        self.debug("headersFlat_Cache: {}".format(self._headersFlat_Cache))
        self.debug("data: {}".format(self._dataCache))
        self.debug("Empty Headers: {}".format(self.getEmptyHeaders()))


    # Nested_Cache of the data 
    def __appendDataCacheRow(self, data):
        self.debug("__appendDataCacheRow(data={})", data)
        headers = self.getHeaders()

        rowFlat_Cache = Flat_Cache()

        # [1,"some text", "$4.50"]
        # go through the headers and setup the data object for the data cache
        for index, headerValue in enumerate(headers):
            cellData = {"value": headerValue, "position": index}

            rowFlat_Cache.set(location=headerValue, data=cellData)
        
        # add the row to the data store
        self.__appendCacheRow(rowFlat_Cache)

        self.debug("Data Cache Rows: {}".format(self._dataCache.totalSize()))


    ####
    #
    # Header Management
    #
    ####

    #
    def __setupHeadersCaches(self, headers):
        self.debug("__setupHeaderCaches(headers={})".format(headers))
        cache = Flat_Cache()

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

        self.__setHeadersFlat_Cache(cache)

        # Build the HeadersList
        # ['headerOne', 'headerTwo']
        self._setHeadersList(headers)

    def __setHeadersList(self, headers):
        self.debug("__setHeadersList(headers={})", headers)
        self._headersList = headers
        return self._headersList

    def __setHeadersFlat_Cache(self, data):
        self.debug("__setHeadersFlat_Cache({})".format(data))
        self._headersFlat_Cache = cache

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
        return self._headersFlat_Cache.get(header)

    def getEmptyHeaders(self):
        self.debug("getEmptyHeaders()")
        return self._emptyHeaderIndexes

    ####
    #
    # Cache Writing Methods
    #
    ####
    def __appendCacheRow(self, Flat_CacheObject):
        self.debug("__appendCacheRow({})".format(Flat_CacheObject))
        self._dataCache.append(rowFlat_Cache)
