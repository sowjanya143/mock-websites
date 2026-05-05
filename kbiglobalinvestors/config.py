"""Application configuration."""
import os


class Config:
    """Base configuration."""
    
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Email configuration (for future use)
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER', 'noreply@gip-test.com')


class DevelopmentConfig(Config):
    """Development configuration."""
    
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """Production configuration."""
    
    DEBUG = False
    TESTING = False


class TestingConfig(Config):
    """Testing configuration."""
    
    DEBUG = True
    TESTING = True


class DefaultConfig(DevelopmentConfig):
    """Default configuration (uses development settings)."""
    pass
