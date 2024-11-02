from flask import Blueprint, jsonify, request, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
import os
from extensions import db
from models import User

profile_bp = Blueprint("profile", __name__)

# Checks allowed file types
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
def allowed_file(filename):         # example filename: "profile_picture.JPG"
    extension = filename.split('.')[-1].lower()
    return extension in ALLOWED_EXTENSIONS

MAX_FILE_SIZE = 2 * 1024 * 1024     # 2 MB

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
@jwt_required()
def upload_profile_picture():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        if file.content_length > MAX_FILE_SIZE:
            return jsonify({"error": "File size exceeds the maximum limit of 2 MB"}), 400

        # sanitize filename to make it secure on the server (prevent spaces and unsafe characters in filename)
        filename = secure_filename(f"{user_id}_{file.filename}")    # add id to prevent issue if 2 users upload a file with the same filename
        # construct the full path where the file will be saved
        filepath = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)    # example filepath: "static/profile_pictures/id_filename.jpg"

        # create the folder if it doesnt exist
        os.makedirs(current_app.config["UPLOAD_FOLDER"], exist_ok=True)

        # delete old picture if it exists
        if user.profile_picture:
            old_picture_path = user.profile_picture.lstrip("/") # removes leading '/' in the path
            if os.path.exists(old_picture_path):
                os.remove(old_picture_path)

        try:
            file.save(filepath)     # save the file to the filepath on the server
            
            # user.profile_picture = f"/{filepath}"   # relative path     # f"/{filepath.replace(os.path.sep, '/')}"
            relative_path = os.path.relpath(filepath, current_app.config["UPLOAD_FOLDER"])
            user.profile_picture = f"/{relative_path.replace(os.path.sep, '/')}"
            
            db.session.commit()
            return jsonify({
                "message": "Profile picture uploaded successfully", 
                "profile_picture": user.profile_picture
            }), 200
        except Exception as e:
            return jsonify({"error": f"Failed to save profile picture: {str(e)}"}), 500
    else:
        return jsonify({"error": "File type not allowed"}), 400

@profile_bp.route('/api/profile/delete-picture', methods=['DELETE'])
@jwt_required()
def delete_profile_picture():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    if user.profile_picture:
        picture_path = user.profile_picture.lstrip("/")
        if os.path.exists(picture_path):
            try:
                os.remove(picture_path)     # delete the picture from the storage
            except OSError as e:
                return jsonify({"error": f"Error deleting file: {str(e)}"}), 500
        # clear the url in the database
        user.profile_picture = None
        db.session.commit()
        return jsonify({"message": "Profile picture deleted succcessfully"}), 200
    else:
        return jsonify({"error": "No profile picture to delete"}), 400

# Fix get_jwt_identity in delete
# Add 2 mb limit for photo
# Change home response