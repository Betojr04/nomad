"""
This module initializes the Flask application, sets up database configurations,
and registers the application routes.
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config, TestingConfig
from flask_cors import CORS
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
import os

db = SQLAlchemy()

"""
    Create and configure an instance of the Flask application.

    Initializes the database and migrations using Flask-SQLAlchemy and Flask-Migrate.
    Registers the 'auth' Blueprint for handling user related routes.

    Returns:
        app: The Flask application instance.
    """
def create_app():    
    app = Flask(__name__)
    env = os.getenv('FLASK_ENV')

    if env == 'development':
        # Development configuration
        app.config.from_object(Config)
    elif env == 'testing':
        # Testing configuration
        app.config.from_object(TestingConfig)
    else:
        # Default to production configuration
        app.config.from_object(Config)
    
    CORS(app) 

    db.init_app(app)
    Migrate(app, db)
    
    jwt=JWTManager(app)

    # Import routes and models
    from .models import User  
    from .auth import auth  
    from .itineraryRoutes import itinerary
    from .socialRoutes import social

    # Register the api Blueprint with the app
    app.register_blueprint(auth)
    app.register_blueprint(itinerary)
    app.register_blueprint(social)
    
    return app

