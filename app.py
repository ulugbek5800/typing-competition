from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from routes.game import game_bp
from routes.auth import auth_bp
from routes.leaderboard import leaderboard_bp

# Initialize Flask app
app = Flask(__name__)

# Configure the database for app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Security keys for auth_bp
app.config['SECRET_KEY'] = 'webster_hackathon'
app.config['JWT_SECRET_KEY'] = 'jwt_webster_hackathon'

db = SQLAlchemy(app)    # initializing the database
jwt = JWTManager(app)   # initializing jwt manager

# For deployment, enable cors for routes
CORS(app, origins=[])

# Register blueprints (routes)
app.register_blueprint(game_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(leaderboard_bp)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run()