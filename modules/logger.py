# setup_logger.py
import logging, sys
from pydantic import BaseModel as PydanticBaseModel
from modules.config import config
from modules.helper import Helper
from modules.loggers.exception import Logger_Exception
from termcolor import colored, cprint
from typing import TypeVar, List

Typevar_List_Str = TypeVar("Typevar_List_Str", list, str)

#get the log_level from the config.ini
#we are grabbing the attribute of the log_level from the logging object here, not just setting a string
logging_level = getattr(logging, config("log_level"))

#setup the level of logging we care about
logging.basicConfig(level=logging_level)

#define the main logger object
logger = logging.getLogger('logs')


class Logger():
    base_logger_name = "logs"
    logger_name = ""
    logger_configured = False
    output_to_console = False

    def info(msg:str, data=None, new_lines:int=1, prefix:str=""):
        # print(f"msg={msg}")
        msg = Logger.prepareString(msg=msg, data=data, new_lines=new_lines, prefix=prefix, textColor="blue")
        logger.info(msg)


    def warning(msg:str, data=None, new_lines:int=1, prefix:str=""):
        # print(f"msg={msg}")
        msg = Logger.prepareString(msg=msg, data=data, new_lines=new_lines, prefix=prefix, textColor="magenta")    
        logger.warning(msg)


    def error(msg:str, data=None, new_lines:int=1, prefix=""):
        # print(f"msg={msg}")
        msg = Logger.prepareString(msg=msg, data=data, new_lines=new_lines, prefix=prefix, textColor="yellow")
        logger.error(msg)

    def critical(msg:str, data=None, new_lines:int=1, prefix:str=""):
        # print(f"msg={msg}")
        msg = Logger.prepareString(msg=msg, data=data, new_lines=new_lines, prefix=prefix, textColor="red")
        logger.critical(msg)
        raise Logger_Exception("Logged a critical issue: " + msg)

    @staticmethod
    def debug(msg:str, data=None, new_lines:int=0, prefix:str=""):
        # print(f"msg={msg}")
        msg = Logger.prepareString(msg=msg, data=data, new_lines=new_lines, prefix=prefix, textColor="cyan")
        logger.debug(msg)

    # Output something to the console, if the config allows it
    # if we're in debug mode for the logs, set the console outputs aside by adding extra lines
    # default colors of Console: blue on grey
    @staticmethod
    def console(msg:str=None, data=None, new_lines:int=1, prefix:str="", postfix:str=""):

        if "" == prefix:
            prefix = "\n\n" + colored("CONSOLE: ", "white")
        if 1 == new_lines:
            new_lines = 2

        # only print to console if we are allowing it via config.ini `output_to_console`

        if True == config("output_to_console"):
            # print(f"msg={msg}")
            msg = Logger.prepareString(msg=msg, data=data, prefix=prefix, new_lines=new_lines, postfix=postfix, textColor="blue", dataColor="blue", dataBgColor="grey")

            # only print something if we pass something
            if None != msg:
                print(msg)


    # handle prefix and new_lines being added to the string, one call to do everything, reduce repetition above
    @staticmethod
    def prepareString(msg:str, data=None, prefix:str=None, new_lines:int=0, postfix:str="", textColor:str="white", bgColor:str=None, dataColor:str="white", dataBgColor:str=None, bypassReplace:bool=False) -> str:
        if None != bgColor:
            bgColor = "on_" + bgColor

        if None != dataBgColor:
            dataBgColor = "on_" + dataBgColor

        # add the classname
        msg = Logger.logger_name + ":: " + msg

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

        msg = Logger.prefixStr(msg, prefix=prefix)
        msg = Logger.postfixStr(msg,postfix=postfix, new_lines=new_lines)

        return Logger.insert_newlines(msg)

    @staticmethod
    def insert_newlines(string:str, every:int=115):
        # return '\n\t\t\t\t\t\t'.join(string[i:i+every] for i in range(0, len(string), every))

        import textwrap
        return textwrap.fill(string, every).replace("\n", "\n\t\t\t\t\t\t")

    @staticmethod
    def prefixStr(msg:str, prefix: str=""):
        if None != prefix:
            msg = prefix + msg
        return msg

    # returns the methodName with the prefix
    @staticmethod
    def prefixMethodName(methodName:str):
        return Logger.methodNamePrefix(methodName) + methodName

    # returns only the prefix
    @staticmethod
    def methodNamePrefix(methodName:str):
        prefix = ""
        if not methodName in ["__init__"]:
            spltz = methodName.count("_")
            for _ in range(0,spltz): 
                prefix += "\t"

        return prefix

    @staticmethod
    def postfixStr(msg:str, postfix:str="", new_lines:int =0):
        msg += postfix
        msg = Logger.appendNewLines(msg, new_lines=new_lines)
        return msg

    @staticmethod
    def appendNewLines(msg: str, new_lines: int=0):
        nl_str = ""
        if new_lines > 0:
            for _ in range(new_lines):
                nl_str += "\n"

        #print the number of new lines requested
        return "{}{}".format(msg, nl_str)


    # created the debug string, by calling like so:
    # e.g. Logger.method("nameofMethod", locals())
    @staticmethod
    def method(method:str, data=None):
        #indent the method
        method = Logger.prefixMethodName(method)

        Logger.debug(msg=method, data=data)


    # only allow the validation debug to be written if the flag is on in config.ini
    @staticmethod
    def validation_method_debug(method, data=None):

        if True == config("debug_validations"):
            Logger.method(method, data)

    @staticmethod
    def prepareMethodString(method, data):
        methodParams = Logger.createMethodSignature(data)
        return Logger.createMethodString(method, methodParams)

    @staticmethod
    def createMethodSignature(data):
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


    @staticmethod
    def createMethodString(methodName: str, methodAdditions: list):
        return "{}({})".format(methodName, (",").join(map(str, methodAdditions)))


    @staticmethod
    def createParamDataValueString(paramName, paramData):
        return "{}={}".format(paramName, paramData)