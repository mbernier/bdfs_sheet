import time
from collections import OrderedDict
from modules.cache import BdfsCache
from modules.caches.exception import Flat_Cache_Exception
from modules.decorator import Debugger
from pydantic import BaseModel as PydanticBaseModel, Field, validate_arguments
from pydantic.dataclasses import dataclass
from typing import Union

class Flat_Cache_Data(PydanticBaseModel):
    storage:dict = Field(default_factory=dict)
    size:int = Field(default_factory=int)
    update_timestamp:float = Field(default_factory=float)


class Flat_Cache(BdfsCache):

    ####
    #
    # Validations for params
    #
    ####

    #@Debugger
    @validate_arguments
    def __init__(self, locations:list=None, data:list=None):
        
        self.data = Flat_Cache_Data()
        
        if None != locations: # locations are set    
            self.load_locations(locations=locations)

            if None != data: # initdata is set
                self.load(data=data)
        
        elif None != data: # locations are not set and initdata is set
            raise Flat_Cache_Exception("Need locations in order to load data to Flat_Cache")


    #@Debugger
    @validate_arguments
    def load_locations(self, locations:list):
        if self.size() > 0:
            raise Flat_Cache_Exception("Locations are already loaded, to add new keys use insert_location(location)")

        for location in locations:
            self.insert_location(position=location, skip_update_timestamp=True)


    #@Debugger
    @validate_arguments
    def load(self, data:list=None):
        if None != data:
            foundTimestamp = False
            for index,value in enumerate(data):
                # let's treat updated date as special
                if index == "update_timestamp":
                    self.data.update_timestamp = value
                    foundTimestamp = True
                else:
                    self.insert(index, value, skip_update_timestamp=True)

            if False == foundTimestamp:
                self.update_timestamp()

    ####
    #
    # Helper methods, bc data is stored in two places in Nested_Cache_Row
    #
    ####

    #@Debugger
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

    #@Debugger
    @validate_arguments
    def getBothDicts(self, position:Union[int, str]):
        
        self.fail_if_position_dne(position)

        dict1 = self.data.storage[position]
        
        # we don't have anything here to return, we can't create a data dict either bc we only have position
        if dict1 == None:
            return None, None

        dict2 = self.data.storage[dict1["position"]]

        locationDict = dict1 if type(dict1["position"]) is int else dict2
        indexDict = dict2 if dict1 == locationDict else dict1

        return locationDict, indexDict

    #@Debugger
    @validate_arguments
    def getOtherPosition(self, position:Union[int, str]):
        self.fail_if_position_dne(position)

        dict1 = self.data.storage[position]

        locationPosition = position if type(position) is str else dict1["position"]
        indexPosition = dict1["position"] if position == locationPosition else position

        return locationPosition, indexPosition

    ####
    #
    # Updated - whenever the data is changed, let's record and then hand this back on select
    #
    ####
    
    # This is added on __writeSpecial so that it is captured whenever data changes
    # timestamp is output on getAs methods
    #@Debugger
    def update_timestamp(self):
        self.data.update_timestamp = time.time()

    #@Debugger
    def getUpdateTimestamp(self):
        return self.data.update_timestamp

    ####
    #
    # Insert Data
    #
    ####

    # put data in a location if it doesn't have data, if it does, error out
    #@Debugger
    @validate_arguments(config=dict(smart_union=True))
    def insert(self, position: Union[int,str], data=None, skip_update_timestamp=False):
        self.fail_if_position_dne(position)

        if None == self.select(position): # is there data in the location?
            self.__write(position=position, data=data, skip_update_timestamp=skip_update_timestamp)
        else:
            raise Flat_Cache_Exception("Flat_Cache has '{}' at location: {}. To update data in the cache, use update()".format(self.select(position), position))


    ####
    #
    # Update Datapos
    #
    ####

    #change the data at the location
    #@Debugger
    def update(self, position: Union[int,str], data=None):
        self.fail_if_position_dne(position)
        self.__write(position=position, data=data)

    ####
    #
    # Select Data
    #
    ####

    # get the data at the location, or get everything from string keys as a dict
    #@Debugger
    @validate_arguments
    def select(self, position: Union[int,str] = None, updated_timestamp:bool=True):
        if None == position:
            return self.getAsDict(updated_timestamp=updated_timestamp)
        else:
            self.fail_if_position_dne(position)
            return self.data.storage.get(position)['data']


    ####
    #
    # Delete Data
    #
    ####

    #@Debugger
    @validate_arguments
    def delete(self, position:Union[str,int]):
        self.fail_if_position_dne(position)
        self.__write(position, None)


    ####
    #
    # Write Data - the only way to change what is in the data field
    #
    ####

    # write whatever data we get to the cache location/index pair
    #@Debugger
    @validate_arguments
    def __write(self, position: Union[int,str], data=None, skip_update_timestamp=False):
        locationDict, indexDict = self.getBothDicts(position)

        # get the right positions from the opposite object
        index = locationDict['position']
        location = indexDict['position']

        self.__writeSpecial(location=location, index=index, data=data, skip_update_timestamp=skip_update_timestamp)

    # lets us write to whatever location/index combination we want
    #   normally, we would get the right pair and pass it here
    #   when we need to shift locations up/down this will be called to overwrite
    #   items that may already exist
    #@Debugger
    @validate_arguments
    def __writeSpecial(self, location:str, index:int, data=None, skip_update_timestamp=False):
        locationDict, indexDict = self.createDataDicts(location=location, index=index, data=data)
        
        if None != data: # it's already set, why set it again?
            # set the data to whatever is passed
            locationDict['data'] = data
            indexDict['data'] = data

        # write the data to storage
        self.data.storage[location] = locationDict
        self.data.storage[index] = indexDict
    
        if False == skip_update_timestamp:
            self.update_timestamp()

    ####
    #
    # Location Methods
    #
    ####

    #@Debugger
    @validate_arguments
    def positionExists(self, position: Union[int,str]):
        return (position in self.data.storage.keys()) # use the storage object here, to prevent excess looping through keys


    #@Debugger
    @validate_arguments
    def fail_if_position_dne(self, position:Union[int,str]):
        if not self.positionExists(position):
            raise Flat_Cache_Exception("Location '{}' does not exist, try \"insert_location('{}')\"".format(position, position))        
    

    #@Debugger
    def increaseSize(self):
        self.data.size += 1
    

    #@Debugger
    def decreaseSize(self):
        self.data.size -= 1


    # remove a location from storage
    #@Debugger
    @validate_arguments
    def delete_location(self, position: Union[int,str]):
        # you can't delete the updated_timestamp
        if position == "updated_timestamp":
            return

        self.fail_if_position_dne(position)
        
        # cache the data locally just in case
        removeLocationDict, removeIndexDict = self.getBothDicts(position)
        removeLocation = removeIndexDict['position']
        removeIndex = removeLocationDict['position']

        # remove the old locations from storage
        del self.data.storage[removeLocation]
        del self.data.storage[removeIndex]

        self.__shift_indexes(removeIndex+1, -1)
        self.decreaseSize() 


    #@Debugger
    @validate_arguments
    def __shift_indexes(self, shiftFromIndex:int, shiftBy:int, skip_update_timestamp=False):
        # we can go from the index to the end, bc we are shifting down
        # e.g. 3->2, 4->3, 5->4
        # assumes you don't care about what's in 2, so 3 can replace, then 3 is gone so 4 can replace
        rangeToShift = range(
                            shiftFromIndex, 
                            self.size() # use size+1 here so that we can 
                        )
        if shiftBy > 0:
            # we need to go through from the end to the index, so we don't overwrite data that exists
            # e.g. 3->4, 4->5, 5->6
            # if we shift 3->4 first, then we overwrite 4 and 5 to 3
            rangeToShift = reversed(rangeToShift)
            
        # update the indexes after the removed index
        for changeIndex in rangeToShift:
            # shift the index to one position lower
            changeIndexTo = changeIndex + shiftBy
            
            # allows us to migrate to a new index
            self.update_index(changeIndex, changeIndexTo)
        
        if False == skip_update_timestamp:
            self.update_timestamp()


    #@Debugger
    @validate_arguments
    def insert_location(self, position:str, index:int=None, skip_update_timestamp=False):
        # you can't insert the updated_timestamp
        if position == "updated_timestamp":
            return

        if self.positionExists(position):
            raise Flat_Cache_Exception(f"Position '{position}' already exists, you cannot insert a new location to Flat_Cache that already exists")
    
        if None == index or index == self.size():
            index = self.size()
        elif index > self.size(): # we have this second, bc if index is None for this, python barfs
            # we are well beyond the limit
            # @todo, maybe, allow entering indexes with no positional dataDict and adding checks whenever we retrieve both dicts, to validate whether we have a named dict.
                # another option would be to add the positional dicts, but as strings of the index dict like "FC_auto:1" and adding checks for "FC_auto", then throwing errors if they don't get fixed
                # this is a lot of extra work that is not needed right now
            raise Flat_Cache_Exception(f"index '{index}' is much greater than the current size of Flat_Cache: {self.size()}, try adding items in between {self.size()} and '{index}'")
        else:
            self.__shift_indexes(index,1, skip_update_timestamp=skip_update_timestamp)

        # we put the location in with None as the data
        self.__writeSpecial(location=position, index=index, data=None, skip_update_timestamp=skip_update_timestamp)
        self.increaseSize()


    #@Debugger
    @validate_arguments
    def update_index(self, oldIndex, newIndex):
        if self.positionExists(newIndex):
            raise Flat_Cache_Exception(f"Cannot move index:{oldIndex} to index:{newIndex} bc there is already data at index:{newIndex}")

        # get whatever we have at the original Index
        locationDict, indexDict = self.getBothDicts(oldIndex)

        # delete the old data
        del self.data.storage[oldIndex]
        del self.data.storage[indexDict['position']]

        #create the item at the new positions
        self.__writeSpecial(location=indexDict['position'], index=newIndex, data=indexDict['data'])
        

    ####
    #
    # Clear Data
    #
    ####

    # clears the entire cache
    #@Debugger
    def clear_all(self):
        for key in self.getKeys():
            self.delete(key)

    ####
    #
    # Meta Methods
    #
    ####

    # returns a list of the string keys from the storage dict
    #@Debugger
    @validate_arguments(config=dict(arbitrary_types_allowed=True))
    def getKeys(self, keyType=None, all:bool = False) -> list:
        output = []

        #pydantic didn't like typing or being passed "types", so changed method sig from keyType:type=str or keyType=str to keyType=None
        #   and then overloaded the default here
        if None == keyType:
            keyType = str

        if not str is keyType and not int is keyType: # we don't have expected types
            raise Flat_Cache_Exception(f"Flat Cache can output either int or str keys, but not '{keyType}'")

        for indexKey in range(0,self.size()):

            if int is keyType or True == all:
                # append indexKey or 
                # add the index key first if True == all
                output.append(indexKey)
            
            if str is keyType or True == all:
                # get the string keys in the correct order
                output.append(self.data.storage[indexKey]['position'])

        return output


    # self.data.size is managed through the places where we update locations, via increaseSize() and decreaseSize()
    #@Debugger
    def size(self) -> int:
        return self.data.size


    #@Debugger
    @validate_arguments
    def __str__(self, updated_timestamp:bool=True) -> str:
        output = "Flat_Cache: \n"
        timestamp = self.getUpdateTimestamp()
        for item in self.getKeys():
            if item == "update_timestamp" and updated_timestamp == True:
                data = self.getUpdateTimestamp()
            else:
                data = self.select(item)
            output += "\t{}: {}\n".format(item, data)
        return output


    #@Debugger
    @validate_arguments
    def getAsList(self, updated_timestamp:bool=True) -> list:
        output = []
        for index in self.getKeys(keyType=int):
            output.insert(index, self.select(index))
        if True == updated_timestamp:
            output.append(self.getUpdateTimestamp())
        return output


    #@Debugger
    @validate_arguments
    def getAsDict(self, updated_timestamp:bool=True) -> dict:
        output = OrderedDict()
        for index in self.getKeys(keyType=int): #it really doesn't matter which type you choose here
            position, index = self.getOtherPosition(index)
            output[position] = self.select(index)
        if True == updated_timestamp:
            output["update_timestamp"] = self.getUpdateTimestamp()
        return output