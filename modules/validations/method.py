import sys
from dataclasses import dataclass, field as dc_field
from inspect import signature, Parameter
from modules.helper import Helper
from modules.validation import Validation
from modules.validations.annotation import Validation_Annotation
from modules.decorators.exception import Decorator_Exception
from modules.validations.field import Validation_Field
from modules.validations.exception import Validation_Method_Exception

SHITTY_NONE_DEFAULT_VALUE = 'NoneZeroDefaultFail'

@dataclass
class Validation_Method_Data():
    newFunctionParams:dict = dc_field(default_factory=dict)
    classBeingValidated:str = dc_field(default_factory=str)
    methodName:str = dc_field(default_factory=str)


class Validation_Method(Validation):
    data: Validation_Method_Data = Validation_Method_Data()

    def __init__(self, func, validateargs, validateParams, decoratorargs, decoratorkwargs, funcParams, wrapperkwargs):

        self.data.newFunctionParams = {}
        self.data.classBeingValidated = None
        self.data.methodName = None

        # print("Validation Method Params: ")
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

        # didn't code for these, so throw a hissy if they show up
        if not () == validateargs:
            raise Decorator_Exception('Received unexpected validateargs in validate Decorator:: {} for method {}'.format(validateargs, func.__name__))

        if not () == decoratorargs:
            raise Decorator_Exception('Received unexpected decoratorargs in validate Decorator:: {} for method {}'.format(decoratorargs, func.__name__))
        
        # hold onto self for a second, so we can pass all the other vars to Validate class
        tempSelf = funcSig['self']
        
        if len(funcParamsList) > 0:
            tempSelf = funcParamsList[0]

        self.data.classBeingValidated = tempSelf
        self.data.methodName = func.__name__

        validationArgs = {} 

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
            defaultValue = self.getFieldDefault(funcSig, key)
            paramValidations = []
            
            # do we get a free validator from the method definition
            annotation = Validation_Annotation.getValidations(funcSig, key)

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
                raise Decorator_Exception("Positional arg '{}' was not set and has no default for method {}".format(key, func.__name__))
            else: 
                currentValue = defaultValue

            # check if validitors were passed
            if key in validateParams:
                paramValidations = validateParams[key]

            # add validators based on annotations and default values
            if SHITTY_NONE_DEFAULT_VALUE != defaultValue and None != annotation:
                # we have an annotation and we have a default value
                self.addParamValidation(f'ifSetType:{annotation}', paramValidations)
            else:
                if None != annotation: # if we have an annotation, add it to paramValidations
                    self.addParamValidation(f'isType:{annotation}', paramValidations)

                if None != defaultValue:
                    # no default is set, so set notNone
                    self.addParamValidation('notNone', paramValidations)

            validationArgs[key] = {
                'validations': paramValidations,
                'data': currentValue
            }

            newFuncParams[key] = currentValue


        self.data.newFunctionParams = newFuncParams

        # print(f"newFuncParams: {newFuncParams}")
        # print(f"validationArgs: {validationArgs}")

        self.__doValidations(validationArgs)



    def __doValidations(self, paramData):
        
        passTheseArgs = {}

        # set up the args dict for passing to Validation_Field
        for key in paramData:
            if "self" == key:
                continue
            
            passTheseArgs[key] = paramData[key]['data']

        for key in paramData:
            if "self" == key:
                continue
            
            # print((self._classBeingValidated, key,  paramData[key]['validations'], passTheseArgs))
            #            Validation_Field(classBeingValidated, field, validations, args)
            validation = Validation_Field(classBeingValidated=self.data.classBeingValidated, 
                                            method=self.data.methodName,
                                            field=key,
                                            validations=paramData[key]['validations'], 
                                            paramValues=passTheseArgs)

    def getFunctionParams(self):
        # print(self._newFunctionParams)
        return self.data.newFunctionParams


    def getFieldDefault(self, sig, field):
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


    def addParamValidation(self, validation, paramValidations):
        if not validation in paramValidations:
            paramValidations.append(validation)

        return paramValidations