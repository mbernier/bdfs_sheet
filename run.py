import sys, time, pydantic
from collections import OrderedDict
from modules.caches.flat import Flat_Cache
from modules.helper import Helper
from pydantic.dataclasses import dataclass
from pydantic.typing import Annotated, Type, Optional, Union
from modules.dataMoves.originalbdfs_inventory.sarto_inventory.sarto import Originalbdfs_Inventory_To_Sarto_Inventory
from modules.decorator import Debugger
from pydantic import validate_arguments

if __name__ == "__main__":

    # migrator = Originalbdfs_Inventory_To_Sarto_Inventory()
    # migrator.run() 

    @dataclass
    class DC1():
        name:str
        flag:bool
    
    @dataclass
    class DC2(DC1):
        cake: str

    class Example():
        data: Type[DC1]

        @Debugger
        @validate_arguments(config=dict(arbitrary_types_allowed=True))
        def __init__(self, obj:Union[DC1, Type[dataclass]]):
            self.data = obj
        
        @staticmethod
        def static():
            print("static worked")
    
    dc1 = DC1(name="matt", flag=True)
    print(type(dc1))
    dc2 = DC2(name="MATT", flag=False, cake="Van")

    obj1 = Example(dc1)
    obj2 = Example(dc2)

