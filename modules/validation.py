import sys
from modules.logger import Logger
from modules.validations.exception import ValidationException

class FieldValidation(Logger):

    _paramToValidate = None
    _paramValues = {}
    _validatedData = {}
    _methodAdditions = []

    _validationsToRun = {}

    _otherObj = None

    def __init__(self, field, validations, **kwargs):

        self._paramToValidate = field
        self._validationsToRun = validations

        self._paramValues = kwargs

        self.__setupParam()

        self.__doValidations()


    def getParams(self):
        return self.__validatedData


    def __getParamToValidate(self):
        return self._paramToValidate


    def __setupParam(self):
        self._validated = {"inValidate": False, "inParams": False, "data" : None}

        if self._paramToValidate in self._paramValues:
            self.__updateValidated(field='inParams', data=True)
        self.__updateValidated(field='data', data=self._paramValues[self._paramToValidate])


    def __updateValidated(self, field, data):
        self._method("__updateValidated", locals())
        self._validatedData[field] = data


    def __doValidations(self):
        self._method("__runValidations", locals())

        self.console("{}".format(self._validationsToRun))

        param = self._paramToValidate
        paramValue = self.getParamValue(param)

        for validationToRun in self._validationsToRun:
            dataToPass = None
            if ":" in validationToRun:
                validationToRun, dataToPass = validationToRun.split(":")

            do = f"validation_{validationToRun}"

            if hasattr(self, do) and callable(validFunc := getattr(self, do)):
                if None != dataToPass:
                    validFunc(item = dataToPass, param=param, paramValue=paramValue)
                else: 
                    validFunc(param=param, paramValue=paramValue)
            else:
                raise ValidationException("Tried to validate {} but no method for this validation exists".format(validationToRun))
    

    ####
    #
    # Validators: Existence
    #
    ####

    # due to the way we're writing the wrapper, all params will always exist, so long as they are in the signature
    #   this could cause bad behavior in coding methods...
    def validation_exists(self, param, paramValue=None):
        self._method("validation_exists()")
        # check if the field is in the _paramValues and is not None

        if not self.__existsInList(param, paramValue):
            raise ValidationException("{} was not in the passed parameters".format(param))
        return True


    def validation_orExists(self, item, param, paramValue=None):
        self._method("validation_OrExists", item)
        paramExists = self.__existsInList(param, paramValue)
        otherParamExists = self.__existsInList(item, paramValue)

        if not paramExists or otherParamExists:
            raise ValidationException("Either {} or {} was expected but neither was found".format(param, item))

    def validation_notNone(self, param, paramValue=None):
        self._method("validation_notNone")

        if None == paramValue:
            raise ValidationException("{} was passed as None, but needs to be set".format(param))
        return True

    ####
    #
    # Validators: Math
    #
    ####

    def validation_gt(self, item, param, paramValue=None):
        self._method("validation_gt")
        if paramValue < int(item):
            raise ValidationException("{} was expected to be gt than {}".format(paramValue, item))

    ####
    #
    # Helper Methods
    #
    ####

    def __existsInList(self, item, lookIn):
        if item in lookIn:
            return True
        return False

    def getParamValue(self, param):
        return self._paramValues[param]
