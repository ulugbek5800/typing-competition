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
            "welcome_message": "Welcome to the Typing Competition API!",
            "features": [
                {
                    "title": "User Authentication",
                    "description": "Secure signup and login for a personalized experience."
                },
                {
                    "title": "Gameplay",
                    "description": "Test your typing speed in 'normal' and 'hard' modes and submit scores to compete."
                },
                {
                    "title": "Leaderboards",
                    "description": "See how you rank against others in both gameplay modes."
                },
                {
                    "title": "Profile Customization",
                    "description": "Upload and manage your profile picture to personalize your account."
                }
            ],
            "authentication": {
            "method": "JWT-based",
            "description": "Use JSON Web Tokens for secure authentication across endpoints.",
            "note": "Ensure to include your access token in requests to access protected routes."
            },
            "endpoints": {
                "User Registration": {
                    "endpoint": "/api/signup",
                    "method": "POST",
                    "description": "Create a new account with a username and password."
                },
                "User Login": {
                    "endpoint": "/api/login",
                    "method": "POST",
                    "description": "Login to your account and receive an access token for secure session management."
                },
                "User Profile": {
                    "endpoint": "/api/profile",
                    "method": "GET",
                    "authentication": "required",
                    "description": "View your profile details, including your top scores and profile picture."
                },
                "Upload Profile Picture": {
                    "endpoint": "/api/profile/upload-picture",
                    "method": "POST",
                    "authentication": "required",
                    "description": "Upload a new profile picture. Supported formats: PNG, JPG, JPEG."
                },
                "Delete Profile Picture": {
                    "endpoint": "/api/profile/delete-picture",
                    "method": "DELETE",
                    "authentication": "required",
                    "description": "Delete your current profile picture from your account."
                },
                "Submit Score": {
                    "endpoint": "/api/submit-score",
                    "method": "POST",
                    "description": "Submit your typing test score and compete for a place on the leaderboard."
                },
                "View Leaderboard": {
                    "endpoint": "/api/leaderboard",
                    "method": "GET",
                    "query_parameters": {
                        "mode": "normal or hard"
                    },
                    "description": "Retrieve the leaderboard to see top scores in each difficulty level."
                }
            },
            "support": {
                "contact": "support@typing-competition.com",
                "documentation": "For full documentation, visit our GitHub repository."
            }
        }
        return jsonify(info), 200       

    with app.app_context():
            db.create_all()

    return app

if __name__ == "__main__":
    app = create_app()
    app.run()