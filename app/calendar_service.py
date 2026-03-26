from googleapiclient.discovery import build
from datetime import datetime, timedelta
from google_auth import get_credentials

def create_event(manager_email, candidate_email, start_time):

    creds = get_credentials()
    service = build('calendar', 'v3', credentials=creds)

    end_time = start_time + timedelta(hours=1)

    event = {
        'summary': 'Interview Scheduled',
        'location': 'Google Meet',
        'description': 'Interview between manager and candidate',

        'start': {
            'dateTime': start_time.isoformat(),
            'timeZone': 'Asia/Kolkata',
        },
        'end': {
            'dateTime': end_time.isoformat(),
            'timeZone': 'Asia/Kolkata',
        },

        # ✅ VERY IMPORTANT (this sends email + invite)
        'attendees': [
            {'email': manager_email},
            {'email': candidate_email},
        ],

        # ✅ Google Meet link
        'conferenceData': {
            'createRequest': {
                'requestId': 'sample123',
                'conferenceSolutionKey': {'type': 'hangoutsMeet'}
            }
        }
    }

    event = service.events().insert(
        calendarId='primary',
        body=event,
        conferenceDataVersion=1,
        sendUpdates='all'   # ✅ THIS SENDS EMAILS
    ).execute()

    print("✅ Event created:", event.get("htmlLink"))
