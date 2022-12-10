from modules.worksheets.data import WorksheetData

def setup():
    return [["name","email", "cake"],["bob", "something@example.com", "chocolate"],["mary", "example@example.com", "strawberry"]]

def test_wd():
    data = setup()
    worksheet = WorksheetData()
    worksheet.load(data)

def test_wd2():
    data = setup()
    worksheet = WorksheetData(data)

def test_getHeaders():
    data = setup()
    checkRow = data[0]
    worksheet = WorksheetData(data)
    assert checkRow == worksheet.getHeaders()

def test_width():
    data = setup()
    worksheet = WorksheetData(data)
    assert 3 == worksheet.width()

def test_height():
    data = setup()
    worksheet = WorksheetData(data)
    assert worksheet.height() == 2