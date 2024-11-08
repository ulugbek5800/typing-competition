from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token
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
    return jsonify({
        "message": "Signup successfull",
        "username": username,
        "access_token": access_token
    }), 201

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
        return jsonify({
            "message": "Login successful", 
            "username": username, 
            "access_token": access_token, 
        }), 200
    else:
        return jsonify({"error": "Invalid username or password"}), 401

""" # add /api/users route to get all info of users (make accessible only to admin)
@auth_bp.route('/api/test-users')
def test_users():
    users = User.query.all()
    return jsonify([{"id": user.id, "username": user.username} for user in users])
"""