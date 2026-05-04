"""Hokuyo Bank site configuration."""

import os


class Config:
    """Configuration for Hokuyo Bank site."""

    # Site identification
    COMPANY_NAME = 'Hokuyo Bank'
    SITE_NAME = 'hokuyo'

    # Security
    SECRET_KEY = os.environ.get('SECRET_KEY', 'hokuyo-dev-key-54321')

    # CAPTCHA configuration (NO CAPTCHA - this is the control site)
    CAPTCHA_ON_EVERY_PAGE = False
    CAPTCHA_REQUIRED_PAGES = []

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
