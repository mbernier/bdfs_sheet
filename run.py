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


if __name__ == "__main__":
    # logger.debug("run.py running __main__")

    # Bdfs Sheet Processor functionality
    # run = BdfsInventory_SheetProcessor()
    # run.main(sys.argv[1:]) 
    

    # cache = Nested_Cache(locations=["one", "two", "three"])
    
    print(isinstance(False, bool))
    print(isinstance(False, int))

    print(isinstance(0, bool))
    print(isinstance(0, int))    