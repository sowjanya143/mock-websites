"""Nexus Capital site configuration."""

import os


class Config:
    """Configuration for Nexus Capital site - Bot detection emphasis."""

    COMPANY_NAME = 'Nexus Capital'
    SITE_NAME = 'nexus'
    SECRET_KEY = os.environ.get('SECRET_KEY', 'nexus-dev-key-54321')

    # Cookie banner (optional - data accessible but banner shown)
    COOKIE_BANNER_MODE = 'optional'

    # Bot detection
    HONEYPOT_ENABLED = True
    HIDDEN_LINKS = True
    STRICT_BOT_DETECTION = True

    # Security
    SHOW_POPUPS = False
    RATE_LIMIT_ENABLED = True
    MAX_REQUESTS = 8
    TIME_WINDOW = 60

    # Performance
    ARTIFICIAL_DELAY = 0.2

    # Data presentation
    DATA_LAYOUT = 'fragmented'

    # Financial data
    GLOBAL_AUM = '$320,000,000,000'

    DEBUG = os.environ.get('DEBUG', True)
