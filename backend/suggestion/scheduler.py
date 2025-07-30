from datetime import datetime, timedelta
from suggestion.slot_suggestion import suggest_slots_for_activity
from datetime import timedelta

def schedule_activity(activity, duration, importance, gaps, desired_start):
    # If user provided a desired time, try to use it directly
    if desired_start:
        start = desired_start
        end = start + timedelta(minutes=duration)
        for gap in gaps:
            g_start, g_end = gap["start"], gap["end"]
            if g_start <= start and end <= g_end:
                return {
                    "start": start.isoformat(),
                    "end": end.isoformat(),
                    "status": "scheduled at user-specified time"
                }
        return {"status": "desired time not available"}

    # AI fallback: search gaps for best-fit slot
    for gap in gaps:
        g_start, g_end = gap["start"], gap["end"]
        slot_duration = (g_end - g_start).total_seconds() / 60
        if slot_duration >= duration:
            start = g_start
            end = start + timedelta(minutes=duration)
            return {
                "start": start.isoformat(),
                "end": end.isoformat(),
                "status": "suggested by AI"
            }

    return {"status": "no suitable slot found"}

