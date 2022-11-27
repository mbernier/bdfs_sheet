import sys

#setup logging
import logging
# from modules.sheetProcessors.bdfs_inventory import BdfsInventory_SheetProcessor
# from modules.caches.nested import NestedCache
from modules.base import BaseClass


from modules.logger import logger

if __name__ == "__main__":
    logger.debug("run.py running __main__")

    # Bdfs Sheet Processor functionality
    # run = BdfsInventory_SheetProcessor()
    # run.main(sys.argv[1:]) 


    # outside ur class
    def setupMethod(validate=None):
        def wrapper(func, *args, **kwargs):
            def wrapper_f(self, *args, **kwargs):
                # print(func)
                # print(args)
                # print(kwargs)
                #call the debug method
                self._method(func.__name__, args, kwargs)

                if () == args:




                    # @todo add validations here! 




                    func(self)
                elif {} != kwargs:
                    func(self, args, kwargs)
                else:
                    func(self, args)
            return wrapper_f
        return wrapper

    class A(BaseClass):
        @setupMethod(validate=["location","data"])
        def foo(self):
            pass

        @setupMethod()
        def bar(self, args):
            pass

        @setupMethod()
        def bat(self, var1=None, var2=None):
            pass

    var = A()
    var.foo()
    var.bar("hello")
    var.bat(2, "4")
    var.bat(1, var2="3")