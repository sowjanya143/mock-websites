from functools import wraps
from flask import session, render_template, request, jsonify

# Known headless browser fingerprints
BLOCKED_FINGERPRINTS = {
    'puppeteer_default_hash',
    'playwright_default_hash',
    '00d41e2f2721cdcd',
    '00000000000000000000000000000000'
}


def inject_fingerprint_routes(app):
    """Register the canvas fingerprint verification endpoint."""
    @app.route('/verify-fingerprint', methods=['POST'])
    def verify_fingerprint():
        data = request.get_json()
        hash_value = data.get('hash')

        if hash_value in BLOCKED_FINGERPRINTS:
            return jsonify({'error': 'Headless browser detected'}), 403

        session['fp_verified'] = True
        return jsonify({'status': 'OK'}), 200


def require_fingerprint(f):
    """Decorator to require fingerprint verification before accessing a route."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'fp_verified' not in session:
            return render_template('fingerprint_challenge.html')
        return f(*args, **kwargs)
    return decorated_function
