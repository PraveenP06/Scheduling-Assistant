from datetime import timedelta

def detect_gaps(events, min_duration_minutes=30, day_start=None, day_end=None, buffer_minutes=0):
    """
    Detects gaps between calendar events.
    
    Parameters:
        events: List of (start_time, end_time) tuples
        min_duration_minutes: Minimum gap duration to consider
        day_start: Start boundary for the day (datetime)
        day_end: End boundary for the day (datetime)
        buffer_minutes: Optional padding before/after events
    
    Returns:
        List of (gap_start, gap_end) tuples
    """
    # Sort events by start time
    sorted_events = sorted(events, key=lambda e: e[0])

    # Apply day boundaries
    if day_start:
        sorted_events = [(day_start, day_start)] + sorted_events
    if day_end:
        sorted_events.append((day_end, day_end))

    gaps = []
    for i in range(len(sorted_events) - 1):
        current_end = sorted_events[i][1] + timedelta(minutes=buffer_minutes)
        next_start = sorted_events[i + 1][0] - timedelta(minutes=buffer_minutes)

        gap_duration = (next_start - current_end).total_seconds() / 60
        if gap_duration >= min_duration_minutes:
            gaps.append((current_end, next_start))

    return gaps
