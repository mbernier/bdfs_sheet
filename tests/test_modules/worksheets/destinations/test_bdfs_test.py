import gspread, pytest
from modules.caches.flat import Flat_Cache
from modules.worksheets.exception import Bdfs_Worksheet_Exception
from tests.test_modules.worksheets.destinations.destination_helper import destination_helper

class Test_Bdfs_Worksheet_Destination:
    @classmethod
    def setup_class(self):
        print("\n\tstarting class: {} execution".format(self.__name__))
        self.worksheetName = "test_easy_data"
        self.renameWorksheetName = "test_easy_data_new_title"
        self.copyFromWorksheetName = "demo_worksheet"
        self.class_setup = True
        # Do the setup of the objects for this test, done outside of the testing file to work around pytest oddities
        self.test_worksheet = destination_helper(None, self.worksheetName, self.copyFromWorksheetName, self.renameWorksheetName, True)
        
    @classmethod
    def teardown_class(self):
        print("\tstarting Test_Bdfs_Worksheet_Destination: {} execution".format(self.__name__))

    def setup_method(self, method):
        # This will cause the code to only run for the methods we care about that need this separately
        # as of now, this is test_commit and test_commit_with_larger_data
        self.test_worksheet = destination_helper(self.test_worksheet, self.worksheetName, self.copyFromWorksheetName, self.renameWorksheetName, method)

    def teardown_method(self, method):
        print("\tstarting execution of Destination: {}".format(method.__name__))

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
        assert dataRange == "A1:M4" #this counts the header row as row 1, where normally we don't do that in the code, bc gspread counts header row as row 1

    def test_getExpectedColumns(self):
        cols = self.test_worksheet.getExpectedColumns()
        assert cols == ['Name', 'Birthday', 'Email', 'Yearly Salary', 'Hours Worked', 'Hourly Pay', 'Total Pay']


    def test_getColumns(self):
        cols = self.test_worksheet.getColumns()
        assert cols == ['Name', 'Birthday', 'Email', 'Yearly Salary', 'Hours Worked', 'Favorite Cake', 'update_timestamp', 'Name_update_timestamp', 'Birthday_update_timestamp', 'Email_update_timestamp', 'Yearly Salary_update_timestamp', 'Hours Worked_update_timestamp', 'Favorite Cake_update_timestamp']
    

    def test_getColumnCounts(self):
        counts = self.test_worksheet.getColumnCounts()
        
        # we are adding columns that don't exist with the timestamps, so the local data will be 
        # 2x + 1 of the gspread data
        assert counts['data'] == (2 * counts['gspread_worksheet'] + 1)



    def test_addColumns(self):
        self.test_worksheet.addColumn("newColumn1")
        assert self.test_worksheet.getColumns() == ['Name', 'Birthday', 'Email', 'Yearly Salary', 'Hours Worked', 'Favorite Cake', 'newColumn1', 'update_timestamp', 'Name_update_timestamp', 'Birthday_update_timestamp', 'Email_update_timestamp', 'Yearly Salary_update_timestamp', 'Hours Worked_update_timestamp', 'Favorite Cake_update_timestamp', 'newColumn1_update_timestamp']

        self.test_worksheet.addColumn(name="newColumn3", index=3)
        assert self.test_worksheet.getColumns() == ['Name', 'Birthday','Email', 'newColumn3', 'Yearly Salary', 'Hours Worked', 'Favorite Cake', 'newColumn1', 'update_timestamp', 'Name_update_timestamp', 'Birthday_update_timestamp', 'Email_update_timestamp', 'Yearly Salary_update_timestamp', 'Hours Worked_update_timestamp', 'Favorite Cake_update_timestamp', 'newColumn1_update_timestamp', 'newColumn3_update_timestamp']


    # def test_alignToColumns(self):
    #     newColumns = ['Name', 'cake', 'giraffe', 'Birthday']
    #     self.test_worksheet.alignToColumns(newColumns)
    #     assert self.test_worksheet.getColumns() == newColumns


    # def test_getRow(self):
    #     # we have tested flat cache up to this point, so let's use it
    #     # also, of note - we are using the local version of the workshet, not the remote here
    #     #   so the previous tests affect what's available
    #     fcache = Flat_Cache(
    #                 ['Name', 'cake', 'giraffe', 'Birthday'], 
    #                 ['Matt', None, None, '1/1/2001']
    #             )

    #     assert self.test_worksheet.getRow(0, update_timestamp=False) == fcache.select(update_timestamp=False)


    # def test_getCell(self):
    #     assert self.test_worksheet.getCell(0, "Name") == "Matt"
    #     assert self.test_worksheet.getCell(0, "Birthday") == "1/1/2001"


    # def test_commit(self):
    #     #pushes all the changes we have make to the sheet
    #     self.test_worksheet.commit()

    #     print("\n\n\nNeed to add tests to verify that the data was setup correctly in the gspread sheet\n\n\n")


    # def test_commit_with_larger_data(self):
    #     # the worksheet is only 5 columns wide right now, let's see what happens if we add a lot more data
    #     self.test_worksheet.addColumn("newColumn4")
    #     self.test_worksheet.addColumn("newColumn5")
    #     self.test_worksheet.addColumn("newColumn6")
    #     self.test_worksheet.commit()