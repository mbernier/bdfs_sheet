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

    # class A(BaseClass):

    #     @validate(var1=['isType:int'], var2 = ['exists', 'notNone'])
    #     def bat(self, var1=None, var2=None):
    #         pass

    #     @validate(var2=['orExists:var3'])
    #     def foo(self, var1=None, var2=None, var3=None):
    #         pass

    #     @validate(var2=['orExists:var3'])
    #     def foo2(self, var1, var2, var3=None):
    #         pass


    #     @validate(var1=['notNone'], var2=['notNone'])
    #     def positional(self, var1, var2):
    #         pass

    #     @validate(var1=['notNone'], var2=['notNone'],var3=['notNone'], var4=['notNone'])
    #     def annotations_with_validate_set(self, var1:int, var2:list, var3:dict, var4:str):
    #         pass

    #     @validate(var1=['notNone'], var2=['notNone'])
    #     def annotations_without_validate_set(self, var1:int, var2:list, var3:dict, var4:str):
    #         pass
    class A(BaseClass):

        @validate(var1=['isType:int'], var2 = ['notNone'])
        def bat(self, var1=None, var2=None):
            return True

        @validate(var2=['oneIsNotNone:var3'])
        def foo(self, var1=None, var2=None, var3=None):
            return True

        @validate(var2=['oneIsNotNone:var3'])
        def foo2(self, var1, var2, var3=None):
            pass

        @validate(var1=['notNone'], var2=['notNone'])
        def positional(self, var1, var2):
            pass

        @validate(var1=['notNone'], var2=['notNone'],var3=['notNone'], var4=['notNone'])
        def annotations_with_validate_set(self, var1:int, var2:list, var3:dict, var4:str):
            return True

        @validate(var1=['notNone'], var2=['notNone'])
        def annotations_without_validate_set(self, var1:int, var2:list, var3:dict, var4:str):
            return True

    var = A()
    var.foo(1, "Something Here", None)


    # var.annotations_without_validate_set(var1=1, var2={}, var3={}, var4="some string")

