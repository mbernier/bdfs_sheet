import sys, logging
from inspect import signature
from modules.base import BaseClass
from modules.helper import Helper
from modules.decorator import debug_log, validate
from modules.caches.nested import Nested_Cache
from modules.logger import Logger
from modules.sheetProcessors.bdfs_inventory import BdfsInventory_SheetProcessor


if __name__ == "__main__":
    # logger.debug("run.py running __main__")

    # Bdfs Sheet Processor functionality
    # run = BdfsInventory_SheetProcessor()
    # run.main(sys.argv[1:]) 
    

    list1 = [1,2,3,4]
    list2 = [1,2,3,4,5]
    print(Helper.compareLists(list1,list2))
    print(Helper.compareLists(list2,list1))