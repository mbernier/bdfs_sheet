import sys, logging
from inspect import signature
from modules.caches.nested import Nested_Cache
from modules.logger import Logger
from modules.sheetProcessors.bdfs_inventory import BdfsInventory_SheetProcessor


if __name__ == "__main__":
    print()
    # logger.debug("run.py running __main__")

    # Bdfs Sheet Processor functionality
    # run = BdfsInventory_SheetProcessor()
    # run.main(sys.argv[1:]) 


    # print("need to test Nested_Cache and iron out the rest of the decorators, before proceeding")
    # cache = Nested_Cache(["col1", "col2", "col3"]) #, [["a","b", "c"], [1,2,3],[4,5,6]])


    # cache = Nested_Cache(['b'],[[3]])

    # cache.set(row=2, location='c', data=3)


    logger = Logger()
    logger.info("test")

