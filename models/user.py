from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

from extensions import db

class User(db.Model):
    __tablename__ = 'usuaris'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, username, password, is_hashed=False):
        self.username = username
        if is_hashed:
            self.password_hash = password
        else:
            self.password_hash = generate_password_hash(password)

    def check_password(self, password_attempt):
        return check_password_hash(self.password_hash, password_attempt)

    @property
    def vist(self):
        return getattr(self, '_vist', False)
    
    @vist.setter
    def vist(self, value):
        self._vist = value

    def get_anotacions(self):
        return getattr(self, '_anotacions', "")

    def set_anotacions(self, text):
        self._anotacions = text

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

    def __str__(self):
        return f"User: {self.username} | Score: {self.total_score}"
from werkzeug.security import generate_password_hash, check_password_hash

class User:
    def __init__(self, username, password, total_score=0, is_hashed=False):
        self.username = username
        self.total_score = total_score

        if is_hashed:
            self.password = password
        else:
            self.password = generate_password_hash(password)

    def check_password(self, password_attempt):
        return check_password_hash(self.password, password_attempt)

    def add_score(self, points):
        self.total_score += points

    def to_dict(self):
        return {
            "username": self.username,
            "password": self.password,
            "total_score": self.total_score
        }

    def __str__(self):
        return f"User: {self.username}"