from modules.worksheets.data import Bdfs_Worksheet_Data

# There is odd assignment behavior, so rather than worrying about scope just return this same array everytime
def setupData():
    return [["name","email", "cake"],["bob", "something@example.com", "chocolate"],["mary", "example@example.com", "strawberry"]]

class Test_Worksheet_Data:
    @classmethod
    def setup_class(self):
        print("\tstarting class: {} execution".format(self.__name__))
        
    @classmethod
    def teardown_class(self): 
        print("\tstarting class: {} execution".format(self.__name__))

    def setup_method(self, method):
        print("\tstarting method execution: {}".format(method.__name__))
        if method.__name__ == "test_wd":
            self.worksheet = Bdfs_Worksheet_Data()
        else:
            self.worksheet = Bdfs_Worksheet_Data(setupData())

    def teardown_method(self, method):
        pass

    def test_wd(self):
        self.worksheet.load(setupData())

    def test_wd2(self):
        #double checking that the pytest class setup method works and passing data into the class works
        pass

    def test_getHeaders(self):
        checkRow = setupData()[0]
        assert checkRow == self.worksheet.getHeaders()

    def test_width(self):
        assert 3 == self.worksheet.width()

    def test_height(self):
        assert self.worksheet.height() == 2

    def test_remove_header(self):
        checkRow = setupData()[0]
        assert self.worksheet.getHeaders() == checkRow
        self.worksheet.removeHeader("cake")
        checkRow.remove('cake')
        assert checkRow == self.worksheet.getHeaders()