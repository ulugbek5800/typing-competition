from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Initialize Flask app
app = Flask(__name__)

if __name__ == "__main__":
    app.run(debug=True)