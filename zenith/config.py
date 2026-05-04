"""Oaktree Capital Management site configuration."""

import os


class Config:
    """Configuration for Oaktree Capital Management site - Most Complex."""

    # Site identification
    COMPANY_NAME = 'Oaktree Capital Management'
    SITE_NAME = 'oaktree'

    # Security
    SECRET_KEY = os.environ.get('SECRET_KEY', 'oaktree-dev-key-99999')

    # CAPTCHA configuration (most complex: first visit + data pages)
    CAPTCHA_FIRST_VISIT = True
    CAPTCHA_DATA_PAGES = True
    CAPTCHA_REQUIRED_PAGES = ['/strategies', '/investor-resources', '/funds', '/fund/<id>']

    # Feature flags
    SHOW_POPUPS = True
    POPUP_TYPE = 'sticky_footer'
    AUTO_DISMISS_POPUP = True
    AUTO_DISMISS_DELAY = 5000  # milliseconds

    # Rate limiting (strictest: 3 requests per 60 seconds)
    RATE_LIMIT_ENABLED = True
    MAX_REQUESTS = 3
    TIME_WINDOW = 60

    # Performance (0.5 second artificial delay on every request)
    ARTIFICIAL_DELAY = 0.5

    # Data presentation
    DATA_LAYOUT = 'ajax_loaded'

    # Financial data
    GLOBAL_AUM = '$290,000,000,000'

    # Debug mode
    DEBUG = os.environ.get('DEBUG', True)
