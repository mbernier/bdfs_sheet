import sys
from collections import OrderedDict
from pprint import pprint

from modules.caches.nested_cache.rows.row import Nested_Cache_Row
from modules.caches.exception import Nested_Cache_Row_Exception, Flat_Cache_Exception
from modules.config import config
from modules.decorator import debug_log, validate


# This is a wrapper for Nested_Cache on top of Flat Cache
#   in order to reduce the complexity in the Nested_Cache implementation
#   and to wrap Flat_Cache with the logic needed for Nested_Cache in a clean way.
#   A nested Cache Row can be created with values or not and can be written 
#   to the Flat Cache either way.
class Nested_Cache_Row_Data(Flat_Cache):

