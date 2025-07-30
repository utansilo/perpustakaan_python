from flask import Blueprint, request, jsonify
from models import db
from models.user import User
from utils.jwt_utils import generate_token
from schemas.user_schema import UserSchema

auth_bp = Blueprint('auth_bp', __name__)
user_schema = UserSchema()

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    errors = user_schema.validate(data)
    if errors:
        return jsonify({"error": errors}), 400
    if User.query.filter_by(username=data['username']).first():
        return jsonify({"message": "Username sudah digunakan!"})
    
    user = User(username=data['username'])
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "Registrasi berhasil!!"})

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and user.check_password(data['password']):
        token = generate_token(user.id)
        return jsonify({"message": "Login berhasil!!", "token": token})
    return jsonify({"message": "Username atau password salah"})