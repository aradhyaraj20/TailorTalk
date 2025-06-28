from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime, timedelta
import pytz

# Setup service
SCOPES = ['https://www.googleapis.com/auth/calendar']
SERVICE_ACCOUNT_FILE = 'credentials.json'  # Ensure this file is in your folder

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('calendar', 'v3', credentials=credentials)

calendar_id = 'primary'

def check_and_book_slot(text):
    # Simple booking logic for tomorrow 3-5 PM
    now = datetime.utcnow()
    tomorrow = now + timedelta(days=1)
    start_time = tomorrow.replace(hour=15, minute=0, second=0).isoformat() + 'Z'
    end_time = tomorrow.replace(hour=17, minute=0, second=0).isoformat() + 'Z'

    events_result = service.events().list(
        calendarId=calendar_id,
        timeMin=start_time,
        timeMax=end_time,
        singleEvents=True,
        orderBy='startTime'
    ).execute()

    events = events_result.get('items', [])

    if not events:
        event = {
            'summary': 'TailorTalk Appointment',
            'start': {'dateTime': start_time},
            'end': {'dateTime': end_time},
        }
        service.events().insert(calendarId=calendar_id, body=event).execute()
        return "✅ Appointment booked from 3 PM to 5 PM tomorrow!"
    else:
        return "❌ You're busy during that time."
