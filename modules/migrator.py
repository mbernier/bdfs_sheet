import sys
from collections import OrderedDict
from dataclasses import dataclass, Field as dc_field
from enum import Enum
from gspread.worksheet import Worksheet
from pydantic import validate_arguments, Field
from pydantic.typing import Annotated, Type, Optional, Union
from modules.caches.flat import UPDATE_TIMESTAMP_KEY, UPDATE_TIMESTAMP_POSTFIX, Flat_Cache
from modules.caches.exception import Nested_Cache_Exception
from modules.config import config
from modules.dataMove import DataMove
from modules.dataMoves.exception import DataMove_Exception
from modules.decorator import Debugger
from modules.exception import Bdfs_Exception
from modules.helper import Helper
from modules.helpers.exception import Helper_Exception
from modules.logger import Logger, logger_name
from modules.spreadsheets.destination import Bdfs_Spreadsheet_Destination
from modules.spreadsheets.source import Bdfs_Spreadsheet_Source
from modules.spreadsheets.exception import Bdfs_Spreadsheet_Exception
from modules.worksheet import Bdfs_Worksheet, Worksheet_DataClass
from modules.worksheets.source import Bdfs_Worksheet_Source
from modules.worksheets.destination import Bdfs_Worksheet_Destination

#  Each class should
#   take in the config params
#   set the fields
#   call the setup methods from the super()
#   then act like the super()

class ObjTypeEnum(str, Enum):
    worksheet = "Worksheet"
    spreadsheet = "Spreadsheet"

class DirectionEnum(str, Enum):
    source = 'Source'
    destination = 'Destination'

class Migrator_Exception(Bdfs_Exception):
    def __init__(self, message="Migrator Exception raised"):
        self.message = message
        super().__init__(self.message)

class Migrator_Field_Exception(Bdfs_Exception):
    def __init__(self, type:ObjTypeEnum, field:str, direction:DirectionEnum):
        self.message = f"{type}.{field} is a required param for Migrator_Spreadsheet_{direction}"
        super().__init__(self.message)


class Migrator_Spreadsheet_Source(Bdfs_Spreadsheet_Source):
    """Takes in config and sets up the class parameters needed for Bdfs_Spreadsheet_Source
        Gets a Dict like this: 
        # source = {
            "spreadsheet": {
                "id": '16gp8awjSaawEdBvV6bLDUQoA5Ha-j1NB82O2Zifhmns'
                "worksheetKeeperPattern": "inventory"
            },
            "worksheet": {
                "name": "sarto_barn_single_inventory",
                "expectedCols": Sarto_Base.cols_expected,
                "expectedCols_extra": Sarto_Base.cols_expected_extra,
                "uniqueField": "URL_key",
                "data_class": Sarto_Worksheet_DataClass()# uses the default if this is not set
            }
        }
    """

    @Debugger
    @validate_arguments
    def __init__(self, source_dict:dict):
        self.source_dict = source_dict
        Migrator.setupMigratorSpreadsheet(source_dict["spreadsheet"], source_dict["worksheet"]) #sets the params that we pass from the dicts
        super().__init__(self)


    @Debugger
    @validate_arguments
    def createWorksheet(self, worksheetTitle):
        """This is its own method so it can be overridden by Migrator
            Finds the worksheet class name and then instantiates a worksheet obj"""
        worksheet = Migrator_Worksheet_Source(source_dict=self.source_dict, worksheet=self.data.gspread_worksheets[worksheetTitle])
        self.data.worksheets[worksheetTitle] = worksheet


class Migrator_Spreadsheet_Destination(Bdfs_Spreadsheet_Destination):
    """Takes in config and sets up the class parameters needed for Bdfs_Spreadsheet_Destination
        Gets a dict like this:
        destination = {
            "spreadsheet": {
                "id": '16gp8awjSaawEdBvV6bLDUQoA5Ha-j1NB82O2Zifhmns',
                "worksheetKeeperPattern": "inventory"
            },
            "worksheet": {
                "names": [
                    "barndoor_single",
                    "slabs_single"],
                "expectedCols": Sarto_Base.cols_expected,
                "extra_expectedCols": Sarto_Base.cols_expected_extra,
                "uniqueField": "URL_key",
                "data_class": Sarto_Worksheet_DataClass(),
                "map_fields": MapFields()
            }
        }
    """

    @Debugger
    @validate_arguments
    def __init__(self, dest_dict:dict):
        self.dest_dict = dest_dict
        Migrator.setupMigratorSpreadsheet(dest_dict["spreadsheet"], dest_dict["worksheet"]) #sets the params that we pass from the dicts
        super().__init__(self)


    @Debugger
    @validate_arguments
    def createWorksheet(self, worksheetTitle):
        """This is its own method so it can be overridden by Migrator
            Finds the worksheet class name and then instantiates a worksheet obj"""
        worksheet = Migrator_Worksheet_Destination(dest_dict=self.dest_dict, worksheet=self.data.gspread_worksheets[worksheetTitle])
        worksheet.setupParams(self.dest_dict)
        self.data.worksheets[worksheetTitle] = worksheet


@dataclass
class Migrator_Worksheet_Dataclass(Worksheet_DataClass):
    discount:int = dc_field(default_factory=int)    # discount data
    title:str = dc_field(default_factory=str)      # The Sheet title


class Migrator_Worksheet_Source(Bdfs_Worksheet_Source):
    
    def __init__(self, worksheet:Worksheet, source_dict:dict):
        """Delays the Bdfs_Worksheet_Source __init__ behind setting the params passed from config"""
        self.data.expectedColumns = source_dict['worksheet']['expectedCols']
        self.data.expectedColumns_extra = source_dict['worksheet']['expectedCols_extra']
        self.data.uniqueField = source_dict['worksheet']['uniqueField']

        if "data_class" in source_dict['worksheet'].keys():
            self.setDataClass(source_dict['worksheet']['data_class'])

        self.initialSetup()
    

class Migrator_Worksheet_Destination(Bdfs_Worksheet_Destination):
    def __init__(self, dest_dict:dict, worksheet:Worksheet):
        """Delays the Bdfs_Worksheet_Destination __init__ behind setting the params passed from config"""
        self.data.expectedColumns = dest_dict['worksheet']['expectedCols']
        self.data.expectedColumns_extra = dest_dict['worksheet']['expectedCols_extra']
        self.data.uniqueField = dest_dict['worksheet']['uniqueField']

        if "data_class" in dest_dict['worksheet'].keys():
            self.setDataClass(dest_dict['worksheet']['data_class'])

        self.initialSetup()

# @todo create a base dataclass for all source worksheets
# @todo by default the MapFields method that is used is the same as the worksheet name

class MapFields():
    def __init__(self):
        pass


class Migrator(DataMove):
    """Wraps the tested Data Move functionality.
        Provides accessors to override the default DataMove data and methods,
        allowing classes to be passed in rather than called dynamically.
        This makes it possible to create a config based dataMove instead of
        creating all new Spreadsheet, Worksheet, and dataclasses for each migration
    """
    
    @Debugger
    def __init__(self, source:dict, destination:dict, fieldMapper:Type[MapFields]) -> None:

        # check the configs before we do anything else
        self.checkMigratorConfig(source, "Source")
        self.checkMigratorConfig_Destination(destination)

        # pass in the class that will do fieldMapping
        self.fieldMapper = fieldMapper

        # setup the expected parameters
        self.sourceWorksheetName = source['worksheet']['name']
        self.destinationWorksheetNames = destination['worksheet']['names']

        # setup the spreadsheets 
        self.sourceSpreadsheet = Migrator_Spreadsheet_Source(source)
        self.destinationSpreadsheet = Migrator_Spreadsheet_Destination(destination)

        super().__init__(self)


    @staticmethod
    @Debugger
    @validate_arguments
    def setupMigratorSpreadsheet(klass:Type[Bdfs_Worksheet], spreadsheet:dict, worksheet:dict):
        klass.spreadsheetId = spreadsheet["id"]

        if "worksheetKeeperPattern" in spreadsheet.keys():
            klass.worksheetKeeperPattern = spreadsheet['worksheetKeeperPattern']

        klass.cols_expected = worksheet["cols_expected"]

        if "expectedCols_extra" in worksheet.keys():
            klass.cols_expected_extra = worksheet["expectedCols_extra"]


    @Debugger
    @validate_arguments
    def checkMigratorConfig(self, spreadsheet:dict, worksheet:dict, direction:DirectionEnum):
        """Reviews the data within the objects passed and makes sure the right params are set before the objects are called"""

        if not "id" in spreadsheet:
            raise Migrator_Field_Exception("spreadsheet", "id", "Source")
            
        if not "name" in worksheet:
            raise Migrator_Field_Exception("worksheet", "name", "Source")
        
        if not "expectedCols" in worksheet:
            raise Migrator_Field_Exception("worksheet", "expecteCols", "Source")
        
        if not "uniqueField" in worksheet:
            raise Migrator_Field_Exception("worksheet", "uniqueField", "Source")


    @Debugger
    @validate_arguments
    def checkMigratorConfig_Destination(self, spreadsheet:dict, worksheet:dict):
        # check the spreadsheet basics
        self.checkMigratorConfig(spreadsheet, worksheet, "Destination")

        # check the destnation keys that are required
        worksheetKeys = worksheet.keys()
        if not "names" in worksheetKeys:
            raise Migrator_Field_Exception("worksheet", "names", "Destination")
        
        if not list == type(worksheet['names']):
            raise Migrator_Exception(f"destination.worksheet.names should be type list, {type(worksheet['names'])} found")

        if not "map_fields" in worksheetKeys:
            raise Migrator_Field_Exception("worksheet", "map_fields", "Destination")


    @Debugger
    @validate_arguments
    def callFieldMapperMethod(self, methodName:str, sourceData:dict, klass=None):
        """Overrides DataMove.callFieldMapperMethod():
            Ignores klass param, replaces it with the fieldMapper class we setup in __init__"""
        Helper.callMethod(klass=self.fieldMapper, methodName=methodName, sourceData=sourceData)