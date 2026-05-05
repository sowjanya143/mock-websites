"""Nexus Capital Flask application - Bot detection emphasis."""

import json
import os
import sys
import time
from pathlib import Path

from flask import Flask, jsonify, render_template, request, session

parent_dir = str(Path(__file__).parent.parent)
current_dir = str(Path(__file__).parent)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from utils import (
    generate_dynamic_aum,
    generate_team,
    get_paginated_data,
    inject_js_routes,
    inject_user_agent_middleware,
    inject_headers_middleware,
    require_javascript,
    require_cookie_acceptance,
    inject_cookie_banner_routes,
    rate_limit,
    inject_honeypot_fields,
    validate_form_submission,
)

from config import Config

from jinja2 import FileSystemLoader, ChoiceLoader

nexus_dir = Path(__file__).parent
shared_dir = nexus_dir.parent / 'shared'

loader = ChoiceLoader([
    FileSystemLoader(str(nexus_dir / 'templates')),
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


@app.before_request
def apply_artificial_delay():
    """Apply slight artificial delay to bot detection."""
    time.sleep(Config.ARTIFICIAL_DELAY)


@app.context_processor
def inject_globals():
    """Inject global data into all templates."""
    data = load_data()
    honeypot = inject_honeypot_fields(session) if Config.HONEYPOT_ENABLED else None
    return {
        'company_name': Config.COMPANY_NAME,
        'global_aum': Config.GLOBAL_AUM,
        'aum_data': data['aum'],
        'team_data': data['team'],
        'news_data': data['news'],
        'honeypot': honeypot,
    }


@app.route('/')
@require_javascript
@require_cookie_acceptance(mode='optional')
@rate_limit(Config.MAX_REQUESTS, Config.TIME_WINDOW)
def home():
    """Home page route."""
    return render_template('home.html')


@app.route('/about')
@require_javascript
@require_cookie_acceptance(mode='optional')
@rate_limit(Config.MAX_REQUESTS, Config.TIME_WINDOW)
def about():
    """About page route."""
    return render_template('about.html')


@app.route('/leadership')
@require_javascript
@require_cookie_acceptance(mode='optional')
@rate_limit(Config.MAX_REQUESTS, Config.TIME_WINDOW)
def leadership():
    """Leadership page with paginated team data."""
    data = load_data()
    page = request.args.get('page', 1, type=int)
    paginated = get_paginated_data(data['team'], page=page, per_page=5)
    return render_template('leadership.html', **paginated)


@app.route('/strategies')
@require_javascript
@require_cookie_acceptance(mode='optional')
@rate_limit(Config.MAX_REQUESTS, Config.TIME_WINDOW)
def strategies():
    """Strategies page route."""
    return render_template('strategies.html')


@app.route('/investor-resources')
@require_javascript
@require_cookie_acceptance(mode='optional')
@rate_limit(Config.MAX_REQUESTS, Config.TIME_WINDOW)
def investor_resources():
    """Investor resources page route."""
    return render_template('investor_resources.html')


@app.route('/funds')
@require_javascript
@require_cookie_acceptance(mode='optional')
@rate_limit(Config.MAX_REQUESTS, Config.TIME_WINDOW)
def funds():
    """Funds page route."""
    return render_template('funds.html')


@app.route('/fund/<int:fund_id>')
@require_javascript
@require_cookie_acceptance(mode='optional')
@rate_limit(Config.MAX_REQUESTS, Config.TIME_WINDOW)
def fund_detail(fund_id):
    """Fund detail page route."""
    return render_template('fund_detail.html', fund_id=fund_id)


@app.route('/news')
@require_javascript
@require_cookie_acceptance(mode='optional')
@rate_limit(Config.MAX_REQUESTS, Config.TIME_WINDOW)
def news():
    """News page route."""
    return render_template('news.html')


@app.route('/contact', methods=['GET', 'POST'])
@require_javascript
@require_cookie_acceptance(mode='optional')
@rate_limit(Config.MAX_REQUESTS, Config.TIME_WINDOW)
def contact():
    """Contact page route with honeypot detection."""
    if request.method == 'POST':
        # Check if honeypot filled (bot detection)
        if not validate_form_submission(request.form, session):
            return jsonify({'error': 'Invalid submission'}), 403
        return jsonify({'status': 'ok', 'message': 'Thank you for contacting us'}), 200

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
Crawl-delay: 999999
'''
    return robots_content, 200, {'Content-Type': 'text/plain'}


@app.route('/api/dismiss-popup', methods=['POST'])
def dismiss_popup():
    """Dismiss popup API endpoint."""
    return jsonify({'status': 'ok'})


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5006))
    app.run(debug=Config.DEBUG, host='0.0.0.0', port=port)
