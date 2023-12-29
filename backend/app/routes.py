from flask import Blueprint, jsonify, request
from app.models import db, User
from flask_cors import CORS
from flask_jwt_extended import jwt_required, get_jwt_identity
import hashlib

api = Blueprint('api', __name__)


@api.route('/api/register', methods=['POST'])
def register_new_user():
    try:
        username = request.json['username', None]
        password = request.json['password', None]
        
        if not username or password:
            return jsonify({'error': "Missing username or password"}),
        
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
        
    

