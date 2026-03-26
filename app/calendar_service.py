from googleapiclient.discovery import build
from datetime import datetime, timedelta
from google_auth import get_credentials
import uuid

def create_event(manager_email, candidate_email, start_time):

    creds = get_credentials()
    service = build('calendar', 'v3', credentials=creds)

    end_time = start_time + timedelta(hours=1)

    event = {
        'summary': 'Interview Scheduled',
        'location': 'Google Meet',
        'description': f'Interview between {manager_email} and {candidate_email}',

        'start': {
            'dateTime': start_time.isoformat(),
            'timeZone': 'Asia/Kolkata',
        },
        'end': {
            'dateTime': end_time.isoformat(),
            'timeZone': 'Asia/Kolkata',
        },

        'attendees': [
            {'email': manager_email},
            {'email': candidate_email},
        ],

        'conferenceData': {
            'createRequest': {
                'requestId': str(uuid.uuid4()),  # ✅ FIXED
                'conferenceSolutionKey': {'type': 'hangoutsMeet'}
            }
        },

        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 30},
                {'method': 'popup', 'minutes': 10},
            ],
        }
    }

    event = service.events().insert(
        calendarId='primary',
        body=event,
        conferenceDataVersion=1,
        sendUpdates='all'
    ).execute()

    print("✅ Event created:", event.get("htmlLink"))

    # ✅ Optional: print Meet link
    meet_link = event.get("conferenceData", {}).get("entryPoints", [])
    if meet_link:
        print("🎥 Meet Link:", meet_link[0].get("uri"))
