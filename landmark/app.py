"""Landmark Property Advisors Flask application."""

import json
import os
import sys
from functools import wraps
from pathlib import Path

from flask import Flask, jsonify, render_template, request, session, redirect, url_for

parent_dir = str(Path(__file__).parent.parent)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Add current directory to path for config import
current_dir = str(Path(__file__).parent)
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from utils import (
    generate_dynamic_aum, generate_team, get_paginated_data,
    generate_class_map, inject_dom_obfuscator,
    rate_limit, inject_js_routes,
    inject_user_agent_middleware, inject_headers_middleware,
    require_javascript, require_cookie_acceptance, inject_cookie_banner_routes,
    require_token, inject_token_routes,
    require_fingerprint, inject_fingerprint_routes,
)
from config import Config
from jinja2 import FileSystemLoader, ChoiceLoader

landmark_dir = Path(__file__).parent
shared_dir = landmark_dir.parent / 'shared'

loader = ChoiceLoader([
    FileSystemLoader(str(landmark_dir / 'templates')),
    FileSystemLoader(str(shared_dir / 'templates')),
])

app = Flask(__name__, template_folder=None)
app.jinja_loader = loader
app.config.from_object(Config)
app.secret_key = Config.SECRET_KEY

# Inject middleware
inject_user_agent_middleware(app)
inject_headers_middleware(app)
inject_js_routes(app)
inject_cookie_banner_routes(app, mode=Config.COOKIE_BANNER_MODE)
inject_dom_obfuscator(app)

# Inject token and fingerprint routes
inject_token_routes(app, Config.TOKEN_PAGE_LIMIT)
inject_fingerprint_routes(app)

def load_data():
    """Load financial data from JSON files."""
    data_dir = Path(__file__).parent / 'data'

    aum_file = data_dir / 'aum.json'
    if aum_file.exists():
        with open(aum_file) as f:
            aum_data = json.load(f)
        aum_data = generate_dynamic_aum(aum_data)
    else:
        aum_data = {'global_aum': Config.GLOBAL_AUM}

    team_file = data_dir / 'team.json'
    team_data = json.load(open(team_file)) if team_file.exists() else []
    team_data = generate_team(team_data)

    news_file = data_dir / 'news.json'
    news_data = json.load(open(news_file)) if news_file.exists() else []

    return {'aum': aum_data, 'team': team_data, 'news': news_data}

@app.context_processor
def inject_globals():
    """Inject global data into templates."""
    data = load_data()
    return {
        'company_name': Config.COMPANY_NAME,
        'global_aum': Config.GLOBAL_AUM,
        'aum_data': data['aum'],
        'team_data': data['team'],
        'news_data': data['news'],
    }

@app.route('/')
@rate_limit(Config.MAX_REQUESTS, Config.TIME_WINDOW)
@require_javascript
@require_fingerprint
@require_token(Config.TOKEN_PAGE_LIMIT)
def home():
    return render_template('home.html')

@app.route('/landmark-difference')
@rate_limit(Config.MAX_REQUESTS, Config.TIME_WINDOW)
@require_javascript
@require_fingerprint
@require_token(Config.TOKEN_PAGE_LIMIT)
def landmark_difference():
    return render_template('landmark_difference.html')

@app.route('/investment-strategies')
@rate_limit(Config.MAX_REQUESTS, Config.TIME_WINDOW)
@require_javascript
@require_fingerprint
@require_token(Config.TOKEN_PAGE_LIMIT)
def investment_strategies():
    return render_template('investment_strategies.html')

@app.route('/investment-strategies/private-equity-re')
@rate_limit(Config.MAX_REQUESTS, Config.TIME_WINDOW)
@require_javascript
@require_fingerprint
@require_token(Config.TOKEN_PAGE_LIMIT)
def private_equity_re():
    return render_template('investment_strategies/private_equity_re.html')

@app.route('/investment-strategies/private-debt-re')
@rate_limit(Config.MAX_REQUESTS, Config.TIME_WINDOW)
@require_javascript
@require_fingerprint
@require_token(Config.TOKEN_PAGE_LIMIT)
def private_debt_re():
    return render_template('investment_strategies/private_debt_re.html')

@app.route('/investment-strategies/public-equity-re')
@rate_limit(Config.MAX_REQUESTS, Config.TIME_WINDOW)
@require_javascript
@require_fingerprint
@require_token(Config.TOKEN_PAGE_LIMIT)
def public_equity_re():
    return render_template('investment_strategies/public_equity_re.html')

@app.route('/investment-strategies/<slug>')
@rate_limit(Config.MAX_REQUESTS, Config.TIME_WINDOW)
@require_javascript
@require_fingerprint
@require_token(Config.TOKEN_PAGE_LIMIT)
def strategy_detail(slug):
    return render_template('strategy_detail.html', slug=slug)

@app.route('/about')
@rate_limit(Config.MAX_REQUESTS, Config.TIME_WINDOW)
@require_javascript
@require_fingerprint
@require_token(Config.TOKEN_PAGE_LIMIT)
def about():
    return render_template('about.html')

@app.route('/about/team')
@rate_limit(Config.MAX_REQUESTS, Config.TIME_WINDOW)
@require_javascript
@require_fingerprint
@require_token(Config.TOKEN_PAGE_LIMIT)
def team():
    data = load_data()
    page = request.args.get('page', 1, type=int)
    paginated = get_paginated_data(data['team'], page=page, per_page=5)
    return render_template('team.html', **paginated)

@app.route('/about/sustainability')
@rate_limit(Config.MAX_REQUESTS, Config.TIME_WINDOW)
@require_javascript
@require_fingerprint
@require_token(Config.TOKEN_PAGE_LIMIT)
def sustainability():
    return render_template('sustainability.html')

@app.route('/news')
@rate_limit(Config.MAX_REQUESTS, Config.TIME_WINDOW)
@require_javascript
@require_fingerprint
@require_token(Config.TOKEN_PAGE_LIMIT)
def news():
    return render_template('news.html')

@app.route('/careers')
@rate_limit(Config.MAX_REQUESTS, Config.TIME_WINDOW)
@require_javascript
@require_fingerprint
@require_token(Config.TOKEN_PAGE_LIMIT)
def careers():
    return render_template('careers.html')

@app.route('/contact')
@rate_limit(Config.MAX_REQUESTS, Config.TIME_WINDOW)
@require_javascript
@require_fingerprint
@require_token(Config.TOKEN_PAGE_LIMIT)
def contact():
    return render_template('contact.html')

@app.route('/robots.txt')
def robots():
    return 'User-agent: *\nDisallow: /\nCrawl-delay: 999999\n', 200, {'Content-Type': 'text/plain'}

if __name__ == '__main__':
    port = int(os.environ.get('PORT', Config.PORT))
    app.run(debug=Config.DEBUG, host='0.0.0.0', port=port)
