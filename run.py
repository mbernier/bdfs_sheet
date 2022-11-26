import sys

#setup logging
import logging
from modules.sheetProcessors.bdfs_inventory import BdfsInventory_SheetProcessor

from modules.logger import logger

if __name__ == "__main__":
    logger.debug("run.py running __main__")

    # Bdfs Sheet Processor functionality
    run = BdfsInventory_SheetProcessor()
    run.main(sys.argv[1:]) 