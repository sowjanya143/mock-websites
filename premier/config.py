"""Premier Financial Services site configuration."""

import os


class Config:
    """Configuration for Premier Financial Services site."""

    # Site identification
    COMPANY_NAME = 'Premier Financial Services'
    SITE_NAME = 'premier'

    # Security
    SECRET_KEY = os.environ.get('SECRET_KEY', 'premier-dev-key-54321')

    # CAPTCHA configuration (NO CAPTCHA - this is the control site)
    CAPTCHA_ON_EVERY_PAGE = False
    CAPTCHA_REQUIRED_PAGES = []

    # Cookie banner (optional - user can dismiss and still access)
    COOKIE_BANNER_MODE = 'optional'  # Show banner but data accessible

    # Feature flags
    SHOW_POPUPS = False
    RATE_LIMIT_ENABLED = False

    # Performance
    ARTIFICIAL_DELAY = 0

    # Data presentation
    DATA_LAYOUT = 'clean_tables'

    # Financial data
    GLOBAL_AUM = '$220,000,000,000'

    # Debug mode
    DEBUG = os.environ.get('DEBUG', True)
