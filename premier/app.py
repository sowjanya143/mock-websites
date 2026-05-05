"""Premier Financial Services Flask application."""

import json
import os
import sys
from pathlib import Path

from flask import Flask, jsonify, render_template, request

# Add parent directory to path to import utils
parent_dir = str(Path(__file__).parent.parent)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from utils import (
    generate_dynamic_aum,
    generate_team,
    get_paginated_data,
    inject_js_routes,
    inject_cookie_middleware,
    inject_user_agent_middleware,
    inject_headers_middleware,
    require_javascript,
    require_cookie_acceptance,
    inject_cookie_banner_routes,
)

from config import Config

# Create Flask app with template loaders for premier and shared templates
from jinja2 import FileSystemLoader, ChoiceLoader

premier_dir = Path(__file__).parent
shared_dir = premier_dir.parent / 'shared'

loader = ChoiceLoader([
    FileSystemLoader(str(premier_dir / 'templates')),
    FileSystemLoader(str(shared_dir / 'templates')),
])

app = Flask(__name__, template_folder=None)
app.jinja_loader = loader
app.config.from_object(Config)
app.secret_key = Config.SECRET_KEY

# Inject global middleware for security features
inject_user_agent_middleware(app)
inject_headers_middleware(app)
inject_cookie_middleware(app)
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
@require_javascript
def home():
    """Home page route."""
    return render_template('home.html')


@app.route('/about')
@require_javascript
def about():
    """About page route."""
    return render_template('about.html')


@app.route('/leadership')
@require_javascript
def leadership():
    """Leadership page with paginated team data."""
    data = load_data()
    page = request.args.get('page', 1, type=int)
    paginated = get_paginated_data(data['team'], page=page, per_page=5)

    return render_template('leadership.html', **paginated)


@app.route('/strategies')
@require_javascript
def strategies():
    """Strategies page route."""
    return render_template('strategies.html')


@app.route('/investor-resources')
@require_javascript
def investor_resources():
    """Investor resources page route."""
    return render_template('investor_resources.html')


@app.route('/funds')
@require_javascript
def funds():
    """Funds page route."""
    return render_template('funds.html')


@app.route('/fund/<int:fund_id>')
@require_javascript
def fund_detail(fund_id):
    """Fund detail page route."""
    return render_template('fund_detail.html', fund_id=fund_id)


@app.route('/news')
@require_javascript
def news():
    """News page route."""
    return render_template('news.html')


@app.route('/contact')
@require_javascript
def contact():
    """Contact page route."""
    return render_template('contact.html')


@app.route('/api/dismiss-popup', methods=['POST'])
@require_javascript
def dismiss_popup():
    """Dismiss popup API endpoint."""
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
    app.run(debug=Config.DEBUG, host='0.0.0.0', port=int(os.environ.get('PORT', 5003)))
