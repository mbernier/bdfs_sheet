import functools
from modules.logger import Logger, logger_name

def Debugger_prepArgs(*args, **kwargs):
    args_repr = [repr(a) for a in args]                      # 1
    kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]  # 2
    
    return args_repr + kwargs_repr

def Debugger(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        if 0 < len(args):
            print(f"Set logger name to {args[0].__class__.__name__}")
            logger_name.name = args[0].__class__.__name__
        Logger.debug(f"{f}({Debugger_prepArgs(args,kwargs)})")
        return f(*args, **kwargs)
    return wrapper