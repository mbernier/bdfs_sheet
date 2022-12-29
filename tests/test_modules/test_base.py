import pytest
from modules.base import Base_Class

class newClass(Base_Class):
    def importClass(self, klass): 
        return super().importClass(klass)


def test_importClass():
    klass = newClass()
    klass.importClass("modules.base.Base_Class")
    with pytest.raises(ModuleNotFoundError) as excinfo:
        klass.importClass("modules.some.bullshit")

    assert excinfo.value.msg == "No module named 'modules.some'"