import jwt
import os
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