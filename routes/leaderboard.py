from flask import Blueprint, jsonify, request
from models import User

leaderboard_bp = Blueprint('leaderboard', __name__)

@leaderboard_bp.route('/api/leaderboard', methods=['GET'])
def leaderboard():
    data = request.get_json()
    if data is None or 'mode' not in data:
        return jsonify({"error": "Game mode is required"}), 400

    mode = data.get('mode')
    if mode not in ["normal", "hard"]:
        return jsonify({"message": "Invalid game mode"}), 400

    if mode == "normal":
        top_players = User.query.order_by(User.highest_wpm_normal.desc()).filter(User.highest_wpm_normal > 0).all()
        # top_players is a list of User objects, with all attributes from the model
        # [ User(id=5, username="David", password="qwerty", highest_wpm_normal="140", created_at=datetime), ... ]
        leaderboard = list()
        for player in top_players:
            leaderboard.append({"username": player.username, "highest_wpm": player.highest_wpm_normal})
        # leaderboard is a list of dictionaries
    elif mode == "hard":
        top_players = User.query.order_by(User.highest_wpm_hard.desc()).filter(User.highest_wpm_hard > 0).all()
        leaderboard = [{"username": player.username, "highest_wpm": player.highest_wpm_hard} for player in top_players]

    return jsonify({"leaderboard": leaderboard, "mode": mode}), 200