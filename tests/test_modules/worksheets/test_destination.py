import pytest, time
from modules.spreadsheets.destination import Bdfs_Spreadsheet_Destination
from modules.worksheets.destination import Bdfs_Worksheet_Destination
from modules.worksheets.exception import Bdfs_Worksheet_Destination_Exception
from modules.spreadsheets.exception import Bdfs_Spreadsheet_Exception
from modules.caches.exception import Flat_Cache_Exception, Nested_Cache_Exception


####
#
# Fail with the check for "kept" spreadsheets
#
####

class Simple_Spreadsheet_Destination_Fail(Bdfs_Spreadsheet_Destination):
    spreadsheetId = '1FEO3BKhyEtr7uF5ZmmodNm7vK3M5i5jrL2_AoOuAwlI' #test_inventory

    worksheetKeeperPattern = "test"

    worksheet_class = "tests.test_modules.worksheets.test_destination.Simple_Worksheet_Destination"

class Simple_Worksheet_Destination(Bdfs_Worksheet_Destination):
    # hourly Pay and total Pay will be added in testing
    cols_expected = []

    cols_expected_extra = {}
    
    def __init__(self, worksheet):
        super().__init__(worksheet)
    
def test_failed_destination_worksheet_not_kept():
    with pytest.raises(Bdfs_Spreadsheet_Exception) as excinfo:
        destination = Simple_Spreadsheet_Destination_Fail()
        spreadsheet = destination.setupSpreadsheet()
        test_worksheet = destination.getWorksheet("demo_worksheet")
    assert "The worksheet 'demo_worksheet' was not found in the kept worksheets" in excinfo.value.message
    time.sleep(5)

####
#
# Fail bc Expected Columns are not set up
#
####

class Failed_Spreadsheet_Destination(Bdfs_Spreadsheet_Destination):
    spreadsheetId = '1FEO3BKhyEtr7uF5ZmmodNm7vK3M5i5jrL2_AoOuAwlI' #test_inventory

    worksheetKeeperPattern = ""

    worksheet_class = "tests.test_modules.worksheets.test_destination.Failed_Worksheet_Destination"

class Failed_Worksheet_Destination(Bdfs_Worksheet_Destination):
    # hourly Pay and total Pay will be added in testing
    cols_expected = []

    cols_expected_extra = {}
    
    def __init__(self, worksheet):
        super().__init__(worksheet)

def test_failed_destination():
    with pytest.raises(Bdfs_Worksheet_Destination_Exception) as excinfo:
        destination = Failed_Spreadsheet_Destination()
        spreadsheet = destination.setupSpreadsheet()
        test_worksheet = destination.getWorksheet("demo_worksheet")

    assert "Cols expected was not set before instantiating Spreadsheet class" in excinfo.value.message
    time.sleep(5)

####
#
# Run through basic functionality on a known good spreadsheet, that has no timestamps to start with
#
####

class Good_Simple_Spreadsheet_Destination(Bdfs_Spreadsheet_Destination):
    spreadsheetId = '1FEO3BKhyEtr7uF5ZmmodNm7vK3M5i5jrL2_AoOuAwlI' #test_inventory

    worksheetKeeperPattern = "demo"

    worksheet_class = "tests.test_modules.worksheets.test_destination.Good_Worksheet_Destination"

class Good_Worksheet_Destination(Bdfs_Worksheet_Destination):
    # hourly Pay and total Pay will be added in testing
    cols_expected = ["one", "two", "three"]

    cols_expected_extra = {"test": ["four","five"],
                            "demo": ["six"]}
    
    def __init__(self, worksheet):
        super().__init__(worksheet)

class Test_Good_Worksheet_Data:
    @classmethod
    def setup_class(self):
        print("\n\tStarting class: {} execution".format(self.__name__))
        sheet = Good_Simple_Spreadsheet_Destination()
        sheet.setupSpreadsheet()
        self.sheet = sheet
        self.worksheet = self.sheet.getWorksheet("demo_worksheet")
        time.sleep(5)
        
    @classmethod
    def teardown_class(self): 
        print("\n\tTeardown class: {} execution".format(self.__name__))

    def setup_method(self, method):
        print(f"\n\tSetting up method {self.__class__.__name__}:: {method.__name__}")

    def teardown_method(self, method):
        pass

    def test_good_destination(self):
        assert ["one", "two", "three", "six"] == self.worksheet.getExpectedColumns()

    def test_good_remove_column(self):
        with pytest.raises(Flat_Cache_Exception) as excinfo:
            self.worksheet.removeColumn("six")
        assert "Location 'six' does not exist, try \"insert_location('six')\"" in excinfo.value.message

        columns = self.worksheet.getColumns()
        assert not "one" in self.worksheet.getColumns()
        assert not "two" in self.worksheet.getColumns()
        assert not "three" in self.worksheet.getColumns()
        assert not "six" in self.worksheet.getColumns()

        columns = self.worksheet.getColumns() + self.worksheet.getExpectedColumns()
        self.worksheet.alignToColumns(columns)

        columns = self.worksheet.getColumns()
        assert "one" in self.worksheet.getColumns()
        assert "two" in self.worksheet.getColumns()
        assert "three" in self.worksheet.getColumns()
        assert "six" in self.worksheet.getColumns()
    
        # add six from expected, then remove
        self.worksheet.removeColumn("six")

        columns = self.worksheet.getColumns()
        assert "one" in self.worksheet.getColumns()
        assert "two" in self.worksheet.getColumns()
        assert "three" in self.worksheet.getColumns()
        assert not "six" in self.worksheet.getColumns()


    def test_good_remove_columns(self):

        columns = self.worksheet.getColumns() + self.worksheet.getExpectedColumns()
        self.worksheet.alignToColumns(columns)

        columns = self.worksheet.getColumns()
        assert "one" in self.worksheet.getColumns()
        assert "two" in self.worksheet.getColumns()
        assert "three" in self.worksheet.getColumns()
        assert "six" in self.worksheet.getColumns()

        self.worksheet.removeColumns(["one", "two", "three", "six"])

        columns = self.worksheet.getColumns()
        assert not "one" in self.worksheet.getColumns()
        assert not "two" in self.worksheet.getColumns()
        assert not "three" in self.worksheet.getColumns()
        assert not "six" in self.worksheet.getColumns()

####
#
# Start with an empty sheet, no unique
#
####

class Empty_Simple_Spreadsheet_Destination(Bdfs_Spreadsheet_Destination):
    spreadsheetId = '1FEO3BKhyEtr7uF5ZmmodNm7vK3M5i5jrL2_AoOuAwlI' #test_inventory

    worksheetKeeperPattern = "empty"

    worksheet_class = "tests.test_modules.worksheets.test_destination.Empty_Worksheet_Destination"

class Empty_Worksheet_Destination(Bdfs_Worksheet_Destination):
    # hourly Pay and total Pay will be added in testing
    cols_expected = ["one", "two", "three"]

    cols_expected_extra = {"test": ["six"]}
    
    def __init__(self, worksheet):
        super().__init__(worksheet)


class Test_Empty_Worksheet_Data:
    @classmethod
    def setup_class(self):
        print("\n\tStarting class: {} execution".format(self.__name__))
        sheet = Empty_Simple_Spreadsheet_Destination()
        sheet.setupSpreadsheet()
        self.sheet = sheet
        self.worksheet = self.sheet.getWorksheet("test_empty")
        time.sleep(5)
        self.worksheet.gspread_worksheet_clear()
        time.sleep(5)
        
    @classmethod
    def teardown_class(self): 
        print("\n\tTeardown class: {} execution".format(self.__name__))

    def setup_method(self, method):
        print(f"\n\tSetting up method {self.__class__.__name__}:: {method.__name__}")

    def teardown_method(self, method):
        pass

    def test_empty_expectedCols(self):
        assert ["one", "two", "three", "six"] == self.worksheet.getExpectedColumns()

    def test_empty_remove_column(self):

        columns = self.worksheet.getColumns()
        assert not "one" in self.worksheet.getColumns()
        assert not "two" in self.worksheet.getColumns()
        assert not "three" in self.worksheet.getColumns()
        assert not "six" in self.worksheet.getColumns()

        with pytest.raises(Nested_Cache_Exception) as excinfo:
            self.worksheet.removeColumn("eleven")
        assert "Cannot delete a column from an empty Row" in excinfo.value.message
        
        columns = self.worksheet.getColumns() + self.worksheet.getExpectedColumns()
        self.worksheet.alignToColumns(columns)

        columns = self.worksheet.getColumns()
        assert "one" in self.worksheet.getColumns()
        assert "two" in self.worksheet.getColumns()
        assert "three" in self.worksheet.getColumns()
        assert "six" in self.worksheet.getColumns()
    
        # add six from expected, then remove
        self.worksheet.removeColumn("six")

        columns = self.worksheet.getColumns()
        assert "one" in self.worksheet.getColumns()
        assert "two" in self.worksheet.getColumns()
        assert "three" in self.worksheet.getColumns()
        assert not "six" in self.worksheet.getColumns()


    def test_empty_remove_columns(self):

        columns = self.worksheet.getColumns() + self.worksheet.getExpectedColumns()
        self.worksheet.alignToColumns(columns)

        columns = self.worksheet.getColumns()
        assert "one" in self.worksheet.getColumns()
        assert "two" in self.worksheet.getColumns()
        assert "three" in self.worksheet.getColumns()
        assert "six" in self.worksheet.getColumns()

        self.worksheet.removeColumns(["one", "two", "three", "six"])

        columns = self.worksheet.getColumns()
        assert not "one" in columns
        assert not "two" in columns
        assert not "three" in columns
        assert not "six" in columns

####
#
# Start with Empty Sheet, but utilize unique fields
#
####

class Empty_w_Unique_Simple_Spreadsheet_Destination(Bdfs_Spreadsheet_Destination):
    spreadsheetId = '1FEO3BKhyEtr7uF5ZmmodNm7vK3M5i5jrL2_AoOuAwlI' #test_inventory

    worksheetKeeperPattern = "empty"

    worksheet_class = "tests.test_modules.worksheets.test_destination.Empty_w_Unique_Worksheet_Destination"

class Empty_w_Unique_Worksheet_Destination(Bdfs_Worksheet_Destination):
    # hourly Pay and total Pay will be added in testing
    cols_expected = ["one", "two", "three"]

    cols_expected_extra = {"test": ["six"]}
    
    def setupParams(self):
        self.data.uniqueField = "one"
        self.data.expectedColumns = self.cols_expected
        self.data.expectedColumns_extra = self.cols_expected_extra

class Test_Empty_w_Unique_Worksheet_Data:
    @classmethod
    def setup_class(self):
        print("\n\tStarting class: {} execution".format(self.__name__))
        sheet = Empty_w_Unique_Simple_Spreadsheet_Destination()
        sheet.setupSpreadsheet()
        self.sheet = sheet
        self.worksheet = self.sheet.getWorksheet("test_empty")
        time.sleep(5)
        # make sure it's empty
        self.worksheet.gspread_worksheet_clear()
        time.sleep(5)
        
    @classmethod
    def teardown_class(self): 
        # Make it empty at the end
        # self.worksheet.gspread_worksheet_clear()
        print("\n\tTeardown class: {} execution".format(self.__name__))

    def setup_method(self, method):
        print(f"\n\tSetting up method {self.__class__.__name__}:: {method.__name__}")

    def teardown_method(self, method):
        pass

    def test_empty_expectedCols(self):
        assert ["one", "two", "three", "six"] == self.worksheet.getExpectedColumns()

    def test_empty_remove_column(self):

        columns = self.worksheet.getColumns()
        assert not "one" in columns
        assert not "two" in columns
        assert not "three" in columns
        assert not "six" in columns

        with pytest.raises(Nested_Cache_Exception) as excinfo:
            self.worksheet.removeColumn("eleven")
        assert "Cannot delete a column from an empty Row" in excinfo.value.message
        
        columns = self.worksheet.getColumns() + self.worksheet.getExpectedColumns()
        self.worksheet.alignToColumns(columns)

        columns = self.worksheet.getColumns()
        assert "one" in columns
        assert "two" in columns
        assert "three" in columns
        assert "six" in columns
        assert 1 == columns.count("one")
        assert 1 == columns.count("two")
        assert 1 == columns.count("three")
        assert 1 == columns.count("update_timestamp")

        # add six from expected, then remove
        self.worksheet.removeColumn("six")

        columns = self.worksheet.getColumns()
        assert "one" in columns
        assert "two" in columns
        assert "three" in columns
        assert not "six" in columns

        assert 1 == columns.count("one")
        assert 1 == columns.count("two")
        assert 1 == columns.count("three")
        assert 1 == columns.count("update_timestamp")


    def test_empty_add_data(self):
        
        with pytest.raises(Nested_Cache_Exception) as excinfo:
            self.worksheet.addRow([1,2,3,6])
        assert "rowData was expected to be of length 3 but 4 was passed" == excinfo.value.message
        
        self.worksheet.addRow([1,2,3])

        data = self.worksheet.getRow()
        assert type(data) == list
        assert len(data) == 1
        row0 = data[0]
        assert row0['one'] == 1
        assert row0['two'] == 2
        assert row0['three'] == 3

        columns = self.worksheet.getColumns()
        assert 1 == columns.count("one")
        assert 1 == columns.count("two")
        assert 1 == columns.count("three")
        assert 1 == columns.count("update_timestamp")
    
    def test_empty_commit(self):
        self.worksheet.commit()
        time.sleep(5)
        self.worksheet = self.sheet.getWorksheet("test_empty")

        columns = self.worksheet.getColumns()
        assert 1 == columns.count("one")
        assert 1 == columns.count("two")
        assert 1 == columns.count("three")
        assert 1 == columns.count("one_update_timestamp")
        assert 1 == columns.count("two_update_timestamp")
        assert 1 == columns.count("three_update_timestamp")
        assert 1 == columns.count("update_timestamp")
        assert type

####
#
# Start with a sheet that already has timestamps, some filled, some empty
#   just testing the loading of the data to local, not testing commit()
#
####

class Start_With_Timestamp_Data_Simple_Spreadsheet_Destination(Bdfs_Spreadsheet_Destination):
    spreadsheetId = '1FEO3BKhyEtr7uF5ZmmodNm7vK3M5i5jrL2_AoOuAwlI' #test_inventory

    worksheetKeeperPattern = "test_start"

    worksheet_class = "tests.test_modules.worksheets.test_destination.Start_With_Timestamp_Data_Worksheet_Destination"

class Start_With_Timestamp_Data_Worksheet_Destination(Bdfs_Worksheet_Destination):
    # hourly Pay and total Pay will be added in testing
    cols_expected = ["Name", "Email", "Birthday"]

    cols_expected_extra = {"test": ["Cake"]}
    
    def setupParams(self):
        self.data.uniqueField = "Email"
        self.data.expectedColumns = self.cols_expected
        self.data.expectedColumns_extra = self.cols_expected_extra

class Test_Start_With_Timestamp_Data_Worksheet_Data:
    @classmethod
    def setup_class(self):
        print("\n\tStarting class: {} execution".format(self.__name__))
        sheet = Start_With_Timestamp_Data_Simple_Spreadsheet_Destination()
        sheet.setupSpreadsheet()
        self.sheet = sheet
        self.worksheet = self.sheet.getWorksheet("test_start_with_columns")
        time.sleep(5)
        
    @classmethod
    def teardown_class(self): 
        # Make it empty at the end
        # self.worksheet.gspread_worksheet_clear()
        print("\n\tTeardown class: {} execution".format(self.__name__))

    def setup_method(self, method):
        print(f"\n\tSetting up method {self.__class__.__name__}:: {method.__name__}")

    def teardown_method(self, method):
        pass

    def test_empty_expectedCols(self):
        assert ["Name", "Email", "Birthday", "Cake"] == self.worksheet.getExpectedColumns()

    def test_empty_add_data(self):
        
        with pytest.raises(Nested_Cache_Exception) as excinfo:
            self.worksheet.addRow(["Nate","something@example.com","1/1/2000","Purple"])
        assert "rowData was expected to be of length 3 but 4 was passed" == excinfo.value.message
        assert self.worksheet.height() == 4

        self.worksheet.addRow(["Nate","something@example.com","1/1/2000"])
        assert self.worksheet.height() == 5

        data = self.worksheet.getRow()
        assert type(data) == list
        assert len(data) == 5

        row0 = data[4]
        assert row0['Name'] == 'Nate'
        assert row0['Email'] == 'something@example.com'
        assert row0['Birthday'] == '1/1/2000'

        columns = self.worksheet.getColumns()
        assert 1 == columns.count("Name")
        assert 1 == columns.count("Email")
        assert 1 == columns.count("Birthday")
        assert 1 == columns.count("update_timestamp")