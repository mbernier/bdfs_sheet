# setup_logger.py
import logging, sys
from modules.config import config
from modules.helper import Helper
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
    critical = True
    debug = False
    error = True
    info = True
    warning = True
    output_to_console = False

    def __init__(self):
        # allow this to be overriden in child classes
        if not self.debug:
            if "DEBUG" == config.get("log_level"):
                self.debug = True
        if not self.output_to_console:
            if config["output_to_console"]:
                self.output_to_console = True
        if config["critical_messages"]:
            self.info = config["critical_messages"]
        if config["error_messages"]:
            self.info = config["error_messages"]
        if config["info_messages"]:
            self.info = config["info_messages"]
        if config["warning_messages"]:
            self.info = config["warning_messages"]

    def info(self, msg, data=None, new_lines=1, prefix=""):
        msg = self._prepareString(msg=msg, data=data, new_lines=new_lines, prefix=prefix, textColor="blue")
        if self.info:
            logger.info(msg)


    def warning(self, msg, data=None, new_lines=2, prefix=""):
        msg = self._prepareString(msg=msg, data=data, new_lines=new_lines, prefix=prefix, textColor="magenta")
        if self.warning:
            logger.warning(msg)


    def error(self, msg, data=None, new_lines=3, prefix="\n\n\n"):
        msg = self._prepareString(msg=msg, data=data, new_lines=new_lines, prefix=prefix, textColor="yellow")
        if self.error:
            logger.error(msg)


    def critical(self, msg, data=None, new_lines=3, prefix="\n\n\n"):
        msg = self._prepareString(msg=msg, data=data, new_lines=new_lines, prefix=prefix, textColor="red")
        if self.critical:
            logger.critical(msg)
        raise Exception("Logged a critical issue: " + msg)


    def debug(self, msg, data=None, new_lines=0, prefix=""):
        msg = self._prepareString(msg=msg, data=data, new_lines=new_lines, prefix=prefix, textColor="cyan")
        if self.debug:
            logger.debug(msg)

    # Output something to the console, if the config allows it
    # if we're in debug mode for the logs, set the console outputs aside by adding extra lines
    # default colors of Console: blue on grey
    def console(self, msg = None, data = None, new_lines=1, prefix="", postfix=""):

        if self.debug:
            if "" == prefix:
                prefix = "\n\n" + colored("CONSOLE: ", "white")
            if 1 == new_lines:
                new_lines = 2

        # only print to console if we are allowing it via config.ini `output_to_console`

        if self.output_to_console:
            msg = self._prepareString(msg=msg, data=data, prefix=prefix, new_lines=new_lines, postfix=postfix, textColor="blue", dataColor="blue", dataBgColor="grey")

            # only print something if we pass something
            if None != msg:
                print(msg)


    # handle prefix and new_lines being added to the string, one call to do everything, reduce repetition above
    def _prepareString(self, msg, data=None, prefix=None, new_lines=0, postfix="", textColor="white", bgcolor=None, dataColor="white", dataBgColor=None, bypassReplace=False) -> str:
        # logger.debug("_prepareString(self={}, msg={},data={},prefix={},new_lines={},postfix={},textcolor={},bgcolor={},dataColor={},dataBgColor={},bypassReplace={})".format(locals()))
        if None != bgcolor:
            bgcolor = "on_" + bgcolor

        if None != dataBgColor:
            dataBgColor = "on_" + dataBgColor

        # add the classname
        msg = self.__className() + ":: " + msg

        # change the color to make it pretty
        msg = colored(msg, textColor, bgcolor)

        if bypassReplace == False:
            if None != data:
                if "{}" in msg:
                    if isinstance(data, str):
                        msg = msg.format(data)
                    elif type(data) is tuple:
                        msg = msg.format(*data)
                    else:
                        # print(msg)
                        msg = msg.format(data)
                else:
                    data = colored(data, dataColor, dataBgColor)
                    if type(data) is str:
                        msg += data
                    else:
                        msg += ",".join(data)

        msg = self.prefixStr(msg, prefix=prefix)
        msg = self.postfixStr(msg,postfix=postfix, new_lines=new_lines)

        return self.insert_newlines(msg)

    def insert_newlines(self, string, every=100):
        # return '\n\t\t\t\t\t\t'.join(string[i:i+every] for i in range(0, len(string), every))

        import textwrap
        return textwrap.fill(string, every).replace("\n", "\n\t\t\t\t\t\t")

    def prefixStr(self, msg:str, prefix: str=""):
        if None != prefix:
            msg = prefix + msg
        return msg

    # returns the methodName with the prefix
    @staticmethod
    def prefixMethodName(methodName):
        return Logger.methodNamePrefix(methodName) + methodName

    # returns only the prefix
    @staticmethod
    def methodNamePrefix(methodName):
        prefix = ""
        if not methodName in ["__init__"]:
            spltz = methodName.count("_")
            for _ in range(0,spltz): 
                prefix += "\t"

        return prefix

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
    def _method(self, method, data=None):
        #indent the method
        method = Logger.prefixMethodName(method)

        if not None == data:
            if not Helper.is_dict(data):
                raise Exception("_method expects params as a dict, suggest using locals(). {} was passed".format(data))

        self.debug(msg=method, data=data)


    def __prepareMethodString(self, method, data):
        methodAdditions = self.__createMethodAdditions(data)
        return self.__createMethodString(method, methodAdditions)


    def __createMethodAdditions(self, data):
        # if this is empty, return empty list
        if {} == data: return []

        methodAdditions = []            
        if not data == None:
            if Helper.is_str(data):
                methodAdditions.append(data)
            else:
                for paramName in data:
                    dataToPass = data[paramName]
                    methodAdditions.append(self.__createParamDataValueString(paramName=paramName, paramData=dataToPass))
        return methodAdditions


    def __createMethodString(self, methodName: str, methodAdditions: list):
        return "{}({})".format(methodName, (",").join(map(str, methodAdditions)))


    def __createParamDataValueString(self, paramName, paramData):
        return "{}={}".format(paramName, paramData)