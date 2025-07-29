from datetime import timedelta

def detect_gaps_between_events(events, day_start, day_end, min_duration_minutes=30, buffer_minutes=0):
    """
    Detects gaps between calendar events within a specific time window.
    
    Parameters:
        events: List of dicts with 'start' and 'end' datetime values
        day_start: datetime marking start of scheduling window
        day_end: datetime marking end of scheduling window
        min_duration_minutes: Minimum duration for a gap to be included
        buffer_minutes: Time to pad before/after each event
    
    Returns:
        List of dicts with 'start' and 'end' keys for free time slots
    """
    # Sort events by start time
    sorted_events = sorted(events, key=lambda e: e['start'])

    # Add artificial boundaries to cover full day range
    event_blocks = [{'start': day_start, 'end': day_start}] + sorted_events + [{'start': day_end, 'end': day_end}]

    gaps = []
    for i in range(len(event_blocks) - 1):
        current_end = event_blocks[i]['end'] + timedelta(minutes=buffer_minutes)
        next_start = event_blocks[i + 1]['start'] - timedelta(minutes=buffer_minutes)

        gap_duration = (next_start - current_end).total_seconds() / 60
        if gap_duration >= min_duration_minutes:
            gaps.append({
                'start': current_end,
                'end': next_start
            })

    return gaps
