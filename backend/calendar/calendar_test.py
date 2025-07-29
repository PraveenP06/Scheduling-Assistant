from __future__ import print_function
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

def main():
    flow = InstalledAppFlow.from_client_secrets_file(
        'scheduler_credentials.json', SCOPES)
    creds = flow.run_local_server(port=0)

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
    for event in events:
        raw_start = event['start'].get('dateTime', event['start'].get('date'))
        raw_end = event['end'].get('dateTime', event['end'].get('date'))
        start = parse(raw_start).astimezone(eastern)
        end = parse(raw_end).astimezone(eastern)
        parsed_events.append({'start': start, 'end': end})
        print(f"- {event['summary']}: {start.isoformat()} → {end.isoformat()}")

    # Define bounds with timezone-aware EDT
    day_start = eastern.localize(datetime.now().replace(hour=8, minute=0, second=0, microsecond=0))
    day_end = eastern.localize(datetime.now().replace(hour=22, minute=0, second=0, microsecond=0))

    # Detect gaps
    gaps = detect_gaps_between_events(parsed_events, day_start, day_end)

    print("\n🕳️ Available Time Slots:")
    for gap in gaps:
        print(f"→ {gap['start'].strftime('%Y-%m-%d %I:%M %p')} to {gap['end'].strftime('%Y-%m-%d %I:%M %p')}")

if __name__ == '__main__':
    main()
