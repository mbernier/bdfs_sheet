import sys
from modules.base import BaseClass
from modules.validations.exception import ValidationException


class MethodValidation(BaseClass):
    _params = []
    _paramsToValidate = []

    _validatedData = {}
    _methodName = ""
    _methodAdditions = []

    _validationsToRun = {}

    def __init__(self, methodName, params, validations):
        self._paramsToValidate = params
        self._validationsToRun = validations
        self._methodName = methodName

        self.__checkParams()

        self.__setupMethodName()

        self.__doValidation()


    def getParams(self):
        return self.__validatedData


    def getParamsToValidation(self):
        return self._paramsToValidate


    def getMethodName(self):
        return "{}({})".format(self._methodName, (",").join(self._methodAdditions))


    def __checkParams(self): 
        for param in self._params:
            self.__setupParam(param)


    def __setupParams(self, param):
        self.debug("__checkParams(param={})".format(param))

        self._validated[param] = {"inValidate": False, "inParams": False, "data" : None}

        if paramName in self.getParams():
            self.__updateValidated(param=param, 'data', self._params[param])
            self.__updateValidated(param=param, 'inParams', True)
            self.__appendMethod("{}={}".format(paramName, param))

    def __doValidations(self)
        self.debug("__doValidations()")

        if paramName in self.getParamsToValidate():
            self.__updateValidated(param=param, 'inValidations', True)

            self.__runValidations(param=param)

            if not inParams:
                raise ValidationException("'{}' was requested as validation in __setupMethod(), but it was not passed in params to be validated".format(paramName))

    def __getValidationsToRunByParam(self):
        self.debug("__getValidationsToRunByParam(param={})".format(param))
        return self._validationsToRun

    def __getParams(self):
        self.__method("__getParams")
        return self._params
    
    def __updateValidated(param, field, data):
        self.__method("__updateValidated", locals())
        self._validatedData[param][field] = data


    def __runValidations(self, param):
        self.__method("__runValidations", locals())

        for validationToRun, paramData in self.__getValidationsToRunByParam(param):
            if "orExists" == validationToRun:
                self._validation_OrExists(paramData)

            if "exists" == validationToRun:
                self._validation_Exists(paramData)


    def __validation_OrExists(self, params):
        self.__method("__validation_OrExists", params)

    # created the debug string, by calling like so:
    # e.g. self.__method("nameofMethod", locals())
    def __method(self, method, data=None):
        self.debug(self.__prepareMethodString(method, data)) 


    def __prepareMethodString(self, method, data=None):
        methodAdditions = self.__createMethodAdditions(data)
        return self.__createMethodString(method, methodAdditions)


    def __createParamDataValueString(self, localsData):
        return "{}={}".format(paramName, paramValue)


    def __createMethodAdditions(self, data):
        methodAdditions = []
        if None != data:
            for paramName, paramValue in data:
                methodAdditions.append(self.__createParamDataValueString(data))
        return methodAdditions


    def __createMethodString(self, methodName: string, methodAdditions: list):
        return "{}({})".format(method, (",").join(self._methodAdditions))



