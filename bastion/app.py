"""Bastion Investment Group Flask application."""

import base64
import json
import os
import sys
import time
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
    generate_timed_captcha, validate_timed_captcha,
    generate_class_map, inject_dom_obfuscator,
    rate_limit, inject_js_routes,
    inject_user_agent_middleware, inject_headers_middleware,
    require_javascript, require_cookie_acceptance, inject_cookie_banner_routes,
)
from config import Config
from jinja2 import FileSystemLoader, ChoiceLoader

bastion_dir = Path(__file__).parent
shared_dir = bastion_dir.parent / 'shared'

loader = ChoiceLoader([
    FileSystemLoader(str(bastion_dir / 'templates')),
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

def require_captcha_for_page(current_path):
    """Check if current path requires CAPTCHA."""
    if current_path in Config.CAPTCHA_REQUIRED_PAGES:
        return True
    if current_path.startswith('/what-we-do/') and '/what-we-do' in Config.CAPTCHA_REQUIRED_PAGES:
        return True
    return False

def require_captcha(f):
    """Decorator to require CAPTCHA on data pages."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if require_captcha_for_page(request.path) and 'captcha_passed' not in session:
            captcha_image = generate_timed_captcha(session)
            captcha_base64 = base64.b64encode(captcha_image).decode('utf-8')
            return render_template('captcha.html', captcha_image=captcha_base64)
        return f(*args, **kwargs)
    return decorated

@app.before_request
def check_captcha():
    """Check CAPTCHA submission."""
    if request.method == 'POST' and 'captcha_answer' in request.form:
        answer = request.form.get('captcha_answer', '').strip()
        result = validate_timed_captcha(answer, session, Config.CAPTCHA_TIME_LIMIT)

        if result == 'ok':
            session['captcha_passed'] = True
            return redirect(request.referrer or url_for('home'))
        else:
            return jsonify({'status': 'error', 'message': f'CAPTCHA {result}'}), 403

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
def home():
    return render_template('home.html')

@app.route('/what-we-do')
@rate_limit(Config.MAX_REQUESTS, Config.TIME_WINDOW)
@require_javascript
@require_captcha
def what_we_do():
    return render_template('what_we_do.html')

@app.route('/what-we-do/<slug>')
@rate_limit(Config.MAX_REQUESTS, Config.TIME_WINDOW)
@require_javascript
@require_captcha
def strategy_detail(slug):
    return render_template('strategy_detail.html', slug=slug)

@app.route('/who-we-are')
@rate_limit(Config.MAX_REQUESTS, Config.TIME_WINDOW)
@require_javascript
def who_we_are():
    return render_template('who_we_are.html')

@app.route('/who-we-are/team')
@rate_limit(Config.MAX_REQUESTS, Config.TIME_WINDOW)
@require_javascript
def team():
    data = load_data()
    page = request.args.get('page', 1, type=int)
    paginated = get_paginated_data(data['team'], page=page, per_page=5)
    return render_template('team.html', **paginated)

@app.route('/investors')
@rate_limit(Config.MAX_REQUESTS, Config.TIME_WINDOW)
@require_javascript
@require_captcha
def investors():
    return render_template('investors.html')

@app.route('/financial-advisors')
@rate_limit(Config.MAX_REQUESTS, Config.TIME_WINDOW)
@require_javascript
@require_captcha
def financial_advisors():
    return render_template('financial_advisors.html')

@app.route('/media')
@rate_limit(Config.MAX_REQUESTS, Config.TIME_WINDOW)
@require_javascript
def media():
    return render_template('media.html')

@app.route('/careers')
@rate_limit(Config.MAX_REQUESTS, Config.TIME_WINDOW)
@require_javascript
def careers():
    return render_template('careers.html')

@app.route('/contact')
@rate_limit(Config.MAX_REQUESTS, Config.TIME_WINDOW)
@require_javascript
def contact():
    return render_template('contact.html')

@app.route('/aum')
def aum_blocked():
    return jsonify({'error': 'Access denied'}), 403

@app.route('/robots.txt')
def robots():
    return 'User-agent: *\nDisallow: /\nCrawl-delay: 999999\n', 200, {'Content-Type': 'text/plain'}

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5009))
    app.run(debug=Config.DEBUG, host='0.0.0.0', port=port)
