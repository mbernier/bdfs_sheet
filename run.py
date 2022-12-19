import sys, logging
from inspect import signature
from pydoc import locate

from modules.base import BaseClass
from modules.cache import BdfsCache
from modules.caches.flat import Flat_Cache
from modules.caches.nested import Nested_Cache
from modules.caches.exception import Nested_Cache_Row_Exception
# from modules.cell import Cell
# from modules.config import config
# from modules.decorator import Debugger
# from modules.exception import BdfsException
# from modules.helper import Helper
# from modules.logger import Logger
from modules.sheetProcessor import SheetProcessor
from modules.sheetProcessors.bdfs_inventory import BdfsInventory_SheetProcessor
# from modules.sheetProcessors.exception import SheetProcessorException
# from modules.spreadsheet import Bdfs_Spreadsheet
from modules.spreadsheets.bdfs_inventory import BdfsInventory_Spreadsheet
from modules.spreadsheets.bdfs_test import BdfsInventory_Test_Spreadsheet
# from modules.spreadsheets.exception import SpreadSheetException
### removing these?
# from modules.validation import Validation
# from modules.validations.exception import Validation_Exception

# from modules.worksheet import Worksheet
# from modules.worksheets.bdfs_inventory import BdfsInventory_Worksheet
# from modules.worksheets.bdfs_test import BdfsInventory_Test_Worksheet
# from modules.worksheets.data import WorksheetData
# from modules.worksheets.exception import WorksheetException, WorksheetData_Exception


if __name__ == "__main__":
    # logger.debug("run.py running __main__")

    # Bdfs Sheet Processor functionality
    # run = BdfsInventory_SheetProcessor()
    # run.main(sys.argv[1:]) 


    list1 = ['Name', 'Birthday', 'Email', 'newColumn3', 'newColumn1']
    list2 = [['Matt', '1/1/2001', 'matt@example.com', None, None], ['Bob', '1/2/2023', 'bob@example.com', None, None], ['Mary', '5/7/2017', 'mary@example.com', None, None]]

    print([list1]+list2)
    print("\n\n")
    print(list2.insert(0,list1))
    print("\n\n")