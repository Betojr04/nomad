from flask import Blueprint, jsonify, request
from app.models import db, User, Follower, Comment, Like, DirectMessage
from flask_cors import CORS
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from datetime import datetime

social = Blueprint('social', __name__)
CORS(social)

"""
ROUTE FOR RETREIVING A USERS FOLLOWERS
"""
@social.route('/followers', methods=['GET'])
@jwt_required()
def get_followers():
    current_user_id = get_jwt_identity()

"""
ROUTE FOR RETREIVING A USERS FOLLOWING
"""

"""
ROUTE FOLLOWING A NEW PERSON
"""

"""
ROUTE FOR UNFOLLOWING SOMEONE
"""

"""
ROUTE FOR REQUESTING TO FOLLOW SOMEONE THAT IS ON PRIVATE
"""

"""
ROUTE FOR ACCEPTING OR DENYING SOMEONES FOLLOW REQUEST
"""
