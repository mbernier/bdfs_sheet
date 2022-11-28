# setup_logger.py
import logging, sys
from modules.config import config
from termcolor import colored, cprint

#get the log_level from the config.ini
#we are grabbing the attribute of the log_level from the logging object here, not just setting a string
logging_level = getattr(logging, config["log_level"])
#setup the level of logging we care about
logging.basicConfig(level=logging_level)
#define the main logger object
logger = logging.getLogger('logs') 

class Logger:
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

    # cheater method to make setting debug statements a little faster
    def __className(self):
        return self.__class__.__name__


   # created the debug string, by calling like so:
    # e.g. self.__method("nameofMethod", locals())
    def _method(self, method, *args, **kwargs):
        self.debug(self.__prepareMethodString(method, args, kwargs)) 


    def __prepareMethodString(self, method, args, kwargs):
        tupleAdditions = self.__createTupleAdditions(args)
        methodAdditions = self.__createMethodAdditions(kwargs)
        return self.__createMethodString(method, tupleAdditions, methodAdditions)


    def __createTupleAdditions(self, args):
        if () == args: return []
        return list(args)


    def __createMethodAdditions(self, data):
        if {} == data: return []

        methodAdditions = []            
        for paramName in data:
            methodAdditions.append(self.__createParamDataValueString(paramName=paramName, paramData=data[paramName]))
        return methodAdditions

    def __createParamDataValueString(self, paramName, paramData):
        return "{}={}".format(paramName, paramData)

    def __createMethodString(self, methodName: str, tupleAdditions, methodAdditions: list):
        # print(tupleAdditions)
        # print(methodAdditions)
        additions = tupleAdditions + methodAdditions
        # print(additions)
        return "{}({})".format(methodName, (",").join(map(str, additions)))