from functools import wraps
from flask import request
from utils.jwt_utils import verify_token
from models.user import User
from models import db
from utils.response import error_message

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth = request.headers.get('Authorization')
        if not auth or not auth.startswith('Bearer '):
            return error_message(message="Token tidak ditemukan atau tidak valid!!", status_code=401)
        token = auth.split()[1]
        try:
            payload = verify_token(token)
            user = User.query.get(payload["user_id"])
            if not user:
                return error_message(message="User tidak ditemukan", status_code=401)
            request.user = user
        except Exception as e:
            return error_message(message=f"Token tidak valid: {str(e)}", status_code=401)
        
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization', None)
        if not auth_header:
            return error_message("Token tidak ditemukan atau tidak valid!!", status_code=401)

        token = auth_header.split(" ")[1] if " " in auth_header else auth_header
        payload = verify_token(token)
        if not payload:
            return error_message("Token tidak valid!", status_code=401)
        
        user = db.session.get(User, payload['user_id'])
        if not user or user.role != 'admin':
            return error_message("Akses ditolak, Lapor ke admin!!", status_code=403)
        
        return f(*args, **kwargs)
    return decorated