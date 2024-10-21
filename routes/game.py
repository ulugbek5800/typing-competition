from flask import Blueprint, jsonify, request, session
from models import db, User, Score
import json
import random

game_bp = Blueprint('game', __name__)

# Load words from json file
with open('english_5k.json') as file:
    word_data = json.load(file)
    words = word_data['words']  # takes list of words

@game_bp.route('/api/start-game', methods=['GET'])
def start_game():
    # return 250 random words joint into text
    random_text = " ".join(random.sample(words, 250))
    return jsonify({"text": random_text}), 200

@game_bp.route('api/submit-score', methods=['POST'])
def submit_score():
    data = request.get_json()
    wpm = data.get('wpm')

    if 'user_id' in session:    # if session was saved in /login route (line 33 in auth.py)
        user_id = session['user_id']
        user = User.query.get(user_id)
        new_score = Score(user_id=user.id, wpm=wpm) # user_id=user.id -> assigning id from User table to user_id (FK) in Score table
        db.session.add(new_score)
        if user.highest_wpm < wpm:
            user.highest_wpm = wpm
        db.session.commit()
        return jsonify({"message": "Score submitted", "new_highest_wpm": user.highest_wpm < wpm}), 201
    else:
        return jsonify({"message": "Score not saved (guest)", "wpm": wpm}), 200