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
        logger = Logger()
        logger.info("test")
        popped = caplog.record_tuples.pop()
        assert popped == ("logs", logging.INFO, "Logger:: test")


def test_warning(caplog):
    with caplog.at_level(logging.WARNING):
        logger = Logger()
        logger.warning("test")
        popped = caplog.record_tuples.pop()
        assert popped == ("logs", logging.WARNING, "Logger:: test")


def test_critical(caplog):
    with caplog.at_level(logging.CRITICAL):
        logger = Logger()
        with pytest.raises(Logger_Exception) as excinfo:
            logger.critical("test")
        assert excinfo.value.message == "Logged a critical issue: Logger:: test"
        popped = caplog.record_tuples.pop()
        assert popped == ("logs", logging.CRITICAL, "Logger:: test")


def test_error(caplog):
    with caplog.at_level(logging.ERROR):
        logger = Logger()
        logger.error("test")
        popped = caplog.record_tuples.pop()
        assert popped == ("logs", logging.ERROR, "Logger:: test")


def test_debug(caplog):
    with caplog.at_level(logging.DEBUG):
        logger = Logger()
        logger.debug("test")

        # without @Debugger decorator
        # assert caplog.record_tuples == [("logs", logging.DEBUG, "Logger:: test")] 
        popped = caplog.record_tuples.pop()
        # with debug decorator
        assert popped == ('logs', 10, 'Logger:: test')


def test_console(capsys):
    logger = Logger()
    logger.console("test")
    captured = capsys.readouterr()
    assert "  CONSOLE: Logger:: test\n" in captured.out

def test_prepareString():
    logger = Logger()

    assert "Logger:: test"                          == logger._prepareString("test")
    assert "Logger:: testone,two"                   == logger._prepareString("test", data={"one": 1, "two": 2})
    assert "prefix Logger:: testone,two"            == logger._prepareString("test", data={"one": 1, "two": 2}, prefix="prefix ")
    assert "prefix Logger:: testone,twopostfix"    == logger._prepareString("test", data={"one": 1, "two": 2}, prefix="prefix ", postfix="postfix")
    assert "prefix Logger:: testone,twopostfix"    == logger._prepareString("test", data={"one": 1, "two": 2}, prefix="prefix ", postfix="postfix", textColor="dark_green")
    assert "prefix Logger:: testone,twopostfix"    == logger._prepareString("test", data={"one": 1, "two": 2}, prefix="prefix ", postfix="postfix", textColor="dark_green", bgColor="white")
    assert "prefix Logger:: testone,twopostfix"    == logger._prepareString("test", data={"one": 1, "two": 2}, prefix="prefix ", postfix="postfix", textColor="dark_green", bgColor="white", dataColor="white")
    assert "prefix Logger:: testone,twopostfix"    == logger._prepareString("test", data={"one": 1, "two": 2}, prefix="prefix ", postfix="postfix", textColor="dark_green", bgColor="white", dataColor="white", dataBgColor="dark_green")
    assert "prefix Logger:: testpostfix"           == logger._prepareString("test", data={"one": 1, "two": 2}, prefix="prefix ", postfix="postfix", textColor="dark_green", bgColor="white", dataColor="white", dataBgColor="dark_green", bypassReplace=True)

def test_insert_newlines():
    logger = Logger()
    msg = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco"
    validation = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore\n\t\t\t\t\t\tet dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco"

    assert validation == logger.insert_newlines(msg, 100)


def test_prefixStr():
    logger = Logger()
    string = logger.prefixStr("test", "~~~")
    assert "~~~test" == string

def test_methodNamePrefix():
    logger = Logger()

    string = logger.methodNamePrefix("__notinitmethod__")
    assert "\t\t\t\t" == string

def test_prefixMethonName():
    logger = Logger()
    string = logger.prefixMethodName("someMethod")
    assert "someMethod" == string

    string = logger.prefixMethodName("__notinitmethod__")
    assert "\t\t\t\t__notinitmethod__" == string

def test_appendNewLines():
    # self, msg: str, new_lines: int=0):
    logger = Logger()
    string = logger.appendNewLines("message", 3)
    assert "message\n\n\n" == string

def test_postfixStr():
    # self, msg:str, postfix:str="", new_lines:int =0):
    logger = Logger()
    
    string = logger.postfixStr("message")
    assert "message" == string
    
    string = logger.postfixStr("message", " ~~postfix")
    assert "message ~~postfix" == string
    
    string = logger.postfixStr("message", " ~~postfix", 5)
    assert "message ~~postfix\n\n\n\n\n" == string


def test_method(caplog):
    # self, method:str, data:Typevar_List_Str=None):

    with caplog.at_level(logging.DEBUG):
        logger = Logger()
        logger._method("__notinitmethod__", {"one": 1, "two": 2})
        #without @Debugger decorator
        # assert caplog.record_tuples == [('logs', 10, 'Logger::                                __notinitmethod__one,two')]
        
        popped = caplog.record_tuples.pop()
        # print(f"popped={popped}")
        #with debug decorator
        assert popped == ('logs', 10, 'Logger::                                __notinitmethod__one,two')


def test_validation_method_debug(caplog):
    logger = Logger()

    from modules.config import config
    config_obj = configparser.ConfigParser()
    config_obj.read("config.ini")

    config_obj.set("DEFAULT", "debug_validations", "True")
    # set up the defaults first
    config = config_obj["DEFAULT"]

    with caplog.at_level(logging.DEBUG):
        logger.validation_method_debug("methodName")
        logger.validation_method_debug("methodName", {"one": 1, "two": 2})
        popped = caplog.record_tuples.pop()
        assert popped == ('logs', 10, 'Logger:: methodNameone,two')

def test_validation_method_debug2(caplog):
    logger = Logger()

    from modules.config import config
    config_obj = configparser.ConfigParser()
    config_obj.read("config.ini")

    config_obj.set("DEFAULT", "debug_validations", "False")
    # set up the defaults first
    config = config_obj["DEFAULT"]

    logger.validation_method_debug("methodName")
    logger.validation_method_debug("methodName", {"one": 1, "two": 2})

    assert caplog.record_tuples == []