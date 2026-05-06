"""
Rotating session token utility for defeating scrapers.
Tokens expire after N page views, breaking mid-crawl.
"""

import uuid
from functools import wraps
from flask import session, redirect, url_for


def issue_token(sess, page_limit=5):
    """
    Create a new UUID token and store it in the session.

    Args:
        sess: Flask session object
        page_limit: Maximum number of page views before token expires

    Returns:
        Generated token (UUID string)
    """
    token = str(uuid.uuid4())
    sess['page_token'] = token
    sess['page_count'] = 0
    return token


def validate_token(sess, page_limit=5):
    """
    Validate and increment the session token.

    Increments page_count and checks if it has reached the limit.
    If limit reached, deletes the token and marks session as expired.

    Args:
        sess: Flask session object
        page_limit: Maximum number of page views before token expires

    Returns:
        True if token is valid and not expired, False otherwise
    """
    if 'page_count' not in sess:
        sess['page_count'] = 0

    sess['page_count'] += 1

    if sess['page_count'] >= page_limit:
        if 'page_token' in sess:
            del sess['page_token']
        sess['token_expired'] = True
        return False

    return True


def require_token(page_limit=5):
    """
    Decorator that validates session token on each route request.

    Redirects to 'refresh_token' if validation fails.

    Args:
        page_limit: Maximum number of page views before token expires

    Returns:
        Decorated function
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not validate_token(session, page_limit):
                return redirect(url_for('refresh_token'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def inject_token_routes(app, page_limit=5):
    """
    Inject /refresh-token route into the Flask app.

    The route issues a new token and redirects to HTTP_REFERER or '/'.

    Args:
        app: Flask application instance
        page_limit: Maximum number of page views before token expires
    """
    @app.route('/refresh-token', methods=['GET'])
    def refresh_token():
        issue_token(session, page_limit)
        referer = app.request.referrer or '/'
        return redirect(referer)
