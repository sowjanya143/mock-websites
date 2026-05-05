"""Application entry point."""
import os
from app import create_app

# Get configuration from environment variable
config_name = os.environ.get('FLASK_CONFIG', 'default')
app = create_app(config_name)

if __name__ == '__main__':
    # Run the application
    app.run(
        host='0.0.0.0',
        port=int(os.environ.get('PORT', 5000)),
        debug=app.config['DEBUG']
    )
