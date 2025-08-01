from flask import Blueprint, request, jsonify
from models import db
from models.user import User
from werkzeug.security import generate_password_hash
from utils.jwt_utils import generate_token, get_current_user
from utils.decoration import admin_required
from utils.response import success_message, error_message
from schemas.user_schema import UserSchema

auth_bp = Blueprint('auth_bp', __name__)
user_schema = UserSchema()

# @auth_bp.route('/setup-admin', methods=['POST'])
# def setupAdmin():
#     existing_admin = User.query.filter_by(role='admin').first()
#     if existing_admin:
#         return error_message("Admin sudah ada!!", 400)
    
#     data = request.get_json()
#     hashed_pass = generate_password_hash(data['password'])
#     admin = User(
#         username = data['username'],
#         name = data['name'],
#         nim = data['nim'],
#         jurusan = data['jurusan'],
#         password_hash = hashed_pass,
#         role = 'admin'
#     )
#     db.session.add(admin)
#     db.session.commit()
#     return success_message(message="Admin berhasil dibuat!", data=UserSchema().dump(admin), status_code=201)

@auth_bp.route('/add-user', methods=['POST'])
@admin_required
def addUser():
    current_user = get_current_user()

    if current_user.role != 'admin':
        return error_message(message="Hanya admin yang bisa menambah user!", status_code=403)
    
    data = request.get_json()
    errors = UserSchema().validate(data)
    if errors:
        return error_message(message=errors, status_code=400)
    
    if User.query.filter_by(username=data['username']).first():
        return error_message(message="Username sudah digunakan", status_code=409)
    
    hashed_password = generate_password_hash(data['password'])

    user = User(
        username=data['username'],
        name=data['name'],
        nim=data['nim'],
        jurusan=data['jurusan'],
        password_hash=hashed_password,
        role=data.get('role', 'user')
    )

    db.session.add(user)
    db.session.commit()

    return success_message(data=UserSchema(exclude=['password']).dump(user), message="User berhasil ditambahkan!")

@auth_bp.route('/all-user', methods=['GET'])
@admin_required
def getAllUser():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)
    user_filter = request.args.get('name', '', type=str)

    query = User.query
    if user_filter:
        query = query.filter(User.name.ilike(f"%{user_filter}%"))

    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    user_list = pagination.items

    if not user_list:
        return error_message(message="Data tidak ditemukan!!", status_code=404)
    
    result = {
        "total": pagination.total,
        "pages": pagination.pages,
        "current_page": pagination.page,
        "per_page": pagination.per_page,
        "user": UserSchema(many=True).dump(user_list)
    }

    return success_message(data=result, message="Daftar user ditampilkan!")

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    errors = user_schema.validate(data)
    if errors:
        return error_message(message=errors, status_code=400)
    if User.query.filter_by(username=data['username']).first():
        return error_message(message="Username sudah digunakan", status_code=409)
    
    user = User(username=data['username'])
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    return success_message(data=UserSchema(exclude=['password']).dump(user), message="User berhasil ditambahkan!")

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and user.check_password(data['password']):
        token = generate_token(user.id)
        return success_message(data={'token': token}, message="User berhasil ditambahkan!")
    return jsonify({"message": "Username atau password salah"})