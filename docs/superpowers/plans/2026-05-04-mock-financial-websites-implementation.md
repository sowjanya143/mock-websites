# Mock Financial Services Websites — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build 5 independently deployable Flask mock financial services websites with site-specific CAPTCHA/pop-up/rate-limiting behaviors, dynamic JSON data, paginated leadership pages, and multi-level AUM data discovery.

**Architecture:** Shared Python utilities (`utils/`) provide CAPTCHA generation, pop-up rendering, dynamic data generation, and rate limiting. Each of the 5 sites is an independent Flask app with its own config, routes, templates, and data files. Sites share base templates and styling from `shared/`. Each site deploys independently to Render.

**Tech Stack:** Flask 3.0+, Jinja2, Pillow (images), Python 3.10+, JSON data files, Render web services.

---

## Phase 1: Project Initialization & Shared Infrastructure

### Task 1: Initialize Project Structure & .gitignore

**Files:**
- Create: `.gitignore`
- Create: `.claudeignore`
- Create: `README.md`
- Create: `requirements-shared.txt`

- [ ] **Step 1: Create `.gitignore`**

```
__pycache__/
*.pyc
*.pyo
*.egg-info/
.venv/
venv/
env/
.env
.env.local
*.sqlite
*.db
.DS_Store
node_modules/
.pytest_cache/
.coverage
htmlcov/
dist/
build/
```

- [ ] **Step 2: Create `.claudeignore`**

```
.venv/
venv/
env/
__pycache__/
*.pyc
.pytest_cache/
*.lock
*.egg-info/
.coverage
htmlcov/
```

- [ ] **Step 3: Create `README.md`**

```markdown
# Mock Financial Services Websites

5 independent Flask-based mock financial websites for testing web scraping solutions.

## Sites

- **Fortress** - CAPTCHA on every page, hidden AUM in JS
- **Heitman** - CAPTCHA on data pages, JSON endpoints, 5 req/min rate limit
- **Nomura** - Random CAPTCHA (30%), scattered AUM data, 1s delay
- **Hokuyo Bank** - No CAPTCHA, clean tables, fast responses
- **Oaktree Capital** - CAPTCHA on first visit + data pages, AJAX content, 3 req/min rate limit

## Local Development

```bash
cd fortress
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Then visit `http://localhost:5000` (port varies per site).

## Deployment to Render

Each site has its own Render web service. See `DEPLOYMENT.md` for setup.

## Shared Utilities

All sites use utilities from `utils/`:
- `captcha.py` - CAPTCHA generation and validation
- `popups.py` - Pop-up rendering
- `data_generator.py` - Dynamic AUM/team data
- `rate_limit.py` - Rate limiting

## Project Structure

```
fortress/
  ├── app.py              # Main Flask app
  ├── config.py           # Site-specific config
  ├── routes.py           # Routes and handlers
  ├── data/               # JSON data files
  ├── templates/          # Jinja2 templates
  └── static/             # CSS, JS, images
[5 similar site folders]
```
```

- [ ] **Step 4: Create `requirements-shared.txt`**

```
Flask==3.0.0
Pillow==10.0.0
```

- [ ] **Step 5: Commit**

```bash
git add .gitignore .claudeignore README.md requirements-shared.txt
git commit -m "chore: initialize project structure and documentation"
```

---

### Task 2: Implement Shared Utilities (captcha, popups, data_generator, rate_limit)

**Files:**
- Create: `utils/__init__.py`
- Create: `utils/captcha.py`
- Create: `utils/popups.py`
- Create: `utils/data_generator.py`
- Create: `utils/rate_limit.py`
- Create: `tests/test_utils.py`

**Details:** Implement 4 utility modules with complete code. Test data_generator.

---

### Task 3: Create Shared Templates & Static Assets

**Files:**
- Create: `shared/templates/base.html`
- Create: `shared/static/css/style.css`
- Create: `shared/static/js/common.js`

**Details:** Base HTML template, global CSS, common JavaScript for popups and CAPTCHA handling.

---

## Phase 2: Fortress Site Implementation

### Task 4: Fortress - Setup Config & App

**Files:**
- Create: `fortress/config.py`
- Create: `fortress/app.py`
- Create: `fortress/requirements.txt`

**Key behaviors:**
- CAPTCHA on every page
- No pop-ups
- No rate limiting
- No artificial delays
- Data layout: hidden in JS tables

---

### Task 5: Fortress - Create Routes, Templates & Data

**Files:**
- Create: `fortress/data/aum.json`
- Create: `fortress/data/team.json`
- Create: `fortress/data/news.json`
- Create: `fortress/templates/captcha.html`
- Create: `fortress/templates/fortress/` (11 templates: home, about, leadership, strategies, investor_resources, funds, fund_detail, news, contact, captcha_error, base)

**Details:** Full Fortress site with all routes, templates, and data files. Test locally.

---

### Task 6: Heitman Site (Full Implementation)

**Files:** heitman/config.py, app.py, routes.py, requirements.txt, data/*, templates/*

**Key behaviors:**
- CAPTCHA only on data pages
- Rate limiting: 5 req/min
- JSON endpoint at `/api/aum`
- Dismissible pop-ups
- Same page structure as Fortress

---

### Task 7: Nomura Site (Full Implementation)

**Files:** nomura/config.py, app.py, routes.py, requirements.txt, data/*, templates/*

**Key behaviors:**
- Random CAPTCHA (30% chance)
- 1s artificial delay on all requests
- Modal pop-ups after scroll
- Scattered AUM data across pages

---

### Task 8: Hokuyo Bank Site (Full Implementation)

**Files:** hokuyo/config.py, app.py, routes.py, requirements.txt, data/*, templates/*

**Key behaviors:**
- No CAPTCHA
- No pop-ups
- No rate limiting
- Fastest responses (no delays)
- Clean, simple table-based layout

---

### Task 9: Oaktree Capital Site (Full Implementation)

**Files:** oaktree/config.py, app.py, routes.py, requirements.txt, data/*, templates/*

**Key behaviors:**
- CAPTCHA on first visit + data pages
- Rate limiting: 3 req/min
- Sticky footer pop-ups with auto-dismiss
- AJAX-loaded content
- 0.5s artificial delay

---

## Phase 3: Testing & Documentation

### Task 10: Create Test Suite for All Sites

**Files:**
- Create: `tests/test_sites.py`
- Create: `tests/test_fortress_behavior.py`

**Details:** Test pagination, CAPTCHA rendering, pop-up behavior, rate limiting, AUM data discovery, dynamic variance. Verify each site's unique behaviors.

---

### Task 11: Create Render Deployment Configuration

**Files:**
- Create: `fortress/Procfile`
- Create: `heitman/Procfile`
- Create: `nomura/Procfile`
- Create: `hokuyo/Procfile`
- Create: `oaktree/Procfile`
- Create: `DEPLOYMENT.md`

**Details:** Procfiles for each site, environment setup, deployment instructions.

---
