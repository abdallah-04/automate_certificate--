import email
import gspread
from dotenv import load_dotenv,dotenv_values
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import pickle
load_dotenv()

scopes = [os.getenv("SCOPES")]
creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
client = gspread.authorize(creds)

sheet_id = os.getenv("SHEET_ID")
sheet = client.open_by_key(sheet_id).sheet1  

Names_list = sheet.col_values(2)
Emails_list=sheet.col_values(3)

fixed_names = []

for name in Names_list:
    parts = name.strip().split()
    if len(parts) >= 2:
        fixed_name = f"{parts[0]} {parts[-1]}"
        fixed_names.append(fixed_name)
