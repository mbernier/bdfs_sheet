import functools
from modules.logger import Logger, logger_name
from modules.config import config

configObj = config()

def Debugger_prepArgs(*args, **kwargs):
    args_repr = [repr(a) for a in args]                      # 1
    kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]  # 2
    
    return args_repr + kwargs_repr

def isclassmethod(method):
    bound_to = getattr(method, '__self__', None)
    if not isinstance(bound_to, type):
        # must be bound to a class
        return False
    name = method.__name__
    for cls in bound_to.__mro__:
        descriptor = vars(cls).get(name)
        if descriptor is not None:
            return isinstance(descriptor, classmethod)
    return False

def Debugger(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        writeDebug = True
        if 0 < len(args):
            className = args[0].__class__.__name__
            # This will handle @classmethods who don't have a "class" that is as easily accessible
            if hasattr(args[0],f.__name__):
                if isclassmethod(getattr(args[0],f.__name__)):
                    cls = args[0]
                    className = cls.__name__

            logger_name.name = className
            
            debug_name = logger_name.name.lower() + "_debug"
            # if we turned off debugging for this object, then don't debug it
            if debug_name in configObj and False == config(debug_name):
                writeDebug = False
        
        if True == writeDebug:
            Logger.debug(f"{f}({Debugger_prepArgs(args,kwargs)})")

        return f(*args, **kwargs)
    return wrapper