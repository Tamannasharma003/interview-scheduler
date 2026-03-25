from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import os

SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_credentials():
    creds = None

    # If token already exists
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    # If no valid creds → login
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'app/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)



        # Save token
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return creds

if __name__ == "__main__":
    creds = get_credentials()
    print("✅ Authentication successful!")

