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
            "status": "Operational",
            "message": "API is running on the server",
            "description": "Welcome to the Typing Competition API.",
            "features": [
                "User Authentication: Register and manage your account.",
                "Gameplay: Test your typing speed and submit your scores to compete with others.",
                "Leaderboard: View rankings based on performance in different modes."
            ],
            "available_endpoints": [
                "/api/signup - Register a new account.",
                "/api/login - Log in to your account.",
                "/api/profile - Retrieve user information (requires authentication).",
                "/api/submit-score - Submit your typing score after a game (guest and registered users).",
                "/api/leaderboard?mode=normal - View leaderboard in normal mode.",
                "/api/leaderboard?mode=hard - View leaderboard in hard mode."
            ]
        }
        return jsonify(info), 200        

    with app.app_context():
            db.create_all()

    return app

if __name__ == "__main__":
    app = create_app()
    app.run()