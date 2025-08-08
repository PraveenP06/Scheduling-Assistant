from datetime import datetime, timedelta
from suggestion.slot_suggestion import suggest_slots_for_activity

def schedule_activity(activity, duration, importance, gaps, desired_start):
    # If user provided a desired time, try to use it directly
    if desired_start:
        start = desired_start
        end = start + timedelta(minutes=duration)
        for gap in gaps:
            g_start, g_end = gap["start"], gap["end"]
            if g_start <= start and end <= g_end:
                return [{
                    "start": start.isoformat(),
                    "end": end.isoformat(),
                    "status": "scheduled at user-specified time",
                    "score": None
                }]

        return [{"status": "desired time not available"}]

    # AI fallback: search gaps for best-fit slot
    suggestions = suggest_slots_for_activity(
        gaps=gaps,
        activity_name=activity,
        duration_minutes=duration,
        importance_rank=importance,
        max_suggestions=3
    )

    results = []
    for slot in suggestions:
        start = datetime.fromisoformat(slot["start"])
        end = start + timedelta(minutes=duration)
        status = "suggested by AI (preferred time)" if slot["score"] >= importance + 10 else "suggested by AI (fallback time)"
        results.append({
            "start": start.isoformat(),
            "end": end.isoformat(),
            "status": status,
            "score": slot["score"]
        })

    return results if results else [{"status": "no suitable slot found"}]
