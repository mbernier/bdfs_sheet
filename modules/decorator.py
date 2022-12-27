import functools
from modules.logger import Logger, logger_name
from modules.config import config

configObj = config()

def Debugger_prepArgs(*args, **kwargs):
    args_repr = [repr(a) for a in args]                      # 1
    kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]  # 2
    
    return args_repr + kwargs_repr

def Debugger(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        writeDebug = True
        if 0 < len(args):
            logger_name.name = args[0].__class__.__name__
            debug_name = logger_name.name.lower() + "_debug"
            # if we turned off debugging for this object, then don't debug it
            if debug_name in configObj and False == config(debug_name):
                writeDebug = False
        if True == writeDebug:
            Logger.debug(f"{f}({Debugger_prepArgs(args,kwargs)})")

        return f(*args, **kwargs)
    return wrapper