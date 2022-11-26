import sys

#setup logging
import logging
from modules.sheetProcessors.bdfs_inventory import BdfsInventory_SheetProcessor
from modules.caches.nested import NestedCache

from modules.logger import logger

if __name__ == "__main__":
    logger.debug("run.py running __main__")

    # Bdfs Sheet Processor functionality
    # run = BdfsInventory_SheetProcessor()
    # run.main(sys.argv[1:]) 

    cache = NestedCache(['b','c','d'],[[3],[3,4],[5,1,5]])
    cache.set(row=3,location="d",data=4)
    cache.delete(row=2, location="c")
    assert 2 == cache.width()
    cache.delete(row=1, location="c")
    assert 1 == cache.width()