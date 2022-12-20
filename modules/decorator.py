import functools
from modules.logger import Logger

def Debugger_prepArgs(*args, **kwargs):
    args_repr = [repr(a) for a in args]                      # 1
    kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]  # 2
    
    return args_repr + kwargs_repr

def Debugger(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        Logger.debug(f"{f}({Debugger_prepArgs(args,kwargs)})")
        return f(*args, **kwargs)
    return wrapper