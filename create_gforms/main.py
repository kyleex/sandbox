from dotenv import load_dotenv
import os
load_dotenv()

from google.oauth2 import service_account
from googleapiclient.discovery import build

GC_SERVICE_ACCOUNT_CREDENTIAL_PATH = os.getenv("GC_SERVICE_ACCOUNT_CREDENTIAL_PATH")
SCOPES = ['https://www.googleapis.com/auth/forms', 'https://www.googleapis.com/auth/drive']

credentials = service_account.Credentials.from_service_account_file(
    GC_SERVICE_ACCOUNT_CREDENTIAL_PATH,
    scopes=SCOPES
)

# Create a Google Forms API service
forms_service = build('forms', 'v1', credentials=credentials)

# Request body for creating a form
NEW_FORM = {
    "info": {
        "title": "Quickstart form",
    }
}

# Request body to add a multiple-choice question
NEW_QUESTION = {
    "requests": [{
        "createItem": {
            "item": {
                "title": "In what year did the United States land a mission on the moon?",
                "questionItem": {
                    "question": {
                        "required": True,
                        "choiceQuestion": {
                            "type": "RADIO",
                            "options": [
                                {"value": "1965"},
                                {"value": "1967"},
                                {"value": "1969"},
                                {"value": "1971"}
                            ],
                            "shuffle": True
                        }
                    }
                },
            },
            "location": {
                "index": 0
            }
        }
    }]
}

# Creates the initial form
result = forms_service.forms().create(body=NEW_FORM).execute()

# Adds the question to the form
question_setting = forms_service.forms().batchUpdate(formId=result["formId"], body=NEW_QUESTION).execute()

# Prints the result to show the question has been added
get_result = forms_service.forms().get(formId=result["formId"]).execute()
print(get_result)
