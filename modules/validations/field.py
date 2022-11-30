import sys
from modules.logger import Logger
from modules.helper import Helper
from modules.validation import Validation
from modules.validations.exception import FieldValidationException


class FieldValidation(Validation):

    _paramToValidate = None
    _paramValues = {}
    _validatedData = {}
    _methodAdditions = []

    _validationsToRun = {}

    _otherObj = None

    def __init__(self, classBeingValidated, field, validations, paramValues):
        self._method("__init__", locals())
        self._classBeingValidated = classBeingValidated
        self._paramToValidate = field
        self._validationsToRun = validations

        self._paramValues = paramValues

        self.__setupParam()

        self.__doValidations()


    def getParams(self):
        self._method("__getParams")
        return self.__validatedData


    def __getParamToValidate(self):
        self._method("__getParamToValidate")
        return self._paramToValidate


    def __getParamValues(self):
        self._method("__getParamValues")
        return self._paramValues


    def __getParamValue(self, param):
        self._method("__getParamValue", locals())
        return self.__getParamValues()[param]


    def __setupParam(self):
        self._validated = {"inValidate": False, "inParams": False, "data" : None}

        if self._paramToValidate in self._paramValues:
            self.__updateValidated(field='inParams', data=True)
        self.__updateValidated(field='data', data=self._paramValues[self._paramToValidate])


    def __updateValidated(self, field, data):
        self._method("__updateValidated()", locals())
        self._validatedData[field] = data


    def __doValidations(self):
        self._method("__runValidations", locals())

        for validationToRun in self._validationsToRun:

            # setup the dict of params we want to pass to our method
            methodParams = {
                'param': self._paramToValidate,
                'paramValue': self.__getParamValue(self._paramToValidate)
            }

            # default methodName, set as own variable for using in 2 places later
            methodName = f"validation_{validationToRun}"

            if ":" in validationToRun:
                # breakup the string that has the method and sub-info in it
                validationName, dataToPass = validationToRun.split(":")

                # set the method name param
                methodName = f"validation_{validationName}"
                
                # Try on the Validation class, if it's not there, try on the class where the decorator is being run
                methodParams['item'] = dataToPass

            #set the parameter so we can pass it
            methodParams['methodName'] = methodName

            # Call the classmethod that we find first, allowing the method's class's validation method to win, even if the Validation class has that method
            if Helper.classHasMethod(self._classBeingValidated, methodName):
                Helper.callMethod(self._classBeingValidated, **methodParams)
            elif Helper.classHasMethod(self, methodName):
                Helper.callMethod(self, **methodParams)
            else: 
                raise FieldValidationException("Could not find a {} method on FieldValidations or {}".format(methodName, Helper.className(self._classBeingValidated)))


    ####
    #
    # FieldValidation specific methods
    #
    ####
    def validation_oneIsNotNone(self, item, param, paramValue=None):
        self._method("validation_oneIsNotNone", locals())
        
        # if either of these are false, then we are good to go
        paramNotNone = (None == paramValue)
        otherParamNotNone = (None == self.__getParamValue(item))

        if True == paramNotNone and True == otherParamNotNone:
            raise FieldValidationException("Either {} or {} was expected to not be 'None'".format(param, item))
        return True