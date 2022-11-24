import sys
from modules.sheetProcessor import SheetProcessor


from modules.spreadsheets.bdfs_inventory import Bdfs_Spreadsheet
from modules.sheetProcessors.bdfs_inventory import Bdfs_SheetProcessor

#setup logging
import logging
from modules.logger import logger

if __name__ == "__main__":
    logger.debug("run.py running __main__")

    # Sheet processor functionality without a specific spreadsheet, this will fail
    # run = SheetProcessor()
    # run.main(sys.argv[1:])


    # data = [
    #         ['1', "somedata", {"a": "b"}], 
    #         ['2', "anotehr datas", {"c": "d"}]
    #         ]

    # headers = ['h1', 'h2', 'h3'] 
    # from modules.caches.nested import NestedCache
    # nestedCache = NestedCache(headers, data)

    # print(nestedCache)


    # Bdfs Sheet Processor functionality
    run = Bdfs_SheetProcessor()
    run.main(sys.argv[1:])

    # For testing the spreadsheet functionality
    # sheet = Bdfs_Spreadsheet()
    # print(sheet.getSpreadsheetId())