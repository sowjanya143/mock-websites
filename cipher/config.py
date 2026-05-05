"""Cipher Wealth Management site configuration."""

import os


class Config:
    """Configuration for Cipher Wealth Management site - API encryption."""

    COMPANY_NAME = 'Cipher Wealth Management'
    SITE_NAME = 'cipher'
    SECRET_KEY = os.environ.get('SECRET_KEY', 'cipher-dev-key-11111')

    # API security
    API_KEY_REQUIRED = True
    ENCRYPT_RESPONSES = True
    REQUIRE_API_KEY_HEADER = True
    SIGNING_REQUIRED = True

    # Rate limiting (per API key)
    RATE_LIMIT_ENABLED = True
    MAX_REQUESTS = 12
    TIME_WINDOW = 60

    # Performance
    ARTIFICIAL_DELAY = 0

    # Data presentation
    DATA_LAYOUT = 'encrypted_api'

    # Financial data
    GLOBAL_AUM = '$520,000,000,000'

    DEBUG = os.environ.get('DEBUG', True)
