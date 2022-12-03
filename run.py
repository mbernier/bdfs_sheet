import sys, logging
from inspect import signature
from modules.base import BaseClass
from modules.caches.nested import NestedCache
from modules.decorator import debug, validate
from modules.logger import logger
from modules.sheetProcessors.bdfs_inventory import BdfsInventory_SheetProcessor


if __name__ == "__main__":
    logger.debug("run.py running __main__")

    # Bdfs Sheet Processor functionality
    # run = BdfsInventory_SheetProcessor()
    # run.main(sys.argv[1:]) 


    print("need to test NestedCache and iron out the rest of the decorators, before proceeding")
    # cache = NestedCache(["col1", "col2", "col3"]) #, [["a","b", "c"], [1,2,3],[4,5,6]])


    cache = NestedCache(['b'],[[3]])

    # cache.set(row=2, location='c', data=3)