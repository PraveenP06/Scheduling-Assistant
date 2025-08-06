from datetime import datetime, timedelta

def classify_activity_type(activity_name):
    name = activity_name.lower()

<<<<<<< HEAD
    if "study" in name or "read" in name or "learn" in name or "write" in name or "code" in name or "project" in name or "research" in name or "focus" in name or "concentrate" in name or "deep work" in name or "brainstorm" in name or "think" in name or "analyze" in name or "design" in name or "develop" in name or "create" in name or "build" in name or "plan" in name or "organize" in name or "strategize" in name or "review" in name or "reflect" in name or "contemplate" in name or "ponder" in name or "consider" in name or "evaluate" in name or "assess" in name or "synthesize" in name or "integrate" in name :
        return "focus"
    elif "gym" in name or "run" in name or "exercise" in name or "workout" in name or "yoga" in name or "stretch" in name or "walk" in name or "hike" in name or "cycle" in name or "swim" in name or "sports" in name or "play" in name or "physical activity" in name or "tennis" in name or "basketball" in name or "soccer" in name or "football" in name or "dance" in name or "martial arts" in name or "aerobics" in name or "pilates" in name or "cardio" in name or "strength training" in name or "fitness" in name or "pickleball" in name or "badminton" in name or "volleyball" in name or "golf" in name or "climbing" in name or "skiing" in name or "snowboarding" in name :
        return "physical"
    elif "call" in name or "meeting" in name or "sync" in name or "chat" in name or "video" in name or "conference" in name or "discussion" in name or "talk" in name or "connect" in name or "network" in name or "collaborate" in name or "team up" in name or "brainstorm" in name or "share ideas" in name or "exchange thoughts" in name or "group work" in name or "co-work" in name or "partner up" in name or "joint effort" in name or "co-create" in name or "co-design" in name or "co-develop" in name or "co-produce" in name or "co-innovate" in name or "co-strategize" in name or "co-plan" in name or "co-organize" in name or "co-ordinate" in name :
        return "social"
    elif "hangout" in name or "coffee" in name or "lunch" in name or "dinner" in name or "relax" in name or "chill" in name or "unwind" in name or "leisure" in name or "casual" in name or "free time" in name or "me time" in name or "self-care" in name or "pamper" in name or "treat myself" in name or "enjoy" in name or "have fun" in name or "play games" in name or "watch movie" in name or "listen to music" in name or "read book" in name or "browse internet" in name or "scroll social media" in name  or "catch up" in name or "relaxation" in name or "downtime" in name or "recreation" in name or "hobby" in name or "interest" in name or "passion" in name:
=======
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
>>>>>>> 851568e6ffab9c6944f787192159adae159362df
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
<<<<<<< HEAD
        # Handle both string and datetime input
        start = datetime.fromisoformat(gap['start']) if isinstance(gap['start'], str) else gap['start']
        end = datetime.fromisoformat(gap['end']) if isinstance(gap['end'], str) else gap['end']
        gap_minutes = (end - start).total_seconds() / 60

        if gap_minutes >= duration_minutes:
            score = 0

            # ⏰ Smarter time-of-day scoring
            slot_hour = start.hour
            end_hour = (start + timedelta(minutes=duration_minutes)).hour

            # Require full containment in preferred time range
            is_preferred = any(start_hr <= slot_hour < end_hr and start_hr <= end_hour <= end_hr
                   for start_hr, end_hr in preferred_ranges)

            score += 10 if is_preferred else -5  # discourage non-preferred times unless necessary


            # 🧱 Favor larger blocks
            score += gap_minutes / 10

            # 🎯 Boost score by importance
            score += importance_rank
=======
        g_start = datetime.fromisoformat(gap['start']) if isinstance(gap['start'], str) else gap['start']
        g_end = datetime.fromisoformat(gap['end']) if isinstance(gap['end'], str) else gap['end']
        preferred_starts = find_preferred_subslots(g_start, g_end, duration_minutes, preferred_ranges)
>>>>>>> 851568e6ffab9c6944f787192159adae159362df

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
