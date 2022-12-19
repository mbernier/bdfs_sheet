from modules.worksheets.data import Bdfs_Worksheet_Data

def setup():
    return [["name","email", "cake"],["bob", "something@example.com", "chocolate"],["mary", "example@example.com", "strawberry"]]

def test_wd():
    data = setup()
    worksheet = Bdfs_Worksheet_Data()
    worksheet.load(data)

def test_wd2():
    data = setup()
    worksheet = Bdfs_Worksheet_Data(data)

def test_getHeaders():
    data = setup()
    checkRow = data[0]
    worksheet = Bdfs_Worksheet_Data(data)
    assert checkRow == worksheet.getHeaders()

def test_width():
    data = setup()
    worksheet = Bdfs_Worksheet_Data(data)
    assert 3 == worksheet.width()

def test_height():
    data = setup()
    worksheet = Bdfs_Worksheet_Data(data)
    assert worksheet.height() == 2