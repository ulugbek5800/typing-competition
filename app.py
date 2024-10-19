from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Initialize Flask app
app = Flask(__name__)

if __name__ == "__main__":
    app.run(debug=True)

# Configure the database for app
app.config['SQLAlchemy_DATABASE_URI'] = 'sqlite:///database.db'
