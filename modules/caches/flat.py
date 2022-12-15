import sys, pydantic
from collections import OrderedDict
from modules.cache import BdfsCache
from modules.caches.exception import Flat_Cache_Exception
from modules.decorator import Debugger
from pprint import pprint
from pydantic import BaseModel as PydanticBaseModel, Field, validate_arguments
from pydantic.dataclasses import dataclass
from typing import Union


class Flat_Cache_Data(PydanticBaseModel):
    storage:dict = Field(default_factory=dict)


class Flat_Cache(BdfsCache):

    ####
    #
    # Validations for params
    #
    ####

    @Debugger
    @validate_arguments
    def __init__(self, locations:OrderedDict=None, data:list=None):
        
        self.data = Flat_Cache_Data()
        
        if None != locations: # locations are set    
            self.load_locations(locations=locations)

            if None != initdata: # initdata is set
                self.load(data=data)
        
        elif None != initdata: # locations are not set and initdata is set
            raise Flat_Cache_Exception("Need locations in order to load data to Flat_Cache")


    @Debugger
    @validate_arguments
    def load_locations(self, locations:OrderedDict):
        if len(self.getKeys()) > 0:
            raise Flat_Cache_Exception("Locations are already loaded, to add new keys use add_location(location)")

        for index, location in locations:
            self.add_location(location)

    @Debugger
    @validate_arguments
    def load(self, data:list=None):
        if None != data:
            for index,value in enumerate(data):
                self.insert(index, value)

    ####
    #
    # Helper methods, bc data is stored in two places in Nested_Cache_Rows_Data
    #
    ####

    @Debugger
    @validate_arguments
    def createDataDicts(self, location:str, index:int, data=None):

        locationData = {
            "position": index,
            "data": data
        }

        indexData = {
            "position": location,
            "data": data 
        }

        return locationData, indexData

    @Debugger
    @validate_arguments
    def getBothDicts(self, position:Union[int, str]):
        dict1 = super()._get_at_location(position)
        
        # we don't have anything here to return, we can't create a data dict either bc we only have position
        if dict1 == None:
            return None, None

        dict2 = super()._get_at_location(dict1["position"])

        locationDict = dict1 if type(dict1["position"]) is int else dict2
        indexDict = dict2 if dict1 == locationDict else dict1

        return locationDict, indexDict

    @Debugger
    @validate_arguments
    def getOtherPosition(self, position:Union[int, str]):
        self.fail_if_location_dne(position)

        dict1 = super()._get_at_location(position)

        locationPosition = position if type(position) is str else dict1["position"]
        indexPosition = dict1["position"] if position == locationPosition else position

        return locationPosition, indexPosition

    ####
    #
    # Insert Data
    #
    ####

    # put data in a location if it doesn't have data, if it does, error out
    @Debugger
    @validate_arguments(config=dict(smart_union=True))
    def insert(self, position: Union[int,str], data=None):
        self.fail_if_position_dne(position)

        if None == self.select(position): # is there data in the location?
            self.__write(position=position, data=data)
        else:
            raise Flat_Cache_Exception("Flat_Cache has '{}' at location: {}. To update data in the cache, use update()".format(self.select(position), position))


    ####
    #
    # Update Datapos
    #
    ####

    #change the data at the location
    @Debugger
    def update(self, position: Union[int,str], data=None):
        self.fail_if_position_dne(position)
        self.__write(position=position, data=data)


    ####
    #
    # Select Data
    #
    ####

    # get the data at the location, or get everything from string keys as a dict
    @Debugger
    @validate_arguments
    def select(self, position: Union[int,str] = None):
        if None == position:
            return self.__select_string_keys()
        else:
            self.fail_if_position_dne(position)
            return self.data.storage.get(position)['data']


    @Debugger
    def __select_string_keys(self):
        output = {}
        for key in self.getKeys():
            output[key] = self.get(key)
        return output


    ####
    #
    # Delete Data
    #
    ####

    @Debugger
    @validate_arguments
    def delete(self, position:Union[str,int]):
        self.__write(position, None)


    ####
    #
    # Write Data - the only way to change what is in the data field
    #
    ####

    # write whatever data we get to the cache location/index pair
    @Debugger
    @validate_arguments
    def __write(self, position: Union[int,str], data=None):
        locationDict, indexDict = self.getBothDicts(position)

        # get the right positions from the opposite object
        index = locationDict['position']
        location = indexDict['position']

        self.__writeSpecial(location=location, index=index, data=data)

    # lets us write to whatever location/index combination we want
    #   normally, we would get the right pair and pass it here
    #   when we need to shift locations up/down this will be called to overwrite
    #   items that may already exist
    @Debugger
    @validate_arguments
    def __writeSpecial(self, location:str, index:int, data=None):
        locationDict, indexDict = createDataDicts(self, location=location, index=index, data=data)
        
        # set the data to whatever is passed
        locationDict['data'] = data
        indexDict['data'] = data

        # write the data to storage
        self.data.storage[location] = locationDict
        self.data.storage[index] = indexDict

    ####
    #
    # Location Methods
    #
    ####

    @Debugger
    @validate_arguments
    def positionExists(self, position: Union[int,str]):
        return (position in self.getKeys(all=True))


    @Debugger
    @validate_arguments
    def fail_if_position_dne(self, position:Union[int,str]):
        if not self.locationExists(position):
            raise Flat_Cache_Exception("Location '{}' does not exist, try \"add_location('{}')\"".format(position, position))


    # add a new location to storage
    @Debugger
    @validate_arguments
    def add_location(self, location: Union[int,str]):
        if self.locationExists(location):
            raise Flat_Cache_Exception("Location '{}' alread exists".format(location))
        else:
            locationDict, indexDict = self.createDataDicts(location, self.size(), None)
            self.data.storage[location] = locationDict
            self.data.storage[index] = indexDict


    # remove a location from storage
    @Debugger
    @validate_arguments
    def remove_location(self, position: Union[int,str]):
        self.fail_if_location_dne(location)

        # cache the data locally just in case
        removeLocationDict, removeIndexDict = self.getBothDicts(position)
        removeLocation = removeIndexDict['position']
        removeIndex = removeLocationDict['position']

        # remove the old locations from storage
        del self.data.storage[removeLocation]
        del self.data.storage[removeIndex]

        # update the indexes after the removed index
        for changeIndex in range(removeIndex+1, self.size()):
            # shift the index to one position lower
            changeIndexTo = changeIndex - 1

            # allows us to migrate to a new index
            self.update_index(changeIndex, changeIndexTo)

    @Debugger
    @validate_arguments
    def update_index(self, oldIndex, newIndex):

        if self.locationExists(newIndex):
            raise Flat_Cache_Exception(f"Cannot move index:{oldIndex} to index:{newIndex} bc there is already data at index:{newIndex}")

        # get whatever we have at the original Index
        indexDict = self.select(oldIndex)

        # delete the item at the oldIndex, so that we don't have two copies
        del self.data.storage[oldIndex]

        #create the item at the newIndex, overwrite the position value of the location item
        self.__writeSpecial(location=indexDict['position'], index=newIndex, data=indexDict['data'])


    ####
    #
    # Clear Data
    #
    ####


    # clears the entire cache
    @Debugger
    def clear_all(self):
        for key in self.getKeys():
            self.delete(key)

    ####
    #
    # Meta Methods
    #
    ####

    # returns a list of the string keys from the storage dict
    @Debugger
    @validate_arguments
    def getKeys(self, all:bool=False):
        output = []
        for key in self.data.storage.keys():
            if False == all and type(key) is str: # by default we return the strings
                output.append(key)
            else: # if asked, we can return the strings and integer keys
                output.append(key)
        return output


    @Debugger
    def size(self):
        return len(self.getKeys())


    @Debugger
    def __str__(self) -> str:
        output = "Flat_Cache: \n"
        for item in self.getKeys():
            output += "\t{}: {}\n".format(item, self.select(item))
        return output


    @Debugger
    def getAsList(self):
        data = self.data.storage
        output = []
        for index in self.getKeys():
            output.insert(index, self.select(index))
        return output


    @Debugger
    def getAsDict(self):
        data = self.data.storage
        output = OrderedDict()
        for index in self.getKeys():
            output[index] = self.select(index)
        return output
