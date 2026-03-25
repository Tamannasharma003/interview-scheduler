from googleapiclient.discovery import build
from datetime import datetime, timedelta
from google_auth import get_credentials


def create_event(manager_email, candidate_email, start_time):
    creds = get_credentials()
    service = build('calendar', 'v3', credentials=creds)

    end_time = start_time + timedelta(hours=1)

    event = {
        'summary': 'Interview Scheduled',
        'location': 'Online',
        'description': 'Interview between manager and candidate',
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
        'reminders': {
            'useDefault': True,
        },
    }

    event = service.events().insert(
        calendarId='primary',
        body=event,
        sendUpdates='all'   # 🔥 THIS sends email automatically
    ).execute()

    print("✅ Event created:", event.get('htmlLink'))
