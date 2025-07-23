# routes/auth.py
from flask import Blueprint, request, jsonify
from models import User
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['POST', 'OPTIONS'])
def register():
    if request.method == 'OPTIONS':
        # Handle preflight request
        response = jsonify({'status': 'ok'})
        response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'POST,OPTIONS')
        return response
        
    try:
        data = request.get_json()
        
        # Validate input data
        if not data or not data.get('username') or not data.get('password'):
            return jsonify({"msg": "Username and password are required"}), 400
            
        if User.objects(username=data['username']).first():
            return jsonify({"msg": "Username already exists"}), 400
            
        # Use pbkdf2:sha256 method which is compatible with Python 3.9
        hashed_pw = generate_password_hash(data['password'], method='pbkdf2:sha256')
        user = User(username=data['username'], password=hashed_pw)
        user.save()
        return jsonify({"msg": "User registered successfully"}), 201
        
    except Exception as e:
        print(f"Registration error: {e}")  # For debugging
        return jsonify({"msg": "Registration failed. Please try again."}), 500

@auth.route('/login', methods=['POST', 'OPTIONS'])
def login():
    if request.method == 'OPTIONS':
        # Handle preflight request
        response = jsonify({'status': 'ok'})
        response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'POST,OPTIONS')
        return response
        
    try:
        data = request.get_json()
        
        # Validate input data
        if not data or not data.get('username') or not data.get('password'):
            return jsonify({"msg": "Username and password are required"}), 400
            
        user = User.objects(username=data['username']).first()
        if not user or not check_password_hash(user.password, data['password']):
            return jsonify({"msg": "Invalid credentials"}), 401
            
        token = create_access_token(identity=str(user.id))
        return jsonify(access_token=token, username=user.username), 200
        
    except Exception as e:
        print(f"Login error: {e}")  # For debugging
        return jsonify({"msg": "Login failed. Please try again."}), 500

@auth.route('/logout', methods=['POST', 'OPTIONS'])
@jwt_required()
def logout():
    if request.method == 'OPTIONS':
        # Handle preflight request
        response = jsonify({'status': 'ok'})
        response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'POST,OPTIONS')
        return response
        
    try:
        # Get the current user's identity from the JWT token
        current_user_id = get_jwt_identity()
        # In a real application, you might want to add the token to a blacklist
        # For now, we'll just return a success message since JWT logout is handled client-side
        return jsonify({"msg": "Successfully logged out"}), 200
        
    except Exception as e:
        print(f"Logout error: {e}")  # For debugging
        return jsonify({"msg": "Logout failed. Please try again."}), 500

@auth.route('/me', methods=['GET', 'OPTIONS'])
@jwt_required()
def get_current_user():
    if request.method == 'OPTIONS':
        # Handle preflight request
        response = jsonify({'status': 'ok'})
        response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,OPTIONS')
        return response
        
    try:
        current_user_id = get_jwt_identity()
        user = User.objects(id=current_user_id).first()
        if user:
            return jsonify({"username": user.username, "id": str(user.id)}), 200
        else:
            return jsonify({"msg": "User not found"}), 404
            
    except Exception as e:
        print(f"Get user error: {e}")  # For debugging
        return jsonify({"msg": "Failed to get user info"}), 500
