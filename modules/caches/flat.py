import sys, pydantic
from collections import OrderedDict
from modules.cache import BdfsCache
from modules.caches.exception import Flat_Cache_Exception
from modules.decorator import Debugger
from pprint import pprint
from pydantic import BaseModel as PydanticBaseModel, Field, validate_arguments
from pydantic.dataclasses import dataclass
from typing import Union

# @todo add a toString method

class Flat_Cache_Data(PydanticBaseModel):
    storage:dict = Field(default_factory=dict)

raise Exception("this is confusing - use insert, update, delete instead of set, get, add, remove. Insert can go if Null, Update otherwise, Delete deletes. Update to unset a field, delete to remove a row")

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
                self.set_at_location(index, value)


    # put data in a location if it doesn't have data, if it does, error out
    @Debugger
    @validate_arguments(config=dict(smart_union=True))
    def set_at_location(self, location: Union[int,str], data=None):
        print(f"FC: location: {location}, data: {self.get_at_location(location)}")
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

    @Debugger
    def delete_at_location(self, location:Union[str,int]):
        self.data.storage[location] = None

    # returns a list of keys from the storage dict
    @Debugger
    def getKeys(self):
        return self.data.storage.keys()


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
        return self.data.storage

    @Debugger
    def size(self):
        return len(self.data.storage)


    @Debugger
    def __str__(self) -> str:
        output = "Flat_Cache: \n"
        for item in self.data.storage:
            output += "\t{}: {}\n".format(item, self.data.storage.get(item))
        return output

    @Debugger
    def getAsList(self):
        data = self.data.storage
        output = []
        for index in data:
            if int == type(index):
                output.insert(index, data[index])
        return output


    @Debugger
    def getAsDict(self):
        data = self.data.storage
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