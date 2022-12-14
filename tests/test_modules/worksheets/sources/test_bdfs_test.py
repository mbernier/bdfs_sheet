import pytest, time
from modules.caches.flat import Flat_Cache
from modules.spreadsheets.sources.simple_sheet import Simple_Spreadsheet_Source
from modules.worksheets.exception import Bdfs_Worksheet_Source_Exception
from tests.test_modules.worksheets.sources.sources_helper import sources_helper


class Test_Bdfs_Worksheet_Source:
    @classmethod
    def setup_class(self):
        print("\n\tStarting class: {} execution".format(self.__name__))
        self.worksheetName = "test_easy_data"
        self.renameWorksheetName = "test_easy_data_new_title"
        self.copyFromWorksheetName = "demo_worksheet"
        self.read_only_exception_msg = "Source Worksheets are not allowed to modify data"

        # Do the setup of the objects for this test, done outside of the testing file to work around pytest oddities
        self.test_worksheet = sources_helper(None, self.worksheetName, self.copyFromWorksheetName, self.renameWorksheetName, True)
        
    @classmethod
    def teardown_class(self): 
        print("\n\tTeardown class: {} execution".format(self.__name__))

    def setup_method(self, method):
        print(f"\n\tSetting up method {self.__class__.__name__}:: {method.__name__}")
        # This will cause the code to only run for the methods we care about that need this separately
        # as of now, this is test_commit and test_commit_with_larger_data
        self.test_worksheet = sources_helper(self.test_worksheet, self.worksheetName, self.copyFromWorksheetName, self.renameWorksheetName, method)

    def teardown_method(self, method):
        pass


    ####
    #
    # Not Implemented, raises Exceptions
    #
    ####

    def test_removeColumns(self):
        with pytest.raises(Bdfs_Worksheet_Source_Exception) as excinfo:
            self.test_worksheet.changed("whatever")
        assert excinfo.value.message == self.read_only_exception_msg


    ####
    #
    # Implemented
    #
    ####
    def test_changed_isChanged(self):
        with pytest.raises(Bdfs_Worksheet_Source_Exception) as excinfo:
            self.test_worksheet.changed("whatever")
        assert excinfo.value.message == self.read_only_exception_msg

        with pytest.raises(Bdfs_Worksheet_Source_Exception) as excinfo:
            self.test_worksheet.changed("data")
        assert excinfo.value.message == self.read_only_exception_msg

        assert False == self.test_worksheet.isChanged("data")

    def test_getTitle(self):
        title = self.test_worksheet.getTitle()
        assert self.worksheetName == title

    def test_setTitle_to_same_title(self):
        #if the titles are the same, we don't set the flag or the uncommitted title
        title = self.test_worksheet.getTitle()

        newTitle = self.test_worksheet.getTitle()

        with pytest.raises(AttributeError) as excinfo:
            self.test_worksheet.setTitle(newTitle)
        assert "has no attribute 'setTitle'" in str(excinfo.value)

        assert title == self.test_worksheet.getTitle()
        
        assert title == self.test_worksheet.getOriginalTitle()

        assert self.test_worksheet.isChanged('title') == False


    def test_setTitle(self):
        title = self.test_worksheet.getTitle()

        newTitle = "test_easy_data_new_title"

        with pytest.raises(AttributeError) as excinfo:
            self.test_worksheet.setTitle(newTitle)
        assert "has no attribute 'setTitle'" in str(excinfo.value)

        assert newTitle != self.test_worksheet.getTitle()
        
        assert title == self.test_worksheet.getOriginalTitle()

        assert self.test_worksheet.isChanged('title') == False

    def test_getA1(self):
        assert "A1" == self.test_worksheet.getA1(1,1)
        assert "E5" == self.test_worksheet.getA1(5,5)


    def test_getDataRange(self):
        dataRange = self.test_worksheet.getDataRange()
        assert dataRange == "A1:N4" #this counts the header row as row 1, where normally we don't do that in the code, bc gspread counts header row as row 1


    def test_getExpectedColumns(self):
        with pytest.raises(AttributeError) as excinfo:
            cols = self.test_worksheet.getExpectedColumns()
        assert "object has no attribute 'getExpectedColumns'" in str(excinfo.value)


    def test_getColumns(self):
        cols = self.test_worksheet.getColumns()
        assert cols == ['Name', 'Birthday', 'Email', 'Yearly Salary', 'Hours Worked', 'Favorite Cake', Flat_Cache.makeTimestampName('Name'), Flat_Cache.makeTimestampName('Birthday'), Flat_Cache.makeTimestampName('Email'), Flat_Cache.makeTimestampName('Yearly Salary'), Flat_Cache.makeTimestampName('Hours Worked'), Flat_Cache.makeTimestampName('Favorite Cake'), 'update_timestamp']


    def test_getColumnCounts(self):
        counts = self.test_worksheet.getColumnCounts()
        # also tests the gspread_worksheet_resize_to_data, bc if the data width is 2x + 1 we got it right
        assert counts['data'] == counts['gspread_worksheet'] * 2 + 1
        assert counts['gspread_worksheet'] == 6


    def test_addColumns(self):
        with pytest.raises(AttributeError) as excinfo:
            self.test_worksheet.addColumn("newColumn1")
        assert "object has no attribute 'addColumn'" in str(excinfo.value)
        
        assert self.test_worksheet.getColumns() == ['Name', 'Birthday','Email', 'Yearly Salary', 'Hours Worked', 'Favorite Cake', Flat_Cache.makeTimestampName('Name'), Flat_Cache.makeTimestampName('Birthday'), Flat_Cache.makeTimestampName('Email'), Flat_Cache.makeTimestampName('Yearly Salary'), Flat_Cache.makeTimestampName('Hours Worked'), Flat_Cache.makeTimestampName('Favorite Cake'), 'update_timestamp']

        with pytest.raises(AttributeError) as excinfo:
            self.test_worksheet.addColumn(name="newColumn3", index=3)
        assert "object has no attribute 'addColumn'" in str(excinfo.value)

        assert self.test_worksheet.getColumns() == ['Name', 'Birthday','Email', 'Yearly Salary', 'Hours Worked', 'Favorite Cake', Flat_Cache.makeTimestampName('Name'), Flat_Cache.makeTimestampName('Birthday'), Flat_Cache.makeTimestampName('Email'), Flat_Cache.makeTimestampName('Yearly Salary'), Flat_Cache.makeTimestampName('Hours Worked'), Flat_Cache.makeTimestampName('Favorite Cake'), 'update_timestamp']
        

    def test_commit(self):
        with pytest.raises(AttributeError) as excinfo:
            #pushes all the changes we have make to the sheet
            self.test_worksheet.commit()
        assert "object has no attribute 'commit'" in str(excinfo.value)
        

    def test_commit_with_larger_data(self):
        # the worksheet is only 5 columns wide right now, let's see what happens if we add a lot more data
        with pytest.raises(AttributeError) as excinfo:
            self.test_worksheet.addColumn("newColumn4")
            self.test_worksheet.addColumn("newColumn5")
            self.test_worksheet.addColumn("newColumn6")
            self.test_worksheet.commit()
        assert "object has no attribute 'addColumn'" in str(excinfo.value)
        