import sys

from modules.caches.flat import FlatCache

class CellCache(Cache):

    logger_name = "CellCache"
    
    def __init__(self):
        print()