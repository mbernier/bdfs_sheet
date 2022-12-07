import sys
from modules.config import config
from modules.decorator import debug_log, validate
from modules.helper import Helper
from modules.logger import Logger


class BaseClass(Logger):

    ####
    #
    # Dynamically call Classes and Methods
    #
    ####

    @debug_log
    def importClass(self, modulePath): 
        spltz = modulePath.split(".")
        classname = spltz.pop()
        path = ".".join(spltz)
        mod = __import__(path, fromlist=[classname])
        klass = getattr(mod, classname)
        return klass