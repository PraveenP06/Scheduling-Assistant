from auth import get_google_credentials
from datetime import datetime
from calendar_utils.calendar_test import detect_gaps_between_events
from suggestion.scheduler import schedule_activity
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from dateutil.parser import parse
import pytz

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def fetch_calendar_events():
    creds = get_google_credentials()
    service = build('calendar', 'v3', credentials=creds)

    now = datetime.utcnow().isoformat() + 'Z'
    events_result = service.events().list(
        calendarId='primary',
        timeMin=now,
        maxResults=10,
        singleEvents=True,
        orderBy='startTime'
    ).execute()

    eastern = pytz.timezone("US/Eastern")
    items = events_result.get('items', [])
    parsed = []

    for event in items:
        raw_start = event['start'].get('dateTime', event['start'].get('date'))
        raw_end = event['end'].get('dateTime', event['end'].get('date'))
        start = parse(raw_start).astimezone(eastern)
        end = parse(raw_end).astimezone(eastern)
        parsed.append({'start': start, 'end': end})

    return parsed

def main():
    eastern = pytz.timezone("US/Eastern")
    today = eastern.localize(datetime.now().replace(hour=0, minute=0, second=0, microsecond=0))
    day_start = today.replace(hour=8)
    day_end = today.replace(hour=22)

    # 📅 Step 1: Fetch events and detect gaps
    events = fetch_calendar_events()
    gaps = detect_gaps_between_events(events, day_start, day_end)

    # 🧠 Step 2: Collect user input
    activity = input("Activity name: ")
    duration = int(input("Duration (minutes): "))
    importance = int(input("Importance (1–10): "))
    desired_input = input("Start time (ISO) or leave blank: ").strip()

    # 🕒 Step 3: Normalize desired time with pytz
    desired = None
    if desired_input:
        parsed = parse(desired_input)
        desired = parsed.astimezone(eastern) if parsed.tzinfo else eastern.localize(parsed)

    # 🎯 Step 4: Schedule activity
    result = schedule_activity(activity, duration, importance, gaps, desired)
    print("\n📅 Scheduling Result:")
    if "start" in result and "end" in result:
        start_dt = parse(result["start"])
        end_dt = parse(result["end"])
        print(f"→ {start_dt.strftime('%b %d, %I:%M %p')} to {end_dt.strftime('%I:%M %p')} ({result['status']})")
    else:
        print(result["status"])


if __name__ == '__main__':
    main()
