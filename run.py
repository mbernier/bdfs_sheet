import sys, logging
from inspect import signature
from modules.base import BaseClass
from modules.decorator import debug_log, validate
from modules.caches.nested import Nested_Cache
from modules.logger import Logger
from modules.sheetProcessors.bdfs_inventory import BdfsInventory_SheetProcessor


if __name__ == "__main__":
    print('hello')
    # logger.debug("run.py running __main__")

    # Bdfs Sheet Processor functionality
    # run = BdfsInventory_SheetProcessor()
    # run.main(sys.argv[1:]) 


    # print("need to test Nested_Cache and iron out the rest of the decorators, before proceeding")
    # cache = Nested_Cache(["col1", "col2", "col3"]) #, [["a","b", "c"], [1,2,3],[4,5,6]])


    # cache = Nested_Cache(['b'],[[3]])

    # cache.set(row=2, location='c', data=3)

    # cache = Nested_Cache([], [])


    class C(BaseClass):
        @debug_log
        @validate()
        def foo(self, var1:int = 100):
            return True

        @debug_log
        @validate()
        def bar(self, var1:int):
            return True

        @debug_log
        @validate()
        def bat(self, var1 = 50):
            return True

        @debug_log
        @validate(var1=['gte:2'])
        def gte(self, var1:int):
            return True

        @debug_log
        @validate(var1=['gt:1'])
        def gt(self, var1:int):
            return True

        @debug_log
        @validate(var1=['ifSetType:dict'])
        def ifSetType(self, var1:dict=None):
            return True

        @debug_log
        @validate(var1=['contains:yes,no'])
        def contains(self, var1:str=None):
            return True

        @debug_log
        @validate(var1=['contains:yes'])
        def contains2(self, var1:str=None):
            return True


    var = C()

    var.ifSetType({'a': 1})
    var.ifSetType(None)

    var.ifSetType([1,2,3])
