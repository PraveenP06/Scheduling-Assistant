from flask import Blueprint, request, jsonify
from models.activity_models import Activity
from extensions import db
from datetime import datetime

activity_bp = Blueprint('activity_bp', __name__)

@activity_bp.route('/add-activity', methods=['POST'])
def add_activity():
    data = request.json

    name = data.get('name')
    difficulty = data.get('difficulty', 2)
    estimated_duration = data.get('estimated_duration', 30)
    start_time_raw = data.get('start_time')

    # Validation
    if not name or not start_time_raw:
        return jsonify({'error': 'Missing required field: name or start_time'}), 400

    try:
        start_time = datetime.fromisoformat(start_time_raw)
    except ValueError:
        return jsonify({
            'error': 'start_time must be in ISO format (YYYY-MM-DDTHH:MM:SS)'
        }), 400

    activity = Activity(
        name=name,
        difficulty=difficulty,
        estimated_duration=estimated_duration,
        start_time=start_time
    )

    db.session.add(activity)
    db.session.commit()
    print("Route hit!")
    return jsonify({'message': 'Activity with start_time saved!'}), 201


@activity_bp.route('/ping', methods=['GET'])
def ping():
    print("🟢 Ping route hit!")
    return jsonify({'message': 'pong'}), 200
