"""
This module initializes the Flask application, sets up database configurations,
and registers the application routes.
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

db = SQLAlchemy()

"""
    Create and configure an instance of the Flask application.

    Initializes the database and migrations using Flask-SQLAlchemy and Flask-Migrate.
    Registers the 'api' Blueprint for handling routes.

    Returns:
        app: The Flask application instance.
    """
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    Migrate(app, db)
    
    jwt=JWTManager(app)

    # Import routes and models
    from .models import User  # Assuming User is a model in models.py
    from .routes import api  # Assuming api is defined in routes.py
    from .itineraryRoutes import itinerary # Assuming itinerary is defined in itineraryRoutes.py

    # Register the api Blueprint with the app
    app.register_blueprint(api)
    app.register_blueprint(itinerary)
    
    return app

