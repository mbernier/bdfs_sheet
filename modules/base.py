#setup logging
import logging, sys
from termcolor import colored, cprint

class BaseClass:
    logger = None
    logger_name = None
    output_to_console = False
    config = []

    def __init__(self):
        from modules.logger import logger
        from modules.config import config

        #make the config obj available to all sub objects
        self.config = config

        log_name = "logs"

        #set up the logger properly
        self.logger = logger

        if None != self.logger_name:
            #define a sub-logger just for this code
            log_name += '.' + self.logger_name
            self.debug("New Logger Name: " + log_name, new_lines=0)
        
            # grab the current instance of the logger object, if this is a sub-logger the logging lib will handle this for you
            self.logger = logging.getLogger(log_name)

        # are we allowing the script to print to the console?
        self.output_to_console = self.config["output_to_console"]
        self.debug("output_to_console = " + self.output_to_console)


    def info(self, str, new_lines=1, prefix=""):
        str = self._prepareString(str, new_lines=new_lines, prefix=prefix, textColor="blue")
        self.logger.info(str)


    def warning(self, str, new_lines=2, prefix=""):
        str = self._prepareString(str, new_lines=new_lines, prefix=prefix, textColor="magenta")
        self.logger.warning(str)


    def error(self, str, new_lines=3, prefix="\n\n\n"):
        str = self._prepareString(str, new_lines=new_lines, prefix=prefix, textColor="yellow")
        self.logger.error(str)


    def critical(self, str, new_lines=3, prefix="\n\n\n"):
        str = self._prepareString(str, new_lines=new_lines, prefix=prefix, textColor="red")
        self.logger.critical(str)


    def debug(self, str, new_lines=0, prefix=""):
        str = self._prepareString(str, new_lines=new_lines, prefix=prefix, textColor="cyan")
        self.logger.debug(str)


    # Output something to the console, if the config allows it
    # if we're in debug mode for the logs, set the console outputs aside by adding extra lines
    # default colors of Console: blue on grey
    def console(self, str = None, new_lines=1, prefix="", postfix=""):

        if "DEBUG" == self.config["log_level"]:
            if "" == prefix:
                prefix = "\n\n" + colored("CONSOLE: ", "white")
            if 1 == new_lines:
                new_lines = 2

        # only print to console if we are allowing it via config.ini `output_to_console`
        if self.output_to_console: 
            str = self._prepareString(str, prefix=prefix, new_lines=new_lines, postfix=postfix, textColor="blue", bgcolor="grey")

            # only print something if we pass something
            if None != str:
                print(str)


    # handle prefix and new_lines being added to the string, one call to do everything, reduce repetition above
    def _prepareString(self, str, prefix=None, new_lines=0, postfix="", textColor="white", bgcolor=None) -> str:
        
        if None != bgcolor:
            bgcolor = "on_" + bgcolor

        str = colored(str, textColor, bgcolor)
        str = self.prefixStr(str, prefix=prefix)
        str = self.postfixStr(str,postfix=postfix, new_lines=new_lines)
        return str


    def prefixStr(self, str:str, prefix: str=""):
        if None != prefix:
            str = prefix + str
        return str


    def postfixStr(self, str:str, postfix:str="", new_lines:int =0):
        str = self.appendNewLines(str, new_lines=new_lines)
        str += postfix
        return str


    def appendNewLines(self, str: str, new_lines: int=0):
        nl_str = ""
        if new_lines > 0:
            for _ in range(new_lines):
                nl_str += "\n"

        #print the number of new lines requested
        return "{} {}".format(str, nl_str)


    #does list1 contain everything in list2?
    def compareLists(self, list1, list2) -> list:
        self.debug("BaseClass.compareLists({},{})".format(list1, list2))
        
        result =  all(elem in list1 for elem in list2)
        self.info("List 1 {} contain all the items in list2".format("does" if(result) else "does not"))
        
        return result