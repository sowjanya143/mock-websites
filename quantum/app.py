"""Quantum Funds Flask application - Geographic blocking."""

import json
import os
import sys
from pathlib import Path

from flask import Flask, jsonify, render_template, request

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
    allow_countries,
    block_vpn,
    inject_geoip_routes,
    get_country_from_ip,
    is_vpn_ip,
)
from utils.geoip_utils import get_client_ip

from config import Config

from jinja2 import FileSystemLoader, ChoiceLoader

quantum_dir = Path(__file__).parent
shared_dir = quantum_dir.parent / 'shared'

loader = ChoiceLoader([
    FileSystemLoader(str(quantum_dir / 'templates')),
    FileSystemLoader(str(shared_dir / 'templates')),
])

app = Flask(__name__, template_folder=None)
app.jinja_loader = loader
app.config.from_object(Config)
app.secret_key = Config.SECRET_KEY

# Inject global middleware
inject_user_agent_middleware(app)
inject_headers_middleware(app)
inject_js_routes(app)
inject_cookie_banner_routes(app, mode=Config.COOKIE_BANNER_MODE)
inject_geoip_routes(app)


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
def check_vpn():
    """Check for VPN access and block if enabled."""
    if Config.BLOCK_VPNS:
        client_ip = get_client_ip(request)
        if is_vpn_ip(client_ip):
            return jsonify({
                'error': 'Access denied',
                'message': 'VPN/proxy access not allowed'
            }), 403


@app.context_processor
def inject_globals():
    """Inject global data into all templates."""
    data = load_data()
    client_ip = request.remote_addr
    country = get_country_from_ip(client_ip)
    return {
        'company_name': Config.COMPANY_NAME,
        'global_aum': Config.GLOBAL_AUM,
        'aum_data': data['aum'],
        'team_data': data['team'],
        'news_data': data['news'],
        'user_country': country,
    }


@app.route('/')
@require_javascript
@require_cookie_acceptance(mode='optional')
@allow_countries(Config.ALLOWED_COUNTRIES)
@block_vpn
@rate_limit(Config.MAX_REQUESTS, Config.TIME_WINDOW)
def home():
    """Home page route."""
    return render_template('home.html')


@app.route('/about')
@require_javascript
@require_cookie_acceptance(mode='optional')
@allow_countries(Config.ALLOWED_COUNTRIES)
@rate_limit(Config.MAX_REQUESTS, Config.TIME_WINDOW)
def about():
    """About page route."""
    return render_template('about.html')


@app.route('/leadership')
@require_javascript
@require_cookie_acceptance(mode='optional')
@allow_countries(Config.ALLOWED_COUNTRIES)
@rate_limit(Config.MAX_REQUESTS, Config.TIME_WINDOW)
def leadership():
    """Leadership page with paginated team data."""
    data = load_data()
    page = request.args.get('page', 1, type=int)
    paginated = get_paginated_data(data['team'], page=page, per_page=5)
    return render_template('leadership.html', **paginated)


@app.route('/team')
@require_javascript
@require_cookie_acceptance(mode='optional')
@allow_countries(Config.ALLOWED_COUNTRIES)
@rate_limit(Config.MAX_REQUESTS, Config.TIME_WINDOW)
def team():
    """Team page with paginated team data."""
    data = load_data()
    page = request.args.get('page', 1, type=int)
    paginated = get_paginated_data(data['team'], page=page, per_page=5)
    return render_template('leadership.html', **paginated)


@app.route('/strategies')
@require_javascript
@require_cookie_acceptance(mode='optional')
@allow_countries(Config.ALLOWED_COUNTRIES)
@rate_limit(Config.MAX_REQUESTS, Config.TIME_WINDOW)
def strategies():
    """Strategies page route."""
    return render_template('strategies.html')


@app.route('/investor-resources')
@require_javascript
@require_cookie_acceptance(mode='optional')
@allow_countries(Config.ALLOWED_COUNTRIES)
@rate_limit(Config.MAX_REQUESTS, Config.TIME_WINDOW)
def investor_resources():
    """Investor resources page route."""
    return render_template('investor_resources.html')


@app.route('/funds')
@require_javascript
@require_cookie_acceptance(mode='optional')
@allow_countries(Config.ALLOWED_COUNTRIES)
@rate_limit(Config.MAX_REQUESTS, Config.TIME_WINDOW)
def funds():
    """Funds page route."""
    return render_template('funds.html')


@app.route('/fund/<int:fund_id>')
@require_javascript
@require_cookie_acceptance(mode='optional')
@allow_countries(Config.ALLOWED_COUNTRIES)
@rate_limit(Config.MAX_REQUESTS, Config.TIME_WINDOW)
def fund_detail(fund_id):
    """Fund detail page route."""
    return render_template('fund_detail.html', fund_id=fund_id)


@app.route('/news')
@require_javascript
@require_cookie_acceptance(mode='optional')
@allow_countries(Config.ALLOWED_COUNTRIES)
@rate_limit(Config.MAX_REQUESTS, Config.TIME_WINDOW)
def news():
    """News page route."""
    return render_template('news.html')


@app.route('/contact')
@require_javascript
@require_cookie_acceptance(mode='optional')
@allow_countries(Config.ALLOWED_COUNTRIES)
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
'''
    return robots_content, 200, {'Content-Type': 'text/plain'}


@app.route('/api/dismiss-popup', methods=['POST'])
def dismiss_popup():
    """Dismiss popup API endpoint."""
    return jsonify({'status': 'ok'})


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5007))
    app.run(debug=Config.DEBUG, host='0.0.0.0', port=port)
