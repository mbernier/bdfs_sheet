from modules.worksheets.data import Bdfs_Worksheet_Data
from modules.caches.flat import Flat_Cache

# There is odd assignment behavior, so rather than worrying about scope just return this same array everytime
def setupData():
    return [["name","email", "cake"],["bob", "something@example.com", "chocolate"],["mary", "example@example.com", "strawberry"]]

class Test_Worksheet_Data:
    @classmethod
    def setup_class(self):
        print("\n\tstarting class: {} execution".format(self.__name__))
        
    @classmethod
    def teardown_class(self): 
        print("\tstarting class: {} execution".format(self.__name__))

    def setup_method(self, method):
        print("\tstarting method execution: {}".format(method.__name__))
        if method.__name__ == "test_wd":
            self.worksheet_data = Bdfs_Worksheet_Data()
        else:
            self.worksheet_data = Bdfs_Worksheet_Data(setupData())

    def teardown_method(self, method):
        pass

    def test_wd(self):
        self.worksheet_data.load(setupData())

    def test_wd2(self):
        #double checking that the pytest class setup method works and passing data into the class works
        pass

    def test_width(self):
        assert 3 == self.worksheet_data.width()

    def test_height(self):
        assert self.worksheet_data.height() == 2

    ####
    #
    # Header Tests
    #
    ####

    def test_getHeaders(self):
        checkRow = setupData()[0]
        assert checkRow == self.worksheet_data.getHeaders()


    def test_remove_header(self):
        checkRow = setupData()[0]
        assert self.worksheet_data.getHeaders() == checkRow
        self.worksheet_data.removeHeader("cake")
        checkRow.remove('cake')
        assert checkRow == self.worksheet_data.getHeaders()
    

    def test_reorder_header(self):
        newHeaderOrder = ["cake", "email", "name"]
        self.worksheet_data.reorderHeaders(newHeaderOrder)
        assert newHeaderOrder == self.worksheet_data.getHeaders()


    def test_align_header(self):
        newHeaderOrder = ["cake", "email", "elephant", "giraffe"]
        self.worksheet_data.alignHeaders(newHeaderOrder)
        assert newHeaderOrder == self.worksheet_data.getHeaders()

    ####
    #
    # Row Tests
    #
    ####

    def test_select(self):
        # we have tested flat cache up to this point, so let's use it
        fcache = Flat_Cache(setupData()[0],setupData()[1])

        # prove that the data we are expecting matches what Flat Cache would give us, minus the timestamp
        assert self.worksheet_data.select(0, update_timestamp=False) == fcache.getAsDict(update_timestamp=False)
    

    def test_validateData_afterAlignHeaders(self):
        cake = self.worksheet_data.select(0,"cake")
        assert cake == setupData()[1][2] # test that we get the right data
        
        email = self.worksheet_data.select(0,"email")
        assert email == setupData()[1][1] # test that we get the right data

        # we have tested flat cache up to this point, so let's use it
        fcache = Flat_Cache(["cake", "email", "elephant", "giraffe"], [cake, email, None, None])
        
        newHeaderOrder = ["cake", "email", "elephant", "giraffe"]
        self.worksheet_data.alignHeaders(newHeaderOrder)

        # let's make sure the data is as expected after the realignment
        assert self.worksheet_data.select(0, update_timestamp=False) == fcache.getAsDict(update_timestamp=False)