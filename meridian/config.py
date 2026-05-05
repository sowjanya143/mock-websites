"""Meridian Global Holdings site configuration."""

import os


class Config:
    """Configuration for Meridian Global Holdings site."""

    # Site identification
    COMPANY_NAME = 'Meridian Global Holdings'
    SITE_NAME = 'meridian'

    # Security
    SECRET_KEY = os.environ.get('SECRET_KEY', 'meridian-dev-key-99999')

    # CAPTCHA configuration (unique to Meridian: random chance on every page)
    CAPTCHA_ON_EVERY_PAGE = False
    CAPTCHA_RANDOM_CHANCE = 0.30

    # Feature flags
    # Cookie banner (optional - user can dismiss and still access)
    COOKIE_BANNER_MODE = 'optional'  # Show banner but data accessible

    SHOW_POPUPS = True
    POPUP_TYPE = 'modal_after_scroll'
    RATE_LIMIT_ENABLED = False

    # Performance
    ARTIFICIAL_DELAY = 1.0

    # Data presentation
    DATA_LAYOUT = 'scattered'

    # Financial data
    GLOBAL_AUM = '$380,000,000,000'

    # Debug mode
    DEBUG = os.environ.get('DEBUG', True)
