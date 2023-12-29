from flask import Blueprint, jsonify, request
from app.models import db, User
from flask_cors import CORS
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token


api = Blueprint('api', __name__)


# @api.route('/')
# def hello():
#     return 'Hello, World!'

# ROUTE REGISTERING A NEW USER
@api.route('/register', methods=['POST'])
def register_new_user():
    try:
        username = request.json.get('username')
        email_address = request.json.get('email_address')
        password = request.json.get('password')

        print(username, email_address, password)
        
        if not username or not password or not email_address:
            return jsonify({'error': "Missing username or password or email address"}), 400
        
        if User.query.filter_by(email_address=email_address).first():
            return jsonify({'error': "Email address already has a user"}), 409
        
        if User.query.filter_by(username=username).first():
            return jsonify({'error': "Username already exists"}), 409
        
        user = User(username=username, email_address=email_address)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        return jsonify({'message': "User created successfully"}), 201
    
    except KeyError:
        return jsonify({'error': "Missing username, password, or email address"}), 400
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
        
        
# ROUTE FOR LOGGING IN A USER
@api.route('/login', methods=['POST'])
def login_user():
    try:
        username = request.json.get('username')
        password = request.json.get('password')
        
        if not username or not password:
            return jsonify({'error': "Missing username or password"}), 400
        
        user = User.query.filter_by(username=username).first()
        
        if not user:
            return jsonify({'error': "User does not exist"}), 404
        
        if not user.check_password(password):
            return jsonify({'error': "Incorrect password"}), 401
        
        # Assuming you are using JWT for token generation
        access_token = create_access_token(identity=username)
        return jsonify({'message': "Login successful", 'access_token': access_token}), 200
    
    except KeyError:
        return jsonify({'error': "Missing username or password"}), 400
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
