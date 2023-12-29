from flask import Blueprint, jsonify, request
from app.models import db, User
from flask_cors import CORS
from flask_jwt_extended import jwt_required, get_jwt_identity


api = Blueprint('api', __name__)


@api.route('/')
def hello():
    return 'Hello, World!'

@api.route('/api/register', methods=['POST'])
def register_new_user():
    try:
        username = request.json['username', None]
        email_address = request.json['email_address', None]
        password = request.json['password', None]
        
        if not username or password or email_address:
            return jsonify({'error': "Missing username or password or email address"}), 400
        
        if User.query.filter_by(email_address=email_address).first():
            return jsonify({'error': "Email address already has a user"}), 409
        
        if User.query.filter_by(username=username).first():
            return jsonify({'error': "Username already exists"}), 409
        
        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        return jsonify({'message': "User created successfully"}), 201
    
    except KeyError:
        return jsonify({'error': "Missing username or password"}), 400
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
        
    

