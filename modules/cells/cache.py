import sys

from modules.caches.flat import Flat_Cache

class CellCache(Cache):

    logger_name = "CellCache"
    
    def __init__(self):
        print()