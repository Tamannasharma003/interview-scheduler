import os
import json
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

SCOPES = ["https://www.googleapis.com/auth/calendar"]

def get_credentials():
    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if creds and creds.expired and creds.refresh_token:
        print("🔄 Refreshing token...")
        creds.refresh(Request())

    if not creds or not creds.valid:
        print("🔐 Generating new token...")

        flow = InstalledAppFlow.from_client_secrets_file(
            "credentials.json",
            SCOPES
        )

        creds = flow.run_local_server(
            port=0,
            access_type="offline",
            prompt="consent"
        )

        with open("token.json", "w") as token:
            token.write(creds.to_json())

        print("✅ token.json created successfully")

    return creds


# ✅ THIS LINE WAS MISSING
if __name__ == "__main__":
    get_credentials()
