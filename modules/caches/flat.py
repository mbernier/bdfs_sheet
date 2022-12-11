import sys, pydantic
from pydantic import Field, BaseModel as PydanticBaseModel
from pydantic.dataclasses import dataclass
# from dataclasses import field as dc_field
from typing import Union
from pydantic import validator, validate_arguments
from modules.cache import BdfsCache
from modules.caches.exception import Flat_Cache_Exception
from modules.decorator import Debugger
from collections import OrderedDict
from pprint import pprint

# @todo add a toString method

class Flat_Cache_Data(PydanticBaseModel):
    storage:dict = Field(default_factory=dict)

class Flat_Cache(BdfsCache):

    ####
    #
    # Validations for params
    #
    ####

    @Debugger
    def __init__(self, initdata=None):
        self.data = Flat_Cache_Data()
        self.load(initdata)

    @Debugger
    def load(self, data=None):
        if None != data:
            for index,value in enumerate(data):
                print(f"index: {index}, value:{value}")
                self.set_at_location(index, value)


    # put data in a location if it doesn't have that data, if it does, error out
    @Debugger
    @validate_arguments(config=dict(smart_union=True))
    def set_at_location(self, location: Union[int,str], data=None):
        if None == self.get_at_location(location):
            self.write(location=location, data=data)
        else:
            raise Flat_Cache_Exception("Flat_Cache has '{}' at location: {}. To update data in the cache, use update_at_location()".format(self.get_at_location(location), location))


    # remove the data from the location, but keep the location index
    @Debugger
    def unset_at_location(self, location: Union[int,str]):
        if self.get_at_location(location):
            self.data.storage[location] = None


    #change the data at the location
    @Debugger
    def update_at_location(self, location: Union[int,str], data=None):
        if None == self.get_at_location(location):
            raise Flat_Cache_Exception("There is nothing to update at position '{}' consider using set".format(location))
        self.write(location=location, data=data)


    # get the data at the location
    @Debugger
    def get_at_location(self, location: Union[int,str]):
        return self.data.storage.get(location)

    @Debugger
    def remove_location(self, location: Union[int,str]):
        del self.data.storage[location]

    # returns a list of keys from the storage dict
    @Debugger
    def getKeys(self):
        self.data.storage.keys()


    # write data to the cache location
    @Debugger
    def write(self, location: Union[int,str], data=None):
        self.data.storage[location] = data


    # clears the entire cache
    @Debugger
    def clear_all(self):
        self.data.storage.clear()


    # give us everything
    @Debugger
    def value(self):
        return self.getStorage()

    @Debugger
    def size(self):
        return len(self.getStorage())


    @Debugger
    def __str__(self) -> str:
        output = "Flat_Cache: \n"
        for item in self.getStorage():
            output += "\t{}: {}\n".format(item, self.get(item))
        return output

    @Debugger
    def getAsList(self):
        data = self.getStorage()
        output = []
        for index in data:
            if int == type(index):
                output.insert(index, data[index])
        return output


    @Debugger
    def getAsDict(self):
        data = self.getStorage()
        output = OrderedDict()
        for index in data:
            if int != type(index):
                output[index] = data[index]
        return output

    @Debugger
    def validate_locationExists(self, location: Union[int,str]):
        if location in self.data.storage.keys():
            return True
        return False