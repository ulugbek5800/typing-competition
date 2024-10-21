from flask import Blueprint, jsonify, request, session
from app import db
from models import User

auth_bp = Blueprint('auth', __name__)

# in-memory session for simplicity
logged_in_users = {}

@auth_bp.route('api/signup', methods=["POST"])
def signup():
    data = request.get_json()
    username = data.get["username"]
    password = data.get["password"]

    if User.query.filter_by(username=username).first:
        return jsonify({"error": "Username already exists"}), 400
    
    new_user = User(username=username, password=password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "registration successfull"}), 201

@auth_bp.route('api/login', methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    user = User.query.filter_by(username=username, password=password)   # returns instance of User model, or none if not found
    if user:
        session['user_id'] = user.id        # stores user.id in sessions
        logged_in_users[username] = user.id # adds user to loggen-in list (dictionary format)
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"error": "invalid username or password"}), 401