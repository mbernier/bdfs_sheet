import pytest
from modules.decorators import validate
from modules.base import BaseClass

class A(BaseClass):

    @validate('var1', ['exists'])
    @validate('var2', ['exists', 'notNone'])
    def bat(self, var1=None, var2=None):
        pass

    @validate('var2', ['orExists:var3'])
    def foo(self, var1=None, var2=None, var3=None):
        pass


def test_passes_validate():
    var = A()
    var.bat(2, "4")
    # no exceptions are thrown

def test_passes_validate2():
    var = A()
    var.bat(1, var2="3")
    # no exceptions are thrown

def fails_validate_notNone():
    var = A()
    with pytest.raises(ValidationException) as excinfo:
        var.bat(1)
    excinfo.value.message == "var2 was passed as None, but needs to be set"
    

def fails_validate_orExists():
    var = A()
    with pytest.raises(ValidationException) as excinfo:
        var.foo(1, None, None)
    excinfo.value.message == "Either var2 or var3 was expected but neither was found"