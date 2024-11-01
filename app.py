from flask import Flask, jsonify
from flask_cors import CORS

from extensions import db, jwt, migrate
from routes.game import game_bp
from routes.auth import auth_bp
from routes.leaderboard import leaderboard_bp
from routes.profile import profile_bp

def create_app():
    app = Flask(__name__)   # initializing Flask app

    # Configure the database for app
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'   # relative path, original
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Security keys for auth_bp
    app.config['SECRET_KEY'] = 'webster_hackathon'
    app.config['JWT_SECRET_KEY'] = 'jwt_webster_hackathon'

    # Configuration for profile_picture folder
    app.config["UPLOAD_FOLDER"] = "static/profile_pictures"

    # Plugins (app)
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    CORS(app, origins=['*'])   # enabling cors for routes   # https://type-com.vercel.app/

    # Register blueprints (routes)
    app.register_blueprint(game_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(leaderboard_bp)
    app.register_blueprint(profile_bp)

    @app.route('/', methods=['GET'])
    def home():
        info = {
            "status": "API is Live",
            "welcome_message": "Welcome to the WebsterType API! Test your typing speed and compete with others.",
            "features": [
                "User Authentication: Register and log in securely.",
                "Gameplay: Compete in 'normal' and 'hard' typing modes.",
                "Leaderboards: View top scores in each difficulty.",
                "Profile Customization: Upload and manage a profile picture."
            ],
            "authentication": "JWT-based authentication is required for most actions.",
            "endpoints": {
                "Signup": "POST /api/signup",
                "Login": "POST /api/login",
                "Profile": "GET /api/profile (auth required)",
                "Upload Profile Picture": "POST /api/profile/upload-picture (auth required)",
                "Delete Profile Picture": "DELETE /api/profile/delete-picture (auth required)",
                "Submit Score": "POST /api/submit-score",
                "Leaderboard": "GET /api/leaderboard?mode=normal/hard"
            },
            "note": "See GitHub for more details: https://github.com/ulugbek5800/typing-competition"
        }
        return jsonify(info), 200       

    with app.app_context():
            db.create_all()

    return app

if __name__ == "__main__":
    app = create_app()
    app.run()