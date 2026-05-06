"""Bastion Investment Group site configuration."""

import os

class Config:
    """Configuration for Bastion Investment Group."""

    COMPANY_NAME = 'Bastion Investment Group'
    SITE_NAME = 'bastion'
    SECRET_KEY = os.environ.get('SECRET_KEY', 'bastion-dev-key-55555')

    # CAPTCHA (timed, on data pages only)
    CAPTCHA_ON_EVERY_PAGE = False
    CAPTCHA_REQUIRED_PAGES = ['/what-we-do', '/investors', '/financial-advisors']
    TIMED_CAPTCHA = True
    CAPTCHA_TIME_LIMIT = 30

    # DOM obfuscation
    DOM_OBFUSCATION = True

    # Rate limiting (10 req/60s)
    RATE_LIMIT_ENABLED = True
    MAX_REQUESTS = 10
    TIME_WINDOW = 60

    # Cookie banner
    COOKIE_BANNER_MODE = 'optional'

    # Data
    GLOBAL_AUM = '$55,000,000,000'
    DATA_LAYOUT = 'js_tables'

    DEBUG = os.environ.get('DEBUG', True)
