from flask import Flask, jsonify
from extensions import db, jwt
from flask_cors import CORS
from routes.game import game_bp
from routes.auth import auth_bp
from routes.leaderboard import leaderboard_bp

def create_app():
    app = Flask(__name__)   # initializing Flask app

    # Configure the database for app
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/ulugbek5800/typing-competition/instance/database.db'   # absolete path, for deployment
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'   # relative path, original
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Security keys for auth_bp
    app.config['SECRET_KEY'] = 'webster_hackathon'
    app.config['JWT_SECRET_KEY'] = 'jwt_webster_hackathon'

    # Plugins (app)
    db.init_app(app)
    jwt.init_app(app)
    CORS(app, origins=['*'])   # enabling cors for routes

    # Register blueprints (routes)
    app.register_blueprint(game_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(leaderboard_bp)

    @app.route('/', methods=['GET'])
    def home():
        return jsonify({"message": "API is running!"}), 200

    with app.app_context():
            db.create_all()

    return app

if __name__ == "__main__":
    app = create_app()
    app.run()