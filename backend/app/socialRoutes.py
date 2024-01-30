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
@social.route('/following', methods=['GET'])
@jwt_required()
def get_following():
    current_user_id = get_jwt_identity()

"""
ROUTE FOLLOWING A NEW PERSON
"""
@social.route('/follow', methods=['POST'])
@jwt_required()
def follow():
    current_user_id = get_jwt_identity()
    

"""
ROUTE FOR UNFOLLOWING SOMEONE
"""
@social.route('/unfollow', methods=['POST'])
@jwt_required()
def unfollow():
    current_user_id = get_jwt_identity()

"""
ROUTE FOR REQUESTING TO FOLLOW SOMEONE THAT IS ON PRIVATE
"""
@social.route('/request', methods=['POST'])
@jwt_required()
def request_to_follow():
    current_user_id = get_jwt_identity()

"""
ROUTE FOR ACCEPTING OR DENYING SOMEONES FOLLOW REQUEST
"""
@social.route('/request', methods=['PUT'])
@jwt_required()
def accept_deny_request():
    current_user_id = get_jwt_identity()
