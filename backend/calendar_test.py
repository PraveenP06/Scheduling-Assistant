from __future__ import print_function
from auth import get_google_credentials
from googleapiclient.discovery import build
from dateutil.parser import parse
from datetime import datetime, timedelta
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
    return dt.strftime("%b %d, %I:%M %p").lstrip("0")

def main():
    creds = get_google_credentials()
    service = build('calendar', 'v3', credentials=creds)

    tz = pytz.timezone('America/New_York')  # handles daylight saving automatically
    now = datetime.now(tz)
    time_min = now.replace(microsecond=0).isoformat()
    time_max = (now + timedelta(days=3)).replace(microsecond=0).isoformat() 


    print(f'📅 Fetching calendar events between {format_dt(now)} and {format_dt(now + timedelta(days=3))}...')
    events_result = service.events().list(
        calendarId='primary',
        timeMin=time_min,
        timeMax=time_max,
        singleEvents=True,
        orderBy='startTime'
    ).execute()

    events = events_result.get('items', [])
    if not events:
        print('No upcoming events found.')
        return

    parsed_events = []
    for event in events:
        raw_start = event['start'].get('dateTime', event['start'].get('date'))
        raw_end = event['end'].get('dateTime', event['end'].get('date'))
        start = parse(raw_start)
        end = parse(raw_end)
        parsed_events.append({'start': start, 'end': end})

    print("\n📆 Upcoming Events:")
    for event in parsed_events:
        print(f"- {format_dt(event['start'])} → {format_dt(event['end'])}")

    print("\n🕳️ Available Time Slots:")
    for i in range(3):
        day = now + timedelta(days=i)
        day_start = day.replace(hour=8, minute=0, second=0, microsecond=0)
        day_end = day.replace(hour=22, minute=0, second=0, microsecond=0)

        events_for_day = [e for e in parsed_events if day.date() == e['start'].date()]
        gaps = detect_gaps_between_events(events_for_day, day_start, day_end)

        print(f"\n📅 {day.strftime('%A, %b %d')}")
        if gaps:
            for gap in gaps:
                print(f"→ {format_dt(gap['start'])} to {format_dt(gap['end'])}")
        else:
            print("No gaps available.")

if __name__ == '__main__':
    main()
