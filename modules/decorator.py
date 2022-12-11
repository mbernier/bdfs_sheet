import sys, functools, pprint
from inspect import signature, Parameter
from modules.config import config
from modules.helper import Helper
from modules.logger import Logger
from modules.decorators.exception import Decorator_Exception
from modules.validations.annotation import Validation_Annotation
from modules.validations.method import Validation_Method


SHITTY_NONE_DEFAULT_VALUE = 'NoneZeroDefaultFail'


def Debugger(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        Logger.logger_name = args[0].__class__.__name__
        return f(*args, **kwargs)
    return wrapper