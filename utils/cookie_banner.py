"""Cookie banner management - GDPR compliance with different enforcement levels."""

import secrets
from functools import wraps
from flask import request, session, render_template, jsonify, make_response

BANNER_MODES = {
    'mandatory': 'data_blocked',  # Block all data until accepted
    'optional': 'data_visible',   # Show banner but data accessible
    'none': 'no_banner',          # No banner, keep set-cookie middleware
}


def generate_banner_token():
    """Generate a unique banner token."""
    return secrets.token_urlsafe(24)


def is_cookie_accepted(session_obj):
    """Check if user accepted cookies."""
    return session_obj.get('cookie_accepted', False)


def is_banner_dismissed(session_obj):
    """Check if user dismissed banner (for optional mode)."""
    return session_obj.get('cookie_dismissed', False)


def require_cookie_acceptance(mode='mandatory'):
    """
    Decorator to require cookie acceptance before showing data.

    Modes:
    - 'mandatory': Show banner blocking page until Accept clicked
    - 'optional': Show banner but allow data access via Dismiss

    The decorator doesn't block execution; the banner is injected by
    the context processor and shown via the template. This allows
    the page to render normally while CSS/JS prevents interaction.
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Just proceed - banner will be shown by context processor
            return f(*args, **kwargs)

        return decorated_function

    return decorator


def inject_cookie_banner_routes(app, mode='mandatory'):
    """Inject cookie banner routes into Flask app."""

    @app.route('/accept-cookies', methods=['POST'])
    def accept_cookies():
        """Accept cookies and redirect to referrer."""
        session['cookie_accepted'] = True
        session['banner_token'] = generate_banner_token()

        # Set cookie too (for set-cookie middleware compat)
        response = make_response({'status': 'ok'})
        response.set_cookie(
            'site_session_cookie',
            secrets.token_urlsafe(24),
            max_age=86400,
            httponly=True,
            secure=False,
            samesite='Lax'
        )
        response.set_cookie(
            'cookie_consent',
            'accepted',
            max_age=31536000,  # 1 year
            secure=False,
            samesite='Lax'
        )

        return response, 200

    @app.route('/reject-cookies', methods=['POST'])
    def reject_cookies():
        """Reject non-essential cookies."""
        session['cookie_accepted'] = False
        session['cookie_rejected'] = True

        # Set minimal cookie for tracking rejection
        response = make_response({'status': 'ok'})
        response.set_cookie(
            'cookie_consent',
            'rejected',
            max_age=31536000,  # 1 year
            secure=False,
            samesite='Lax'
        )

        return response, 200

    @app.route('/dismiss-banner', methods=['POST'])
    def dismiss_banner():
        """Dismiss banner (optional mode only)."""
        session['cookie_dismissed'] = True
        session['banner_token'] = generate_banner_token()

        # Optional: set cookie even without explicit acceptance
        response = make_response({'status': 'ok'})
        response.set_cookie(
            'site_session_cookie',
            secrets.token_urlsafe(24),
            max_age=86400,
            httponly=True,
            secure=False,
            samesite='Lax'
        )

        return response, 200

    @app.context_processor
    def inject_banner_context():
        """Inject banner state into all templates."""
        return {
            'cookie_accepted': is_cookie_accepted(session),
            'cookie_dismissed': is_banner_dismissed(session),
            'banner_mode': mode,
            'banner_shown': mode in ['mandatory', 'optional'],
        }
