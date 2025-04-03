from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
import os

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
TOKEN_SHEETS = os.getenv("TOKEN_SHEETS")

def authenticate_sheets():
    creds = None
    if os.path.exists(TOKEN_SHEETS):
        creds = Credentials.from_authorized_user_file(TOKEN_SHEETS, SCOPES)
    else:
        flow = InstalledAppFlow.from_client_secrets_file(os.getenv("CREDENTIALS_PATH"), SCOPES)
        creds = flow.run_local_server(port=0)
        with open(TOKEN_SHEETS, 'w') as token:
            token.write(creds.to_json())
    return build('sheets', 'v4', credentials=creds)

def get_names_and_emails():
    service = authenticate_sheets()
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=os.getenv("SPREADSHEET_ID"), range="'Form Responses 1'!B2:C").execute()
    values = result.get('values', [])
    names, emails = [], []
    for row in values:
        names.append(row[0])
        emails.append(row[1] if len(row) > 1 else '')
    return names, emails