import sys, logging
from inspect import signature
from modules.base import BaseClass
from modules.helper import Helper
from modules.decorator import debug_log, validate
from modules.caches.nested import Nested_Cache
from modules.caches.nested_cache.rows.location import Nested_Cache_Row_Location
from modules.caches.exception import Nested_Cache_Row_Exception
from modules.validations.exception import Validation_Exception

from modules.logger import Logger
from modules.sheetProcessors.bdfs_inventory import BdfsInventory_SheetProcessor
from pydoc import locate

if __name__ == "__main__":
    # logger.debug("run.py running __main__")

    # # Bdfs Sheet Processor functionality
    # run = BdfsInventory_SheetProcessor()
    # run.main(sys.argv[1:]) 


    thing = "list"
    thing2 = [1,2,3]
    typeThing = locate(thing)
    print(type(typeThing))
    # print(dir(type(typeThing)))
    print(typeThing)
    print(type(thing))

    print(typeThing is type(typeThing))
    print(typeThing is eval(thing))
    print(isinstance(typeThing, eval(thing)))
    print(isinstance(typeThing, type(thing)))
    print(typeThing is list)
    print(isinstance(typeThing, list))

    print(thing2 is eval(thing))
    # print(isinstance(thing2, thing))
    print(isinstance(thing2, typeThing))