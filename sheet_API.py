from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import os

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

def authenticate_sheets():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    else:
        from google_auth_oauthlib.flow import InstalledAppFlow
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)

        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return build('sheets', 'v4', credentials=creds)

def read_sheet_data(spreadsheet_id, range_name):
    service = authenticate_sheets()
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    else: 
        print('Sheet data:')
        for row in values:
            print(row)

    return values
names = []
emails = []

def get_names_and_emails(spreadsheet_id):
    global names, emails
    service = authenticate_sheets()
    sheet = service.spreadsheets()

    range_name = "'Form Responses 1'!B2:C"
    result = sheet.values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
    values = result.get('values', [])

    for row in values:
        if len(row) >= 2:
            names.append(row[0])   
            emails.append(row[1])  # Email
        elif len(row) == 1:
            names.append(row[0])
            emails.append('')      # Empty email

# Automatically populate lists when file is run or imported
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
get_names_and_emails(SPREADSHEET_ID)