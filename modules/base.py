#setup logging
import sys
from modules.config import config
from modules.decorators import debug, validate
from modules.logger import Logger


class BaseClass(Logger):

    #does list1 contain everything in list2?
    def compareLists(self, list1, list2) -> list:
        self.debug("BaseClass.compareLists({},{})", (list1, list2))
        
        result =  all(elem in list1 for elem in list2)
        self.info("List 1 {} contain all the items in list2", ("does" if(result) else "does not"))
        
        return result


    def importClass(self, name): 
        self.debug("importClass(name={})".format(name))
        # components = name.split('.')
        # mod = __import__(components[0])
        # for comp in components[1:]:
        #     mod = getattr(mod, comp)
        # return mod

        spltz = name.split(".")
        classname = spltz.pop()
        path = ".".join(spltz)
        mod = __import__(path, fromlist=[classname])
        klass = getattr(mod, classname)
        return klass



    def __checkArgs(self, required=[], **kwargs):
        for arg in kwargs:
            if arg in required and None == kwargs[arg]:
                raise Exception("You must pass {} to Cache, NoneType was found".format(arg))

    # cheater method to make setting debug statements a little faster
    def __className(self):
        return self.__class__.__name__
