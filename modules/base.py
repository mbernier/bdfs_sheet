import sys
from pydantic import BaseModel as PydanticBaseModel
from modules.config import config
from modules.decorator import Debugger
from modules.helper import Helper
from modules.logger import Logger



class BaseClass():
    class Config:
        arbitrary_types_allowed = True
    ####
    #
    # Dynamically call Classes and Methods
    #
    ####

    @Debugger
    def importClass(self, modulePath): 
        spltz = modulePath.split(".")
        classname = spltz.pop()
        path = ".".join(spltz)
        mod = __import__(path, fromlist=[classname])
        klass = getattr(mod, classname)
        return klass

    # cheater method to make setting debug statements a little faster
    @Debugger
    def className(self):
        return self.__class__.__name__
    
    #placeholder method, allows Source/Destination subclasses to call this and raise protection exceptions
    @Debugger
    def __modifiesData(self):
        pass