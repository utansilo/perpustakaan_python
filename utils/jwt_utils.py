import jwt
import os
from flask import request
from models.user import User
from datetime import datetime, timedelta

def generate_token(user_id, expire_in=300):
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(seconds=expire_in)
    }
    secret_key = os.getenv("SECRET_KEY")
    return jwt.encode(payload, secret_key, algorithm='HS256')

def verify_token(token):
    try:
        secret_key = os.getenv("SECRET_KEY")
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])
        return payload
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None
    
def get_current_user():
    auth_header = request.headers.get('Authorization')

    if not auth_header:
        return None
    
    token = auth_header.split(" ")[1] if " " in auth_header else auth_header
    payload = verify_token(token)

    if not payload:
        return None
    
    user_id = payload.get("user_id")
    return User.query.get(user_id)