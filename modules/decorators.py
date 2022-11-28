import sys
from modules.validation import FieldValidation
import functools
from inspect import signature, Parameter

def debug(func):
    """Print the function signature and return value"""
    @functools.wraps(func)
    def wrapper_debug(*args, **kwargs):
        classObj = args[0]
        args_repr, kwargs_repr, signature = prepArgs(args, kwargs)
        classObj.debug(f"Calling {func.__name__}({signature})")
        value = func(*args, **kwargs)
        classObj.debug(f"{func.__name__!r} returned {value!r}")      # 4
        return value
    return wrapper_debug

# wrapper for 
def validate(field, validations):
    def decorator_validate(func, *args, **kwargs):
        @functools.wraps(func)
        def wrapper_validate(*args, **kwargs):

            sig = signature(func).parameters
            sigKeys = signature(func).parameters.keys()

            allArgs = {}
            tempSelf = None
            for index, key in enumerate(sig):
                defaultValue = sig[key].default
                if defaultValue is Parameter.empty:
                    defaultValue = None

                if key == 'self':
                    # hold onto self for a second, so we can pass all the other vars to Validate class
                    if 0 == len(args):
                        tempSelf = kwargs['self']
                        #we want this out of kwargs for the FieldValidation
                        del kwargs['self']
                    else:
                        tempSelf = args[index]
                elif key in kwargs:
                    if None == kwargs[key] and not None == defaultValue:
                        allArgs[key] = defaultValue
                    else:
                        allArgs[key] = kwargs[key]
                    #remove possibility of conflict when we merge
                    del kwargs[key]
                elif index < len(args):
                    if None == args[index] and not None == defaultValue:
                        allArgs[key] = defaultValue
                    else:
                        # is it in the args array?
                        allArgs[key] = args[index]
                else:
                    if not None == defaultValue:
                        allArgs[key] = defaultValue
                    else:
                        # if we don't have it, set to None
                        allArgs[key] = None

            kwargs.update(allArgs)


            print(kwargs)

            validator = FieldValidation(field, validations, **kwargs)
    
            kwargs['self'] = tempSelf

            value = func(**kwargs)
            return value
        return wrapper_validate
    return decorator_validate



def prepArgs(args, kwargs):
    args_repr = [repr(a) for a in args]                      # 1
    kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]  # 2
    signature = ", ".join(args_repr + kwargs_repr)           # 3
    
    return args_repr, kwargs_repr, signature