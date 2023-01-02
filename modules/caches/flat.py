import time
from collections import OrderedDict
from modules.cache import Bdfs_Cache
from modules.caches.exception import Flat_Cache_Exception
from modules.decorator import Debugger
from pydantic import BaseModel as PydanticBaseModel, Field, validate_arguments
from pydantic.dataclasses import dataclass
from typing import Union

MANUALLY_SETTING_TIMESTAMP_OUTSIDE_INITIAL_LOAD = "manually setting timestamp outside initial data load is forbidden"
UPDATE_TIMESTAMP_KEY = "update_timestamp"
UPDATE_TIMESTAMP_POSTFIX = f"_{UPDATE_TIMESTAMP_KEY}"


class Flat_Cache_Data(PydanticBaseModel):
    storage:dict = Field(default_factory=dict)
    size:int = Field(default_factory=int)
    update_timestamp:float = Field(default_factory=float)
    initial_data:list = Field(default_factory=list)
    # this allows us to know whether to set a timestamp or not when we load data
    # if true, do not modify the timestamp unless it isn't there. 
    # if false and we change the data, modify the timestamps
    initial_data_load:bool = True
    is_empty:bool = True


class Flat_Cache(Bdfs_Cache):

    @Debugger
    @validate_arguments
    def __init__(self, data:dict=None):
        
        self.data = Flat_Cache_Data()
        
        self.__initial_data_load(data)

        # if we never had an update_timestamp and we didn't load data, we want timestamp to be set now
        if 0.0 == self.data.update_timestamp:
            self.update_timestamp(UPDATE_TIMESTAMP_KEY)
        
    ####
    #
    # Setup Methods for the Class
    #
    ####

    @Debugger
    @validate_arguments
    def __initial_data_load(self, data:dict=None):
        if data != None:
            timestamps = {}
            
            for location, value in data.items():

                # if we get a timestamp with the data, we need to remove it from locations and data
                if Flat_Cache.positionIsTimestamp(location): #others will be fieldnameUPDATE_TIMESTAMP_POSTFIX
                    # let's hold onto these for a second
                    timestamps[location] = value
                else:
                    # make sure the location is there
                    self.insert_location(position=location)

                    # add the data to the location
                    self.insert(location, value)
                    
                    # create a timestamp if we didn't get one
                    timestampLocation = Flat_Cache.makeTimestampName(position=location)

                    # update the timestamp to now, we will overwrite if we have it later
                    self.update_timestamp(position=location, timestamp=time.time())
            
            # add in whatever timestamps are left, likely only "update_timestamp"
            for timestamp, value in timestamps.items():
                if "" == value: # if the field is in the spreadsheet, but it's empty we need to account for that
                    value = None
                # load the timestamps properly
                self.update_timestamp(timestamp, value) #set the value
        
        # From now on anything we add should be updated with a new timestamp
        self.data.initial_data_load = False


    ####
    #
    # Data Manipulation Methods
    #
    ####

    # put data in a location if it doesn't have data, if it does, error out
    @Debugger
    @validate_arguments(config=dict(smart_union=True))
    def insert(self, position: Union[int,str], data=None):
        if Flat_Cache.positionIsTimestamp(position): #skip it
            return

        self.fail_if_position_dne(position)

        if None == self.select(position): # is there data in the location?
            self.__write(position=position, data=data)
        else:
            raise Flat_Cache_Exception("Flat_Cache has '{}' at location: {}. To update data in the cache, use update()".format(self.select(position), position))


    #change the data at the location
    @Debugger
    def update(self, position: Union[int,str], data:dict=None):
        if Flat_Cache.positionIsTimestamp(position): #skip it
            return
        self.fail_if_position_dne(position)
        self.__write(position=position, data=data)


    # get the data at the location, or get everything from string keys as a dict
    @Debugger
    @validate_arguments
    def select(self, position: Union[int,str] = None, update_timestamp:bool=True):
        if Flat_Cache.positionIsTimestamp(position): #skip it
            raise Flat_Cache_Exception(f"To select a timestamp, like '{position}', use the timestamp methods")

        if None == position:
            return self.getAsDict(update_timestamp=update_timestamp)
        else:
            self.fail_if_position_dne(position)
            return self.data.storage.get(position)['data']


    @Debugger
    @validate_arguments
    def delete(self, position:Union[str,int]):
        if Flat_Cache.positionIsTimestamp(position): #skip it
            raise Flat_Cache_Exception("You cannot delete a timestamp field")

        self.fail_if_position_dne(position)
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

        self.__writeSpecial(location=location, index=index, data=data, timestamp=time.time())


    # writes whatever is passed, methods that call this method MUST handle the control logic
        # if they don't, then this WILL fuck up the data store all on it's own
    @Debugger
    @validate_arguments
    def __writeSpecial(self, location:str, index:int, data=None, timestamp:float=None):
        # write the data to storage
        locationDict, indexDict = self.__createDataDicts(
                                        location    = location, 
                                        index       = index, 
                                        data        = data, 
                                        timestamp   = timestamp)
        
        self.data.storage[location] = locationDict
        self.data.storage[index] = indexDict

        # if we ever get any data that is not None, set this to false
        if data != None:
            self.data.is_empty = False

    # this is a "dumb" method, will write whatever is passed. ONLY used in __writeSpecial()
    @Debugger
    @validate_arguments
    def __createDataDicts(self, location:str, index:int, data=None, timestamp:float=None):

        locationData = {
            "position": index,
            "data": data,
            "timestamp": timestamp
        }

        indexData = {
            "position": location,
            "data": data,
            "timestamp": timestamp
        }

        return locationData, indexData


    ####
    #
    # Location Methods
    #
    ####

    @Debugger
    @validate_arguments
    def getOtherPosition(self, position:Union[int, str]):
        self.fail_if_position_dne(position)

        dict1 = self.data.storage[position]

        locationPosition = position if type(position) is str else dict1["position"]
        indexPosition = dict1["position"] if position == locationPosition else position

        return locationPosition, indexPosition


    @Debugger
    @validate_arguments
    def positionExists(self, position: Union[int,str]):
        return (position in self.data.storage.keys()) # use the storage object here, to prevent excess looping through keys


    @Debugger
    @validate_arguments
    def fail_if_position_dne(self, position:Union[int,str]):
        if not self.positionExists(position):
            raise Flat_Cache_Exception("Location '{}' does not exist, try \"insert_location('{}')\"".format(position, position))        


    # remove a location from storage
    @Debugger
    @validate_arguments
    def delete_location(self, position: Union[int,str]):
        # you can't delete update_timestamps
        if Flat_Cache.positionIsTimestamp(position):
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


    @Debugger
    @validate_arguments
    def insert_location(self, position:str, index:int=None):
        # you can't insert the update_timestamp
        if Flat_Cache.positionIsTimestamp(position):
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
            self.__shift_indexes(index,1)
        
        # we put the location in with None as the data
        self.__writeSpecial(location=position, index=index, data=None)
        
        self.increaseSize()


    @Debugger
    @validate_arguments
    def update_index(self, oldIndex, newIndex):
        if self.positionExists(newIndex):
            raise Flat_Cache_Exception(f"Cannot move index:{oldIndex} to index:{newIndex} bc there is already data at index:{newIndex}")

        # get whatever we have at the original Index
        _, indexDict = self.getBothDicts(oldIndex)

        # delete the old data
        del self.data.storage[oldIndex]
        del self.data.storage[indexDict['position']]

        #create the item at the new positions
        self.__writeSpecial(location=indexDict['position'], index=newIndex, data=indexDict['data'])
        

    @Debugger
    @validate_arguments
    def __shift_indexes(self, shiftFromIndex:int, shiftBy:int):
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
    # Helper methods, bc data is stored in two places in Nested_Cache_Row
    #
    ####

    @Debugger
    @validate_arguments
    def getBothDicts(self, position:Union[int, str]):
        
        self.fail_if_position_dne(position)

        dict1 = self.data.storage[position].copy()
        
        # we don't have anything here to return, we can't create a data dict either bc we only have position
        if dict1 == None:
            return None, None

        dict2 = self.data.storage[dict1["position"]].copy()

        locationDict = dict1 if type(dict1["position"]) is int else dict2
        indexDict = dict2 if dict1 == locationDict else dict1

        return locationDict.copy(), indexDict.copy()


    @Debugger
    @validate_arguments
    def getDict(self, position:Union[int,str]):
        self.fail_if_position_dne(position)
        return self.data.storage[position].copy()


    ####
    #
    # Update Timestamp Methods
    #
    ####
    
    # This is added on __writeSpecial so that it is captured whenever data changes
    # timestamp is output on getAs methods
    @Debugger
    @validate_arguments
    def update_timestamp(self, position:str, timestamp:float=None):
        if None == timestamp: # if we got none on initial load, set it, otherwise use what's passed
            timestamp = time.time()

        if position == UPDATE_TIMESTAMP_KEY:
            self.data.update_timestamp = timestamp
            return

        if self.data.initial_data_load == False: # we are outside the initial load time            
            # this is the only timestamp we can update outside initial load
            # fail, bc otherwise __write handles the updating of timestamp
            raise Flat_Cache_Exception(MANUALLY_SETTING_TIMESTAMP_OUTSIDE_INITIAL_LOAD)

        # just make sure that the position is a position and not a timestamp
        position = self.__convertTimestampNameToPosition(position)

        locationDict, indexDict = self.getBothDicts(position)
        
        # we want to rewrite the dicts, with the new timestamp
        self.__writeSpecial(location    = indexDict["position"], 
                            index       = locationDict["position"], 
                            data        = locationDict['data'],
                            timestamp   = timestamp)


    @Debugger
    @validate_arguments
    def getUpdateTimestamp(self, position:str)->float:
        # get the default
        if UPDATE_TIMESTAMP_KEY == position:
            return self.data.update_timestamp
        if UPDATE_TIMESTAMP_POSTFIX in position:
            #someone passed the timestamp name, undo this
            position = self.__convertTimestampNameToPosition(position)
        
        # get timestamp for position
        self.fail_if_position_dne(position)
        return self.data.storage[position]['timestamp']


    @classmethod
    @Debugger
    def makeTimestampName(cls, position:str) -> str:
        if Flat_Cache.positionIsTimestamp(position):
            return position
        
        return f"{position}_update_timestamp"
    
    @Debugger
    @validate_arguments
    def __convertTimestampNameToPosition(self, name):
        return name.replace(UPDATE_TIMESTAMP_POSTFIX,"")


    @classmethod
    @Debugger
    def positionIsTimestamp(cls, position):
        if type(position) is str and UPDATE_TIMESTAMP_KEY in position:
            return True
        return False

    ####
    #
    # Meta Methods
    #
    ####

    @Debugger
    def isEmpty(self):
        return self.data.is_empty

    @Debugger
    def increaseSize(self):
        self.data.size += 1
        self.update_timestamp(UPDATE_TIMESTAMP_KEY)
    

    @Debugger
    def decreaseSize(self):
        self.data.size -= 1
        self.update_timestamp(UPDATE_TIMESTAMP_KEY)

    # returns a list of the string keys from the storage dict
    @Debugger
    @validate_arguments(config=dict(arbitrary_types_allowed=True))
    def getKeys(self, keyType=None, all:bool = False) -> list:
        output = []

        #pydantic didn't like typing or being passed "types", so changed method sig from keyType:type=str or keyType=str to keyType=None
        #   and then overloaded the default here
        if None == keyType:
            keyType = str

        if not str is keyType and not int is keyType: # we don't have expected types
            raise Flat_Cache_Exception(f"Flat Cache can output either int or str keys, but not '{keyType}'")
        
        timestamps = []

        for indexKey in range(0,self.size()):
            position = self.data.storage[indexKey]['position']

            if int is keyType or True == all:
                # append indexKey or 
                # add the index key first if True == all
                output.append(indexKey)
            
            if str is keyType or True == all:
                # get the string keys in the correct order
                output.append(self.data.storage[indexKey]['position'])

        return output + timestamps

    # self.data.size is managed through the places where we update locations, via increaseSize() and decreaseSize()
    @Debugger
    def size(self) -> int:
        return self.data.size

    ####
    # 
    # Output Methods
    #
    ####

    @Debugger
    @validate_arguments
    def __str__(self, update_timestamp:bool=True) -> str:
        output = "Flat_Cache: \n"
        for item in self.getKeys():
            if True == Flat_Cache.positionIsTimestamp(item):
                continue

            data = self.getDict(item)
            output += "\t'{}': {}\n".format(item, data['data'])

        if True == update_timestamp:
            output += self.getTimestampsAsStr()

        return output

    def string(self, update_timestamp:bool=True) -> str:
        return self.__str__(update_timestamp=update_timestamp)

    @Debugger
    @validate_arguments
    def getAsList(self, update_timestamp:bool=True) -> list:
        output = []
        for index in self.getKeys(keyType=int):
            if True == Flat_Cache.positionIsTimestamp(index):
                continue
            
            data = self.getDict(index)
            output.insert(index, data['data'])
        
        if True == update_timestamp:
            output += self.getTimestampsAsList()

        return output


    @Debugger
    @validate_arguments
    def getAsDict(self, update_timestamp:bool=True) -> dict:
        output = OrderedDict()
        
        for index in self.getKeys(keyType=int): #it really doesn't matter which type you choose here
            if True == Flat_Cache.positionIsTimestamp(index):
                continue

            data = self.getDict(index)
            output[data['position']] = data['data']
        
        if True == update_timestamp:
            output.update(self.getTimestampsAsDict())
        
        return output

    @Debugger
    @validate_arguments
    def getTimestampsAsStr(self) -> str:
        timestamps = ""
        
        for item in self.getKeys():
            data = self.getDict(item)
            timestamps += f"\t'{Flat_Cache.makeTimestampName(item)}': {data['timestamp']}\n"

        timestamps += f"\t'update_timestamp': {self.data.update_timestamp}\n"
        
        return timestamps

    @Debugger
    @validate_arguments
    def getTimestampsAsList(self) -> list:
        timestamps = []
        
        for index in self.getKeys(keyType=int):
            data = self.getDict(index)
            timestamps.insert(index, data['timestamp'])
        
        timestamps.append(self.data.update_timestamp)

        return timestamps
    
    @Debugger
    @validate_arguments
    def getTimestampKeys(self) -> list:
        timestamps = []
        
        for index in self.getKeys(keyType=str):
            timestamps.append(Flat_Cache.makeTimestampName(index))
        
        timestamps.append(UPDATE_TIMESTAMP_KEY)

        return timestamps
    

    @Debugger
    @validate_arguments
    def getTimestampsAsDict(self) -> dict:
        timestamps = OrderedDict()
        
        for index in self.getKeys(keyType=int): #it really doesn't matter which type you choose here
            data = self.getDict(index)
            timestamps[Flat_Cache.makeTimestampName(data['position'])] = data['timestamp']
        
        timestamps[UPDATE_TIMESTAMP_KEY] = self.data.update_timestamp
        
        return timestamps