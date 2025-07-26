from extensions import db
from datetime import timedelta

class Activity(db.Model):
    __tablename__ = 'activity'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    difficulty = db.Column(db.Integer)
    estimated_duration = db.Column(db.Integer)  # In minutes
    start_time = db.Column(db.DateTime, nullable=False)

    # Computed property for end time
    @property
    def end_time(self):
        if self.start_time and self.estimated_duration:
            return self.start_time + timedelta(minutes=self.estimated_duration)
        return None
