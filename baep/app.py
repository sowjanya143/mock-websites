"""
ZXQP Partners Website - Flask Application
A professional investment management firm website built with Flask.
"""
import os
from flask import Flask, render_template

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here')
app.config['DEBUG'] = os.environ.get('DEBUG', 'False') == 'True'


@app.route('/')
def index():
    """Render the main about us page."""
    return render_template('index.html')


@app.route('/about')
def about():
    """Render the about us page (same as index for now)."""
    return render_template('index.html')


@app.errorhandler(404)
def page_not_found(e):
    """Handle 404 errors."""
    return render_template('index.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    """Handle 500 errors."""
    return "Internal server error", 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=app.config['DEBUG'], host='0.0.0.0', port=port, use_reloader=False)
