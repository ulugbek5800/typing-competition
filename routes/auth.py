from flask import Blueprint, jsonify, request, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token, get_jwt_identity
)
from app import db
from models import User

auth_bp = Blueprint('auth', __name__)
jwt = JWTManager()

@auth_bp.route('api/signup', methods=["POST"])
def signup():
    data = request.get_json()
    username = data.get["username"]
    password = data.get["password"]

    if User.query.filter_by(username=username).first:
        return jsonify({"error": "Username already exists"}), 400

    hashed_password = generate_password_hash(password)    

    new_user = User(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    access_token = create_access_token(identity=new_user.id)
    return jsonify({"message": "Registration successfull", "access_token": access_token}), 201

@auth_bp.route('api/login', methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    user = User.query.filter_by(username=username)   # returns instance of User model, or none if not found
    if user and check_password_hash(user.password, password):
        access_token = create_access_token(identity=user.id)
        return jsonify({"message": "Login successful", "access_token": access_token}), 200
    else:
        return jsonify({"error": "Invalid username or password"}), 401

@auth_bp.route('api/logout')
@jwt_required()
def logout():
    return jsonify({"message": 'Logged out successfully'})