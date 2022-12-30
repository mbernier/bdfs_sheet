import pytest

from modules.decorator import Debugger
from modules.dataMove import DataMove
from pydantic import validate_arguments
from modules.dataMoves.exception import DataMove_Exception

class Simple_Simple_DataMove(DataMove):
    sourceClassPath = "simple_sheet.Simple_Worksheet_Source"
    sourceWorksheetName = "test_start_with_columns"

    destinationClassPath = "simple_sheet.Simple_Worksheet_Destination"
    destinationWorksheetNames = ["test_dataMove1"]

    @Debugger
    @validate_arguments
    def mapFields(self, sourceData:dict):
        
        expectedCols = self.destination_expectedCols
        
        # Source cols are one two three and update_timestamps
        # Destination cols ['Name', 'Birthday', 'Email', 'Yearly Salary', 'Hours Worked', 'Hourly Pay', 'Total Pay']
        sourceData['Name']          = sourceData['one']
        sourceData['Birthday']      = sourceData['two']
        sourceData['Email']         = sourceData['three']
        sourceData['Yearly Salary'] = sourceData['one']
        sourceData['Hours Worked']  = sourceData['two']
        sourceData['Hourly Pay']    = sourceData['three']
        sourceData['Total Pay']     = sourceData['one']

        return sourceData


class Test_Bdfs_Worksheet_Destination:
    @classmethod
    def setup_class(self):
        print("\n\tStarting class: {} execution".format(self.__name__))
        
        self.class_setup = True
        # Do the setup of the objects for this test, done outside of the testing file to work around pytest oddities
        


    @classmethod
    def teardown_class(self):
        print("\n\tTeardown class: {} execution".format(self.__name__))


    def setup_method(self, method):
        print(f"\n\tSetting up method {self.__class__.__name__}:: {method.__name__}")
        # This will cause the code to only run for the methods we care about that need this separately
        # as of now, this is test_commit and test_commit_with_larger_data
        self.test_worksheet = destination_helper(self.test_worksheet, self.worksheetName, self.copyFromWorksheetName, self.renameWorksheetName, method)


    def teardown_method(self, method):
        pass