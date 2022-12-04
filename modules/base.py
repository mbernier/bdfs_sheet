import sys
from modules.config import config
from modules.decorator import debug, validate
from modules.helper import Helper
from modules.logger import Logger


class BaseClass():

    ####
    #
    # Dynamically call Classes and Methods
    #
    ####

    @debug
    def importClass(self, name): 
        logger.debug("importClass(name={})".format(name))

        spltz = name.split(".")
        classname = spltz.pop()
        path = ".".join(spltz)
        mod = __import__(path, fromlist=[classname])
        klass = getattr(mod, classname)
        return klass

    # cheater method to make setting debug statements a little faster
    @debug
    def __className(self):
        return Helper.className(self)

    @debug
    def __callMethod(self, methodName:str, **kwargs):
        return Helper.callMethod(self, methodName, *kwargs)
