"""
This module defines the data models for the Flask application using SQLAlchemy.

The primary model defined here is the User model, which represents a user in the database.
"""

from flask_sqlalchemy import SQLAlchemy
import hashlib
import datetime
from . import db

class User(db.Model):
    """
    User model, representing a user in the database.

    Attributes:
        id (int): Unique identifier for the user.
        username (str): Unique username for the user.
        email_address (str): Unique email address for the user.
        password_hash (str): Hashed password for the user.
        created_at (datetime): Timestamp indicating when the user was created.

    Methods:
        set_password(password): Sets the user's password.
        serialize(): Serializes the user object to a dictionary.
    """
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email_address = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(80), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    itinerary = db.relationship('Itinerary', backref='user', lazy=True)
    
    def __repr__(self):
        """
        Represent instance as a unique string.

        Returns:
            str: Representation of the user, including their username.
        """
        return f'<User {self.username}>'
    
    def set_password(self, password):
        """
        Set the password for the user by hashing it.

        Args:
            password (str): The plaintext password to hash and store.
        """
        self.password_hash = hashlib.sha256(password.encode()).hexdigest()
        
    def check_password(self, password):
        """
        Check if the provided password matches the stored hashed password.

        Args:
            password (str): The plaintext password to verify.

        Returns:
            bool: True if the password matches, False otherwise.
        """
        return self.password_hash == hashlib.sha256(password.encode()).hexdigest()
    
    def serialize(self):
        """
        Serialize the user object to a dictionary.

        Returns:
            dict: A dictionary representation of the user object.
        """
        return {
            'id': self.id,
            'username': self.username,
            'email_address': self.email_address,
            'created_at': self.created_at
        }
        
class Itinerary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    itinerary_name = db.Column(db.String(80), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    events = db.relationship('Event', backref='itinerary', lazy=True)
    locations = db.relationship('Location', backref='itinerary', lazy=True)
    
class Locations(db.Model):
    id = db.Column(db.Integer, primary_key=True)
