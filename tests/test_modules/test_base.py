import pytest
from modules.base import BaseClass

class newClass(BaseClass):
    def importClass(self, klass): 
        return super().importClass(klass)


def test_importClass():
    klass = newClass()
    klass.importClass("modules.base.BaseClass")
    with pytest.raises(ModuleNotFoundError) as excinfo:
        klass.importClass("modules.some.bullshit")

    assert excinfo.value.msg == "No module named 'modules.some'"