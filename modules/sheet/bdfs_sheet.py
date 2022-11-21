from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import gspread

class Bdfs_sheet:
    def _init_():
        self.data = []

    def read_sheet(this, creds):
        # The ID and range of a sample spreadsheet.
        SPREADSHEET_ID = '1RyODmeydoIlMO75xa5wIxHRxqnZWRkDcxWZyp6fK-H8'
        SAMPLE_RANGE_NAME = 'sarto_barn_single!D2:CR'

        gc = gspread.service_account()

        sh = gc.open_by_key(SPREADSHEET_ID)
        
        worksheet_list = sh.worksheets()
        print(worksheet_list)

        for sheet in worksheet_list:
            print(sheet)