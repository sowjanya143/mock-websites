"""JavaScript validation - requires client-side JS execution."""

import secrets
from functools import wraps
from flask import request, session, render_template, redirect, url_for, jsonify


def generate_js_token():
    """Generate a token that only JS can set."""
    return secrets.token_urlsafe(32)


def require_javascript(f):
    """Decorator to require JavaScript validation before accessing route."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Allow /validate-js and /set-js-cookie routes through
        if request.path in ['/validate-js', '/set-js-cookie']:
            return f(*args, **kwargs)

        # Check if JS validated
        if 'js_validated' not in session:
            # Generate token and redirect to validation page
            session['js_token'] = generate_js_token()
            session['js_requested_path'] = request.path
            return redirect(url_for('validate_js'))

        return f(*args, **kwargs)

    return decorated_function


def inject_js_routes(app):
    """Inject JS validation routes into Flask app."""

    @app.route('/validate-js')
    def validate_js():
        """JS validation page - generates token, requires JS to set it."""
        if 'js_token' not in session:
            session['js_token'] = generate_js_token()

        return render_template('validate-js.html', js_token=session['js_token'])

    @app.route('/set-js-cookie', methods=['POST'])
    def set_js_cookie():
        """Endpoint for JS to POST back token (proves JS executed)."""
        data = request.get_json() or {}
        token = data.get('token', '')
        expected_token = session.get('js_token', '')

        if token and token == expected_token:
            session['js_validated'] = True
            redirects_to = session.pop('js_requested_path', '/')
            return jsonify({'status': 'ok', 'redirect': redirects_to}), 200

        return jsonify({'status': 'error', 'message': 'Invalid token'}), 403
