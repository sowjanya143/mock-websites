"""Nomura site configuration."""

import os


class Config:
    """Configuration for Nomura Investment Bank site."""

    # Site identification
    COMPANY_NAME = 'Nomura Inc.'
    SITE_NAME = 'nomura'

    # Security
    SECRET_KEY = os.environ.get('SECRET_KEY', 'nomura-dev-key-99999')

    # CAPTCHA configuration (unique to Nomura: random chance on every page)
    CAPTCHA_ON_EVERY_PAGE = False
    CAPTCHA_RANDOM_CHANCE = 0.30

    # Feature flags
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
