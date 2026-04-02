import os
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

SCOPES = ["https://www.googleapis.com/auth/calendar"]


def get_credentials():
    creds = None

    # =========================
    # 🔹 Load token from ENV
    # =========================
    token_json = os.getenv("GOOGLE_TOKEN")

    if token_json:
        creds = Credentials.from_authorized_user_info(
            json.loads(token_json),
            SCOPES
        )

    # =========================
    # 🔹 Refresh if expired
    # =========================
    if creds and creds.expired and creds.refresh_token:
        print("🔄 Refreshing token...")
        creds.refresh(Request())

    # =========================
    # ❌ If no token → STOP
    # =========================
    if not creds or not creds.valid:
        raise Exception("❌ No valid Google token found. Generate it locally first.")

    return creds
