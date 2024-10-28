from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token, get_jwt_identity
)
from extensions import db
from models import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/api/signup', methods=["POST"])
def signup():
    data = request.get_json()
    if data is None or "username" not in data or "password" not in data:
        return jsonify({"error": "Username and password are required"}), 400

    username = data.get("username")
    password = data.get("password")

    if len(password) < 8:
        return jsonify({"error": "Password must contain at least 8 characters"}), 400
    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Username already exists"}), 400

    hashed_password = generate_password_hash(password)
    new_user = User(username=username, password=hashed_password)

    try:
        db.session.add(new_user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"There was an error adding a new user: {str(e)}"}), 500

    access_token = create_access_token(identity=new_user.id)
    return jsonify({"message": "Signup successfull", "username": username, "access_token": access_token}), 201

@auth_bp.route('/api/login', methods=["POST"])
def login():
    data = request.get_json()
    if data is None or "username" not in data or "password" not in data:
        return jsonify({"error": "Username and password are required"}), 400

    username = data.get("username")
    password = data.get("password")

    user = User.query.filter_by(username=username).first()   # returns instance of User model, or none if not found
    if user and check_password_hash(user.password, password):
        access_token = create_access_token(identity=user.id)
        return jsonify({"message": "Login successful", "username": username, "access_token": access_token}), 200
    else:
        return jsonify({"error": "Invalid username or password"}), 401

@auth_bp.route('/api/profile')
@jwt_required()
def profile():
    user_id = get_jwt_identity()    # gets the id of the current user from JWT
    user = User.query.get(user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    user_data = {
        "id": user.id,
        "username": user.username,
        "highest_wmp_normal": user.highest_wpm_normal,
        "highest_wpm_hard": user.highest_wpm_hard,
        "created_at": user.created_at
    }

    return jsonify({"profile": user_data}), 200

# Latest minor update:
# 1. Removed /api/logout route from auth.py
# 2. Added /api/profile route to auth.py
# 3. Included username in responses for /api/signup and /api/login

# Further updates plan:
# 1. add 'name' field to User model (nullable=True), support name in singup/login, add /profile/edit
# 2. add profile picture logic (new /api)
# 3. add /api/users route to get all info of users (accessible only to admin)