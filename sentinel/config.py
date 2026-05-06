"""Sentinel Capital Partners site configuration."""

import os


class Config:
    """Configuration for Sentinel Capital Partners site."""

    # Site identification
    COMPANY_NAME = 'Sentinel Capital Partners'
    SITE_NAME = 'sentinel'

    # Security
    SECRET_KEY = os.environ.get('SECRET_KEY', 'sentinel-dev-key-12345')

    # CAPTCHA configuration (unique to Fortress: on every page)
    CAPTCHA_ON_EVERY_PAGE = True
    CAPTCHA_REQUIRED_PAGES = []

    # Cookie banner (mandatory acceptance required)
    COOKIE_BANNER_MODE = 'mandatory'  # Block data until Accept clicked

    # Feature flags
    SHOW_POPUPS = False
    RATE_LIMIT_ENABLED = False
    USER_AGENT_BLOCKING = os.environ.get('USER_AGENT_BLOCKING', 'true').lower() == 'true'

    # Performance
    ARTIFICIAL_DELAY = 0

    # Data presentation
    DATA_LAYOUT = 'js_tables'

    # Financial data
    GLOBAL_AUM = '$850,000,000,000'

    # Debug mode
    DEBUG = os.environ.get('DEBUG', True)
