import gspread

class Bdfs_sheet:
    def _init_():
        self.data = []

    def read_sheet(this):
        # The ID and range of a sample spreadsheet.
        SPREADSHEET_ID = '1RyODmeydoIlMO75xa5wIxHRxqnZWRkDcxWZyp6fK-H8'
        SAMPLE_RANGE_NAME = 'sarto_barn_single!D2:CR'

        gc = gspread.service_account()

        sh = gc.open_by_key(SPREADSHEET_ID)
        
        worksheet_list = sh.worksheets()
        print(worksheet_list)

        for sheet in worksheet_list:
            print(sheet)