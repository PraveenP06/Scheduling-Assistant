from datetime import datetime, timedelta

def classify_activity_type(activity_name):
    name = activity_name.lower()

    if any(kw in name for kw in ["study", "read", "learn", "research", "write", "code", "program", "develop", "design",
                                 "analyze", "review", "plan", "organize", "brainstorm", "think", "reflect", "contemplate",
                                 "concentrate", "focus", "deep work", "focus time", "cognitive task", "mental task",
                                 "intellectual work", "knowledge work", "academic work", "scholarly work", "research task",
                                 "study session", "learning activity", "reading session", "writing task"]):
        return "focus"
    elif any(kw in name for kw in ["gym", "run", "exercise", "workout", "yoga", "walk", "hike", "swim", "cycle", "sport",
                                   "play", "train", "fitness", "physical", "activity", "stretch", "cardio", "strength",
                                   "aerobics", "dance", "martial arts", "pilates", "zumba", "kickboxing", "crossfit",
                                   "bootcamp", "sports", "team sport", "athletics", "exercise class", "workout session",
                                   "physical activity", "fitness class", "sports practice", "athletic training",
                                   "physical training", "exercise routine", "fitness routine", "sports training",
                                   "athletic workout", "physical exercise", "fitness training"]):
        return "physical"
    elif any(kw in name for kw in ["call", "meeting", "sync", "chat", "video", "conference", "hangout", "catch-up",
                                   "network", "connect", "discuss", "talk"]):
        return "social"
    elif any(kw in name for kw in ["hangout", "coffee", "lunch", "dinner", "meal", "snack", "break", "relax", "chill",
                                   "unwind", "leisure", "casual", "free time", "downtime", "rest", "recreation", "fun",
                                   "enjoyment", "entertainment"]):
        return "casual"
    else:
        return "generic"

user_time_preferences = {
    "focus": [(9, 11), (20, 22)],
    "physical": [(6, 8), (17, 19)],
    "social": [(12, 14), (18, 21)],
    "casual": [(11, 13), (17, 20)],
    "generic": [(10, 16)]
}

def is_within_preferred(hour, preferred_ranges):
    return any(start_hr <= hour < end_hr for start_hr, end_hr in preferred_ranges)

def find_preferred_subslots(start, end, duration_minutes, preferred_ranges):
    candidate_starts = []
    current = start

    while current + timedelta(minutes=duration_minutes) <= end:
        if is_within_preferred(current.hour, preferred_ranges):
            candidate_starts.append(current)
        current += timedelta(minutes=15)

    return candidate_starts

def suggest_slots_for_activity(gaps, activity_name, duration_minutes, importance_rank, max_suggestions=3):
    activity_type = classify_activity_type(activity_name)
    preferred_ranges = user_time_preferences.get(activity_type, [])

    scored_slots = []

    def score_slot(slot_start, slot_end, label):
        gap_minutes = (slot_end - slot_start).total_seconds() / 60
        score = importance_rank + (gap_minutes / 10)
        score *= 1.5 if label == "preferred time" else 1.0
        return score

    # Pass 1: look inside gaps for preferred subslots
    for gap in gaps:
        g_start = datetime.fromisoformat(gap['start']) if isinstance(gap['start'], str) else gap['start']
        g_end = datetime.fromisoformat(gap['end']) if isinstance(gap['end'], str) else gap['end']
        preferred_starts = find_preferred_subslots(g_start, g_end, duration_minutes, preferred_ranges)

        for start in preferred_starts:
            end = start + timedelta(minutes=duration_minutes)
            scored_slots.append({
                'start': start.isoformat(),
                'end': end.isoformat(),
                'score': score_slot(start, end, "preferred time"),
                'label': "preferred time"
            })

    # Pass 2: fallback—use start of entire gap
    if not scored_slots:
        for gap in gaps:
            g_start = datetime.fromisoformat(gap['start']) if isinstance(gap['start'], str) else gap['start']
            g_end = datetime.fromisoformat(gap['end']) if isinstance(gap['end'], str) else gap['end']
            gap_minutes = (g_end - g_start).total_seconds() / 60

            if gap_minutes >= duration_minutes:
                slot_end = g_start + timedelta(minutes=duration_minutes)
                scored_slots.append({
                    'start': g_start.isoformat(),
                    'end': slot_end.isoformat(),
                    'score': score_slot(g_start, slot_end, "fallback time"),
                    'label': "fallback time"
                })

    sorted_slots = sorted(scored_slots, key=lambda s: s['score'], reverse=True)
    return sorted_slots[:max_suggestions]
