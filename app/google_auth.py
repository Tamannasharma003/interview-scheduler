import os
import json
from google.oauth2.service_account import Credentials

SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_credentials():
    creds_json = os.getenv("GOOGLE_CREDENTIALS")

    # 🔥 ADD THIS LINE HERE
    print("DEBUG GOOGLE_CREDENTIALS:", creds_json[:100] if creds_json else "NONE")

    if not creds_json:
        raise ValueError("❌ GOOGLE_CREDENTIALS not set")

    creds_dict = json.loads(creds_json)

    creds = Credentials.from_service_account_info(
        creds_dict,
        scopes=SCOPES
    )

    return creds
