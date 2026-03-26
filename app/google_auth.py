import os
import json
from google.oauth2.credentials import Credentials

SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_credentials():

    token_data = os.getenv("TOKEN_JSON")

    if not token_data:
        raise Exception("TOKEN_JSON not found in Railway")

    creds_dict = json.loads(token_data)

    creds = Credentials.from_authorized_user_info(creds_dict, SCOPES)

    return creds
