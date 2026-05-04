"""Hokuyo Bank Flask application."""

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
)

from config import Config

# Create Flask app with template loaders for hokuyo and shared templates
from jinja2 import FileSystemLoader, ChoiceLoader

hokuyo_dir = Path(__file__).parent
shared_dir = hokuyo_dir.parent / 'shared'

loader = ChoiceLoader([
    FileSystemLoader(str(hokuyo_dir / 'templates')),
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
def home():
    """Home page route."""
    return render_template('home.html')


@app.route('/about')
def about():
    """About page route."""
    return render_template('about.html')


@app.route('/leadership')
def leadership():
    """Leadership page with paginated team data."""
    data = load_data()
    page = request.args.get('page', 1, type=int)
    paginated = get_paginated_data(data['team'], page=page, per_page=5)

    return render_template('leadership.html', **paginated)


@app.route('/strategies')
def strategies():
    """Strategies page route."""
    return render_template('strategies.html')


@app.route('/investor-resources')
def investor_resources():
    """Investor resources page route."""
    return render_template('investor_resources.html')


@app.route('/funds')
def funds():
    """Funds page route."""
    return render_template('funds.html')


@app.route('/fund/<int:fund_id>')
def fund_detail(fund_id):
    """Fund detail page route."""
    return render_template('fund_detail.html', fund_id=fund_id)


@app.route('/news')
def news():
    """News page route."""
    return render_template('news.html')


@app.route('/contact')
def contact():
    """Contact page route."""
    return render_template('contact.html')


@app.route('/api/dismiss-popup', methods=['POST'])
def dismiss_popup():
    """Dismiss popup API endpoint."""
    return jsonify({'status': 'ok'})


if __name__ == '__main__':
    app.run(debug=Config.DEBUG, port=5003)
