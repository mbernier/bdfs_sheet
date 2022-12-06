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
    def importClass(self, name): 
        # print("BaseClass: importClass")
        logger.debug("importClass(name={})".format(name))

        spltz = name.split(".")
        classname = spltz.pop()
        path = ".".join(spltz)
        mod = __import__(path, fromlist=[classname])
        klass = getattr(mod, classname)
        return klass

    # cheater method to make setting debug statements a little faster
    @debug_log
    def __className(self):
        return Helper.className(self)

    @debug_log
    def __callMethod(self, methodName:str, **kwargs):
        return Helper.callMethod(klass=self, methodName=methodName, **kwargs)
