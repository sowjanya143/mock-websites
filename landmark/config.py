"""Landmark Property Advisors site configuration."""

import os

class Config:
    """Configuration for Landmark Property Advisors."""

    COMPANY_NAME = 'Landmark Property Advisors'
    SITE_NAME = 'landmark'
    SECRET_KEY = os.environ.get('SECRET_KEY', 'landmark-dev-key-5010')

    # Rotating session tokens (expire after 5 page views)
    ROTATING_TOKENS = True
    TOKEN_PAGE_LIMIT = 5

    # Canvas fingerprint blocking on first visit
    FINGERPRINT_BLOCKING = True

    # Rate limiting (4 req/60s - stricter than Bastion's 10)
    RATE_LIMIT_ENABLED = True
    MAX_REQUESTS = 4
    TIME_WINDOW = 60

    # Cookie banner (mandatory, not optional)
    COOKIE_BANNER_MODE = 'mandatory'

    # Data
    GLOBAL_AUM = '$47,000,000,000'
    DATA_LAYOUT = 'js_tables'

    # Port
    PORT = 5010

    DEBUG = os.environ.get('DEBUG', True)
