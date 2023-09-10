from dotenv import load_dotenv
import os
load_dotenv()

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build

# Define the Google Sheets and Drive API scopes
scopes = [
    "https://www.googleapis.com/auth/spreadsheets", 
    "https://www.googleapis.com/auth/drive"
]

# Authenticate
GC_SERVICE_ACCOUNT_CREDENTIAL_PATH = os.getenv("GC_SERVICE_ACCOUNT_CREDENTIAL_PATH")

creds = ServiceAccountCredentials.from_json_keyfile_name(GC_SERVICE_ACCOUNT_CREDENTIAL_PATH, scopes)
client = gspread.authorize(creds)

# Setup the Drive API client
drive_service = build('drive', 'v3', credentials=creds)

# Search for the Google Sheet by name
results = drive_service.files().list(
    q="name='test' and mimeType='application/vnd.google-apps.spreadsheet'",
    fields="files(id, name)").execute()

# Check if we have results
items = results.get('files', [])
if not items:
    print('No Google Sheets found.')
    exit()

# Assuming the first result is the sheet you want
sheet_id = items[0]['id']
sheet_name = items[0]['name']

# Now use gspread to open the sheet by ID
sheet = client.open_by_key(sheet_id).sheet1

# Fetch the data (like in the previous example)
records = sheet.get_all_records()

# Print the first_name and last_name
for record in records:
    print(record['nom'], record['prenom'])