import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials
import os


class GSheet:

    def __init__(self, key, worksheet):
        scopes = ['https://spreadsheets.google.com/feeds',
                  'https://www.googleapis.com/auth/drive']
        cred_dict = json.loads(os.environ['CREDS'], strict=False)
        credentials = ServiceAccountCredentials.from_json_keyfile_dict(
            cred_dict,
            scopes=scopes)
        gc = gspread.authorize(credentials)
        self.spreadsheet = gc.open_by_key(key)
        self.worksheet = self.spreadsheet.worksheet(worksheet)

    def add_row(self, row_values):
        self.worksheet.append_row(row_values)
