"""
This module contains the configuration settings for the Flask application.

It defines settings for the SQLAlchemy database, including the URI and track modifications setting.
It also sets the secret key for JWT (JSON Web Token) authentication.
"""

class Config:
    """
    Configuration class for the Flask application.

    Attributes:
        SQLALCHEMY_DATABASE_URI (str): Database connection URI.
        SQLALCHEMY_TRACK_MODIFICATIONS (bool): Flag to track modifications of objects and emit signals.
        JWT_SECRET_KEY (str): Secret key used for JWT authentication.
    """
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'Echelon'
