import sys
from dataclasses import dataclass, field as dc_field
from modules.helper import Helper
from modules.validation import Validation
from modules.validations.exception import Validation_Field_Exception


@dataclass
class Validation_Field_Data():
    classBeingValidated = None
    field: str = dc_field(default_factory=str)
    methodName: str = dc_field(default_factory=str)
    paramToValidate: str = dc_field(default_factory=str)
    paramValues:dict = dc_field(default_factory=dict)
    validatedData:dict = dc_field(default_factory=dict)
    methodAdditions:list = dc_field(default_factory=list)
    validationsToRun:dict = dc_field(default_factory=dict)
    otherObj = None

class Validation_Field(Validation):
    data: Validation_Field_Data = Validation_Field_Data()

    def __init__(self, classBeingValidated, method, field, validations, paramValues):

        self.data.classBeingValidated = classBeingValidated

        Logger.method("__init__", locals())

        self.data.methodName = method
        self.data.paramToValidate = field
        self.data.validationsToRun = validations
        self.data.paramValues = paramValues

        self.__setupParam()

        self.__doValidations()


    def getParams(self):
        Logger.method("__getParams")
        return Nested_Cache_Rows_LocationvalidatedData


    def __getParamToValidate(self):
        Logger.method("__getParamToValidate")
        return self.data.paramToValidate


    def __getParamValues(self):
        Logger.method("__getParamValues")
        return self.data.paramValues


    def __getParamValue(self, param):
        Logger.method("__getParamValue", locals())
        return self.__getParamValues()[param]


    def __setupParam(self):
        self.data.validated = {"inValidate": False, "inParams": False, "data" : None}

        if self.data.paramToValidate in self.data.paramValues:
            self.__updateValidated(field='inParams', data=True)
        self.__updateValidated(field='data', data=self.data.paramValues[self.data.paramToValidate])


    def __updateValidated(self, field, data):
        Logger.method("__updateValidated()", locals())
        self.data.validatedData[field] = data


    def __doValidations(self):
        Logger.method("__doValidations", locals())

        for validationToRun in self.data.validationsToRun:

            # setup the dict of params we want to pass to our method
            methodParams = {
                'param': self.data.paramToValidate,
                'paramValue': self.__getParamValue(self.data.paramToValidate)
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
            if Helper.classHasMethod(klass=self.data.classBeingValidated, methodName=methodName):
                Helper.callMethod(klass=self.data.classBeingValidated, **methodParams)
            elif Helper.classHasMethod(klass=self, methodName=methodName):
                Helper.callMethod(klass=self, **methodParams)
            else: 
                raise Validation_Field_Exception("Could not find a {} method on Validation_Fields or {} for method {}".format(
                    methodName, 
                    Helper.className(self.data.classBeingValidated), 
                    self.data.methodName))

    ####
    #
    # Validation_Field specific methods
    #
    ####
    def validation_oneIsNotNone(self, item, param, paramValue=None):
        Logger.method("validation_oneIsNotNone", locals())
        
        # if either of these are false, then we are good to go
        paramNotNone = (None != paramValue)
        otherParamNotNone = (None != self.__getParamValue(item))

        if False == paramNotNone and False == otherParamNotNone:
            raise Validation_Field_Exception("Either {} or {} was expected to not be 'None' for method {}".format(param, item, self.data.methodName))
        return True