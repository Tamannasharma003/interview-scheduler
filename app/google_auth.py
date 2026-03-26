import os
import json
from google.oauth2 import service_account

SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_credentials():
    creds_dict = json.loads(os.getenv("GOOGLE_CREDENTIALS"))

    return service_account.Credentials.from_service_account_info(
        creds_dict,
        scopes=SCOPES
    )
