from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import os

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

def authenticate_sheets():
   
    creds = None
    token_path = 'token.json'

    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    else:
        from google_auth_oauthlib.flow import InstalledAppFlow
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
        with open(token_path, 'w') as token:
            token.write(creds.to_json())

    return build('sheets', 'v4', credentials=creds)

def get_names_and_emails(spreadsheet_id, range_name="'Form Responses 1'!B2:C"):

    service = authenticate_sheets()
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
    values = result.get('values', [])

    names, emails = [], []
    for row in values:
        names.append(row[0])
        emails.append(row[1] if len(row) > 1 else '')

    return names, emails


SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
names, emails = get_names_and_emails(SPREADSHEET_ID)
