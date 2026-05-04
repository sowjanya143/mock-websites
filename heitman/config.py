"""Heitman Capital Management site configuration."""

import os


class Config:
    """Configuration for Heitman Capital Management site."""

    # Site identification
    COMPANY_NAME = 'Heitman Capital Management'
    SITE_NAME = 'heitman'

    # Security
    SECRET_KEY = os.environ.get('SECRET_KEY', 'heitman-dev-key-54321')

    # CAPTCHA configuration (unique to Heitman: only on data pages)
    CAPTCHA_ON_EVERY_PAGE = False
    CAPTCHA_REQUIRED_PAGES = ['/strategies', '/investor-resources', '/funds', '/fund/<id>']

    # Feature flags
    SHOW_POPUPS = True
    POPUP_TYPE = 'dismissible'
    RATE_LIMIT_ENABLED = True

    # Rate limiting
    MAX_REQUESTS = 5
    TIME_WINDOW = 60

    # Performance
    ARTIFICIAL_DELAY = 0

    # Data presentation
    DATA_LAYOUT = 'json_endpoint'

    # Financial data
    GLOBAL_AUM = '$450,000,000,000'

    # Debug mode
    DEBUG = os.environ.get('DEBUG', True)
