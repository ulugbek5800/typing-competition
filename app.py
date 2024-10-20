from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Initialize Flask app
app = Flask(__name__)

# Configure the database for app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLAlchemy_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)    # initializing the database

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)