from datetime import datetime

# 🔍 NLP-style activity classifier
def classify_activity_type(activity_name):
    name = activity_name.lower()

    if "study" in name or "read" in name or "learn" in name:
        return "focus"
    elif "gym" in name or "run" in name or "exercise" in name:
        return "physical"
    elif "call" in name or "meeting" in name or "sync" in name:
        return "social"
    elif "hangout" in name or "coffee" in name or "lunch" in name:
        return "casual"
    else:
        return "generic"

# 🧠 Behavioral preference map (can be dynamic later)
user_time_preferences = {
    "focus": [(9, 11), (20, 22)],
    "physical": [(6, 8), (17, 19)],
    "social": [(12, 14), (18, 21)],
    "casual": [(11, 13), (17, 20)],
    "generic": [(10, 16)]
}

# 💡 Main suggestion function
def suggest_slots_for_activity(gaps, activity_name, duration_minutes, importance_rank, max_suggestions=3):
    """
    Suggest optimal slots for an activity based on behavior, time, and priority.

    Parameters:
        gaps: List of {'start': datetime or ISO str, 'end': datetime or ISO str}
        activity_name: Description of the task
        duration_minutes: Approximate time needed
        importance_rank: 1–10 priority level
        max_suggestions: How many slots to return

    Returns:
        List of {'start': ISO string, 'end': ISO string, 'score': float}
    """
    activity_type = classify_activity_type(activity_name)
    preferred_ranges = user_time_preferences.get(activity_type, [])

    scored_slots = []

    for gap in gaps:
        # Handle both string and datetime input
        start = datetime.fromisoformat(gap['start']) if isinstance(gap['start'], str) else gap['start']
        end = datetime.fromisoformat(gap['end']) if isinstance(gap['end'], str) else gap['end']
        gap_minutes = (end - start).total_seconds() / 60

        if gap_minutes >= duration_minutes:
            score = 0

            # ⏰ Time-of-day preference boost
            for start_hr, end_hr in preferred_ranges:
                if start_hr <= start.hour < end_hr:
                    score += 10

            # 🧱 Favor larger blocks
            score += gap_minutes / 10

            # 🎯 Boost score by importance
            score += importance_rank

            scored_slots.append({
                'start': start.isoformat(),
                'end': end.isoformat(),
                'score': score
            })

    sorted_slots = sorted(scored_slots, key=lambda s: s['score'], reverse=True)
    return sorted_slots[:max_suggestions]
