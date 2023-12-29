# backend/app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config
from flask_migrate import Migrate

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    Migrate(app, db)

    # Import routes and models
    from .models import User  # Assuming User is a model in models.py
    from .routes import api  # Assuming api is defined in routes.py

    # Register the api Blueprint with the app
    app.register_blueprint(api)
    
    return app
