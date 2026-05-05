"""
ZXQP Partners Website - Flask Application
A professional investment management firm website built with Flask.
"""
from flask import Flask, render_template

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = 'your-secret-key-here'  # Change this in production


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
    app.run(debug=True, host='0.0.0.0', port=5000)
