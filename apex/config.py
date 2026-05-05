"""Apex Investment Group site configuration."""

import os


class Config:
    """Configuration for Apex Investment Group site."""

    # Site identification
    COMPANY_NAME = 'Apex Investment Group'
    SITE_NAME = 'apex'

    # Security
    SECRET_KEY = os.environ.get('SECRET_KEY', 'apex-dev-key-54321')

    # CAPTCHA configuration (unique to Apex: only on data pages)
    CAPTCHA_ON_EVERY_PAGE = False
    CAPTCHA_REQUIRED_PAGES = ['/strategies', '/investor-resources', '/funds', '/fund/<id>']

    # Cookie banner (mandatory acceptance required)
    COOKIE_BANNER_MODE = 'mandatory'  # Block data until Accept clicked

    # Feature flags
    SHOW_POPUPS = True
    POPUP_TYPE = 'dismissible'
    POPUP_ON_HOME = True  # Show newsletter popup on home page
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
