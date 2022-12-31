import pytest, sys

from modules.decorator import Debugger
from modules.dataMove import DataMove
from pydantic import validate_arguments
from modules.dataMoves.exception import DataMove_Exception
from modules.spreadsheets.source import Bdfs_Spreadsheet_Source
from modules.spreadsheets.destination import Bdfs_Spreadsheet_Destination
from modules.worksheets.source import Bdfs_Worksheet_Source
from modules.worksheets.destination import Bdfs_Worksheet_Destination
from modules.spreadsheets.exception import Bdfs_Spreadsheet_Destination_Exception
####
# Things to test here:
# - pushing to a single destination
# - breaking single source data to destination data
# - choosing which data to keep, based on timestamp of source/destination in various combinations
# - committing to two worksheets in rapid succession
####

class Simple_Spreadsheet_Source(Bdfs_Spreadsheet_Source):
    spreadsheetId = '1FEO3BKhyEtr7uF5ZmmodNm7vK3M5i5jrL2_AoOuAwlI' #test_inventory

    worksheetKeeperPattern = "test"

    worksheet_class = "tests.test_modules.test_dataMove.Simple_Worksheet_Source"

class Simple_Worksheet_Source(Bdfs_Worksheet_Source):
    cols_expected = ['Name', 'Birthday', 'Email', 'Yearly Salary', 'Hours Worked', 'Hourly Pay', 'Total Pay']
    cols_expected_extra = {}


class Simple_Spreadsheet_Destination(Bdfs_Spreadsheet_Destination):
    spreadsheetId = '1FEO3BKhyEtr7uF5ZmmodNm7vK3M5i5jrL2_AoOuAwlI' #test_inventory

    worksheetKeeperPattern = "test"

    worksheet_class = "tests.test_modules.test_dataMove.Simple_Worksheet_Destination"

class Simple_Worksheet_Destination(Bdfs_Worksheet_Destination):
    # hourly Pay and total Pay will be added in testing
    cols_expected = ['Name', 'Birthday', 'Email', 'Yearly Salary', 'Hours Worked', 'Hourly Pay', 'Total Pay']

    cols_expected_extra = {}
    
    def setupParams(self):
        self.data.uniqueField = "Email"
        self.data.expectedColumns = self.cols_expected
        self.data.expectedColumns_extra = self.cols_expected_extra


class Simple_Spreadsheet_Source2(Bdfs_Spreadsheet_Source):
    spreadsheetId = '1FEO3BKhyEtr7uF5ZmmodNm7vK3M5i5jrL2_AoOuAwlI'
    worksheetKeeperPattern = "test"
    worksheet_class = "tests.test_modules.test_dataMove.Simple_Worksheet_Source2"

class Simple_Worksheet_Source2(Bdfs_Worksheet_Source):
    cols_expected = ['Name', 'Birthday', 'Email', 'Yearly Salary', 'Hours Worked', 'Hourly Pay', 'Total Pay']
    cols_expected_extra = {}



class Simple_DataMove(DataMove):
    sourceBasePath = "tests.test_modules."
    sourceClassPath = "test_dataMove.Simple_Spreadsheet_Source"
    sourceWorksheetName = "test_start_with_columns"

    destinationBasePath = "tests.test_modules."
    destinationClassPath = "test_dataMove.Simple_Spreadsheet_Destination"
    destinationWorksheetNames = ["test_dataMove1"]

    destinationWorksheetCreateIfNotFound = True

    # we want the destinations for this test to be clean
    @Debugger
    @validate_arguments
    def pre_destination_open_create_worksheet(self, data:str):
        print("doing the pre_destination_setup hook")
        worksheetName = data
        self.destinationSpreadsheet.clearWorksheet(worksheetName)

    # does the field mapping for the destination worksheet called "test_dataMove1"
    # the timestamps are already in the sourceData so you don't need to do anything with them
    # the code that runs in dataMove will look for the most up-to-date timestamp and pick that data point
    @Debugger
    @validate_arguments
    def mapFields_test_dataMove1(self, sourceData:dict):
        if sourceData['Name'] == "MattB":
            self.noteProblem(self.sourceWorksheetName, "Name", "MattB is an asshole, skipping him")
            return

        # Source cols are one two three and update_timestamps
        # Destination cols ['Name', 'Birthday', 'Email', 'Yearly Salary', 'Hours Worked', 'Hourly Pay', 'Total Pay']
        # Name, Birthday, Email are already in the sourceData

        sourceData['Yearly Salary'] = 2008 * 20
        sourceData['Hours Worked']  = 100
        sourceData['Hourly Pay']    = 20.00
        sourceData['Total Pay']     = 100 * 20.00

        return sourceData


class Test_Bdfs_Worksheet_Destination:
    @classmethod
    def setup_class(self):
        print("\n\tStarting class: {} execution".format(self.__name__))
        self.migrator = Simple_DataMove()
        self.class_setup = True
        # Do the setup of the objects for this test, done outside of the testing file to work around pytest oddities

    @classmethod
    def teardown_class(self):
        print("\n\tTeardown class: {} execution".format(self.__name__))


    def setup_method(self, method):
        print(f"\n\tSetting up method {self.__class__.__name__}:: {method.__name__}")


    def teardown_method(self, method):
        pass

    def test_run(self):
        self.migrator.run()
        spreadsheet = Simple_Spreadsheet_Source2()
        worksheet = spreadsheet.getWorksheet(worksheetTitle="test_dataMove1")
        
        # get the data we will start with
        row0 = worksheet.getRow(0, update_timestamp=True)
        assert row0['Name'] == "Matt"
        assert row0['Birthday'] == "1/1/2001"
        assert row0['Email'] == "email@example.com"
        assert row0['Yearly Salary'] == "40160"
        assert row0['Hours Worked'] == "100"
        assert row0['Hourly Pay'] == "20"
        assert row0['Total Pay'] == "2000"
        assert row0['Name_update_timestamp'] == 12345.0
        assert row0['Birthday_update_timestamp'] == 12345.0
        assert row0['Email_update_timestamp'] == 12345.0
        # these were all set at the same time, so the timestamp is the same for these
        timestamp = row0['Yearly Salary_update_timestamp']
        assert row0['Hours Worked_update_timestamp'] == timestamp
        assert row0['Hourly Pay_update_timestamp'] == timestamp
        assert row0['Total Pay_update_timestamp'] == timestamp
        assert row0['update_timestamp'] == timestamp

        row1 = worksheet.getRow(1, update_timestamp=True)
        timestamp = row1['Yearly Salary_update_timestamp']
        assert row1['Hours Worked_update_timestamp'] == timestamp
        assert row1['Hourly Pay_update_timestamp'] == timestamp
        assert row1['Total Pay_update_timestamp'] == timestamp
        assert row1['update_timestamp'] == timestamp
        assert row1['Name_update_timestamp'] == timestamp
        assert row1['Birthday_update_timestamp'] == timestamp
        assert row1['Email_update_timestamp'] == timestamp

        row2 = worksheet.getRow(2,update_timestamp=True)
        assert row0['Name_update_timestamp'] == 54321.0
        assert row0['Birthday_update_timestamp'] == 54321.0
        assert row0['Email_update_timestamp'] == 54321.0
        # these were all set at the same time, so the timestamp is the same for these
        timestamp = row0['Yearly Salary_update_timestamp']
        assert row0['Hours Worked_update_timestamp'] == timestamp
        assert row0['Hourly Pay_update_timestamp'] == timestamp
        assert row0['Total Pay_update_timestamp'] == timestamp
        assert row0['update_timestamp'] == timestamp