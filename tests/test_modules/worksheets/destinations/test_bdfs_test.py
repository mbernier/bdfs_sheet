import gspread, pytest
from modules.spreadsheets.destinations.bdfs_test import BdfsInventory_Test_Spreadsheet_Destination
from modules.worksheets.exception import Bdfs_Worksheet_Exception
from tests.test_modules.worksheets.destinations.destination_helper import worksheet_helper

class Test_Bdfs_Worksheet_Destination:
    @classmethod
    def setup_class(self):
        print("starting class: {} execution".format(self.__name__))
        self.worksheetName = "test_easy_data"
        self.renameWorksheetName = "test_easy_data_new_title"
        self.copyFromWorksheetName = "demo_worksheet"
        self.class_setup = True
        # Do the setup of the objects for this test, done outside of the testing file to work around pytest oddities
        self.test_worksheet = worksheet_helper(None, self.worksheetName, self.copyFromWorksheetName, self.renameWorksheetName, True)
        
    @classmethod
    def teardown_class(self):
        print("starting class: {} execution".format(self.__name__))

    def setup_method(self, method):
        # This will cause the code to only run for the methods we care about that need this separately
        # as of now, this is test_commit and test_commit_with_larger_data
        self.test_worksheet = worksheet_helper(self.test_worksheet, self.worksheetName, self.copyFromWorksheetName, self.renameWorksheetName, method)

    def teardown_method(self, method):
        print("starting execution of tc: {}".format(method.__name__))

    ####
    #
    # Not Implemented, raises Exceptions
    #
    ####

    def test_removeColumns(self):
        with pytest.raises(Bdfs_Worksheet_Exception) as excinfo:
            self.test_worksheet.changed("whatever")
        assert excinfo.value.message == f"there is no 'whatever' in data.changes keys, add it to __setup() to track it"

    ####
    #
    # Implemented
    #
    ####


    def test_changed_isChanged(self):
        with pytest.raises(Bdfs_Worksheet_Exception) as excinfo:
            self.test_worksheet.changed("whatever")
        assert excinfo.value.message == f"there is no 'whatever' in data.changes keys, add it to __setup() to track it"
        
        self.test_worksheet.changed("data")
        assert True == self.test_worksheet.isChanged("data")
        
        self.test_worksheet.changed("data", False)
        assert False == self.test_worksheet.isChanged("data")

    def test_getTitle(self):
        title = self.test_worksheet.getTitle()
        assert self.worksheetName == title

    def test_setTitle_to_same_title(self):
        #if the titles are the same, we don't set the flag or the uncommitted title
        title = self.test_worksheet.getTitle()

        newTitle = self.test_worksheet.getTitle()

        self.test_worksheet.setTitle(newTitle)

        assert title == self.test_worksheet.getTitle()
        assert title == self.test_worksheet.getOriginalTitle()
        assert False == self.test_worksheet.isChanged('title')


    def test_setTitle(self):
        title = self.test_worksheet.getTitle()

        newTitle = "test_easy_data_new_title"

        self.test_worksheet.setTitle(newTitle)

        assert newTitle == self.test_worksheet.getTitle()
        assert title == self.test_worksheet.getOriginalTitle()
        assert self.test_worksheet.isChanged('title') == True


    def test_getA1(self):
        assert "A1" == self.test_worksheet.getA1(1,1)
        assert "E5" == self.test_worksheet.getA1(5,5)


    def test_getDataRange(self):
        dataRange = self.test_worksheet.getDataRange()
        assert dataRange == "A1:C4" #this counts the header row as row 1, where normally we don't do that in the code, bc gspread counts header row as row 1


    def test_getExpectedColumns(self):
        cols = self.test_worksheet.getExpectedColumns()
        assert cols == ['Updated Date', 'Title', 'Hardware', 'Published', 'Type', 'On BDFS?', 'Vendor', 'Handle', 'Type', 'Glass', 'SKU', 'SEO Title', 'Tags', 'Sarto SKU', 'Color', 'UnitedPorte URL', 'Image 1 URL', 'Image 1 SEO', 'Image 2 URL', 'Image 2 SEO', 'Image 3 URL', 'Image 3 SEO', 'Image 4 URL', 'Image 4 SEO', 'Image 5 URL', 'Image 5 SEO', 'Description']


    def test_getColumns(self):
        cols = self.test_worksheet.getColumns()
        assert cols == ['Name', 'Birthday', 'Email']
    

    def test_getColumnCounts(self):
        counts = self.test_worksheet.getColumnCounts()
        # also tests the gspread_worksheet_resize_to_data, bc if the data width is the same we got it right
        # not setting to a specific number, bc we don't care what the width is, just that they are the same
        assert counts['data'] == counts['gspread_worksheet'] 


    def test_addColumns(self):
        self.test_worksheet.addColumn("newColumn1")
        assert self.test_worksheet.getColumns() == ['Name', 'Birthday','Email', 'newColumn1']

        self.test_worksheet.addColumn(name="newColumn3", index=3)
        assert self.test_worksheet.getColumns() == ['Name', 'Birthday','Email', 'newColumn3', 'newColumn1']

    def test_commit(self):
        #pushes all the changes we have make to the sheet
        self.test_worksheet.commit()

        print("\n\n\nNeed to add tests to verify that the data was setup correctly in the gspread sheet\n\n\n")

    def test_commit_with_larger_data(self):
        # the worksheet is only 5 columns wide right now, let's see what happens if we add a lot more data
        self.test_worksheet.addColumn("newColumn4")
        self.test_worksheet.addColumn("newColumn5")
        self.test_worksheet.addColumn("newColumn6")
        self.test_worksheet.commit()