from backend.app import db
from models.models import Activity

try:
    test_activity = Activity(name="Ping", difficulty=2, estimated_duration=15)
    db.session.add(test_activity)
    db.session.commit()
    print("DB connected and activity inserted.")
except Exception as e:
    print("DB connection failed:", e)
