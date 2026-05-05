"""Fortis Banking Group Flask application - CAPTCHA on data pages."""

import base64
import json
import os
import sys
from pathlib import Path
from functools import wraps

from flask import Flask, jsonify, render_template, request, session, redirect, url_for

parent_dir = str(Path(__file__).parent.parent)
current_dir = str(Path(__file__).parent)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from utils import (
    generate_captcha,
    generate_dynamic_aum,
    generate_team,
    get_paginated_data,
    validate_captcha,
    inject_js_routes,
    inject_user_agent_middleware,
    inject_headers_middleware,
    require_javascript,
    require_cookie_acceptance,
    inject_cookie_banner_routes,
    rate_limit,
)

from config import Config

from jinja2 import FileSystemLoader, ChoiceLoader

fortis_dir = Path(__file__).parent
shared_dir = fortis_dir.parent / 'shared'

loader = ChoiceLoader([
    FileSystemLoader(str(fortis_dir / 'templates')),
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
inject_cookie_banner_routes(app, mode=Config.COOKIE_BANNER_MODE)


def load_data():
    """Load financial data from JSON files."""
    data_dir = Path(__file__).parent / 'data'

    aum_file = data_dir / 'aum.json'
    if aum_file.exists():
        with open(aum_file, 'r') as f:
            aum_data = json.load(f)
        aum_data = generate_dynamic_aum(aum_data)
    else:
        aum_data = {'total_aum': Config.GLOBAL_AUM}

    team_file = data_dir / 'team.json'
    if team_file.exists():
        with open(team_file, 'r') as f:
            team_data = json.load(f)
        team_data = generate_team(team_data)
    else:
        team_data = []

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
    """Check if current path requires CAPTCHA."""
    if current_path in Config.CAPTCHA_REQUIRED_PAGES:
        return True
    for page in Config.CAPTCHA_REQUIRED_PAGES:
        if page.endswith('<id>'):
            base_path = page.replace('/<id>', '').replace('/<int:fund_id>', '')
            if current_path.startswith(base_path):
                return True
    return False


def require_captcha(f):
    """Decorator to require CAPTCHA validation before accessing route."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if require_captcha_for_page(request.path) and 'captcha_passed' not in session:
            captcha_image = generate_captcha()
            captcha_base64 = base64.b64encode(captcha_image).decode('utf-8')
            return render_template('captcha.html', captcha_image=captcha_base64)
        return f(*args, **kwargs)
    return decorated_function


@app.before_request
def check_captcha():
    """Check CAPTCHA submission."""
    if request.method == 'POST' and 'captcha_answer' in request.form:
        user_answer = request.form.get('captcha_answer', '').strip()
        if validate_captcha(user_answer):
            session['captcha_passed'] = True
            referrer = request.referrer or url_for('home')
            return redirect(referrer)
        else:
            return jsonify({'status': 'error', 'message': 'Invalid CAPTCHA'}), 403


@app.context_processor
def inject_globals():
    """Inject global data into all templates."""
    data = load_data()
    return {
        'company_name': Config.COMPANY_NAME,
        'global_aum': Config.GLOBAL_AUM,
        'aum_data': data['aum'],
        'team_data': data['team'],
        'news_data': data['news'],
    }


@app.route('/')
@require_javascript
@require_cookie_acceptance(mode='mandatory')
@rate_limit(Config.MAX_REQUESTS, Config.TIME_WINDOW)
def home():
    """Home page route."""
    return render_template('home.html')


@app.route('/about')
@require_javascript
@require_cookie_acceptance(mode='mandatory')
@rate_limit(Config.MAX_REQUESTS, Config.TIME_WINDOW)
def about():
    """About page route."""
    return render_template('about.html')


@app.route('/leadership')
@require_javascript
@require_cookie_acceptance(mode='mandatory')
@rate_limit(Config.MAX_REQUESTS, Config.TIME_WINDOW)
def leadership():
    """Leadership page with paginated team data."""
    data = load_data()
    page = request.args.get('page', 1, type=int)
    paginated = get_paginated_data(data['team'], page=page, per_page=5)
    return render_template('leadership.html', **paginated)


@app.route('/strategies')
@require_javascript
@require_cookie_acceptance(mode='mandatory')
@require_captcha
@rate_limit(Config.MAX_REQUESTS, Config.TIME_WINDOW)
def strategies():
    """Strategies page route."""
    return render_template('strategies.html')


@app.route('/investor-resources')
@require_javascript
@require_cookie_acceptance(mode='mandatory')
@require_captcha
@rate_limit(Config.MAX_REQUESTS, Config.TIME_WINDOW)
def investor_resources():
    """Investor resources page route."""
    return render_template('investor_resources.html')


@app.route('/funds')
@require_javascript
@require_cookie_acceptance(mode='mandatory')
@require_captcha
@rate_limit(Config.MAX_REQUESTS, Config.TIME_WINDOW)
def funds():
    """Funds page route."""
    return render_template('funds.html')


@app.route('/fund/<int:fund_id>')
@require_javascript
@require_cookie_acceptance(mode='mandatory')
@require_captcha
@rate_limit(Config.MAX_REQUESTS, Config.TIME_WINDOW)
def fund_detail(fund_id):
    """Fund detail page route."""
    return render_template('fund_detail.html', fund_id=fund_id)


@app.route('/news')
@require_javascript
@require_cookie_acceptance(mode='mandatory')
@rate_limit(Config.MAX_REQUESTS, Config.TIME_WINDOW)
def news():
    """News page route."""
    return render_template('news.html')


@app.route('/contact')
@require_javascript
@require_cookie_acceptance(mode='mandatory')
@rate_limit(Config.MAX_REQUESTS, Config.TIME_WINDOW)
def contact():
    """Contact page route."""
    return render_template('contact.html')


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
Disallow: /admin

User-agent: Googlebot
Disallow: /api
Allow: /

Crawl-delay: 999999
Sitemap: /fake-sitemap.xml
'''
    return robots_content, 200, {'Content-Type': 'text/plain'}


@app.route('/api/dismiss-popup', methods=['POST'])
def dismiss_popup():
    """Dismiss popup API endpoint."""
    return jsonify({'status': 'ok'})


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5005))
    app.run(debug=Config.DEBUG, host='0.0.0.0', port=port)
