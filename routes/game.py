from flask import Blueprint, jsonify, request, session
from models import db, User, Score
import json
import random

game_bp = Blueprint('game', __name__)

@game_bp.route('api/submit-score', methods=['POST'])
def submit_score():
    # add game mode: normal, hard (in JSON and database, and make logic to save)
    # handle 2 leaderboards for 2 modes
    # connect backend and frontend, deploy and check (it should be complete working project)

    data = request.get_json()
    wpm = data.get('wpm')
    mode = data.get('mode') # "normal" or "hard"

    if mode not in ["normal", "hard"]:
        return jsonify({"error": "Invalid game mode"}), 400

    if 'user_id' in session:    # if session was saved in /login route (line 33 in auth.py)
        user_id = session['user_id']
        user = User.query.get(user_id)

        new_score = Score(user_id=user.id, wpm=wpm, mode=mode) # user_id=user.id -> assigning id from User table to user_id (FK) in Score table
        db.session.add(new_score)

        if mode == "normal" and user.highest_wpm_normal < wpm:
            user.highest_wpm_normal = wpm
            is_new_highest = True
        elif mode == "hard" and user.highest_wpm_normal < wpm:
            user.highest_wpm_normal = wpm
            is_new_highest = True
        else:
            is_new_highest = False

        db.session.commit()
        return jsonify({"message": "Score submitted", "is_new_highest": is_new_highest}), 201
    else:
        return jsonify({"message": "Score not saved (guest)", "wpm": wpm, "mode": mode}), 200