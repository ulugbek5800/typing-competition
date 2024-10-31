from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
import os
from extensions import db
from models import User

profile_bp = Blueprint("profile", __name__)

# Configuration for profile_picture
UPLOAD_FOLDER = "static/profile_pictures"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    pass

@profile_bp.route('/api/profile')
@jwt_required()
def profile():
    user_id = get_jwt_identity()    # gets the id of the current user from JWT
    user = User.query.get(user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    user_data = {
        "id": user.id,
        "username": user.username,
        "highest_wpw_normal": user.highest_wpm_normal,
        "highest_wpm_hard": user.highest_wpm_hard,
        "created_at": user.created_at,
        "profile_picture": user.profile_picture
    }

    return jsonify({"profile": user_data}), 200

@profile_bp.route('/api/profile/upload-picture', methods=['POST'])
@jwt_required
def upload_profile_picture():
    pass

@profile_bp.route('/api/profile/delete-picture', methods=['DELETE'])
@jwt_required
def delete_profile_picture():
    pass

# Further updates plan:
# 1. add profile picture logic (/upload-picture, /delete-picture) to profile.py
# 2. change home route response, based on changes and restructuring you made
