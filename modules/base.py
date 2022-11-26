#setup logging
import logging, sys
from termcolor import colored, cprint
from modules.config import config

from modules.logger import logger

class BaseClass:

    base_logger_name = "logs"
    logger_name = ""
    logger_configured = False

    def info(self, msg, data=None, new_lines=1, prefix=""):
        msg = self._prepareString(msg=msg, data=data, new_lines=new_lines, prefix=prefix, textColor="blue")
        logger.info(msg)


    def warning(self, msg, data=None, new_lines=2, prefix=""):
        msg = self._prepareString(msg=msg, data=data, new_lines=new_lines, prefix=prefix, textColor="magenta")
        logger.warning(msg)


    def error(self, msg, data=None, new_lines=3, prefix="\n\n\n"):
        msg = self._prepareString(msg=msg, data=data, new_lines=new_lines, prefix=prefix, textColor="yellow")
        logger.error(msg)


    def critical(self, msg, data=None, new_lines=3, prefix="\n\n\n"):
        msg = self._prepareString(msg=msg, data=data, new_lines=new_lines, prefix=prefix, textColor="red")
        logger.critical(msg)
        raise Exception("Logged a critical issue: " + msg)


    def debug(self, msg, data=None, new_lines=0, prefix=""):
        msg = self._prepareString(msg=msg, data=data, new_lines=new_lines, prefix=prefix, textColor="cyan")
        logger.debug(msg)

    # Output something to the console, if the config allows it
    # if we're in debug mode for the logs, set the console outputs aside by adding extra lines
    # default colors of Console: blue on grey
    def console(self, msg = None, data = None, new_lines=1, prefix="", postfix=""):

        if "DEBUG" == config.get("log_level"):
            if "" == prefix:
                prefix = "\n\n" + colored("CONSOLE: ", "white")
            if 1 == new_lines:
                new_lines = 2

        # only print to console if we are allowing it via config.ini `output_to_console`

        if config["output_to_console"]: 
            msg = self._prepareString(msg=msg, data=data, prefix=prefix, new_lines=new_lines, postfix=postfix, textColor="blue", dataColor="blue", dataBgColor="grey")

            # only print something if we pass something
            if None != msg:
                print(msg)


    # handle prefix and new_lines being added to the string, one call to do everything, reduce repetition above
    def _prepareString(self, msg, data=None, prefix=None, new_lines=0, postfix="", textColor="white", bgcolor=None, dataColor="white", dataBgColor=None) -> str:
        
        if None != bgcolor:
            bgcolor = "on_" + bgcolor

        if None != dataBgColor:
            dataBgColor = "on_" + dataBgColor

        # add the classname
        msg = self.__className() + ":: " + msg

        # change the color to make it pretty
        msg = colored(msg, textColor, bgcolor)

        if "{}" in msg:
            if isinstance(data, str):
                msg = msg.format(data)
            elif type(data) is tuple:
                msg = msg.format(*data)
            else:
                msg = msg.format(data)

        elif (None != data):
            data = colored(data, dataColor, dataBgColor)
            for _ in data:
                msg += "{}".format(data)

        msg = self.prefixStr(msg, prefix=prefix)
        msg = self.postfixStr(msg,postfix=postfix, new_lines=new_lines)
        return msg


    def prefixStr(self, msg:str, prefix: str=""):
        if None != prefix:
            msg = prefix + msg
        return msg


    def postfixStr(self, msg:str, postfix:str="", new_lines:int =0):
        msg = self.appendNewLines(msg, new_lines=new_lines)
        msg += postfix
        return msg


    def appendNewLines(self, msg: str, new_lines: int=0):
        nl_str = ""
        if new_lines > 0:
            for _ in range(new_lines):
                nl_str += "\n"

        #print the number of new lines requested
        return "{} {}".format(msg, nl_str)


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