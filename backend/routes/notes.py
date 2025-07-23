# routes/notes.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Note, User

notes = Blueprint('notes', __name__)

@notes.route('/notes', methods=['OPTIONS'])
def notes_options():
    # Handle preflight request
    response = jsonify({'status': 'ok'})
    response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,PUT,DELETE,OPTIONS')
    return response

@notes.route('/notes', methods=['GET'])
@jwt_required()
def get_notes():
    user_id = get_jwt_identity()
    user = User.objects(id=user_id).first()
    if not user:
        return jsonify({"msg": "User not found"}), 404
        
    all_notes = Note.objects(user=user).order_by('-created_at')
    return jsonify([{
        "id": str(note.id),
        "title": note.title,
        "content": note.content,
        "created_at": note.created_at.strftime("%Y-%m-%d %H:%M:%S")
    } for note in all_notes])

@notes.route('/notes', methods=['POST'])
@jwt_required()
def create_note():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    if not data or not data.get('title') or not data.get('content'):
        return jsonify({"msg": "Title and content are required"}), 400
        
    user = User.objects(id=user_id).first()
    if not user:
        return jsonify({"msg": "User not found"}), 404
        
    note = Note(title=data['title'], content=data['content'], user=user)
    note.save()
    return jsonify({"msg": "Note created!", "id": str(note.id)}), 201

@notes.route('/notes/<note_id>', methods=['PUT'])
@jwt_required()
def update_note(note_id):
    user_id = get_jwt_identity()
    data = request.get_json()
    note = Note.objects(id=note_id).first()
    
    if not note:
        return jsonify({"msg": "Note not found"}), 404
        
    # Check if the note belongs to the current user
    if str(note.user.id) != user_id:
        return jsonify({"msg": "Unauthorized"}), 403
        
    Note.objects(id=note_id).update_one(**data)
    return jsonify({"msg": "Note updated!"})

@notes.route('/notes/<note_id>', methods=['DELETE'])
@jwt_required()
def delete_note(note_id):
    user_id = get_jwt_identity()
    note = Note.objects(id=note_id).first()
    
    if not note:
        return jsonify({"msg": "Note not found"}), 404
        
    # Check if the note belongs to the current user
    if str(note.user.id) != user_id:
        return jsonify({"msg": "Unauthorized"}), 403
        
    Note.objects(id=note_id).delete()
    return jsonify({"msg": "Note deleted!"})
