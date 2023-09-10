import os
from dotenv import load_dotenv
load_dotenv()

from google.oauth2 import service_account
from googleapiclient.discovery import build

GC_SERVICE_ACCOUNT_CREDENTIAL_PATH = os.getenv("GC_SERVICE_ACCOUNT_CREDENTIAL_PATH")
GC_SERVICE_ACCOUNT_CREDENTIAL_OWNER = os.getenv("GC_SERVICE_ACCOUNT_CREDENTIAL_OWNER")



# Load your service account credentials and set the necessary scopes for Google Drive
SERVICE_ACCOUNT_CREDENTIAL_PATH = GC_SERVICE_ACCOUNT_CREDENTIAL_PATH
DRIVE_SCOPES = ['https://www.googleapis.com/auth/drive']

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_CREDENTIAL_PATH,
    scopes=DRIVE_SCOPES
)

# Build the Google Drive API service
drive_service = build('drive', 'v3', credentials=credentials)

# Define the folder metadata
folder_metadata = {
    'name': 'TableTennisApp',  # Replace with your desired folder name
    'mimeType': 'application/vnd.google-apps.folder',
}

# Create the folder in Google Drive
folder = drive_service.files().create(
    body=folder_metadata,
    fields='id'  # This limits the response to just the folder ID
).execute()

# Print the folder ID
print(f'Created folder in Google Drive with folder ID: {folder["id"]}')

# Share the folder with specific users or groups (e.g., your Google account)
# Replace 'user@example.com' with the email addresses of the users or groups you want to share with
share_request_body = {
    'role': 'writer',  # You can use 'reader' or 'commenter' depending on the access level you want to grant
    'type': 'user',
    'emailAddress': GC_SERVICE_ACCOUNT_CREDENTIAL_OWNER,
}

drive_service.permissions().create(
    fileId=folder['id'],
    body=share_request_body,
    fields='id'  # This limits the response to just the permission ID
).execute()

print(f'Shared the folder with {GC_SERVICE_ACCOUNT_CREDENTIAL_OWNER}')
