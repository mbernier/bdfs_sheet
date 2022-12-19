import functools
from modules.logger import Logger

def Debugger(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        Logger.logger_name = args[0].__class__.__name__
        return f(*args, **kwargs)
    return wrapper