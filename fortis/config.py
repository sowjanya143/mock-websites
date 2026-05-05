"""Fortis Banking Group site configuration."""

import os


class Config:
    """Configuration for Fortis Banking Group site - CAPTCHA on data pages."""

    # Site identification
    COMPANY_NAME = 'Fortis Banking Group'
    SITE_NAME = 'fortis'

    # Security
    SECRET_KEY = os.environ.get('SECRET_KEY', 'fortis-dev-key-12345')

    # CAPTCHA configuration (like Apex - data pages only)
    CAPTCHA_ON_EVERY_PAGE = False
    CAPTCHA_REQUIRED_PAGES = ['/strategies', '/investor-resources', '/funds', '/fund/<id>']

    # Feature flags
    SHOW_POPUPS = False
    RATE_LIMIT_ENABLED = True

    # Rate limiting
    MAX_REQUESTS = 7
    TIME_WINDOW = 60

    # Performance
    ARTIFICIAL_DELAY = 0

    # Data presentation
    DATA_LAYOUT = 'clean_tables'

    # Financial data
    GLOBAL_AUM = '$650,000,000,000'

    # Debug mode
    DEBUG = os.environ.get('DEBUG', True)
