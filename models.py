from extensions import db
from datetime import datetime

# User information
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    highest_wpm_normal = db.Column(db.Integer, default=0)
    highest_wpm_hard = db.Column(db.Integer, default=0)
    profile_picture = db.Column(db.String(256), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:              # returns a string every time a new element is created
        return f"User {self.username}"

# Game session
class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)   # user.id refers to 'id' in the User model
    wpm = db.Column(db.Integer, nullable=False)
    mode = db.Column(db.String(16), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"Score {self.wpm} by User {self.user_id}"