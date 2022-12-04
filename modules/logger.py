# setup_logger.py
import logging, sys
from modules.config import config
from modules.helper import Helper
from modules.decorator import debug_log, validate
from modules.loggers.exception import Logger_Exception
from termcolor import colored, cprint
from typing import TypeVar, List

Typevar_List_Str = TypeVar("Typevar_List_Str", list, str)

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
    _debug = False
    logger_configured = False
    output_to_console = False

    @debug_log
    def __init__(self):
        # print("Logger:__init__")
        # allow this to be overriden in child classes

        if not self._debug:
            if "DEBUG" == config["log_level"]:
                self._debug = True

        if not self.output_to_console:
            if config.getboolean("output_to_console"):
                self.output_to_console = True

    @debug_log
    @validate()
    def info(self, msg:str, data=None, new_lines:int=1, prefix:str=""):
        # print(f"msg={msg}")
        msg = self._prepareString(msg=msg, data=data, new_lines=new_lines, prefix=prefix, textColor="blue")
        logger.info(msg)

    @debug_log
    @validate()
    def warning(self, msg:str, data=None, new_lines:int=1, prefix:str=""):
        # print(f"msg={msg}")
        msg = self._prepareString(msg=msg, data=data, new_lines=new_lines, prefix=prefix, textColor="magenta")    
        logger.warning(msg)

    @debug_log
    @validate()
    def error(self, msg:str, data=None, new_lines:int=1, prefix=""):
        # print(f"msg={msg}")
        msg = self._prepareString(msg=msg, data=data, new_lines=new_lines, prefix=prefix, textColor="yellow")
        logger.error(msg)

    @debug_log
    @validate()
    def critical(self, msg:str, data=None, new_lines:int=1, prefix:str=""):
        # print(f"msg={msg}")
        msg = self._prepareString(msg=msg, data=data, new_lines=new_lines, prefix=prefix, textColor="red")
        logger.critical(msg)
        raise Logger_Exception("Logged a critical issue: " + msg)

    # @debug_log # these create an infinite loop, not great
    # @validate()
    def debug(self, msg:str, data=None, new_lines:int=0, prefix:str=""):
        # print(f"msg={msg}")
        msg = self._prepareString(msg=msg, data=data, new_lines=new_lines, prefix=prefix, textColor="cyan")
        logger.debug(msg)

    # Output something to the console, if the config allows it
    # if we're in debug mode for the logs, set the console outputs aside by adding extra lines
    # default colors of Console: blue on grey
    @debug_log
    @validate()
    def console(self, msg:str=None, data=None, new_lines:int=1, prefix:str="", postfix:str=""):

        if "" == prefix:
            prefix = "\n\n" + colored("CONSOLE: ", "white")
        if 1 == new_lines:
            new_lines = 2

        # only print to console if we are allowing it via config.ini `output_to_console`

        if self.output_to_console:
            # print(f"msg={msg}")
            msg = self._prepareString(msg=msg, data=data, prefix=prefix, new_lines=new_lines, postfix=postfix, textColor="blue", dataColor="blue", dataBgColor="grey")

            # only print something if we pass something
            if None != msg:
                print(msg)


    # handle prefix and new_lines being added to the string, one call to do everything, reduce repetition above
    # @debug_log
    # @validate()
    def _prepareString(self, msg:str, data=None, prefix:str=None, new_lines:int=0, postfix:str="", textColor:str="white", bgColor:str=None, dataColor:str="white", dataBgColor:str=None, bypassReplace:bool=False) -> str:
        # logger.debug("_prepareString(self={}, msg={},data={},prefix={},new_lines={},postfix={},textcolor={},bgColor={},dataColor={},dataBgColor={},bypassReplace={})".format(locals()))
        if None != bgColor:
            bgColor = "on_" + bgColor

        if None != dataBgColor:
            dataBgColor = "on_" + dataBgColor

        # add the classname
        msg = self.__className() + ":: " + msg

        # change the color to make it pretty
        msg = colored(msg, textColor, bgColor)

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

    # @debug_log
    # @validate()
    def insert_newlines(self, string:str, every:int=100):
        # return '\n\t\t\t\t\t\t'.join(string[i:i+every] for i in range(0, len(string), every))

        import textwrap
        return textwrap.fill(string, every).replace("\n", "\n\t\t\t\t\t\t")

    # @debug_log
    # @validate()
    def prefixStr(self, msg:str, prefix: str=""):
        if None != prefix:
            msg = prefix + msg
        return msg

    # returns the methodName with the prefix
    @staticmethod
    # @debug_log
    # @validate()
    def prefixMethodName(methodName:str):
        return Logger.methodNamePrefix(methodName) + methodName

    # returns only the prefix
    @staticmethod
    # @debug_log
    # @validate()
    def methodNamePrefix(methodName:str):
        prefix = ""
        if not methodName in ["__init__"]:
            spltz = methodName.count("_")
            for _ in range(0,spltz): 
                prefix += "\t"

        return prefix

    # @debug_log
    # @validate()
    def postfixStr(self, msg:str, postfix:str="", new_lines:int =0):
        msg += postfix
        msg = self.appendNewLines(msg, new_lines=new_lines)
        return msg

    # @debug_log # causes recursion
    # @validate()
    def appendNewLines(self, msg: str, new_lines: int=0):
        nl_str = ""
        if new_lines > 0:
            for _ in range(new_lines):
                nl_str += "\n"

        #print the number of new lines requested
        return "{}{}".format(msg, nl_str)


    # cheater method to make setting debug statements a little faster
    # @debug_log # causes recursion 
    # @validate()
    def __className(self):
        return self.__class__.__name__


    # created the debug string, by calling like so:
    # e.g. self.__method("nameofMethod", locals())
    # @debug_log # causes recursion
    # @validate()
    def _method(self, method:str, data=None):
        #indent the method
        method = Logger.prefixMethodName(method)

        # print(f"method={method}, data={data}")

        self.debug(msg=method, data=data)


    # only allow the validation debug to be written if the flag is on in config.ini
    # @debug_log # causes recursion
    # @validate()
    def validation_method_debug(self, method, data=None):
        if config["debug_validations"]:
            self._method(method, data)

    @debug_log
    @validate()
    def __prepareMethodString(self, method, data):
        methodParams = self.__createMethodSignature(data)
        return self.__createMethodString(method, methodParams)

    @debug_log
    @validate()
    def __createMethodSignature(self, data):
        # if this is empty, return empty list
        if {} == data: return ""

        signature = ""

        # make it easy, in case a string was sent, pass that straight through
        if not data == None:
            if Helper.is_str(data):
                signature = data
            else:
                # modified from the debug decorators intro documentation
                data_repr = [f"{k}={v!r}" for k, v in data.items()]
                signature = ", ".join(data_repr)

        return signature


    @debug_log
    def __createMethodString(self, methodName: str, methodAdditions: list):
        return "{}({})".format(methodName, (",").join(map(str, methodAdditions)))


    @debug_log
    def __createParamDataValueString(self, paramName, paramData):
        return "{}={}".format(paramName, paramData)