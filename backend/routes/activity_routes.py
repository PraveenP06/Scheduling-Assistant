from flask import Blueprint, request, jsonify
from models.activity_models import Activity
from extensions import db

activity_bp = Blueprint('activity_bp', __name__)

@activity_bp.route('/add-activity', methods=['POST'])
def add_activity():
    data = request.json
    
    # Optional fallback handling
    name = data.get('name')
    difficulty = data.get('difficulty', 'medium')  # default if not provided
    estimated_duration = data.get('estimated_duration', 30)  # default if not provided

    # Basic validation
    if not name:
        return jsonify({'error': 'Missing required field: name'}), 400

    activity = Activity(
        name=name,
        difficulty=difficulty,
        estimated_duration=estimated_duration
    )

    db.session.add(activity)
    db.session.commit()
    print("Route hit!")  # Confirm server received request
    return jsonify({'message': 'Activity saved!'}), 201

@activity_bp.route('/ping', methods=['GET'])
def ping():
    print("🟢 Ping route hit!")
    return jsonify({'message': 'pong'}), 200
