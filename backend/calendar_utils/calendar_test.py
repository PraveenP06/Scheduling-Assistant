from __future__ import print_function
from auth import get_google_credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from datetime import datetime, timedelta
from dateutil.parser import parse
import pytz

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def detect_gaps_between_events(events, day_start, day_end):
    events = sorted(events, key=lambda x: x['start'])
    gaps = []

    cursor = day_start
    for event in events:
        if event['start'] > cursor:
            gaps.append({'start': cursor, 'end': event['start']})
        cursor = max(cursor, event['end'])

    if cursor < day_end:
        gaps.append({'start': cursor, 'end': day_end})

    return gaps

def format_dt(dt):
    return dt.strftime("%b %d, %I:%M %p").lstrip("0")  # e.g., Jul 31, 1:30 PM

def main():
    creds = get_google_credentials()

    service = build('calendar', 'v3', credentials=creds)

    now = datetime.utcnow().isoformat() + 'Z'  # 'Z' means UTC
    print('📅 Fetching calendar events...')
    events_result = service.events().list(
        calendarId='primary', timeMin=now,
        maxResults=10, singleEvents=True,
        orderBy='startTime').execute()

    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
        return

    eastern = pytz.timezone("US/Eastern")

    parsed_events = []
    print("\n📆 Upcoming Events:")
    for event in events:
        raw_start = event['start'].get('dateTime', event['start'].get('date'))
        raw_end = event['end'].get('dateTime', event['end'].get('date'))
        start = parse(raw_start).astimezone(eastern)
        end = parse(raw_end).astimezone(eastern)
        parsed_events.append({'start': start, 'end': end})
        print(f"- {event.get('summary', '[No Title]')}: {format_dt(start)} → {format_dt(end)}")

    # Define bounds with timezone-aware EDT
    today = eastern.localize(datetime.now().replace(hour=0, minute=0, second=0, microsecond=0))
    day_start = today.replace(hour=8)
    day_end = today.replace(hour=22)

    # Detect gaps
    gaps = detect_gaps_between_events(parsed_events, day_start, day_end)

    print("\n🕳️ Available Time Slots:")
    for gap in gaps:
        print(f"→ {format_dt(gap['start'])} to {format_dt(gap['end'])}")

if __name__ == '__main__':
    main()
