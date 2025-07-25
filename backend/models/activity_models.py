from extensions import db

class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    difficulty = db.Column(db.Integer, nullable=False)
    estimated_duration = db.Column(db.Integer, nullable=False)
