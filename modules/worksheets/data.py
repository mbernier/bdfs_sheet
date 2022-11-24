
import sys
from modules.base import BaseClass
from modules.caches.flat import FlatCache
from modules.caches.nested import NestedCache

class WorksheetData(BaseClass):

    logger_name = "WorksheetData"

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
        self._sheetData = None

        # a place to keep track of empty headers
        #   These are only the ones within the data values
        #   trailing empty headers will be ignored for this
        self._emptyHeaderIndexes = []

        self.debug("init()")

        # don't do things if nothing was passed
        if None != sheetData:
            self.__setSheetData(sheetData)


    # the SheetData is the source of truth
    #   If we want to update our sheet, we will do this from sheetData
    #   If we change sheetData format, we need to update our other caches
    def __setSheetData(self, data):
        self.debug("__setSheetData(data={})".format(data))
        self._sheetData = data
        self.__setupCache()

    def __setupCache(self):
        self.debug("setupCache()")
        data = self.__getSheetData()

        for index, rowData in enumerate(data):
            if 0 == index:
                self.__setupHeaders(rowData)
            else:
                self.__appendDataCacheRow(data=rowData)

        print("\n\n\n")
        self.debug("headersList: {}".format(self._headersList))
        self.debug("headersFlatCache: {}".format(self._headersFlatCache))
        self.debug("data: {}".format(self._dataCache))
        self.debug("Empty Headers: {}".format(self._emptyHeaderIndexes))


    def __setupHeaders(self, headers):
        self.debug("__setupHeaders(headers={})".format(headers))
        cache = FlatCache()

        emptyCol = 1

        for index, headerName in enumerate(headers):
            # build the lookup table
            # {"headerOne": 1, "headerTwo": 2}
            if "" == headerName:
                headerName = "NoHeaderFound_{}".format(emptyCol)
                # replace that one empty header
                headers[index] = headerName
                self._emptyHeaderIndexes.append(index)
                emptyCol+=1
            cache.set(location=headerName, data=index)

        self._headersFlatCache = cache

        # Build the HeadersList
        # ['headerOne', 'headerTwo']
        self._headersList = headers


    # NestedCache of the data 
    def __appendDataCacheRow(self, data):
        self.debug("__appendDataCacheRow(data={})", data)
        headers = self._headersList

        rowFlatCache = FlatCache()

        # [1,"some text", "$4.50"]
        # go through the headers and setup the data object for the data cache
        for index, headerValue in enumerate(headers):
            cellData = {"value": headerValue, "position": index}

            rowFlatCache.set(location=headerValue, data=cellData)
        
        self._dataCache.append(rowFlatCache)

        self.debug("Data Cache Rows: {}".format(self._dataCache.totalSize()))


    #public accessor to retrive the sheet Data
    def getSheetData(self):
        self.debug("getSheetData()")
        return self.__getSheetData()

    # private accessor to retrieve the sheet data
    def __getSheetData(self):
        self.debug("__getSheetData()")
        return self._sheetData

    def __setHeadersList(self, headers):
        self.debug("__setHeadersList(headers={})", headers)
        self._headersList = headers
        return self._headersList

    def getHeadersList(self):
        self.debug("getHeadersList()")
        return self._headersList

    def getHeaderByIndex(self, index):
        self.debug("getHeaderByIndex(index={})", index)
        return self._headersList[index]

    def getIndexByHeader(self, header):
        self.debug("getIndexByHeader(header={})", header)
        return self._headersFlatCache.get(header)

    def __getDataHeight(self):
        self.debug("__getDataHeight()")
        return len(self._sheetData)

    def __getDataWidth(self):
        self.debug("__getDataWidth()")
        return len(self._headersList)

    def getDataRange(self):
        self.debug("getDataRange()")
        endCell = gspread_utils.rowcol_to_a1(self.__getDataHeight(), self.__getDataWidth())
        return "A1:" + endCell