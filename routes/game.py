from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, User, Score

game_bp = Blueprint('game', __name__)

@game_bp.route('/api/submit-score', methods=['POST'])
@jwt_required(optional=True)
def submit_score():
    data = request.get_json()
    if data is None or 'wpm' not in data or 'mode' not in data:
        return jsonify({"error": "WPM and mode are required"}), 400

    wpm = data.get('wpm')
    mode = data.get('mode') # "normal" or "hard"

    if mode not in ["normal", "hard"]:
        return jsonify({"error": "Invalid game mode"}), 400
    if not (isinstance(wpm, (int, float)) and wpm > 0):
        return jsonify({"error": "Invalid WPM value"}), 400

    user_id = get_jwt_identity()
    if user_id:     # if user is logged in
        user = User.query.get(user_id)
        is_new_highest = False
        new_score = Score(user_id=user.id, wpm=wpm, mode=mode) # user_id=user.id -> assigning id from User table to user_id (FK) in Score table

        if mode == "normal" and user.highest_wpm_normal < wpm:
            user.highest_wpm_normal = wpm
            is_new_highest = True
        elif mode == "hard" and user.highest_wpm_hard < wpm:
            user.highest_wpm_hard = wpm
            is_new_highest = True

        db.session.add(new_score)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": f"There was an error when submitting the score: {str(e)}"}), 500

        return jsonify({"message": "Score submitted", "is_new_highest": is_new_highest}), 201
    else:
        return jsonify({"message": "Score not saved (guest scores are not saved permanently)", "wpm": wpm, "mode": mode}), 200