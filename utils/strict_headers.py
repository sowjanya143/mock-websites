"""Strict header validation - requires browser-like headers."""

from functools import wraps
from flask import request, jsonify

# Required headers for browser-like requests
REQUIRED_HEADERS = ['User-Agent', 'Accept']


def has_required_headers():
    """Check if request has all required browser-like headers."""
    for header in REQUIRED_HEADERS:
        if not request.headers.get(header):
            return False
    return True


def require_headers(required=None):
    """Decorator to require specific headers."""
    if required is None:
        required = REQUIRED_HEADERS

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            for header in required:
                if not request.headers.get(header):
                    return jsonify({'error': f'Missing required header: {header}'}), 403

            return f(*args, **kwargs)

        return decorated_function

    return decorator


def inject_headers_middleware(app):
    """Inject header validation middleware into Flask app."""

    @app.before_request
    def check_headers():
        """Validate required headers on all requests."""
        # Allow certain routes through
        if request.path in ['/set-cookie', '/validate-js', '/set-js-cookie']:
            return None

        if not has_required_headers():
            return jsonify({'error': 'Invalid request headers'}), 403

        return None
