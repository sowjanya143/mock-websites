"""Cookie validation - requires specific cookies to be set."""

import secrets
from functools import wraps
from flask import request, make_response, jsonify


REQUIRED_COOKIE_NAME = 'site_session_cookie'


def get_required_cookie_value():
    """Generate a random cookie value."""
    return secrets.token_urlsafe(24)


def inject_cookie_middleware(app):
    """Inject cookie validation middleware into Flask app."""

    @app.before_request
    def check_required_cookie():
        """Ensure required cookie is present on all requests."""
        # Allow /set-cookie route through
        if request.path == '/set-cookie':
            return None

        # Check for required cookie
        cookie_value = request.cookies.get(REQUIRED_COOKIE_NAME)
        if not cookie_value:
            # Redirect to set-cookie endpoint
            return make_response({'error': 'Cookie required', 'redirect': '/set-cookie'}, 403)

        return None

    @app.route('/set-cookie')
    def set_cookie():
        """Set the required cookie and redirect back."""
        from flask import redirect, url_for
        response = make_response(redirect(request.referrer or '/'))
        response.set_cookie(
            REQUIRED_COOKIE_NAME,
            get_required_cookie_value(),
            max_age=86400,  # 24 hours
            httponly=True,
            secure=False,  # Set to True in production
            samesite='Lax'
        )
        return response
