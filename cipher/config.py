"""Cipher Wealth Management site configuration."""

import os


class Config:
    """Configuration for Cipher Wealth Management site - Image CAPTCHA with OCR difficulty."""

    COMPANY_NAME = 'Cipher Wealth Management'
    SITE_NAME = 'cipher'
    SECRET_KEY = os.environ.get('SECRET_KEY', 'cipher-dev-key-11111')

    # CAPTCHA configuration - Image-based with distortion
    CAPTCHA_ON_EVERY_PAGE = True
    CAPTCHA_TYPE = 'image_ocr'  # Image-based CAPTCHA with OCR difficulty
    CAPTCHA_DISTORTION = True  # Apply distortion/noise
    CAPTCHA_LENGTH = 5  # 5 characters (harder)

    # Feature flags
    SHOW_POPUPS = False
    RATE_LIMIT_ENABLED = True

    # Rate limiting
    MAX_REQUESTS = 6
    TIME_WINDOW = 60

    # Performance (add slight delay for "security theater")
    ARTIFICIAL_DELAY = 0.1

    # Data presentation
    DATA_LAYOUT = 'protected_tables'

    # Financial data
    GLOBAL_AUM = '$520,000,000,000'

    DEBUG = os.environ.get('DEBUG', True)
