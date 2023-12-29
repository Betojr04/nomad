from flask_sqlalchemy import SQLAlchemy
import hashlib
import datetime
from . import db

# USER DATA MODEL
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email_address = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(80), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    def set_password(self, password):
        self.password_hash = hashlib.sha256(password.encode()).hexdigest()
    
    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'email_address': self.email_address,
            'created_at': self.created_at
        }

