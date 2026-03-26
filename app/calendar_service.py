from googleapiclient.discovery import build
from datetime import datetime, timedelta
from google_auth import get_credentials


def create_event(manager_email, candidate_email, start_time):
    creds = get_credentials()
    service = build('calendar', 'v3', credentials=creds)

    # ✅ Convert string → datetime if needed
    if isinstance(start_time, str):
        try:
            start_time = datetime.strptime(start_time.strip().lower(), "%I%p")
        except:
            start_time = datetime.strptime(start_time.strip().lower(), "%I %p")

        # ✅ Set today's date
        now = datetime.now()
        start_time = start_time.replace(
            year=now.year,
            month=now.month,
            day=now.day
        )

    end_time = start_time + timedelta(hours=1)

    # ✅ FIXED EVENT (no attendees)
    event = {
        'summary': 'Interview Scheduled',
        'location': 'Online',
        'description': f'Interview scheduled at {start_time.strftime("%I:%M %p")}',
        'start': {
            'dateTime': start_time.isoformat(),
            'timeZone': 'Asia/Kolkata',
        },
        'end': {
            'dateTime': end_time.isoformat(),
            'timeZone': 'Asia/Kolkata',
        },
        'reminders': {
            'useDefault': True,
        },
    }

    try:
        event = service.events().insert(
            calendarId='primary',
            body=event,
            sendUpdates='none'   # ✅ IMPORTANT FIX
        ).execute()

        print("✅ Event created:", event.get('htmlLink'))

    except Exception as e:
        print("❌ Calendar Error:", str(e))
