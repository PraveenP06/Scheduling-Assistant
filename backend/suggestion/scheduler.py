from datetime import datetime, timedelta
from suggestion.slot_suggestion import suggest_slots_for_activity, classify_activity_type, user_time_preferences

def schedule_activity(activity, duration, importance, gaps, desired_start=None):
    now = datetime.now(tz=gaps[0]["start"].tzinfo)
    activity_type = classify_activity_type(activity)
    preferred_ranges = user_time_preferences.get(activity_type, [])

    if desired_start:
        start = desired_start
        end = start + timedelta(minutes=duration)
        for gap in gaps:
            g_start, g_end = gap["start"], gap["end"]
            if g_start <= start and end <= g_end and start >= now:
                return {
                    "start": start.strftime("%b %d, %I:%M %p"),
                    "end": end.strftime("%b %d, %I:%M %p"),
                    "status": "scheduled at user-specified time"
                }
        return {"status": "desired time not available"}

    # 🧠 Use AI suggestions
    suggestions = suggest_slots_for_activity(
        gaps=gaps,
        activity_name=activity,
        duration_minutes=duration,
        importance_rank=importance,
        max_suggestions=5
    )

    for slot in suggestions:
        slot_start = datetime.fromisoformat(slot['start'])
        if slot_start < now:
            continue

        # Prefer preferred hours
        in_preferred = any(start_hr <= slot_start.hour < end_hr for start_hr, end_hr in preferred_ranges)
        slot_end = slot_start + timedelta(minutes=duration)

        return {
            "start": slot_start.strftime("%b %d, %I:%M %p"),
            "end": slot_end.strftime("%b %d, %I:%M %p"),
            "status": "suggested by AI" + (" (preferred time)" if in_preferred else " (fallback time)")
        }

    return {"status": "no suitable slot found"}
