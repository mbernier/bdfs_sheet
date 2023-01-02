import pytest, sys, time
from modules.caches.flat import Flat_Cache, UPDATE_TIMESTAMP_KEY
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

class Simple_DataMove(DataMove):
    sourceBasePath = "tests.test_modules."
    sourceClassPath = "test_dataMove.Simple_Spreadsheet_Source"
    sourceWorksheetName = "test_start_with_columns"

    destinationBasePath = "tests.test_modules."
    destinationClassPath = "test_dataMove.Simple_Spreadsheet_Destination"
    destinationWorksheetNames = ["test_dataMove1", "test_dataMove2"]

    destinationWorksheetCreateIfNotFound = True

    # we want the destinations for this test to be clean
    @Debugger
    @validate_arguments
    def pre_destination_open_create_worksheet(self, data:str):
        worksheets = self.destinationSpreadsheet.getWorksheets()
        worksheetName = data
        if worksheetName in worksheets.keys():
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
    
    @Debugger
    @validate_arguments
    def mapFields_test_dataMove2(self, sourceData:dict):
        sourceData['Yearly Salary'] = 2008 * 10
        sourceData['Hours Worked']  = 10
        sourceData['Hourly Pay']    = 2.00
        sourceData['Total Pay']     = 10 * 20.00

        return sourceData
    
    @Debugger
    def just_a_hook(self):
        return "a test hook ran"
    
    @Debugger
    @validate_arguments
    def just_a_hook_with_data(self, data:str):
        return f"another test hook ran {data}"

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

    def test_hook(self):
        assert "a test hook ran" == self.migrator.run_hook('just_a_hook')

    def test_hook_with_params(self):
        assert "another test hook ran 1234" == self.migrator.run_hook("just_a_hook_with_data", data="1234")

    def test_openOrCreateDestinationWorksheet(self):
        pass

    def test_getSourceClass(self):
        pass

    def test_getDestinationClass(self):
        pass

    def test_getSpreadsheetClass(self):
        pass

    def test_setupDestinations(self):
        pass

    def test_cleanPriceKey(self):
        result = self.migrator.cleanPriceKey('Cost: 18" x 80"')
        assert result == 'Price:18" x 80"'

    def test_calculatePrice(self):
        worksheet = 'test_dataMove1'
        testSource = {'Cost: 18" x 80"': 10000, 'Price:18" x 80"': 100, 'Discount': 0.25}
        # Note - this will NOT use the value in sourceData['Discount'] it will use
        # what is set on the destination class
        price = self.migrator.calculatePrice('Cost: 18" x 80"', worksheet, testSource)
        assert price == 100.00

    def test_calculatePrice_with_symbols(self):
        worksheet = 'test_dataMove1'
        testSource = {'Cost: 18" x 80"': 10000, 'Price:18" x 80"': '$1,000.00', 'Discount': 0.25}
        # Note - this will NOT use the value in sourceData['Discount'] it will use
        # what is set on the destination class
        price = self.migrator.calculatePrice('Cost: 18" x 80"', worksheet, testSource)
        assert price == 1000.00

    def test_calculatePrice_with_blank_price(self):
        worksheet = 'test_dataMove1'
        testSource = {'Cost: 18" x 80"': 10000, 'Price:18" x 80"': '', 'Discount': 0.25}
        # Note - this will NOT use the value in sourceData['Discount'] it will use
        # what is set on the destination class
        price = self.migrator.calculatePrice('Cost: 18" x 80"', worksheet, testSource)
        assert price == ''

    def test_getDestinationRow(self):
        worksheet = "test_dataMove1"
        self.migrator.newData[worksheet]['Email'] = "test@example.com"

        uniqueField = self.migrator.destinationWorksheets[worksheet].getUniqueField()

        assert 'Email' == uniqueField

        row = self.migrator.getUniqueDestinationRow(worksheet)
        assert {} == row

        data = {'Name': 'Test User_Destination', 
                'Email': 'test@example.com', 
                'Birthday':'1/1/1999',
                'Yearly Salary': 100, 
                'Hours Worked': 100, 
                'Hourly Pay': 100, 
                'Total Pay': 100}
        self.migrator.destinationWorksheets[worksheet].putRow(data)
        row = self.migrator.getUniqueDestinationRow(worksheet)
        assert 'Name' in row.keys()
        assert 'Email' in row.keys()
        assert 'Birthday' in row.keys()
        assert 'Yearly Salary' in row.keys()
        assert 'Hours Worked' in row.keys()
        assert 'Hourly Pay' in row.keys()
        assert 'Total Pay' in row.keys()
        assert Flat_Cache.makeTimestampName('Name') in row.keys()
        assert Flat_Cache.makeTimestampName('Email') in row.keys()
        assert Flat_Cache.makeTimestampName('Birthday') in row.keys()
        assert Flat_Cache.makeTimestampName('Yearly Salary') in row.keys()
        assert Flat_Cache.makeTimestampName('Hours Worked') in row.keys()
        assert Flat_Cache.makeTimestampName('Hourly Pay') in row.keys()
        assert Flat_Cache.makeTimestampName('Total Pay') in row.keys()
        assert data['Name']             == row['Name']
        assert data['Email']            == row['Email']
        assert data['Birthday']         == row['Birthday']
        assert data['Yearly Salary']    == row['Yearly Salary']
        assert data['Hours Worked']     == row['Hours Worked']
        assert data['Hourly Pay']       == row['Hourly Pay']
        assert data['Total Pay']        == row['Total Pay']

        # temp unset to test for when we don't have a uniqueField (we should always, but just in case)
        self.migrator.destinationWorksheets[worksheet].data.uniqueField = None
        row = self.migrator.getUniqueDestinationRow(worksheet)
        assert {} == row
        
        # set it back, for subsequent tests
        self.migrator.destinationWorksheets[worksheet].data.uniqueField = uniqueField


    def test_chooseSourceOrDestinationData_useSource(self):
        worksheet = "test_dataMove1"
        self.migrator.newData[worksheet]['Email'] = "test@example.com"
        self.migrator.newData[worksheet]['Name'] = "Test User_Source"
        data = self.migrator.chooseSourceOrDestinationData_useSource(worksheet, "Email", Flat_Cache.makeTimestampName("Email"))
        assert data == {'Email': 'test@example.com'}


    def test_chooseSourceOrDestinationData_useDestination(self): 
        worksheet = "test_dataMove1"
        self.migrator.newData[worksheet]['Email'] = "test@example.com"
        destinationData = self.migrator.getUniqueDestinationRow(worksheet)
        data = self.migrator.chooseSourceOrDestinationData_useDestination("Email", Flat_Cache.makeTimestampName("Email"), destinationData)
        assert 'Email' in data.keys()
        assert data['Email'] == 'test@example.com'
        assert Flat_Cache.makeTimestampName('Email') in data.keys()
        assert data[Flat_Cache.makeTimestampName('Email')] > 0

        with pytest.raises(DataMove_Exception) as excinfo:
            self.migrator.newData[worksheet]['Email'] = "test123@example.com"
            destinationData = self.migrator.getUniqueDestinationRow(worksheet)
            data = self.migrator.chooseSourceOrDestinationData_useDestination("Email", Flat_Cache.makeTimestampName("Email"), destinationData)    
        assert "'Email' not in destination data" in excinfo.value.message


    # def test_chooseSourceOrDestinationData_getSourceTimestamp(self):
    #     worksheet = "test_dataMove1"
    #     self.migrator.newData[worksheet]['Email'] = "test@example.com"
    #     sourceTimestamp = self.migrator.chooseSourceOrDestinationData_getSourceTimestamp(worksheet, Flat_Cache.makeTimestampName('Email'))
    #     assert sourceTimestamp == 0.0

    #     self.migrator.newData[worksheet][Flat_Cache.makeTimestampName('Email')] = time.time()
    #     newSourceTimestamp = self.migrator.chooseSourceOrDestinationData_getSourceTimestamp(worksheet, Flat_Cache.makeTimestampName('Email'))
    #     assert newSourceTimestamp > 0
    #     assert newSourceTimestamp > sourceTimestamp


    # def test_chooseSourceOrDestinationData_getDestinationTimestamp(self):
    #     worksheet = "test_dataMove1"
    #     self.migrator.newData[worksheet]['Email'] = "test@example.com"
    #     destinationData = self.migrator.getDestinationRow(worksheet)
    #     sourceTimestamp = self.migrator.chooseSourceOrDestinationData_getDestinationTimestamp(Flat_Cache.makeTimestampName('Email'), destinationData)
    #     assert sourceTimestamp > 0.0 # this is here from previous test


    # def test_chooseSourceOrDestinationData(self):
    #     worksheet = "test_dataMove1"
    #     output = self.migrator.chooseSourceOrDestinationData('Name', worksheet)
    #     # due to the tests here, the Test User_Destination is newer
    #     assert output == {'Name': 'Test User_Destination'}
    #     self.migrator.newData[worksheet][Flat_Cache.makeTimestampName('Name')] = time.time()
    #     output = self.migrator.chooseSourceOrDestinationData('Name', worksheet)
    #     # we just got at timestamp for the source, so we know it's newer now
    #     assert output == {'Name': 'Test User_Source'}


    # def test_handleWorksheetMethods(self):
    #     pass


    # def test_fieldMapper(self):
    #     sourceData = self.migrator.sourceWorksheet.getRow(0, update_timestamp=True)        
    #     # merge the source and Destination data, based on whatever rules you need
    #     self.migrator.fieldMapper(sourceData)

    #     newDataKeys = self.migrator.newData.keys()
    #     for worksheet in self.migrator.destinationWorksheetNames:
    #         assert worksheet in newDataKeys
    #         newData = self.migrator.newData[worksheet]
    #         assert 'Name' in newData
    #         assert 'Email' in newData
    #         assert 'Birthday' in newData
    #         assert 'Yearly Salary' in newData
    #         assert 'Hours Worked' in newData
    #         assert 'Hourly Pay' in newData
    #         assert 'Total Pay' in newData
    #         assert Flat_Cache.makeTimestampName('Name') in newData
    #         assert Flat_Cache.makeTimestampName('Email') in newData
    #         assert Flat_Cache.makeTimestampName('Birthday') in newData
    #         # These are created in the next step of dataMove, so they are not there yet
    #         assert not Flat_Cache.makeTimestampName('Yearly Salary') in newData
    #         assert not Flat_Cache.makeTimestampName('Hours Worked') in newData
    #         assert not Flat_Cache.makeTimestampName('Hourly Pay') in newData
    #         assert not Flat_Cache.makeTimestampName('Total Pay') in newData

    # def test_verifyRowData(self):
    #     worksheet = "test_dataMove1"
    #     modifiedData = self.migrator.verifyRowData(worksheet)
    #     assert 'Name' in modifiedData
    #     assert 'Email' in modifiedData
    #     assert 'Birthday' in modifiedData
    #     assert 'Yearly Salary' in modifiedData
    #     assert 'Hours Worked' in modifiedData
    #     assert 'Hourly Pay' in modifiedData
    #     assert 'Total Pay' in modifiedData
    #     # These are created in the next step of dataMove, so they are not there yet
    #     assert not Flat_Cache.makeTimestampName('Name') in modifiedData
    #     assert not Flat_Cache.makeTimestampName('Email') in modifiedData
    #     assert not Flat_Cache.makeTimestampName('Birthday') in modifiedData
    #     assert not Flat_Cache.makeTimestampName('Yearly Salary') in modifiedData
    #     assert not Flat_Cache.makeTimestampName('Hours Worked') in modifiedData
    #     assert not Flat_Cache.makeTimestampName('Hourly Pay') in modifiedData
    #     assert not Flat_Cache.makeTimestampName('Total Pay') in modifiedData

    # def test_storeTheData(self):
    #     worksheet = "test_dataMove1"
    #     data = {'Name': 'Test User_storeTheData', 
    #             'Email': 'testStoreTheData@example.com', 
    #             'Birthday':'1/1/1999',
    #             'Yearly Salary': 100000, 
    #             'Hours Worked': 2010, 
    #             'Hourly Pay': 50, 
    #             'Total Pay': 105000}
    #     self.migrator.storeTheData(worksheet, data)
    #     # the data is stored in the local copy, not committed yet
    #     row = self.migrator.destinationWorksheets[worksheet].getRow(unique=data['Email'])
    #     assert 'Name' in row.keys()
    #     assert 'Email' in row.keys()
    #     assert 'Birthday' in row.keys()
    #     assert 'Yearly Salary' in row.keys()
    #     assert 'Hours Worked' in row.keys()
    #     assert 'Hourly Pay' in row.keys()
    #     assert 'Total Pay' in row.keys()
    #     assert Flat_Cache.makeTimestampName('Name') in row.keys()
    #     assert Flat_Cache.makeTimestampName('Email') in row.keys()
    #     assert Flat_Cache.makeTimestampName('Birthday') in row.keys()
    #     assert Flat_Cache.makeTimestampName('Yearly Salary') in row.keys()
    #     assert Flat_Cache.makeTimestampName('Hours Worked') in row.keys()
    #     assert Flat_Cache.makeTimestampName('Hourly Pay') in row.keys()
    #     assert Flat_Cache.makeTimestampName('Total Pay') in row.keys()
    #     assert data['Name']             == row['Name']
    #     assert data['Email']            == row['Email']
    #     assert data['Birthday']         == row['Birthday']
    #     assert data['Yearly Salary']    == row['Yearly Salary']
    #     assert data['Hours Worked']     == row['Hours Worked']
    #     assert data['Hourly Pay']       == row['Hourly Pay']
    #     assert data['Total Pay']        == row['Total Pay']

    # def test_checkMappedData(self):
    #     #so long as this doesn't raise another error, we're good
    #     self.migrator.checkMappedData()


    # def test_doCommit(self):
    #     self.migrator.doCommit()


    # def test_noteProblems(self):
    #     pass


    # # def test_problems(self):
    # #     self.migrator.problems()


    # # def test_run(self):
    # #     self.migrator.run()

    # #     spreadsheet = Simple_Spreadsheet_Source()
    # #     spreadsheet.setupSpreadsheet()
    # #     worksheet = spreadsheet.getWorksheet(worksheetTitle="test_dataMove1")
    # #     data = worksheet.getData()
    # #     # get the data we will start with
    # #     row0 = worksheet.getRow(0, update_timestamp=True)
    # #     assert row0['Name'] == "Matt"
    # #     assert row0['Birthday'] == "1/1/2001"
    # #     assert row0['Email'] == "email@example.com"
    # #     assert row0['Yearly Salary'] == "40160"
    # #     assert row0['Hours Worked'] == "100"
    # #     assert row0['Hourly Pay'] == "20"
    # #     assert row0['Total Pay'] == "2000" 
    # #     assert row0[Flat_Cache.makeTimestampName('Name')] == 12345.0
    # #     assert row0[Flat_Cache.makeTimestampName('Birthday')] == 12345.0
    # #     assert row0[Flat_Cache.makeTimestampName('Email')] == 12345.0
    # #     # these were all set at the same time, so the timestamp is the same for these
    # #     timestamp = row0[Flat_Cache.makeTimestampName('Yearly Salary')]
    # #     assert row0[Flat_Cache.makeTimestampName('Hours Worked')] == timestamp
    # #     assert row0[Flat_Cache.makeTimestampName('Hourly Pay')] == timestamp
    # #     assert row0[Flat_Cache.makeTimestampName('Total Pay')] == timestamp
    # #     assert row0[UPDATE_TIMESTAMP_KEY] == timestamp

    # #     row1 = worksheet.getRow(1, update_timestamp=True)
    # #     timestamp = row1[Flat_Cache.makeTimestampName('Yearly Salary')]
    # #     assert row1[Flat_Cache.makeTimestampName('Hours Worked')] == timestamp
    # #     assert row1[Flat_Cache.makeTimestampName('Hourly Pay')] == timestamp
    # #     assert row1[Flat_Cache.makeTimestampName('Total Pay')] == timestamp
    # #     assert row1[UPDATE_TIMESTAMP_KEY] == timestamp
    # #     assert row1[Flat_Cache.makeTimestampName('Name')] == timestamp
    # #     assert row1[Flat_Cache.makeTimestampName('Birthday')] == timestamp
    # #     assert row1[Flat_Cache.makeTimestampName('Email')] == timestamp

    # #     row2 = worksheet.getRow(2,update_timestamp=True)
    # #     assert row2[Flat_Cache.makeTimestampName('Name')] == 54321.0
    # #     assert row2[Flat_Cache.makeTimestampName('Birthday')] == 54321.0
    # #     assert row2[Flat_Cache.makeTimestampName('Email')] == 54321.0
    # #     # these were all set at the same time, so the timestamp is the same for these
    # #     timestamp = row2[Flat_Cache.makeTimestampName('Yearly Salary')]
    # #     assert row2[Flat_Cache.makeTimestampName('Hours Worked')] == timestamp
    # #     assert row2[Flat_Cache.makeTimestampName('Hourly Pay')] == timestamp
    # #     assert row2[Flat_Cache.makeTimestampName('Total Pay')] == timestamp
    # #     assert row2[UPDATE_TIMESTAMP_KEY] == timestamp


    # #     worksheet = spreadsheet.getWorksheet(worksheetTitle="test_dataMove2")
    # #     data = worksheet.getData()
    # #     # get the data we will start with
    # #     row0 = worksheet.getRow(0, update_timestamp=True)
    # #     assert row0['Name'] == "Matt"
    # #     assert row0['Birthday'] == "1/1/2001"
    # #     assert row0['Email'] == "email@example.com"
    # #     assert row0['Yearly Salary'] == "20080"
    # #     assert row0['Hours Worked'] == "10"
    # #     assert row0['Hourly Pay'] == "2"
    # #     assert row0['Total Pay'] == "200"
    # #     assert row0[Flat_Cache.makeTimestampName('Name')] == 12345.0
    # #     assert row0[Flat_Cache.makeTimestampName('Birthday')] == 12345.0
    # #     assert row0[Flat_Cache.makeTimestampName('Email')] == 12345.0
    # #     # these were all set at the same time, so the timestamp is the same for these
    # #     timestamp = row0[Flat_Cache.makeTimestampName('Yearly Salary')]
    # #     assert row0[Flat_Cache.makeTimestampName('Hours Worked')] == timestamp
    # #     assert row0[Flat_Cache.makeTimestampName('Hourly Pay')] == timestamp
    # #     assert row0[Flat_Cache.makeTimestampName('Total Pay')] == timestamp
    # #     assert row0[UPDATE_TIMESTAMP_KEY] == timestamp

    # #     row1 = worksheet.getRow(1, update_timestamp=True)
    # #     timestamp = row1[Flat_Cache.makeTimestampName('Yearly Salary')]
    # #     assert row1[Flat_Cache.makeTimestampName('Hours Worked')] == timestamp
    # #     assert row1[Flat_Cache.makeTimestampName('Hourly Pay')] == timestamp
    # #     assert row1[Flat_Cache.makeTimestampName('Total Pay')] == timestamp
    # #     assert row1[Flat_Cache.makeTimestampName('update_timestamp')] == timestamp
    # #     assert row1[Flat_Cache.makeTimestampName('Name')] == timestamp
    # #     assert row1[Flat_Cache.makeTimestampName('Birthday')] == timestamp
    # #     assert row1[Flat_Cache.makeTimestampName('Email')] == timestamp

    # #     row2 = worksheet.getRow(2,update_timestamp=True)
    # #     assert row2[Flat_Cache.makeTimestampName('Name')] == 54321.0
    # #     assert row2[Flat_Cache.makeTimestampName('Birthday')] == 54321.0
    # #     assert row2[Flat_Cache.makeTimestampName('Email')] == 54321.0
    # #     # these were all set at the same time, so the timestamp is the same for these
    # #     timestamp = row2[Flat_Cache.makeTimestampName('Yearly Salary')]
    # #     assert row2[Flat_Cache.makeTimestampName('Hours Worked')] == timestamp
    # #     assert row2[Flat_Cache.makeTimestampName('Hourly Pay')] == timestamp
    # #     assert row2[Flat_Cache.makeTimestampName('Total Pay')] == timestamp
    # #     assert row2[UPDATE_TIMESTAMP_KEY] == timestamp