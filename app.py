from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from routes.game import game_bp
from routes.auth import auth_bp
from routes.leaderboard import leaderboard_bp

# Initialize Flask app
app = Flask(__name__)

# Configure the database for app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLAlchemy_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)    # initializing the database

# Register blueprints (routes)
app.register_blueprint(game_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(leaderboard_bp)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)