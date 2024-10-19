from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import db, User, Score

# Initialize Flask app
app = Flask(__name__)

if __name__ == "__main__":
    app.run(debug=True)

# Configure the database for app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db.init_app(app)    # initializes Flask app (app) for use with extension (db, which is imported from models.py)

with app.app_context():
    db.create_all   # creates tables