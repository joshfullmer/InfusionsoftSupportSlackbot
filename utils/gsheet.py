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

    # Params
    # @message dictionary with message information
    def add_message(self, data):
        self.add_row(data)

    def update_message(self, data):
        message_id = data[0]
        message_ids = self.worksheet.col_values(1)
        row_num = message_ids.index(message_id) + 1
        self.worksheet.insert_row(data, index=row_num)
        self.worksheet.delete_row(data, index=row_num+1)

    def delete_message(self, data):
        pass
