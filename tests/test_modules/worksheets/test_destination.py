import pytest
from modules.spreadsheets.destination import Bdfs_Spreadsheet_Destination
from modules.worksheets.destination import Bdfs_Worksheet_Destination
from modules.worksheets.exception import Bdfs_Worksheet_Destination_Exception
from modules.spreadsheets.exception import Bdfs_Spreadsheet_Exception
from modules.caches.exception import Flat_Cache_Exception

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
    assert excinfo.value.message == "The worksheet 'demo_worksheet' was not found in the kept worksheets: ['test_DONTMOVE', 'test_easy_data', 'test_payroll']"



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

    assert excinfo.value.message == "Cols expected was not set before instantiating Spreadsheet class"


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
        
    @classmethod
    def teardown_class(self): 
        print("\n\tTeardown class: {} execution".format(self.__name__))

    def setup_method(self, method):
        print(f"\n\tSetting up method {self.__class__.__name__}:: {method.__name__}")

    def teardown_method(self, method):
        pass

    def test_destination(self):
        assert ["one", "two", "three", "six"] == self.worksheet.getExpectedColumns()

    def test_remove_column(self):
        with pytest.raises(Flat_Cache_Exception) as excinfo:
            self.worksheet.removeColumn("six")
        assert "Location 'six' does not exist, try \"insert_location('six')\"" in excinfo.value.message
        
        assert not "one" in self.worksheet.getColumns()
        assert not "two" in self.worksheet.getColumns()
        assert not "three" in self.worksheet.getColumns()
        assert not "six" in self.worksheet.getColumns()

        columns = self.worksheet.getColumns() + self.worksheet.getExpectedColumns()
        self.worksheet.alignToColumns(columns)

        assert "one" in self.worksheet.getColumns()
        assert "two" in self.worksheet.getColumns()
        assert "three" in self.worksheet.getColumns()
        assert "six" in self.worksheet.getColumns()
    
        # add six from expected, then remove
        self.worksheet.removeColumn("six")

        assert "one" in self.worksheet.getColumns()
        assert "two" in self.worksheet.getColumns()
        assert "three" in self.worksheet.getColumns()
        assert not "six" in self.worksheet.getColumns()


    def test_remove_columns(self):

        columns = self.worksheet.getColumns() + self.worksheet.getExpectedColumns()
        self.worksheet.alignToColumns(columns)

        assert "one" in self.worksheet.getColumns()
        assert "two" in self.worksheet.getColumns()
        assert "three" in self.worksheet.getColumns()
        assert "six" in self.worksheet.getColumns()

        self.worksheet.removeColumns(["one", "two", "three", "six"])

        assert not "one" in self.worksheet.getColumns()
        assert not "two" in self.worksheet.getColumns()
        assert not "three" in self.worksheet.getColumns()
        assert not "six" in self.worksheet.getColumns()