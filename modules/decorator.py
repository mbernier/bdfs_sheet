import sys, functools, pprint
from inspect import signature, Parameter
from modules.decorators.exception import DecoratorException
from modules.helper import Helper
from modules.logger import Logger
from modules.validations.method import MethodValidation

SHITTY_NONE_DEFAULT_VALUE = 'NoneZeroDefaultFail'

def debug(func):
    """Print the function signature and return value"""
    @functools.wraps(func)
    def wrapper_debug(*args, **kwargs):
        # allows us to call the Logger methods, even if we are processing an __init__ method, where we don't know the class
        classObj = Logger()
        if len(args) > 0:
            classObj = args[0]
        
        args_repr, kwargs_repr, signature = prepArgs(args, kwargs)

        # get a prefix to make the logs a little cleaner
        prefix = Logger.methodNamePrefix(func.__name__)
            
        classObj.debug(f"{prefix} Calling {func.__name__}({signature})")
        value = func(*args, **kwargs)
        classObj.debug(f"{prefix} {func.__name__!r} returned {value!r}")      # 4
        return value
    return wrapper_debug


# Validation Decorator
#   To validate method params, add something like this:
#   @validate(paramName, validationsToRun) where validationsToRun is a list of validations from methods.validation.FieldValidation
def validate(*validateargs, **validateParams):
    def decorator_validate(func, *decoratorargs, **decoratorkwargs):
        @functools.wraps(func)
        def wrapper_validate(*funcParams, **wrapperkwargs):

            funcSig = signature(func).parameters
            funcKeys = funcSig.keys()
            funcParamsList = list(funcParams)
            # print("func: {}".format(func))
            # print("funcParams: {}".format(funcParams))
            # print("funcSig: {}".format(funcSig))
            # print("validateParams: {}".format(validateParams))
            # print("funcParamsList: {}".format(funcParamsList))
            # print("wrapperkwargs: {}".format(wrapperkwargs))
            # print("funcKeys: {}".format(funcKeys))
            # print("\n\n")


            # didn't code for these, so throw a hissy if they show up
            if not () == validateargs:
                raise DecoratorException('Received unexpected validateargs in validate Decorator:: {} for method {}'.format(validateargs, func.__name__))

            if not () == decoratorargs:
                raise DecoratorException('Received unexpected decoratorargs in validate Decorator:: {} for method {}'.format(decoratorargs, func.__name__))
            

            # hold onto self for a second, so we can pass all the other vars to Validate class
            tempSelf = funcParamsList[0]

            validationArgs = {'classBeingValidated': tempSelf, 'method': func.__name__}

            # create a new Dict, that can take data from the various places we get data
            #   this will be passed to the function call at the end
            newFuncParams = {}

            # go through the function keys
                # find whether we have validations for them
                # if we do, then create a dict of keys => validations, data
            # pass the dict to MethodValidation
            for index, key in enumerate(funcKeys):
                if 'self' == key:
                    newFuncParams['self'] = tempSelf
                    continue

                # if the param is there, use the value, otherwise use the default
                currentValue = None  # set this to something, we will set to something else below
                defaultValue = getFieldDefault(funcSig, key)
                paramValidations = []
                # do we get a free validator from the method definition?
                annotation = getFieldAnnotation(funcSig, key)

                # print("")
                # print(defaultValue)
                # print(key)
                # print(index)
                # print(len(funcParamsList))

                # set the value, based on values available from args, kwargs, and defaults
                if index < len(funcParamsList):
                    currentValue = funcParamsList[index]
                elif key in wrapperkwargs:
                    currentValue = wrapperkwargs[key]
                elif SHITTY_NONE_DEFAULT_VALUE == defaultValue: # this value is some bullshit I made up, that I hope no one would ever use, fail on me if they do
                    raise DecoratorException("Positional arg '{}' was not set and has no default for method {}".format(key, func.__name__))
                else: 
                    currentValue = defaultValue


                # check if validitors were passed
                if key in validateParams:
                    paramValidations = validateParams[key]

                # add validators based on annotations and default values
                if SHITTY_NONE_DEFAULT_VALUE != defaultValue and None != annotation:
                    # we have an annotation and we have a default value
                    addParamValidation(f'ifSetType:{annotation}', paramValidations)
                else:
                    if None != annotation: # if we have an annotation, add it to paramValidations
                        addParamValidation(f'isType:{annotation}', paramValidations)

                    if None != defaultValue:
                        # no default is set, so set notNone
                        addParamValidation('notNone', paramValidations)

                validationArgs[key] = {
                    'validations': paramValidations,
                    'data': currentValue
                }

                newFuncParams[key] = currentValue

            # FieldValidation.__init__(self, classBeingValidated, field, validations, **kwargs):
            validator = MethodValidation(**validationArgs)
            
            # if we got this far, we passed validation, pass in the original function params to the function            
            value = func(**newFuncParams)
            return value

        def getFieldAnnotation(sig, field):
            annotation = sig[field].annotation
            if annotation.__name__ == "_empty":
                return None

            return annotation.__name__

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
                        raise DecoratorException("default value did something unexpected in decorators, found defaultvalue.__name__ = {} for method {}".format(defaultValue.__name__, func.__name__))

            return defaultValue

        def addParamValidation(validation, paramValidations):
            if not validation in paramValidations:
                paramValidations.append(validation)

            return paramValidations

        return wrapper_validate
    return decorator_validate



def prepArgs(args, kwargs):
    args_repr = [repr(a) for a in args]                      # 1
    kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]  # 2
    signature = ", ".join(args_repr + kwargs_repr)           # 3
    
    return args_repr, kwargs_repr, signature