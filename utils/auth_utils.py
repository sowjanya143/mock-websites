"""Authentication utilities - JWT and login management."""

import jwt
import datetime
from functools import wraps
from flask import request, session, jsonify, redirect, url_for

# Simple secret key for demo - in production use strong key from config
SECRET_KEY = 'your-secret-key-here'


def generate_jwt_token(user_id, username, expiry_minutes=30):
    """Generate a JWT token."""
    payload = {
        'user_id': user_id,
        'username': username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=expiry_minutes),
        'iat': datetime.datetime.utcnow(),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')


def verify_jwt_token(token):
    """Verify and decode JWT token."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def require_login(f):
    """Decorator to require login (JWT in session)."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        jwt_token = session.get('auth_token')

        if not jwt_token:
            return redirect(url_for('login'))

        # Verify token is valid
        payload = verify_jwt_token(jwt_token)
        if not payload:
            session.pop('auth_token', None)
            return redirect(url_for('login'))

        return f(*args, **kwargs)

    return decorated_function


# Demo user credentials
DEMO_USERS = {
    'admin': 'password123',
    'user': 'user123',
    'test': 'test123',
}


def authenticate_user(username, password):
    """Authenticate user credentials."""
    if username in DEMO_USERS and DEMO_USERS[username] == password:
        return True
    return False
