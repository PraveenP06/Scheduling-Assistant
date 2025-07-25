from flask import Blueprint, request, jsonify
from models.activity_models import Activity
from extensions import db

activity_bp = Blueprint('activity_bp', __name__)

@activity_bp.route('/add-activity', methods=['POST'])
def add_activity():
    data = request.json
    activity = Activity(
        name=data['name'],
        difficulty=data['difficulty'],
        estimated_duration=data['estimated_duration']
    )
    db.session.add(activity)
    db.session.commit()
    print("Route hit!")  # Confirm server received request
    return jsonify({'message': 'Activity saved!'}), 201

@activity_bp.route('/ping', methods=['GET'])
def ping():
    print("🟢 Ping route hit!")
    return jsonify({'message': 'pong'}), 200
