"""GeoIP and IP blocking utilities - mock implementation."""

from functools import wraps
from flask import request, jsonify

# Mock IP to country mapping
IP_TO_COUNTRY = {
    '127.0.0.1': 'US',
    '192.168.': 'US',
    '10.': 'US',
    '172.16.': 'US',
}

# Known VPN/proxy IPs (simplified mock)
VPN_IPS = [
    '8.8.8.8',      # Google DNS
    '1.1.1.1',      # Cloudflare DNS
    '208.67.222.222',  # OpenDNS
]


def get_client_ip(request_obj):
    """Get client IP from request."""
    if request_obj.headers.get('X-Forwarded-For'):
        return request_obj.headers.get('X-Forwarded-For').split(',')[0].strip()
    return request_obj.remote_addr


def get_country_from_ip(ip):
    """Mock GeoIP lookup - return country code."""
    # Simplistic mock - in production use MaxMind GeoIP2
    if ip.startswith('127.') or ip.startswith('192.168.') or ip.startswith('10.'):
        return 'US'

    # Default to unknown
    return 'UNKNOWN'


def is_vpn_ip(ip):
    """Mock VPN detection - check against known VPN IPs."""
    return ip in VPN_IPS or ip.startswith('8.8.8.8') or ip.startswith('1.1.1.1')


def allow_countries(allowed_countries):
    """Decorator to restrict access to allowed countries."""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            client_ip = get_client_ip(request)
            country = get_country_from_ip(client_ip)

            if country not in allowed_countries:
                return jsonify({
                    'error': 'Access denied',
                    'message': f'This service is not available in {country}'
                }), 403

            return f(*args, **kwargs)

        return decorated_function

    return decorator


def block_vpn(f):
    """Decorator to block VPN/proxy access."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        client_ip = get_client_ip(request)

        if is_vpn_ip(client_ip):
            return jsonify({
                'error': 'Access denied',
                'message': 'VPN/proxy access not allowed'
            }), 403

        return f(*args, **kwargs)

    return decorated_function


def inject_geoip_routes(app):
    """Inject GeoIP check endpoints."""

    @app.route('/api/check-location')
    def check_location():
        """Check current location for testing."""
        client_ip = get_client_ip(request)
        country = get_country_from_ip(client_ip)
        vpn_detected = is_vpn_ip(client_ip)

        return jsonify({
            'ip': client_ip,
            'country': country,
            'vpn_detected': vpn_detected,
        })
