import sys, functools, pprint
from inspect import signature, Parameter
from modules.config import config
from modules.helper import Helper
from modules.decorators.exception import Decorator_Exception
from modules.validations.annotation import Validation_Annotation
from modules.validations.method import Validation_Method


SHITTY_NONE_DEFAULT_VALUE = 'NoneZeroDefaultFail'

def debug(func):
    # print("decorator_debug")
    """Print the function signature and return value"""
    @functools.wraps(func)
    def wrapper_debug(*args, **kwargs):
        # allows us to call the Logger methods, even if we are processing an __init__ method, where we don't know the class
        # print("wrapper_debug")
        # print(func)
        # print(args)
        # print(kwargs)

        classObj = Helper.className(func)
        # print(classObj)
        if len(args) > 0:
            classObj = args[0]
        else:
            # print(func)
            # print(func.__name__)
            # print(args)
            # print(kwargs)
            raise Decorator_Exception("We don't have args[0] in decorator, so we can't call logging on the wrapped class. What options do we have to provide default classObj?")
        
        args_repr, kwargs_repr = prepArgs(args, kwargs)

        # print(classObj)
        if hasattr(classObj, "_method"):
            classObj._method(f"{func.__name__}", args_repr + kwargs_repr)
        else:
            print(f"\t {classObj} has no method _method()")
        
        # call the function
        value = func(*args, **kwargs)

        # output to log whatever the function returned
        if config.getboolean("debug_decorator_returns"):
            classObj.debug(f"{func.__name__!r} returned {value!r}")      # 4

        return value
    return wrapper_debug


# Validation Decorator
#   To validate method params, add something like this:
#   @validate(paramName, validationsToRun) where validationsToRun is a list of validations from methods.validation.Validation_Field
def validate(*validateargs, **validateParams):
    def decorator_validate(func, *decoratorargs, **decoratorkwargs):
        @functools.wraps(func)
        def wrapper_validate(*funcParams, **wrapperkwargs):

            funcSig = signature(func).parameters

            funcKeys = funcSig.keys()
            funcValues = funcSig.values()
            funcParamsList = list(funcParams)

            print("func: {}".format(func))
            print("funcParams: {}".format(funcParams))
            print("funcKeys: {}".format(funcKeys))
            print("funcVals: {}".format(funcValues))
            print("funcSig: {}".format(funcSig))
            print("validateParams: {}".format(validateParams))
            print("funcParamsList: {}".format(funcParamsList))
            print("wrapperkwargs: {}".format(wrapperkwargs))
            print("\n\n")

            # didn't code for these, so throw a hissy if they show up
            if not () == validateargs:
                raise Decorator_Exception('Received unexpected validateargs in validate Decorator:: {} for method {}'.format(validateargs, func.__name__))

            if not () == decoratorargs:
                raise Decorator_Exception('Received unexpected decoratorargs in validate Decorator:: {} for method {}'.format(decoratorargs, func.__name__))
            
            # hold onto self for a second, so we can pass all the other vars to Validate class
            tempSelf = funcSig['self']

            validationArgs = {'classBeingValidated': tempSelf, 'method': func.__name__}

            # create a new Dict, that can take data from the various places we get data
            #   this will be passed to the function call at the end
            newFuncParams = {}

            # go through the function keys
                # find whether we have validations for them
                # if we do, then create a dict of keys => validations, data
            # pass the dict to Validation_Method
            for index, key in enumerate(funcKeys):
                if 'self' == key:
                    newFuncParams['self'] = tempSelf
                    continue

                # if the param is there, use the value, otherwise use the default
                currentValue = None  # set this to something, we will set to something else below
                defaultValue = getFieldDefault(funcSig, key)
                paramValidations = []
                
                # do we get a free validator from the method definition
                annotation = Validation_Annotation.getValidations(funcSig, key)

                print("")
                print(defaultValue)
                print(key)
                print(index)
                print(len(funcParamsList))

                # set the value, based on values available from args, kwargs, and defaults
                if index < len(funcParamsList):
                    currentValue = funcParamsList[index]
                elif key in wrapperkwargs:
                    currentValue = wrapperkwargs[key]
                elif SHITTY_NONE_DEFAULT_VALUE == defaultValue: # this value is some bullshit I made up, that I hope no one would ever use, fail on me if they do
                    raise Decorator_Exception("Positional arg '{}' was not set and has no default for method {}".format(key, func.__name__))
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

            # Validation_Field.__init__(self, classBeingValidated, field, validations, **kwargs):
            validator = Validation_Method(**validationArgs)
            
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



def prepArgs(args, kwargs):
    args_repr = [repr(a) for a in args]                      # 1
    kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]  # 2
    
    return args_repr, kwargs_repr