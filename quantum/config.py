"""Quantum Funds site configuration."""

import os


class Config:
    """Configuration for Quantum Funds site - Geographic blocking."""

    COMPANY_NAME = 'Quantum Funds'
    SITE_NAME = 'quantum'
    SECRET_KEY = os.environ.get('SECRET_KEY', 'quantum-dev-key-99999')

    # Cookie banner (optional - data accessible but banner shown)
    COOKIE_BANNER_MODE = 'optional'

    # Geographic restrictions
    GEO_BLOCKING = True
    ALLOWED_COUNTRIES = ['US', 'CA', 'UK']
    BLOCK_VPNS = True
    ROTATING_BLOCKS = True

    # Rate limiting (stricter for non-US)
    RATE_LIMIT_ENABLED = True
    MAX_REQUESTS = 6
    TIME_WINDOW = 60

    # Performance
    ARTIFICIAL_DELAY = 0

    # Data presentation
    DATA_LAYOUT = 'geofenced'

    # Financial data
    GLOBAL_AUM = '$410,000,000,000'

    DEBUG = os.environ.get('DEBUG', True)
