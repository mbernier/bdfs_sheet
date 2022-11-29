import sys
from modules.logger import Logger
from modules.helper import Helper
from modules.validations.exception import ValidationException

class FieldValidation(Logger):

    _paramToValidate = None
    _paramValues = {}
    _validatedData = {}
    _methodAdditions = []

    _validationsToRun = {}

    _otherObj = None

    def __init__(self, classBeingValidated, field, validations, **kwargs):
        self._method("__init__", locals())
        self._classBeingValidated = classBeingValidated
        self._paramToValidate = field
        self._validationsToRun = validations

        self._paramValues = kwargs

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

        self.console("{}".format(self._validationsToRun))

        # setup the dict of params we want to pass to our method
        methodParams = {
            'param': self._paramToValidate,
            'paramValue': self.__getParamValue(self._paramToValidate)
        }

        for validationToRun in self._validationsToRun:

            self.console(validationToRun)

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
                raise ValidationException("Could not find a {} method on Validations or {}".format(methodName. Helper.className(self._classBeingValidated)))


    ####
    #
    # Validators: Existence
    #
    ####

    # due to the way we're writing the wrapper, all params will always exist, so long as they are in the signature
    #   this could cause bad behavior in coding methods...
    def validation_exists(self, param, paramValue=None):
        self._method("validation_exists", locals())
        # check if the field is in the _paramValues and is not None

        if not Helper.existsIn(param, paramValue):
            raise ValidationException("{} was not in the passed parameters".format(param))
        return True


    def validation_orExists(self, item, param, paramValue=None):
        self._method("validation_OrExists", locals())
        
        
        paramValues = self.__getParamValues()
        paramExists = Helper.existsIn(param, paramValues)
        otherParamExists = Helper.existsIn(item, paramValues)

        if not (paramExists or otherParamExists):
            raise ValidationException("Either {} or {} was expected but neither was found".format(param, item))
        return True

    def validation_notNone(self, param, paramValue=None):
        self._method("validation_notNone", locals())

        if None == paramValue:
            raise ValidationException("{} was passed as None, but needs to be set".format(param))
        return True


    def validation_isType(self, item, param, paramValue=None):
        self._method("validation_isType", locals())

        if not Helper.isType(item, paramValue):
            raise ValidationException("{} was expected to be type {}, but {} was found for {}".format(param, item, str(type(paramValue)), param))
        return True

    def validate_oneOf(self, item, param, paramValue):
        self._method("validate_oneOf", locals())

        if not Helper.existsInStr(",", item):
            raise ValidationException("oneOf validation expects a comma seperated list of items to check against")

        items = item.split(",")
        
        if Helper.existsIn(item=param, lookIn=items):
            return True
        else:
            raise ValidationException("One of {} was expected, but {} was found for parameter {}".format(item, paramValue,param))

    ####
    #
    # Validators: Math
    #
    ####

    def validation_gt(self, item, param, paramValue=None):
        self._method("validation_gt", locals())
        if paramValue < int(item):
            raise ValidationException("{} was expected to be gt than {}".format(paramValue, item))
        return True