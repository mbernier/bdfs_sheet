import pytest
from modules.decorator import debug, validate
from modules.base import BaseClass
from modules.decorators.exception import DecoratorException
from modules.validations.exception import ValidationException, FieldValidationException, MethodValidationException

# We are testing both MethodValidation and FieldValidation in these tests
# The @validate decorator looks at all of the validations -- MethodValidation
#   It breaks up the validations by field, then passes each one to FieldValidation


# create a dummy class to test Validations against
class A(BaseClass):

    @debug
    @validate(var1=['isType:int'], var2 = ['notNone'])
    def bat(self, var1=None, var2=None):
        return True

    @debug 
    @validate(var2=['oneIsNotNone:var3'])
    def foo(self, var1=None, var2=None, var3=None):
        return True

    @debug
    @validate(var2=['oneIsNotNone:var3'])
    def foo2(self, var1, var2, var3=None):
        pass

    @debug
    @validate(var1=['notNone'], var2=['notNone'])
    def positional(self, var1, var2):
        pass

    @debug
    @validate(var1=['notNone'], var2=['notNone'],var3=['notNone'], var4=['notNone'])
    def annotations_with_validate_set(self, var1:int, var2:list, var3:dict, var4:str):
        return True

    @debug
    @validate(var1=['notNone'], var2=['notNone'])
    def annotations_without_validate_set(self, var1:int, var2:list, var3:dict, var4:str):
        return True

class B(BaseClass):
    @debug
    @validate(arbitvalue=['notNone'])
    def __init__(self, arbitvalue:str=None):
        pass


class C(BaseClass):
    @debug
    @validate()
    def foo(self, var1:int = 100):
        return True

    @debug
    @validate()
    def bar(self, var1:int):
        return True

    @debug
    @validate()
    def bat(self, var1 = 50):
        return True

    @debug
    @validate(var1=['gte:2'])
    def gte(self, var1:int):
        return True

    @debug
    @validate(var1=['gt:1'])
    def gt(self, var1:int):
        return True

    @debug
    @validate(var1=['ifSetType:dict'])
    def ifSetType(self, var1:dict=None):
        return True

    @debug
    @validate(var1=['contains:yes,no'])
    def contains(self, var1:str=None):
        return True

    @debug
    @validate(var1=['contains:yes'])
    def contains2(self, var1:str=None):
        return True


def test_default_and_annotation_sets_isSetType():
    c = C()
    assert True == c.foo(200)


# if default value and annotation, should be testing isSetType
#   - send in an unexpected type
def test_default_and_annotation_sets_isSetType_wrongType():
    c = C()
    with pytest.raises(ValidationException) as excinfo:
        c.foo("string")
    assert excinfo.value.message == "var1 was expected to be type int, but <class 'str'> was found"


# if an annotation, and no default
#   isType should be checked
def test_annotation_no_default():
    c = C()
    assert True == c.bar(200)

def test_annotation_no_default():
    c = C()
    with pytest.raises(ValidationException) as excinfo:
        c.bar("string")
    assert excinfo.value.message == "var1 was expected to be type int, but <class 'str'> was found"


# if no annotaion, with a default
#   notNone should be checked
def test_no_annotation_default_set():
    c = C()
    assert True == c.bat(100)

def test_no_annotation_default_set_fail():
    c = C()
    with pytest.raises(ValidationException) as excinfo:
        c.bat(None)
    assert excinfo.value.message == "var1 was passed as None, but needs to be set"



def test_init_validation():
    with pytest.raises(ValidationException) as excinfo:
        var = B(None)
    assert excinfo.value.message == "arbitvalue was passed as None, but needs to be set"


def test_init_validation_wrong_type_passed():
    with pytest.raises(ValidationException) as excinfo:
        var = B(['string'])
    assert excinfo.value.message == "arbitvalue was expected to be type str, but <class 'list'> was found"


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
    assert excinfo.value.message == "var1 was expected to be type int, but <class 'str'> was found"


def fails_validate_notNone():
    var = A()
    with pytest.raises(ValidationException) as excinfo:
        var.bat(1)
    assert excinfo.value.message == "var2 was passed as None, but needs to be set"
    

def test_success_validate_oneIsNotNone():
    var = A()
    assert True == var.foo(1, "Something Here", None)


def test_fails_validate_oneIsNotNone():
    var = A()
    with pytest.raises(ValidationException) as excinfo:
        var.foo2(1, var2=None, var3=None)
    assert excinfo.value.message == "Either var2 or var3 was expected to not be 'None'"

def test_fails_validate_oneIsNotNone_using_defaults():
    var = A()
    with pytest.raises(ValidationException) as excinfo:
        var.foo(1)
    assert excinfo.value.message == "Either var2 or var3 was expected to not be 'None'"


def test_positional_arg_not_set_no_default():
    #"Positional Argument {} is not set and has no default".format(key)
    var = A()
    with pytest.raises(DecoratorException) as excinfo:
        var.positional(1)
    assert excinfo.value.message == "Positional arg 'var2' was not set and has no default"


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
    assert excinfo.value.message == "var2 was expected to be type list, but <class 'dict'> was found"

def test_annotations_with_validation_set_mismatch_types_missing_param():
    var = A()
    with pytest.raises(DecoratorException) as excinfo:
        var.annotations_with_validate_set(var1=1, var2={}, var3={})
    assert excinfo.value.message == "Positional arg 'var4' was not set and has no default"



def test_annotations_without_validation_set_mismatch_types():
    var = A()
    with pytest.raises(ValidationException) as excinfo:
        var.annotations_without_validate_set(var1=1, var2={}, var3={}, var4="some string")
    assert excinfo.value.message == "var2 was expected to be type list, but <class 'dict'> was found"

def test_annotations_without_validation_set_mismatch_types_with_missing_param():
    var = A()
    with pytest.raises(DecoratorException) as excinfo:
        var.annotations_without_validate_set(var1=1, var2={}, var3={})
    assert excinfo.value.message == "Positional arg 'var4' was not set and has no default"

def test_validation_gte():
    var = C()
    assert True == var.gte(2)
    assert True == var.gte(3)

    with pytest.raises(ValidationException) as excinfo:
        var.gte(1)
    assert excinfo.value.message == "var1 was expected to be greater than or equal to 2, 1 was found"

def test_validation_gte2():
    var = C()

    with pytest.raises(ValidationException) as excinfo:
        var.gte({})
    assert excinfo.value.message == "var1 was expected to be type int, but <class 'dict'> was found"


def test_validation_gt():
    var = C()

    assert True == var.gt(2)
    assert True == var.gt(100)
    with pytest.raises(ValidationException) as excinfo:
        var.gt(1)
    excinfo.value.message == "var1 was expected to be greater than 1, 1 was found"

    with pytest.raises(ValidationException) as excinfo:
        var.gte("blah")
    assert excinfo.value.message == "var1 was expected to be type int, but <class 'str'> was found"    


def test_validation_ifSetType():
    var = C()

    assert True == var.ifSetType({'a': 1})

    assert True == var.ifSetType(None)

    with pytest.raises(ValidationException) as excinfo:
        var.ifSetType([1,2,3])
    assert excinfo.value.message == "var1 was expected to be type dict, but <class 'list'> was found"


def test_validation_contains():
    var = C()

    assert True == var.contains('yes')

    with pytest.raises(ValidationException) as excinfo:
        var.contains2("")
    assert excinfo.value.message == "'contains' validation expects a comma seperated list of items to check against, 'yes' was found"


    with pytest.raises(ValidationException) as excinfo:
        var.contains("something else")
    assert excinfo.value.message == "One of [yes,no] was expected, but 'something else' was found for parameter var1"
