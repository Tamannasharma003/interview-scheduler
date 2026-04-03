import os
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

SCOPES = ["https://www.googleapis.com/auth/calendar"]

def get_credentials():
    token_json = os.getenv("TOKEN_JSON")

    if not token_json:
        raise Exception("❌ No TOKEN_JSON found in environment")

    creds = Credentials.from_authorized_user_info(
        json.loads(token_json), SCOPES
    )

    if creds.expired and creds.refresh_token:
        print("🔄 Refreshing token...")
        creds.refresh(Request())

    return creds
