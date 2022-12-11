import sys
from collections import OrderedDict
from pprint import pprint
from pydantic import validator, validate_arguments
from modules.caches.flat import Flat_Cache
from modules.caches.nested_cache.row import Nested_Cache_Row
from modules.caches.exception import Nested_Cache_Row_Exception, Flat_Cache_Exception
from modules.config import config
from modules.decorator import Debugger


# This is a wrapper for Nested_Cache on top of Flat Cache
#   in order to reduce the complexity in the Nested_Cache implementation
#   and to wrap Flat_Cache with the logic needed for Nested_Cache in a clean way.
#   A nested Cache Row can be created with values or not and can be written 
#   to the Flat Cache either way.
class Nested_Cache_Rows_Data(Flat_Cache):

    ####
    #
    # Helper methods, bc data is stored in two places in Nested_Cache_Rows_Data
    #
    ####
    @Debugger
    @validate_arguments
    def createDataDicts(self, location, index, data):
        locationData = {
            "position": index,
            "data": data
        }

        indexData = {
            "position": location,
            "data": data
        }

        return locationData, indexData

    def getBothDicts(self, position:Union[int, str]):
        dict1 = super().get_at_location(position)
        dict2 = super().get_at_location(dict1["position"])

        locationDict = dict1 if type(dict1["position"]) is int else dict2
        indexDict = dict2 if dict1 == locationDict else dict1

        return locationDict, indexDict

    def getOtherPosition(self, position:Union[int, str]):
        dict1 = super().get_at_location(position)

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

        locationData, indexData = self.createDataDicts()

        self.write(location=location, data=locationData)
        self.write(location=index, data=indexData)

    def add_at_location(self):
        raise Nested_Cache_Rows_Data_Exception("add_at_location DNE for Nested_Cache_Rows_Data, use add_at()")


    ####
    #
    # Set Data At Methods
    #
    ####

    @Debugger
    @validate_arguments
    def set_at(self, location:str, index:int, data=None):

        locationData, indexData = self.createDataDicts()

        super().set_at_location(location, locationData)
        super().set_at_location(index, indexData)

    def set_at_location(self):
        raise Nested_Cache_Rows_Data_Exception("set_at_location DNE for Nested_Cache_Rows_Data, use set_at()")

    ####
    #
    # Get Data Methods
    #
    ####

    @Debugger
    @validate_arguments
    def get_at(self, position:Union[int,str]):
        dictData = super().get_at_location(position)
        return dictData["data"]


    def get_at_location(self):
        raise Nested_Cache_Rows_Data_Exception("get_at_location DNE for Nested_Cache_Rows_Data, use get_at()")


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
        super().update_at_location(indexDict["position"], locationDict)
        super().update_at_location(locationDict["position"], indexDict)


    ####
    #
    # Remove Position Methods
    #
    ####

    @Debugger
    @validate_arguments
    def remove_position(self, position:Union[int, str]):
        raise Exception("Need to adjust the indexes after the one removed")
        super().remove_location(location)
        super().remove_location(index)

    def remove_location(self):
        raise Nested_Cache_Rows_Data_Exception("remove_location is not available, use remove_position")

    ####
    #
    # Clear Methods
    #
    ####

    @Debugger
    @validate_arguments
    def clear_all(self):
        for position in self._storage:
            dataObj = super().get_at_location(position)
            dataObj['data'] = None
            super.update_at_location(position, data)

    ####
    #
    # Output data Methods
    #
    ####

    @Debugger
    def __str__(self) -> str:
        output = "Nested_Cache_Rows_Data: \n"
        storageKeys = self._storage.keys()
        for storageIndex in storageKeys:
            if type(storageIndex) is str:
                output += "\t{}: {}\n".format(storageIndex, self.get_at(storageIndex))
        return output

    @Debugger
    def getAsStringRaw(self) -> str:
        output = self.getAsDictRaw()
        return f"Nested_Cache_Rows_Data:\n {output}"


    @Debugger
    def getAsList(self):
        output = []

        storageKeys = self._storage.keys()
        for storageIndex in storageKeys:
            if type(storageIndex) is int:
                output.insert(storageIndex, self.get_at(storageIndex))
        return output

    @Debugger
    def getAsListRaw(self):
        raise Nested_Cache_Rows_Data_Exception("Raw list doesn't make sense, bc we have the same data in a string and an int position in storage, use getAsDictRaw")


    @Debugger
    def getAsDict(self):
        output = OrderedDict()
        storageKeys = self._storage.keys()
        for storageIndex in storageKeys:
            if type(storageIndex) is str:
                output[storageIndex] = self.get_at(storageIndex)
        return output

    @Debugger
    def getAsDictRaw(self):
        # get everything that we have in the Flat_Cache and return it
        output = super().getAsDict()
        return output
