"""User-Agent blocking for common scrapers."""

from functools import wraps
from flask import request, jsonify

# Common scraper user agents to block
BLOCKED_USER_AGENTS = [
    'requests',
    'curl',
    'wget',
    'python',
    'httpx',
    'scrapy',
    'selenium',
    'headless',
    'phantom',
    'bot',
    'crawler',
    'spider',
    'java',
    'c#',
    'powershell',
    'go-http-client',
    'ruby',
    'perl',
    'node',
    'axios',
    'fetch',
]


def is_blocked_user_agent(user_agent):
    """Check if user agent matches blocked patterns."""
    if not user_agent:
        return True  # Block if no user agent

    user_agent_lower = user_agent.lower()

    for blocked in BLOCKED_USER_AGENTS:
        if blocked.lower() in user_agent_lower:
            return True

    return False


def block_user_agent(f):
    """Decorator to block requests from common scrapers."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_agent = request.headers.get('User-Agent', '')

        if is_blocked_user_agent(user_agent):
            return jsonify({'error': 'Access denied'}), 403

        return f(*args, **kwargs)

    return decorated_function


def inject_user_agent_middleware(app):
    """Inject user-agent validation middleware into Flask app."""

    @app.before_request
    def check_user_agent():
        """Block common scraper user agents globally."""
        user_agent = request.headers.get('User-Agent', '')

        if is_blocked_user_agent(user_agent):
            return jsonify({'error': 'Access denied'}), 403

        return None
