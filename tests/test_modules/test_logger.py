import pytest, logging, configparser, re
from modules.loggers.exception import Logger_Exception
from modules.logger import Logger


def clean_logs_for_matching(logs):
    logs = str(logs)
    return re.sub("0x[0-9a-z]*", "classPointer", logs)

def test_clean_logs_for_matching():
    string = clean_logs_for_matching("0x37382hdd")
    assert string == "classPointer"


# this is the method for testing that python logging is working
def test_logging_default(caplog):
    with caplog.at_level(logging.INFO):
        logging.getLogger().info("boo %s", "arg")
        popped = caplog.record_tuples.pop()
        assert popped == ("root", logging.INFO, "boo arg")


def test_info(caplog):
    with caplog.at_level(logging.INFO):
        Logger.info("test")
        popped = caplog.record_tuples.pop()
        assert popped == ("logs", logging.INFO, "Logger:: test")


def test_warning(caplog):
    with caplog.at_level(logging.WARNING):
        Logger.warning("test")
        popped = caplog.record_tuples.pop()
        assert popped == ("logs", logging.WARNING, "Logger:: test")


def test_critical(caplog):
    with caplog.at_level(logging.CRITICAL):
        with pytest.raises(Logger_Exception) as excinfo:
            Logger.critical("test")
        assert excinfo.value.message == "Logged a critical issue: Logger:: test"
        popped = caplog.record_tuples.pop()
        assert popped == ("logs", logging.CRITICAL, "Logger:: test")


def test_error(caplog):
    with caplog.at_level(logging.ERROR):
        Logger.error("test")
        popped = caplog.record_tuples.pop()
        assert popped == ("logs", logging.ERROR, "Logger:: test")


def test_debug(caplog):
    with caplog.at_level(logging.DEBUG):
        Logger.debug("test")

        # without @Debugger decorator
        # assert caplog.record_tuples == [("logs", logging.DEBUG, "Logger:: test")] 
        popped = caplog.record_tuples.pop()
        # with debug decorator
        assert popped == ('logs', 10, 'Logger:: test')


def test_console(capsys):
    Logger.console("test")
    captured = capsys.readouterr()
    assert "  CONSOLE: Logger:: test\n" in captured.out

def testprepareString():

    assert "Logger:: test"                          == Logger.prepareString("test")
    assert "Logger:: testone,two"                   == Logger.prepareString("test", data={"one": 1, "two": 2})
    assert "prefix Logger:: testone,two"            == Logger.prepareString("test", data={"one": 1, "two": 2}, prefix="prefix ")
    assert "prefix Logger:: testone,twopostfix"    == Logger.prepareString("test", data={"one": 1, "two": 2}, prefix="prefix ", postfix="postfix")
    assert "prefix Logger:: testone,twopostfix"    == Logger.prepareString("test", data={"one": 1, "two": 2}, prefix="prefix ", postfix="postfix", textColor="dark_green")
    assert "prefix Logger:: testone,twopostfix"    == Logger.prepareString("test", data={"one": 1, "two": 2}, prefix="prefix ", postfix="postfix", textColor="dark_green", bgColor="white")
    assert "prefix Logger:: testone,twopostfix"    == Logger.prepareString("test", data={"one": 1, "two": 2}, prefix="prefix ", postfix="postfix", textColor="dark_green", bgColor="white", dataColor="white")
    assert "prefix Logger:: testone,twopostfix"    == Logger.prepareString("test", data={"one": 1, "two": 2}, prefix="prefix ", postfix="postfix", textColor="dark_green", bgColor="white", dataColor="white", dataBgColor="dark_green")
    assert "prefix Logger:: testpostfix"           == Logger.prepareString("test", data={"one": 1, "two": 2}, prefix="prefix ", postfix="postfix", textColor="dark_green", bgColor="white", dataColor="white", dataBgColor="dark_green", bypassReplace=True)

def test_insert_newlines():
    msg = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco"
    validation = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore\n\t\t\t\t\t\tet dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco"

    assert validation == Logger.insert_newlines(msg, 100)


def test_prefixStr():
    string = Logger.prefixStr("test", "~~~")
    assert "~~~test" == string

def test_methodNamePrefix():

    string = Logger.methodNamePrefix("__notinitmethod__")
    assert "\t\t\t\t" == string

def test_prefixMethonName():

    string = Logger.prefixMethodName("someMethod")
    assert "someMethod" == string

    string = Logger.prefixMethodName("__notinitmethod__")
    assert "\t\t\t\t__notinitmethod__" == string

def test_appendNewLines():
    # self, msg: str, new_lines: int=0):

    string = Logger.appendNewLines("message", 3)
    assert "message\n\n\n" == string

def test_postfixStr():
    # self, msg:str, postfix:str="", new_lines:int =0):
    
    string = Logger.postfixStr("message")
    assert "message" == string
    
    string = Logger.postfixStr("message", " ~~postfix")
    assert "message ~~postfix" == string
    
    string = Logger.postfixStr("message", " ~~postfix", 5)
    assert "message ~~postfix\n\n\n\n\n" == string


def test_method(caplog):
    # self, method:str, data:Typevar_List_Str=None):

    with caplog.at_level(logging.DEBUG):
        Logger.method("__notinitmethod__", {"one": 1, "two": 2})
        #without @Debugger decorator
        # assert caplog.record_tuples == [('logs', 10, 'Logger::                                __notinitmethod__one,two')]
        
        popped = caplog.record_tuples.pop()
        # print(f"popped={popped}")
        #with debug decorator
        assert popped == ('logs', 10, 'Logger::                                __notinitmethod__one,two')


def test_validation_method_debug(caplog):

    from modules.config import config_for_testing
    config_for_testing()

    with caplog.at_level(logging.DEBUG):
        Logger.validation_method_debug("methodName")
        Logger.validation_method_debug("methodName", {"one": 1, "two": 2})
        popped = caplog.record_tuples.pop()
        assert popped == ('logs', 10, 'Logger:: methodNameone,two')

def test_validation_method_debug2(caplog):
    from modules.config import config
    config()

    Logger.validation_method_debug("methodName")
    Logger.validation_method_debug("methodName", {"one": 1, "two": 2})

    assert caplog.record_tuples == []

def test_change_logger_name(caplog):    
    from modules.logger import logger_name
    logger_name.name = "TEST_LOGGER"
    
    with caplog.at_level(logging.ERROR):
        Logger.error("test")
        popped = caplog.record_tuples.pop()
        assert popped == ("logs", logging.ERROR, "TEST_LOGGER:: test")