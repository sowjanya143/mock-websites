"""Fortress Investment Group Flask application."""

import base64
import json
import os
import sys
from functools import wraps
from pathlib import Path

from flask import Flask, jsonify, render_template, request, session

# Add parent directory to path to import utils
parent_dir = str(Path(__file__).parent.parent)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from utils import (
    generate_captcha,
    generate_dynamic_aum,
    generate_team,
    get_paginated_data,
    validate_captcha,
)

from config import Config

# Create Flask app with template loaders for fortress and shared templates
from jinja2 import FileSystemLoader, ChoiceLoader

fortress_dir = Path(__file__).parent
shared_dir = fortress_dir.parent / 'shared'

loader = ChoiceLoader([
    FileSystemLoader(str(fortress_dir / 'templates')),
    FileSystemLoader(str(shared_dir / 'templates')),
])

app = Flask(__name__, template_folder=None)
app.jinja_loader = loader
app.config.from_object(Config)
app.secret_key = Config.SECRET_KEY


def load_data():
    """
    Load financial data from JSON files.

    Returns:
        dict: Dictionary with keys: aum, team, news
    """
    data_dir = Path(__file__).parent / 'data'

    # Load and process AUM data
    aum_file = data_dir / 'aum.json'
    if aum_file.exists():
        with open(aum_file, 'r') as f:
            aum_data = json.load(f)
        aum_data = generate_dynamic_aum(aum_data)
    else:
        aum_data = {'total_aum': Config.GLOBAL_AUM}

    # Load and process team data
    team_file = data_dir / 'team.json'
    if team_file.exists():
        with open(team_file, 'r') as f:
            team_data = json.load(f)
        team_data = generate_team(team_data)
    else:
        team_data = []

    # Load news data
    news_file = data_dir / 'news.json'
    if news_file.exists():
        with open(news_file, 'r') as f:
            news_data = json.load(f)
    else:
        news_data = []

    return {
        'aum': aum_data,
        'team': team_data,
        'news': news_data,
    }


def require_captcha(f):
    """
    Decorator to require CAPTCHA validation before accessing a route.

    If CAPTCHA_ON_EVERY_PAGE is enabled and user hasn't passed CAPTCHA,
    render CAPTCHA page instead of the original route.
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if Config.CAPTCHA_ON_EVERY_PAGE and 'captcha_passed' not in session:
            # Generate CAPTCHA and render captcha page
            captcha_image = generate_captcha()
            captcha_base64 = base64.b64encode(captcha_image).decode('utf-8')
            return render_template('captcha.html', captcha_image=captcha_base64)

        # CAPTCHA passed or not required, proceed with original route
        return f(*args, **kwargs)

    return decorated_function


@app.before_request
def check_captcha():
    """
    Check for CAPTCHA submission before request processing.

    If POST request contains captcha_answer field, validate it.
    Set session['captcha_passed'] = True on success.
    Return 403 on failure.
    """
    if request.method == 'POST' and 'captcha_answer' in request.form:
        user_answer = request.form.get('captcha_answer', '').strip()

        if validate_captcha(user_answer):
            session['captcha_passed'] = True
            # Redirect to referrer or home after successful CAPTCHA
            return None
        else:
            # CAPTCHA validation failed
            return jsonify({'status': 'error', 'message': 'Invalid CAPTCHA'}), 403


@app.context_processor
def inject_globals():
    """
    Inject global data into all templates.

    Provides company name, AUM data, team data, and news data.
    """
    data = load_data()

    return {
        'company_name': Config.COMPANY_NAME,
        'global_aum': Config.GLOBAL_AUM,
        'aum_data': data['aum'],
        'team_data': data['team'],
        'news_data': data['news'],
    }


@app.route('/')
@require_captcha
def home():
    """Home page route."""
    return render_template('home.html')


@app.route('/about')
@require_captcha
def about():
    """About page route."""
    return render_template('about.html')


@app.route('/leadership')
@require_captcha
def leadership():
    """Leadership page with paginated team data."""
    data = load_data()
    page = request.args.get('page', 1, type=int)
    paginated = get_paginated_data(data['team'], page=page, per_page=5)

    return render_template('leadership.html', **paginated)


@app.route('/strategies')
@require_captcha
def strategies():
    """Strategies page route."""
    return render_template('strategies.html')


@app.route('/investor-resources')
@require_captcha
def investor_resources():
    """Investor resources page route."""
    return render_template('investor_resources.html')


@app.route('/funds')
@require_captcha
def funds():
    """Funds page route."""
    return render_template('funds.html')


@app.route('/fund/<int:fund_id>')
@require_captcha
def fund_detail(fund_id):
    """Fund detail page route."""
    return render_template('fund_detail.html', fund_id=fund_id)


@app.route('/news')
@require_captcha
def news():
    """News page route."""
    return render_template('news.html')


@app.route('/contact')
@require_captcha
def contact():
    """Contact page route."""
    return render_template('contact.html')


@app.route('/api/dismiss-popup', methods=['POST'])
def dismiss_popup():
    """Dismiss popup API endpoint."""
    return jsonify({'status': 'ok'})


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=Config.DEBUG, host='0.0.0.0', port=port)
