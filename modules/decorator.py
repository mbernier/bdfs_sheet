import sys, functools, pprint
from inspect import signature, Parameter
from modules.config import config
from modules.helper import Helper
from modules.decorators.exception import Decorator_Exception
from modules.validations.annotation import Validation_Annotation
from modules.validations.method import Validation_Method


SHITTY_NONE_DEFAULT_VALUE = 'NoneZeroDefaultFail'

def debug_log(func):
    # print(f"\ndecorator_debug: {func}")
    """Print the function signature and return value"""
    @functools.wraps(func)
    def wrapper_debug(*args, **kwargs):
        # allows us to call the Logger methods, even if we are processing an __init__ method, where we don't know the class
        # print("wrapper_debug")
        # print(f"func: {func}")
        # print(f"args: {args}")
        # print(f"kwargs: {kwargs}")

        classObj = Helper.className(func)
        # print(f"classObj: {classObj}")
        if len(args) > 0:
            classObj = args[0]
        else:
            print(f"func: {func}")
            print(f"funcName: {func.__name__}")
            print(f"args: {args}")
            print(f"kwargs: {kwargs}")
            raise Decorator_Exception("We don't have args[0] in decorator, so we can't call logging on the wrapped class. What options do we have to provide default classObj?")
        
        args_repr, kwargs_repr = Helper.prepArgs(args, kwargs)

        if hasattr(classObj, "_method"):
            classObj._method(f"{func.__name__}", args_repr + kwargs_repr)
        else:
            print(f"func: {func}")
            print(f"funcName: {func.__name__}")
            print(f"args: {args}")
            print(f"kwargs: {kwargs}")
            print(f"classObj: {classObj}")
            raise Decorator_Exception(f"\t {classObj.__class__.__name__} has no method _method()")
        
        # call the function
        value = func(*args, **kwargs)

        # output to log whatever the function returned
        if True == config("debug_decorator_returns"):
            # print(f"FUNCNAME: {func.__name__}")
            classObj.debug(f"{func.__name__!r} returned {value!r}")      # 4

        return value
    return wrapper_debug


# Validation Decorator
#   To validate method params, add something like this:
#   @validate(paramName, validationsToRun) where validationsToRun is a list of validations from methods.validation.Validation_Field
def validate(*validateargs, **validateParams):
    # print("\nvalidate")
    # print(f"validateargs: {validateargs}")
    # print(f"validateParams: {validateParams}")
    def decorator_validate(func, *decoratorargs, **decoratorkwargs):
        # print(f"decorator_validate: {func}")
        # print(f"func: {func}")
        # print(f"decoratorargs: {decoratorargs}")
        # print(f"decoratorkwargs: {decoratorkwargs}")
        @functools.wraps(func)
        def wrapper_validate(*funcParams, **wrapperkwargs):
            # print("wrapper_validate")

            # print(f"func: {func}")
            # print(f"validateargs: {validateargs}")
            # print(f"validateParams: {validateParams}")
            # print(f"decoratorargs: {decoratorargs}")
            # print(f"decoratorkwargs: {decoratorkwargs}")
            # print(f"funcParams: {funcParams}")
            # print(f"wrapperkwargs: {wrapperkwargs}")


            funcSig = signature(func).parameters
            funcKeys = funcSig.keys()
            funcValues = funcSig.values()
            funcParamsList = list(funcParams)

            # print("func: {}".format(func))
            # print("funcParams: {}".format(funcParams))
            # print("funcKeys: {}".format(funcKeys))
            # print("funcVals: {}".format(funcValues))
            # print("funcSig: {}".format(funcSig))
            # print("validateParams: {}".format(validateParams))
            # print("funcParamsList: {}".format(funcParamsList))
            # print("wrapperkwargs: {}".format(wrapperkwargs))
            # print("\n\n")


            # Validation_Field.__init__(self, classBeingValidated, field, validations, **kwargs):
            validator = Validation_Method(func, validateargs, validateParams, decoratorargs, decoratorkwargs, funcParams, wrapperkwargs)
            
            newFuncParams = validator.getFunctionParams()

            # if we got this far, we passed validation, pass in the original function params to the function            
            value = func(**newFuncParams)
            
            return value


        def getFieldDefault(sig, field):
            defaultValue = SHITTY_NONE_DEFAULT_VALUE  # this value is some bullshit I made up, that I hope no one would ever use, fail on me if they do
            # print("\n\n")
            # print(sig)
            # print(sig[field])
            if hasattr(sig[field], 'default'):
                defaultValue = sig[field].default
                # print(defaultValue)
                if hasattr(defaultValue, "__name__"):
                    if defaultValue.__name__  == "_empty":
                        return SHITTY_NONE_DEFAULT_VALUE
                    else:
                        raise Decorator_Exception("default value did something unexpected in decorators, found defaultvalue.__name__ = {} for method {}".format(defaultValue.__name__, func.__name__))

            return defaultValue

        def addParamValidation(validation, paramValidations):
            if not validation in paramValidations:
                paramValidations.append(validation)

            return paramValidations

        return wrapper_validate
    return decorator_validate
