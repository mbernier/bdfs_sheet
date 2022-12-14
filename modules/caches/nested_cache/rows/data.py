import sys
from collections import OrderedDict
from modules.caches.flat import Flat_Cache
from modules.caches.nested_cache.row import Nested_Cache_Row
from modules.caches.exception import Nested_Cache_Rows_Data_Exception, Flat_Cache_Exception
from modules.config import config
from modules.decorator import Debugger
from typing import Union
from pprint import pprint
from pydantic import validator, validate_arguments

# This is a wrapper for Nested_Cache on top of Flat Cache
#   in order to reduce the complexity in the Nested_Cache implementation
#   and to wrap Flat_Cache with the logic needed for Nested_Cache in a clean way.
#   A nested Cache Row can be created with values or not and can be written 
#   to the Flat Cache either way.
# This assumes that it is created with the headers/indexes passed in - see NestedCache createRowFromData() method
class Nested_Cache_Rows_Data(Nested_Cache_Row):

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
        dict1 = super()._get_at_location(position)

        locationPosition = position if type(position) is str else dict1["position"]
        indexPosition = dict1["position"] if position == locationPosition else position

        return locationPosition, indexPosition

    ####
    #
    # Add Data Methods
    #
    ####

    @Debugger
    @validate_arguments
    def add_at(self, location:str, index:int, data=None):

        locationData, indexData = self.createDataDicts(location=location, index=index, data=data)
        try:
            self._add_at_location(location=location, data=locationData)
            self._add_at_location(location=index, data=indexData)
        except Flat_Cache_Exception as err:
            raise Nested_Cache_Rows_Data_Exception(str(err))
        

    def add_at_location(*args, **kwargs):
        raise Nested_Cache_Rows_Data_Exception("add_at_location DNE for Nested_Cache_Rows_Data, use add_at()")


    ####
    #
    # Set Data At Methods
    #
    ####

    @Debugger
    @validate_arguments
    def set_at(self, location:str, index:int, data=None):


        currentLocationData, currentIndexData = self.getBothDicts(location)

        if currentLocationData == None:
            self.add_at(location=location, index=index, data=data)
        else: 
            locationData, indexData = self.createDataDicts(location=location, index=index, data=data)
            # print(f"locationData: {locationData}")
            # print(f"indexData: {indexData}")
            atLoc = super()._get_at_location(location)
            # print(f"atLoc: {atLoc}")
            atLoc = super()._get_at_location(index)
            # print(f"atLoc: {atLoc}")
            
            try:
                if (self.get_at(location) == None and self.get_at(index) == None):
                    # make sure that both location/index dicts have data = None
                    self.unset_at(location) #unset both location and index in one go
                    self.update_at(location, data)
            except Flat_Cache_Exception as err:
                raise Nested_Cache_Rows_Data_Exception(str(err))
        

    def set_at_location(*args, **kwargs):
        raise Nested_Cache_Rows_Data_Exception("set_at_location DNE for Nested_Cache_Rows_Data, use set_at()")


    ####
    #
    # Get Data Methods
    #
    ####

    @Debugger
    @validate_arguments
    def get_at(self, position:Union[int,str]):
        dictData = super()._get_at_location(position)
        if None == dictData:
            return None
        return dictData["data"]

    def get_at_location(*args, **kwargs):
        raise Nested_Cache_Rows_Data_Exception("get_at_location DNE for Nested_Cache_Rows_Data, use get_at()")

    ####
    #
    # Update Data Methods
    #
    ####

    @Debugger
    @validate_arguments
    def update_at(self, position:Union[int,str], data=None):

        locationDict, indexDict = self.getBothDicts(position)
        locationDict['data'] = data
        indexDict['data'] = data

        # can get the proper otherLocation from the other dict's position attr
        # this is an update at action, because we don't want to lose the index:location mapping
        self._update_at_location(indexDict["position"], locationDict)
        self._update_at_location(locationDict["position"], indexDict)

    def unset_at_location(*args, **kwargs):
        raise Nested_Cache_Rows_Data_Exception("unset_at_location DNE for Nested_Cache_Rows_Data, use unset_at()")

    ####
    #
    # Unset Data Methods
    #
    ####

    @Debugger
    @validate_arguments
    def unset_at(self, position:Union[int,str]):
        locationDict, indexDict = self.getBothDicts(position)
        locationDict['data'] = None
        indexDict['data'] = None
        # can get the proper otherLocation from the other dict's position attr
        # this is an update at action, because we don't want to lose the index:location mapping
        self._update_at_location(indexDict["position"], locationDict)
        self._update_at_location(locationDict["position"], indexDict)

    def unset_at_location(*args, **kwargs):
        raise Nested_Cache_Rows_Data_Exception("unset_at_location DNE for Nested_Cache_Rows_Data, use unset_at()")

    ####
    #
    # Remove Position Methods
    #
    ####

    @Debugger
    @validate_arguments
    def remove_position(self, position:Union[int, str]):
        raise Exception("Need to adjust the indexes after the one removed")
        self._remove_location(location)
        self._remove_location(index)

    def remove_location(self, *args, **kwargs):
        raise Nested_Cache_Rows_Data_Exception("remove_location DNE for Nested_Cache_Rows_Data, use remove_position()")

    ####
    #
    # Clear Methods
    #
    ####

    @Debugger
    @validate_arguments
    def clear_all(self):
        for position in self._storage.getKeys():
            if type(position) is str: # pick one, doesn't matter, just reducing work by 1/2
                locationdict, indexdict = self.getBothDicts(position)
                locationdict['data'] = None
                indexdict['data'] = None
                self._update_at_location(position, locationdict)
                # get the correct index
                self._update_at_location(locationdict['position'], indexdict)

    ####
    #
    # Output data Methods
    #
    ####

    @Debugger
    def __str__(self) -> str:
        output = "Nested_Cache_Rows_Data: \n"
        storageKeys = self._storage.getKeys()
        for storageIndex in storageKeys:
            if type(storageIndex) is str:
                output += "\t{}: {}\n".format(storageIndex, self.get_at(storageIndex))
        return output

    @Debugger
    def getAsStringRaw(self) -> str:
        output = self.getAsDictRaw()
        return f"Nested_Cache_Rows_Data:\n {output}"


    @Debugger
    @validate_arguments
    def getAsList(self, position:Union[str,int]=None):
        output = []

        storageKeys = self._storage.getKeys()
        for storageIndex in storageKeys:
            if type(storageIndex) is int or (None != position and storageIndex == position):
                output.insert(storageIndex, self.get_at(storageIndex))
        return output

    @Debugger
    def getAsListRaw(self):
        raise Nested_Cache_Rows_Data_Exception("Raw list doesn't make sense for Nested_Cache_Rows_Data, bc we have the same data in a string and an int position in storage, use getAsDictRaw")


    @Debugger
    @validate_arguments
    def getAsDict(self, position:Union[str,int]=None):
        output = OrderedDict()
        storageKeys = self._storage.getKeys()
        for storageIndex in storageKeys:
            if type(storageIndex) is str or (None != position and storageIndex == position):
                output[storageIndex] = self.get_at(storageIndex)
        return output


    @Debugger
    def getAsDictRaw(self):
        output = OrderedDict()
        storageKeys = self._storage.getKeys()
        for storageIndex in storageKeys:
            output[storageIndex] = self.get_at(storageIndex)
        return output
