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

    class C():
        @validate()
        def foo(self, var1:int = 100):
            return True

        @validate()
        def bar(self, var1:int):
            return True

        @validate()
        def bat(self, var1 = 50):
            return True


    c6 = C()
    c6.bat(None)