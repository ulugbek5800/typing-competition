from flask import Blueprint, jsonify
from models import User

leaderboard_bp = Blueprint('leaderboard', __name__)

@leaderboard_bp.route('/api/leaderboard', methods=['GET'])
def leaderboard():
    top_players = User.query.order_by(User.highest_wpm.desc()).all()
    # top_players is a list of User objects, with all attributes from the model
    # [ User(id=5, username="David", password="qwerty", highest_wpm="140", created_at=datetime), ... ]

    leaderboard = list()    # leaderboard is a list of dictionaries
    for player in top_players:
        d = {"username": player.username, "highest_wpm": player.highest_wpm}
        leaderboard.append(d)

    return jsonify({"leaderboard": leaderboard}), 200