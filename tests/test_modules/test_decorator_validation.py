import pytest
from modules.decorator import validate
from modules.base import BaseClass
from modules.decorators.exception import DecoratorException
from modules.validations.exception import ValidationException, FieldValidationException, MethodValidationException

# We are testing both MethodValidation and FieldValidation in these tests
# The @validate decorator looks at all of the validations -- MethodValidation
#   It breaks up the validations by field, then passes each one to FieldValidation


# create a dummy class to test Validations against
class A(BaseClass):

    @validate(var1=['isType:int'], var2 = ['notNone'])
    def bat(self, var1=None, var2=None):
        return True

    @validate(var2=['oneIsNotNone:var3'])
    def foo(self, var1=None, var2=None, var3=None):
        return True

    @validate(var2=['oneIsNotNone:var3'])
    def foo2(self, var1, var2, var3=None):
        pass

    @validate(var1=['notNone'], var2=['notNone'])
    def positional(self, var1, var2):
        pass

    @validate(var1=['notNone'], var2=['notNone'],var3=['notNone'], var4=['notNone'])
    def annotations_with_validate_set(self, var1:int, var2:list, var3:dict, var4:str):
        return True

    @validate(var1=['notNone'], var2=['notNone'])
    def annotations_without_validate_set(self, var1:int, var2:list, var3:dict, var4:str):
        return True

class B():
    @validate(arbitvalue=['notNone'])
    def __init__(self, arbitvalue:str=None):
        pass


def test_init_validation():
    with pytest.raises(ValidationException) as excinfo:
        var = B(None)
    excinfo.value.message == "arbitvalue was expected to be type str, but <class 'NoneType'> was found for arbitvalue"


def test_init_validation_wrong_type_passed():
    with pytest.raises(ValidationException) as excinfo:
        var = B(['string'])
    excinfo.value.message == "arbitvalue was expected to be type str, but <class 'NoneType'> was found for arbitvalue"


def test_passes_validate_positional_args():
    var = A()
    assert True == var.bat(2, "4")
    # no exceptions are thrown


def test_passes_validate_positional_and_named_args():
    var = A()
    assert True == var.bat(1, var2="3")
    # no exceptions are thrown

def test_fails_validate_using_isTypeInt():
    var = A()
    with pytest.raises(ValidationException) as excinfo:
        var.bat("this is a string", var2="3")
    excinfo.value.message == "var1 was expected to be type int, but <class 'str'> was found for var1"


def fails_validate_notNone():
    var = A()
    with pytest.raises(ValidationException) as excinfo:
        var.bat(1)
    excinfo.value.message == "var2 was passed as None, but needs to be set"
    

def test_success_validate_oneIsNotNone():
    var = A()
    assert True == var.foo(1, "Something Here", None)


def test_fails_validate_oneIsNotNone():
    var = A()
    with pytest.raises(ValidationException) as excinfo:
        var.foo2(1, var2=None, var3=None)
    excinfo.value.message == "Either var2 or var3 was expected to not be 'None'"

def test_fails_validate_oneIsNotNone_using_defaults():
    var = A()
    with pytest.raises(ValidationException) as excinfo:
        var.foo(1)
    excinfo.value.message == "Either var2 or var3 was expected to not be 'None'"


def test_positional_arg_not_set_no_default():
    #"Positional Argument {} is not set and has no default".format(key)
    var = A()
    with pytest.raises(DecoratorException) as excinfo:
        var.positional(1)
    excinfo.value.message == "Positional Argument var2 is not set and has no default"


def test_annotations_with_validation_set():
    var = A()
    assert True == var.annotations_with_validate_set(var1=1, var2=[], var3={}, var4="some string")


def test_annotations_without_validation_set():
    var = A()
    assert True == var.annotations_without_validate_set(var1=1, var2=[], var3={}, var4="some string")


def test_annotations_with_validation_set_mismatch_types():
    var = A()
    with pytest.raises(ValidationException) as excinfo:
        var.annotations_with_validate_set(var1=1, var2={}, var3={}, var4="some string")
    excinfo.value.message == "var2 was expected to be type list, but <class 'dict'> was found for var2"

def test_annotations_with_validation_set_mismatch_types_missing_param():
    var = A()
    with pytest.raises(DecoratorException) as excinfo:
        var.annotations_with_validate_set(var1=1, var2={}, var3={})
    excinfo.value.message == "var2 was expected to be type list, but <class 'dict'> was found for var2"



def test_annotations_without_validation_set_mismatch_types():
    var = A()
    with pytest.raises(ValidationException) as excinfo:
        var.annotations_without_validate_set(var1=1, var2={}, var3={}, var4="some string")
    excinfo.value.message == "var2 was expected to be type list, but <class 'dict'> was found for var2"

def test_annotations_without_validation_set_mismatch_types_with_missing_param():
    var = A()
    with pytest.raises(DecoratorException) as excinfo:
        var.annotations_without_validate_set(var1=1, var2={}, var3={})
    excinfo.value.message == "var2 was expected to be type list, but <class 'dict'> was found for var2"
        