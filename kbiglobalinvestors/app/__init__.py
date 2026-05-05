"""Flask application initialization."""
from flask import Flask


def create_app(config_name='default'):
    """
    Application factory pattern.
    
    Args:
        config_name: Configuration to use (default, development, production)
        
    Returns:
        Flask application instance
    """
    app = Flask(__name__)
    app.config.from_object(f'config.{config_name.capitalize()}Config')
    
    # Register blueprints
    from app.routes import main
    app.register_blueprint(main.bp)
    
    return app
