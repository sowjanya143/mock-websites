"""Fortis Banking Group site configuration."""

import os


class Config:
    """Configuration for Fortis Banking Group site - Authentication required."""

    # Site identification
    COMPANY_NAME = 'Fortis Banking Group'
    SITE_NAME = 'fortis'

    # Security
    SECRET_KEY = os.environ.get('SECRET_KEY', 'fortis-dev-key-12345')

    # Authentication
    LOGIN_REQUIRED = True
    REQUIRE_JWT = True
    SESSION_EXPIRY = 300  # 5 minutes
    RATE_LIMIT_LOGIN = True  # Rate limit login attempts

    # Feature flags
    SHOW_POPUPS = False
    RATE_LIMIT_ENABLED = True

    # Rate limiting (general)
    MAX_REQUESTS = 10
    TIME_WINDOW = 60

    # Rate limiting (login - stricter)
    LOGIN_MAX_REQUESTS = 5
    LOGIN_TIME_WINDOW = 300

    # Performance
    ARTIFICIAL_DELAY = 0

    # Data presentation
    DATA_LAYOUT = 'secure_tables'

    # Financial data
    GLOBAL_AUM = '$650,000,000,000'

    # Debug mode
    DEBUG = os.environ.get('DEBUG', True)
