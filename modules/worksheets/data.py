
import sys
from modules.base import BaseClass
from modules.caches.nested import NestedCache
from pprint import pprint

class WorksheetData(BaseClass):

    dataStore = None
    logger_name = "WorksheetData"

    def __init__(self, sheetData = None):
        # store all the data in the data store
        headers = sheetData.pop(0)
        headers = self.__prepHeaders(headers)

        self.dataStore = NestedCache(headers, sheetData)

    # replaces empty headers with "NoHeaderFound_{index}"
    def __prepHeaders(self, headers):
        uniqueHeaders = []
        duplicateHeaders = []
        for index, header in enumerate(headers):
            if "" == header:
                header = "NoHeaderFound_{}".format(index)
                #replace the header with a placeholder name
                headers[index] = header

            # check for duplication
            if header not in uniqueHeaders:
                uniqueHeaders.append(header)
            else:
                duplicateHeaders.append(header)

        if 0 < len(duplicateHeaders):
            self.critical("There are duplicate headers in your spreadsheet with these names: {}".format(duplicateHeaders))

        return headers

    # gives the worksheet range for the data, starting at the topleft corner
    def range(self):
        self.debug("getDataRange()")

        width, height = self.dataStore.size()

        endCell = gspread_utils.rowcol_to_a1(height, width)

        return "A1:" + endCell