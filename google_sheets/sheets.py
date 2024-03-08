from __future__ import print_function
import os.path
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


class GoogleSheet:
    SPREADSHEET_ID = '1ptV3jmmGTdcS8SvLgSHRNC-A44BLw-69dJRhvQvcc_0'
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    service = None

    def __init__(self):
        creds = None
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                print('flow')
                flow = InstalledAppFlow.from_client_secrets_file(
                    'google_sheets/credentials.json', self.SCOPES)
                creds = flow.run_local_server(port=0)
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        self.service = build('sheets', 'v4', credentials=creds)

    def updateRangeValues(self, range, values):
        data = [{
            'range': range,
            'values': values
        }]
        body = {
            'valueInputOption': 'USER_ENTERED',
            'data': data
        }
        
        self.service.spreadsheets().values().batchUpdate(spreadsheetId=self.SPREADSHEET_ID, body=body).execute()

        
    def updateCellBackground(self, cell, color):
        orange_rgb = {"red": 1.0, "green": 0.647, "blue": 0.0}
        green_rgb = {"red": 0.0, "green": 1.0, "blue": 0.0}

        if color == "orange":
            background_color = orange_rgb
        elif color == "green":
            background_color = green_rgb
        else:

            background_color = orange_rgb

        body = {
            "requests": [
                {
                    "repeatCell": {
                        "range": {
                            "sheetId": 0, 
                            "startRowIndex": int(cell[1:]) - 1,
                            "endRowIndex": int(cell[1:]),
                            "startColumnIndex": ord(cell[0]) - 65,
                            "endColumnIndex": ord(cell[0]) - 64
                        },
                        "cell": {
                            "userEnteredFormat": {
                                "backgroundColor": background_color
                            }
                        },
                        "fields": "userEnteredFormat(backgroundColor)"
                    }
                }
            ]
        }
        
        self.service.spreadsheets().batchUpdate(spreadsheetId=self.SPREADSHEET_ID, body=body).execute()


