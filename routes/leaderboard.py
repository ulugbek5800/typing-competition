from flask import Blueprint, jsonify, request
from models import User

leaderboard_bp = Blueprint('leaderboard', __name__)

@leaderboard_bp.route('/api/leaderboard', methods=['GET'])
def leaderboard():
    mode = request.args.get('mode')
    if mode not in ["normal", "hard"]:
        return jsonify({"message": "Invalid game mode"}), 400

    if mode == "normal":
        top_players = User.query.order_by(User.highest_wpm_normal.desc()).filter(User.highest_wpm_normal > 0).all()
        # top_players is a list of User objects, with all attributes from the model
        # [ User(id=5, username="David", password="qwerty", highest_wpm_normal="140", created_at=datetime), ... ]
        leaderboard = [{"username": player.username, "highest_wpm": player.highest_wpm_normal} for player in top_players]
        # leaderboard is a list of dictionaries
    elif mode == "hard":
        top_players = User.query.order_by(User.highest_wpm_hard.desc()).filter(User.highest_wpm_hard > 0).all()
        leaderboard = [{"username": player.username, "highest_wpm": player.highest_wpm_hard} for player in top_players]

    if not leaderboard:
        return jsonify({"leaderboard": [], "mode": mode, "message": "No scores available"}), 200

    return jsonify({"leaderboard": leaderboard, "mode": mode}), 200