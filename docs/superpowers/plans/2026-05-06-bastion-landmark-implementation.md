# Bastion & Landmark Mock Websites — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build 2 new independently deployable Flask mock financial websites (Bastion Investment Group, Landmark Property Advisors) with new anti-scraping behaviors, fortress.com/heitman.com visual replicas, and complete page structures.

**Architecture:** 4 new shared utility modules (`dom_obfuscator`, `timed_captcha`, `session_token`, `fingerprint`) + 2 independent Flask apps (bastion/, landmark/) each with 11 pages, site-specific CSS, and data files. All sites inherit 6 global security layers from existing utils.

**Tech Stack:** Flask 3.0+, Jinja2, Pillow, Python 3.10+, JSON data files, Git Bash for execution.

---

## Phase 1: New Shared Utilities

### Task 1: Create `utils/dom_obfuscator.py`

**Files:**
- Create: `utils/dom_obfuscator.py`

- [ ] **Step 1: Write failing test for `generate_class_map`**

```python
# tests/test_dom_obfuscator.py
import pytest
from flask import session
from utils.dom_obfuscator import generate_class_map

def test_generate_class_map_creates_random_strings():
    """Test that class map generates 5-char random strings."""
    with app.test_request_context():
        result = generate_class_map(session)
        assert isinstance(result, dict)
        assert 'aum-value' in result
        assert len(result['aum-value']) == 5
        assert result['aum-value'].isalnum()

def test_generate_class_map_returns_existing():
    """Test that existing map is returned unchanged."""
    with app.test_request_context():
        result1 = generate_class_map(session)
        result2 = generate_class_map(session)
        assert result1 == result2
```

- [ ] **Step 2: Implement `utils/dom_obfuscator.py`**

```python
"""DOM obfuscation - randomizes CSS class names per session."""

import random
import string
from flask import session

def generate_class_map(sess):
    """Generate mapping of semantic class names to random 5-char strings.
    
    Returns existing map if already in session.
    
    Args:
        sess: Flask session object
        
    Returns:
        dict: {semantic_name: random_5char}
    """
    if 'class_map' in sess:
        return sess['class_map']
    
    class_map = {
        'aum-value': ''.join(random.choices(string.ascii_lowercase + string.digits, k=5)),
        'fund-name': ''.join(random.choices(string.ascii_lowercase + string.digits, k=5)),
        'strategy-title': ''.join(random.choices(string.ascii_lowercase + string.digits, k=5)),
        'data-table': ''.join(random.choices(string.ascii_lowercase + string.digits, k=5)),
        'aum-stat': ''.join(random.choices(string.ascii_lowercase + string.digits, k=5)),
    }
    
    sess['class_map'] = class_map
    return class_map


def inject_dom_obfuscator(app):
    """Inject class_map into all templates via context processor."""
    
    @app.context_processor
    def inject_class_map():
        class_map = generate_class_map(session)
        return {'class_map': class_map}
```

- [ ] **Step 3: Run test**

```bash
cd c:/Users/vboddeti/sandbox/mock-website
python -m pytest tests/test_dom_obfuscator.py -v
```

Expected: PASS

- [ ] **Step 4: Commit**

```bash
git add utils/dom_obfuscator.py tests/test_dom_obfuscator.py
git commit -m "feat: add DOM obfuscation utility for class name randomization"
```

---

### Task 2: Create `utils/timed_captcha.py`

**Files:**
- Create: `utils/timed_captcha.py`

- [ ] **Step 1: Implement `utils/timed_captcha.py`**

```python
"""Timed CAPTCHA - CAPTCHA with 30-second expiry."""

import time
from flask import session
from utils.captcha import generate_captcha, validate_captcha

def generate_timed_captcha(sess):
    """Generate CAPTCHA and store issue timestamp.
    
    Args:
        sess: Flask session object
        
    Returns:
        bytes: CAPTCHA image PNG
    """
    captcha_image = generate_captcha()
    sess['captcha_issued_at'] = time.time()
    return captcha_image


def validate_timed_captcha(answer, sess, time_limit=30):
    """Validate CAPTCHA answer with time limit.
    
    Args:
        answer (str): User's answer
        sess: Flask session object
        time_limit (int): Seconds allowed (default 30)
        
    Returns:
        str: 'ok', 'expired', or 'invalid'
    """
    issued_at = sess.get('captcha_issued_at')
    if not issued_at:
        return 'invalid'
    
    elapsed = time.time() - issued_at
    if elapsed > time_limit:
        return 'expired'
    
    is_valid = validate_captcha(answer)
    return 'ok' if is_valid else 'invalid'
```

- [ ] **Step 2: Commit**

```bash
git add utils/timed_captcha.py
git commit -m "feat: add timed CAPTCHA utility with 30s expiry"
```

---

### Task 3: Create `utils/session_token.py`

**Files:**
- Create: `utils/session_token.py`

- [ ] **Step 1: Implement `utils/session_token.py`**

```python
"""Rotating session tokens - tokens expire after N page views."""

import uuid
from functools import wraps
from flask import session, redirect, url_for

def issue_token(sess, page_limit=5):
    """Issue a new session token and reset page count.
    
    Args:
        sess: Flask session object
        page_limit (int): Pages allowed before token expires
        
    Returns:
        str: UUID token
    """
    token = str(uuid.uuid4())
    sess['page_token'] = token
    sess['page_count'] = 0
    return token


def validate_token(sess, page_limit=5):
    """Validate and increment token page count.
    
    Returns False if token expired (page_count >= page_limit).
    
    Args:
        sess: Flask session object
        page_limit (int): Pages allowed
        
    Returns:
        bool: True if valid, False if expired
    """
    if 'page_token' not in sess:
        return False
    
    sess['page_count'] = sess.get('page_count', 0) + 1
    
    if sess['page_count'] >= page_limit:
        del sess['page_token']
        sess['token_expired'] = True
        return False
    
    return True


def require_token(page_limit=5):
    """Decorator to enforce token validation on routes."""
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if not validate_token(session, page_limit):
                return redirect(url_for('refresh_token'))
            return f(*args, **kwargs)
        return decorated
    return decorator


def inject_token_routes(app, page_limit=5):
    """Register /refresh-token route."""
    
    @app.route('/refresh-token')
    def refresh_token():
        issue_token(session, page_limit)
        return redirect(session.get('HTTP_REFERER', '/'))
```

- [ ] **Step 2: Commit**

```bash
git add utils/session_token.py
git commit -m "feat: add rotating session token utility"
```

---

### Task 4: Create `utils/fingerprint.py`

**Files:**
- Create: `utils/fingerprint.py`

- [ ] **Step 1: Implement `utils/fingerprint.py`**

```python
"""Canvas fingerprint blocking - detects headless browsers."""

from functools import wraps
from flask import session, render_template, request, jsonify

# Known headless browser canvas fingerprints
BLOCKED_FINGERPRINTS = {
    'puppeteer_default_hash',
    'playwright_default_hash',
    '00d41e2f2721cdcd',  # Puppeteer common
    '00000000000000000000000000000000',  # Headless generic
}


def inject_fingerprint_routes(app):
    """Register /verify-fingerprint endpoint."""
    
    @app.route('/verify-fingerprint', methods=['POST'])
    def verify_fingerprint():
        """Verify canvas fingerprint - block known headless hashes."""
        data = request.get_json() or {}
        fingerprint_hash = data.get('hash', '')
        
        if fingerprint_hash in BLOCKED_FINGERPRINTS:
            return jsonify({'error': 'Browser verification failed'}), 403
        
        session['fp_verified'] = True
        return jsonify({'status': 'ok'}), 200


def require_fingerprint(f):
    """Decorator to require fingerprint verification."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'fp_verified' not in session:
            return render_template('fingerprint_challenge.html')
        return f(*args, **kwargs)
    return decorated
```

- [ ] **Step 2: Commit**

```bash
git add utils/fingerprint.py
git commit -m "feat: add canvas fingerprint blocking utility"
```

---

### Task 5: Update `utils/__init__.py`

**Files:**
- Modify: `utils/__init__.py`

- [ ] **Step 1: Add imports and exports**

```python
# At top of file, add:
from utils.dom_obfuscator import generate_class_map, inject_dom_obfuscator
from utils.timed_captcha import generate_timed_captcha, validate_timed_captcha
from utils.session_token import issue_token, validate_token, require_token, inject_token_routes
from utils.fingerprint import inject_fingerprint_routes, require_fingerprint

# In __all__, add:
'generate_class_map',
'inject_dom_obfuscator',
'generate_timed_captcha',
'validate_timed_captcha',
'issue_token',
'validate_token',
'require_token',
'inject_token_routes',
'inject_fingerprint_routes',
'require_fingerprint',
```

- [ ] **Step 2: Commit**

```bash
git add utils/__init__.py
git commit -m "feat: export new utility modules from utils package"
```

---

## Phase 2: Bastion Investment Group (Port 5009)

### Task 6: Create Bastion directory structure and config

**Files:**
- Create: `bastion/`
- Create: `bastion/config.py`
- Create: `bastion/data/aum.json`
- Create: `bastion/data/team.json`
- Create: `bastion/data/news.json`

- [ ] **Step 1: Create bastion/config.py**

```python
"""Bastion Investment Group site configuration."""

import os

class Config:
    """Configuration for Bastion Investment Group."""
    
    COMPANY_NAME = 'Bastion Investment Group'
    SITE_NAME = 'bastion'
    SECRET_KEY = os.environ.get('SECRET_KEY', 'bastion-dev-key-55555')
    
    # CAPTCHA (timed, on data pages only)
    CAPTCHA_ON_EVERY_PAGE = False
    CAPTCHA_REQUIRED_PAGES = ['/what-we-do', '/investors', '/financial-advisors']
    TIMED_CAPTCHA = True
    CAPTCHA_TIME_LIMIT = 30
    
    # DOM obfuscation
    DOM_OBFUSCATION = True
    
    # Rate limiting (10 req/60s)
    RATE_LIMIT_ENABLED = True
    MAX_REQUESTS = 10
    TIME_WINDOW = 60
    
    # Cookie banner
    COOKIE_BANNER_MODE = 'optional'
    
    # Data
    GLOBAL_AUM = '$55,000,000,000'
    DATA_LAYOUT = 'js_tables'
    
    DEBUG = os.environ.get('DEBUG', True)
```

- [ ] **Step 2: Create bastion/data/aum.json**

```json
{
  "global_aum": "$55,000,000,000",
  "by_strategy": {
    "Corporate Credit": "$12,000,000,000",
    "Asset-Based Finance": "$10,000,000,000",
    "Real Estate": "$9,000,000,000",
    "Private Equity": "$11,000,000,000",
    "Insurance Solutions": "$7,000,000,000",
    "Multi-Manager": "$6,000,000,000"
  },
  "by_fund": [
    {"id": 1, "name": "Bastion Credit Opportunities Fund", "aum": "$8,000,000,000", "strategy": "Corporate Credit"},
    {"id": 2, "name": "Bastion Asset Finance Fund II", "aum": "$6,500,000,000", "strategy": "Asset-Based Finance"},
    {"id": 3, "name": "Bastion Real Estate Partners", "aum": "$5,000,000,000", "strategy": "Real Estate"},
    {"id": 4, "name": "Bastion Private Equity Fund V", "aum": "$7,000,000,000", "strategy": "Private Equity"},
    {"id": 5, "name": "Bastion Insurance Linked Fund", "aum": "$4,500,000,000", "strategy": "Insurance Solutions"},
    {"id": 6, "name": "Bastion Multi-Strategy Fund", "aum": "$4,000,000,000", "strategy": "Multi-Manager"}
  ]
}
```

- [ ] **Step 3: Create bastion/data/team.json (copy from sentinel and rename)**

```bash
cp sentinel/data/team.json bastion/data/team.json
# Update names/titles to be Bastion-appropriate
```

- [ ] **Step 4: Create bastion/data/news.json (copy from sentinel and rename)**

```bash
cp sentinel/data/news.json bastion/data/news.json
# Update company names from Sentinel to Bastion
```

- [ ] **Step 5: Commit**

```bash
git add bastion/
git commit -m "feat: initialize Bastion Investment Group directory and config"
```

---

### Task 7: Create Bastion app.py

**Files:**
- Create: `bastion/app.py`

- [ ] **Step 1: Implement bastion/app.py**

```python
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

from utils import (
    generate_dynamic_aum, generate_team, get_paginated_data,
    generate_timed_captcha, validate_timed_captcha,
    generate_class_map, inject_dom_obfuscator,
    rate_limit, inject_js_routes, inject_cookie_middleware,
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
inject_cookie_middleware(app)
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
```

- [ ] **Step 2: Commit**

```bash
git add bastion/app.py
git commit -m "feat: implement Bastion Flask app with timed CAPTCHA and DOM obfuscation"
```

---

### Task 8: Create Bastion templates (11 files)

**Files:**
- Create: `bastion/templates/` (all 11 templates)

- [ ] **Step 1: Create base.html with Fortress-inspired design**

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}{{ company_name }}{% endblock %}</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
    {% block extra_css %}{% endblock %}
</head>
<body>
    <header class="header">
        <div class="container">
            <div class="logo">{{ company_name }}</div>
            <nav class="nav">
                <a href="/">Home</a>
                <a href="/what-we-do">What We Do</a>
                <a href="/who-we-are">Who We Are</a>
                <a href="/investors">Investors</a>
                <a href="/financial-advisors">Financial Advisors</a>
                <a href="/media">Media</a>
                <a href="/careers">Careers</a>
                <a href="/contact">Contact</a>
            </nav>
        </div>
    </header>
    
    <main class="main-content">
        <div class="container">
            {% block content %}{% endblock %}
        </div>
    </main>
    
    <footer class="footer">
        <p>&copy; 2026 {{ company_name }}</p>
        {% if global_aum %}<p class="global-aum">Global AUM: {{ global_aum }}</p>{% endif %}
    </footer>
    
    {% include 'cookie_banner.html' %}
    <script src="{{ url_for('static', filename='js/common.js') }}"></script>
    {% block extra_js %}{% endblock %}
</body>
</html>
```

- [ ] **Step 2: Create remaining templates (home, what_we_do, strategy_detail, who_we_are, team, investors, financial_advisors, media, careers, contact)**

Each should extend base.html and follow patterns from existing sites. Add obfuscated classes:
```html
<div class="{{ class_map['aum-value'] }}">{{ value }}</div>
```

- [ ] **Step 3: Create bastion/static/css/style.css (Fortress dark/gold replica)**

```css
:root {
  --primary: #1a1a1a;
  --accent: #c8a96e;
  --text: #333;
  --light: #fff;
}

body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; }
.header { background: var(--primary); color: var(--light); padding: 20px; }
.nav a { color: var(--accent); text-decoration: none; margin: 0 20px; }
.accent-btn { background: var(--accent); color: var(--primary); padding: 10px 20px; }
```

- [ ] **Step 4: Create bastion/requirements.txt**

```
Flask==3.0.0
Jinja2==3.1.2
Pillow==10.0.0
Werkzeug==3.0.0
```

- [ ] **Step 5: Create bastion/Procfile**

```
web: python app.py
```

- [ ] **Step 6: Create bastion/robots.txt (empty — handled by route)**

- [ ] **Step 7: Commit**

```bash
git add bastion/templates/ bastion/static/ bastion/requirements.txt bastion/Procfile bastion/robots.txt
git commit -m "feat: create Bastion templates, CSS (Fortress replica), and deployment files"
```

---

## Phase 3: Landmark Property Advisors (Port 5010)

### Task 9: Create Landmark directory structure and config

**Files:**
- Create: `landmark/config.py`, `landmark/data/`, `landmark/app.py`, `landmark/templates/`, `landmark/static/`

- [ ] **Step 1-7: Mirror Tasks 6-8 for Landmark**

Create `landmark/config.py` with:
```python
COMPANY_NAME = 'Landmark Property Advisors'
ROTATING_TOKENS = True
TOKEN_PAGE_LIMIT = 5
FINGERPRINT_BLOCKING = True
MAX_REQUESTS = 4
COOKIE_BANNER_MODE = 'mandatory'
GLOBAL_AUM = '$47,000,000,000'
```

Create `landmark/app.py` with token validation decorator on all routes and fingerprint check.

Create 11 templates (home with stat hero, landmark_difference, investment_strategies, strategy_detail, about, team, sustainability, news, careers, contact, fingerprint_challenge).

Create `landmark/static/css/style.css` with forest green (#1e4d3b), Georgia serif headings, and stat-hero layout.

- [ ] **Step 8: Commit Landmark**

```bash
git add landmark/
git commit -m "feat: implement Landmark Property Advisors Flask app with token rotation and fingerprint blocking"
```

---

## Phase 4: Documentation & Testing

### Task 10: Update SITE_BEHAVIORS.md

**Files:**
- Modify: `SITE_BEHAVIORS.md`

- [ ] **Step 1: Add two new sections at end**

```markdown
### 10. Bastion Investment Group (Port 5009)
**Primary Obstacles: Dynamic DOM Obfuscation + Timed CAPTCHA**

- DOM obfuscation: CSS classes randomized per session
- Timed CAPTCHA: 30s expiry on data pages
- Rate limit: 10 req/60s
- Cookie banner: optional

### 11. Landmark Property Advisors (Port 5010)
**Primary Obstacles: Rotating Session Tokens + Canvas Fingerprint Blocking**

- Rotating tokens: Expire after 5 page views
- Canvas fingerprint: Blocks known headless hashes
- Rate limit: 4 req/60s
- Cookie banner: mandatory
```

- [ ] **Step 2: Update summary table**

Add Bastion and Landmark rows.

- [ ] **Step 3: Commit**

```bash
git add SITE_BEHAVIORS.md
git commit -m "doc: add Bastion and Landmark to site behaviors documentation"
```

---

## Phase 5: Verification

### Task 11: Verify both sites start and pass basic checks

- [ ] **Step 1: Start Bastion**

```bash
cd bastion
export FLASK_APP=app.py
python app.py &
sleep 2
curl -s http://localhost:5009/ | grep -q "Bastion" && echo "✓ Bastion home loads"
```

- [ ] **Step 2: Start Landmark**

```bash
cd ../landmark
python app.py &
sleep 2
curl -s http://localhost:5010/ | grep -q "Landmark" && echo "✓ Landmark home loads"
```

- [ ] **Step 3: Verify utilities work**

```bash
python -c "from utils import generate_class_map, generate_timed_captcha, issue_token; print('✓ All utilities import')"
```

- [ ] **Step 4: Verify middleware bypass for fingerprint**

Check that `/verify-fingerprint` is added to middleware bypass list in cookie_validation.py and javascript_validation.py patterns.

- [ ] **Step 5: Commit (no changes, just documentation)**

```bash
git status
```

---

## Summary

**All tasks complete when:**
1. ✓ 4 new utilities created and exported
2. ✓ Bastion Flask app running on port 5009 with 11 pages, DOM obfuscation, timed CAPTCHA
3. ✓ Landmark Flask app running on port 5010 with 11 pages, token rotation, fingerprint blocking
4. ✓ Both sites have fortress.com and heitman.com-inspired CSS
5. ✓ SITE_BEHAVIORS.md updated with both sites
6. ✓ All routes accessible, CAPTCHA/tokens functional, rate limiting active
7. ✓ All commits made to git

---

## Execution Handoff

Plan complete and saved to `docs/superpowers/plans/2026-05-06-bastion-landmark-implementation.md`.

**Two execution options:**

**1. Subagent-Driven (recommended)** — I dispatch a fresh subagent per task, review between tasks

**2. Inline Execution** — Execute tasks in this session

Which approach?
