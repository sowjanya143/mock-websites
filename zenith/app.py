"""Zenith Asset Management Flask application - Most Complex Site."""

import base64
import json
import os
import sys
import time
from functools import wraps
from pathlib import Path

from flask import Flask, jsonify, render_template, request, session, redirect, url_for

# Add parent directory to path to import utils
parent_dir = str(Path(__file__).parent.parent)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from utils import (
    generate_captcha,
    generate_dynamic_aum,
    generate_team,
    get_paginated_data,
    rate_limit,
    render_popup,
    should_show_popup,
    validate_captcha,
    inject_js_routes,
    inject_user_agent_middleware,
    inject_headers_middleware,
    require_javascript,
    require_cookie_acceptance,
    inject_cookie_banner_routes,
)

from config import Config

# Create Flask app with template loaders for zenith and shared templates
from jinja2 import FileSystemLoader, ChoiceLoader

zenith_dir = Path(__file__).parent
shared_dir = zenith_dir.parent / 'shared'

loader = ChoiceLoader([
    FileSystemLoader(str(zenith_dir / 'templates')),
    FileSystemLoader(str(shared_dir / 'templates')),
])

app = Flask(__name__, template_folder=None)
app.jinja_loader = loader
app.config.from_object(Config)
app.secret_key = Config.SECRET_KEY

# Inject global middleware for security features
inject_user_agent_middleware(app)
inject_headers_middleware(app)
inject_js_routes(app)


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
        aum_data = {'global_aum': 290000000000}

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


def require_captcha_for_page(current_path):
    """
    Check if the current path requires CAPTCHA.

    Args:
        current_path (str): The request path

    Returns:
        bool: True if CAPTCHA is required for this path
    """
    # Check exact matches
    if current_path in Config.CAPTCHA_REQUIRED_PAGES:
        return True

    # Check for fund detail pages (/fund/<id>)
    if current_path.startswith('/fund/') and '/fund/<id>' in Config.CAPTCHA_REQUIRED_PAGES:
        return True

    return False


def require_captcha(f):
    """
    Decorator to require CAPTCHA validation before accessing a route.

    Handles both first-visit CAPTCHA and data page CAPTCHA.
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        current_path = request.path

        # Check if first visit CAPTCHA is required
        if Config.CAPTCHA_FIRST_VISIT and 'visited' not in session:
            captcha_image = generate_captcha()
            captcha_base64 = base64.b64encode(captcha_image).decode('utf-8')
            return render_template('captcha.html', captcha_image=captcha_base64)

        # Check if data page CAPTCHA is required
        if Config.CAPTCHA_DATA_PAGES and require_captcha_for_page(current_path):
            if 'captcha_passed' not in session:
                captcha_image = generate_captcha()
                captcha_base64 = base64.b64encode(captcha_image).decode('utf-8')
                return render_template('captcha.html', captcha_image=captcha_base64)

        # CAPTCHA passed or not required, proceed with original route
        return f(*args, **kwargs)

    return decorated_function


@app.before_request
def before_request():
    """
    Process before each request.

    1. Add artificial delay (0.5 seconds)
    2. Check for CAPTCHA submission
    3. Set visited flag on first page load
    """
    # Add artificial delay to simulate slow responses
    time.sleep(Config.ARTIFICIAL_DELAY)

    # Check for CAPTCHA submission before request processing
    if request.method == 'POST' and 'captcha_answer' in request.form:
        user_answer = request.form.get('captcha_answer', '').strip()

        if validate_captcha(user_answer):
            session['captcha_passed'] = True
            session['visited'] = True
            # Mark popup as shown if this is first visit
            if 'data_page_popup_shown' not in session:
                session['data_page_popup_shown'] = False
            referrer = request.referrer or url_for('home')
            return redirect(referrer)
        else:
            # CAPTCHA validation failed
            return jsonify({'status': 'error', 'message': 'Invalid CAPTCHA'}), 403

    # Mark as visited on any first GET request
    if request.method == 'GET':
        if 'visited' not in session:
            session['visited'] = True


@app.context_processor
def inject_globals():
    """
    Inject global data into all templates.

    Provides company name, AUM data, team data, news data, and popup data.
    """
    data = load_data()

    # Generate popup for sticky footer on data pages if enabled
    popup_data = None
    if Config.SHOW_POPUPS and should_show_popup('data_page'):
        popup_data = render_popup(
            'newsletter',
            auto_dismiss=Config.AUTO_DISMISS_POPUP,
            dismiss_delay=Config.AUTO_DISMISS_DELAY
        )

    return {
        'company_name': Config.COMPANY_NAME,
        'global_aum': Config.GLOBAL_AUM,
        'aum_data': data['aum'],
        'team_data': data['team'],
        'news_data': data['news'],
        'popup_data': popup_data,
        'popup_type': Config.POPUP_TYPE,
    }


@app.route('/')
@rate_limit(Config.MAX_REQUESTS, Config.TIME_WINDOW)
@require_captcha
@require_javascript
def home():
    """Home page route."""
    return render_template('home.html')


@app.route('/about')
@rate_limit(Config.MAX_REQUESTS, Config.TIME_WINDOW)
@require_captcha
@require_javascript
def about():
    """About page route."""
    return render_template('about.html')


@app.route('/leadership')
@rate_limit(Config.MAX_REQUESTS, Config.TIME_WINDOW)
@require_captcha
@require_javascript
def leadership():
    """Leadership page with paginated team data."""
    data = load_data()
    page = request.args.get('page', 1, type=int)
    paginated = get_paginated_data(data['team'], page=page, per_page=5)

    return render_template('leadership.html', **paginated)


@app.route('/team')
@rate_limit(Config.MAX_REQUESTS, Config.TIME_WINDOW)
@require_captcha
@require_javascript
def team():
    """Team page with paginated team data."""
    data = load_data()
    page = request.args.get('page', 1, type=int)
    paginated = get_paginated_data(data['team'], page=page, per_page=5)

    return render_template('leadership.html', **paginated)


@app.route('/strategies')
@rate_limit(Config.MAX_REQUESTS, Config.TIME_WINDOW)
@require_captcha
@require_javascript
def strategies():
    """Strategies page route."""
    return render_template('strategies.html')


@app.route('/investor-resources')
@rate_limit(Config.MAX_REQUESTS, Config.TIME_WINDOW)
@require_captcha
@require_javascript
def investor_resources():
    """Investor resources page route."""
    return render_template('investor_resources.html')


@app.route('/funds')
@rate_limit(Config.MAX_REQUESTS, Config.TIME_WINDOW)
@require_captcha
@require_javascript
def funds():
    """Funds page route."""
    return render_template('funds.html')


@app.route('/fund/<int:fund_id>')
@rate_limit(Config.MAX_REQUESTS, Config.TIME_WINDOW)
@require_captcha
@require_javascript
def fund_detail(fund_id):
    """Fund detail page route."""
    return render_template('fund_detail.html', fund_id=fund_id)


@app.route('/news')
@rate_limit(Config.MAX_REQUESTS, Config.TIME_WINDOW)
@require_captcha
@require_javascript
def news():
    """News page route."""
    return render_template('news.html')


@app.route('/contact')
@rate_limit(Config.MAX_REQUESTS, Config.TIME_WINDOW)
@require_captcha
@require_javascript
def contact():
    """Contact page route."""
    return render_template('contact.html')


@app.route('/api/funds', methods=['GET'])
@rate_limit(Config.MAX_REQUESTS, Config.TIME_WINDOW)
@require_javascript
def api_funds():
    """
    API endpoint for funds data in JSON format.

    This simulates AJAX-loaded content on the funds page.
    Returns JSON with fund list.
    """
    data = load_data()
    aum_data = data['aum']

    return jsonify({
        'funds': aum_data.get('by_fund', []),
        'total_aum': aum_data.get('global_aum', 290000000000),
    })


@app.route('/api/dismiss-popup', methods=['POST'])
@require_javascript
def dismiss_popup():
    """Dismiss popup API endpoint."""
    from utils import mark_popup_dismissed
    mark_popup_dismissed()
    return jsonify({'status': 'ok'})



@app.route('/aum')
def aum_blocked():
    """AUM data access is blocked."""
    return jsonify({'error': 'Access denied'}), 403


@app.route('/robots.txt')
def robots():
    """Return robots.txt with misdirection."""
    robots_content = '''User-agent: *
Disallow: /
Disallow: /api
Crawl-delay: 999999
Sitemap: /fake-sitemap.xml
'''
    return robots_content, 200, {'Content-Type': 'text/plain'}


if __name__ == '__main__':
    app.run(debug=Config.DEBUG, host='0.0.0.0', port=int(os.environ.get('PORT', 5004)))
