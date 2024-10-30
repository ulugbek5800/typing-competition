from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models import User

profile_bp = Blueprint("profile", __name__)

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
        "created_at": user.created_at
    }

    return jsonify({"profile": user_data}), 200

# Further updates plan:
# 1. add profile picture logic (new /apis). move new apis and /profile to routes/profile.py
# 2. check frontend-backend interaction. change home route response, based on changes and restructuring you made

# Other ideas
# 1. add 'name' field to User model, support name in singup/login, add /profile/edit?
# 2. add /api/users route to get all info of users (accessible only to admin)