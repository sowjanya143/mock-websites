# Bastion & Landmark Mock Financial Websites — Design Spec
**Date:** 2026-05-06
**Project:** 2 New Mock Financial Websites (Sites 10 & 11) — Fortress.com + Heitman.com Visual Replicas

---

## Purpose

Add two new Flask-based mock financial websites to the existing 9-site suite. Each site closely replicates the visual design of a real reference company while introducing 2 new anti-scraping behaviors not yet used in the existing sites. Sites share all existing Python utilities and add 4 new utility modules.

**Reference sites:**
- `bastion/` → fortress.com (alternative asset management, $55B AUM, 6 strategies)
- `landmark/` → heitman.com (real estate only, $47B AUM, 3 strategies, stat-hero layout)

---

## Architecture

### Approach
Per-site CSS + shared Python utils (Approach A). Each site has a fully independent `static/css/style.css` replicating its reference site's visual design. All shared Python utilities reused as-is. Four new utility modules added to `utils/`.

### Directory Structure

```
mock-website/
├── bastion/                          # mirrors fortress.com
│   ├── app.py
│   ├── config.py
│   ├── data/
│   │   ├── aum.json
│   │   ├── team.json
│   │   └── news.json
│   ├── templates/
│   │   ├── base.html                 # nav: What We Do | Who We Are | Investors | Financial Advisors | Media | Careers | Contact
│   │   ├── home.html
│   │   ├── what_we_do.html           # /what-we-do — strategy overview cards
│   │   ├── strategy_detail.html      # /what-we-do/<slug> — shared for all 8 strategy slugs
│   │   ├── who_we_are.html           # /who-we-are — overview + impact sections
│   │   ├── team.html                 # /who-we-are/team — paginated leadership
│   │   ├── investors.html            # /investors — institutional/FA/insurance portal tiles
│   │   ├── financial_advisors.html   # /financial-advisors — FA overview + knowledge center + resources
│   │   ├── media.html                # /media — news/press listing
│   │   ├── careers.html              # /careers
│   │   ├── contact.html              # /contact
│   │   ├── captcha.html
│   │   └── captcha_error.html
│   ├── static/css/style.css
│   ├── requirements.txt
│   ├── Procfile
│   └── robots.txt
├── landmark/                         # mirrors heitman.com
│   ├── app.py
│   ├── config.py
│   ├── data/
│   │   ├── aum.json
│   │   ├── team.json
│   │   └── news.json
│   ├── templates/
│   │   ├── base.html                 # nav: The Landmark Difference | Investment Strategies | About | Careers | Contact + language selector
│   │   ├── home.html                 # 5-stat hero: 1 focus · 10 offices · 15 solutions · $47B AUM · 60 years
│   │   ├── landmark_difference.html  # /landmark-difference — philosophy + differentiators
│   │   ├── investment_strategies.html # /investment-strategies — 3 RE strategy cards with AUM
│   │   ├── strategy_detail.html      # /investment-strategies/<slug> — shared for 3 strategies
│   │   ├── about.html                # /about — 60-year timeline + 10 global offices
│   │   ├── team.html                 # /about/team — paginated leadership
│   │   ├── sustainability.html       # /about/sustainability
│   │   ├── careers.html              # /careers
│   │   ├── contact.html              # /contact
│   │   └── fingerprint_challenge.html
│   ├── static/css/style.css
│   ├── requirements.txt
│   ├── Procfile
│   └── robots.txt
└── utils/
    ├── dom_obfuscator.py     # NEW
    ├── timed_captcha.py      # NEW
    ├── session_token.py      # NEW
    ├── fingerprint.py        # NEW
    └── __init__.py           # UPDATED — exports 4 new modules
```

---

## Site 1: Bastion Investment Group (Port 5009)

### Reference
Fortress Investment Group (fortress.com) — alternative asset management, $55B AUM

### Visual Design
- **Color scheme:** Near-black `#1a1a1a` header/hero, white content sections, gold `#c8a96e` accent for CTAs and highlights
- **Typography:** System sans-serif stack, uppercase nav labels, generous whitespace, corporate minimalist
- **Hero:** Full-width dark banner with tagline "Protecting and Growing Capital" + global AUM stat prominently displayed
- **Navigation:** `What We Do | Who We Are | Investors | Financial Advisors | Media | Careers | Contact`
- **Layout pattern:** Wide content areas, subtle section dividers, card-based strategy grid on homepage

**Navigation (mirrors fortress.com):** `What We Do | Who We Are | Investors | Financial Advisors | Media | Careers | Contact`

### Pages (11)
| # | Route | Template | Description |
|---|-------|----------|-------------|
| 1 | `/` | `home.html` | Hero (dark banner, gold CTA) + $55B AUM teaser + 8 strategy/section cards |
| 2 | `/what-we-do` | `what_we_do.html` | Strategy overview: 8 cards (About Fortress, Corporate Credit, Asset-Based Finance, Real Estate, Private Equity, Insurance Solutions, Multi-Manager, Private Wealth Solutions) with AUM per strategy |
| 3 | `/what-we-do/<slug>` | `strategy_detail.html` | Individual strategy page — AUM figure, description, sub-strategies; slugs: `corporate-credit`, `asset-based-finance`, `real-estate`, `private-equity`, `insurance-solutions`, `multi-manager`, `private-wealth-solutions` |
| 4 | `/who-we-are` | `who_we_are.html` | Overview + Impact sections (Responsible Investing, Social Responsibility, D&I) |
| 5 | `/who-we-are/team` | `team.html` | Paginated leadership team (5 per page) |
| 6 | `/investors` | `investors.html` | 3 portal tiles: Institutional Investors, Financial Advisors, Insurance — each with AUM context |
| 7 | `/financial-advisors` | `financial_advisors.html` | FA overview + Knowledge Center (highlights/articles by strategy) + Investor Resources + Team + Contact |
| 8 | `/media` | `media.html` | News/press listing |
| 9 | `/careers` | `careers.html` | Open roles (static) |
| 10 | `/contact` | `contact.html` | Contact form |
| 11 | `/captcha` | `captcha.html` + `captcha_error.html` | CAPTCHA challenge pages |

**AUM depth levels:**
- Level 1: `/` homepage — global $55B teaser
- Level 2: `/what-we-do` — AUM by strategy (JS-rendered table)
- Level 3: `/what-we-do/<slug>` — per-strategy AUM figure + fund breakdown

### Data: `aum.json`
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
±5% dynamic variance applied on load via `generate_dynamic_aum()`.

### Anti-Scraping Behaviors

#### 1. Dynamic DOM Obfuscation (NEW)
- On session creation, `generate_class_map(session)` creates a random mapping of semantic CSS classes to 5-character random strings (e.g., `aum-value → x7k2p`, `fund-name → r3mq9`)
- Class map stored in `session['class_map']`; regenerated on new session
- All AUM-containing elements in templates use `{{ class_map['aum-value'] }}` instead of hardcoded class names
- CSS in `style.css` uses the static semantic names; a `<style>` block in `base.html` dynamically maps random names to the semantic styles via server-side rendering
- Scrapers that scrape by CSS class selector find different class names every session

#### 2. Timed CAPTCHA — 30s Expiry (NEW)
- Applied on data pages: `/strategies`, `/investor-resources`, `/funds`, `/fund/<id>`
- On CAPTCHA generation, `session['captcha_issued_at']` is set to current timestamp
- `validate_timed_captcha(answer)` checks: elapsed > 30s → return `'expired'`; wrong answer → return `'invalid'`; correct → return `'ok'`
- `captcha.html` template includes a JavaScript countdown timer (30 → 0)
- On expiry, JavaScript disables the submit button and shows "Challenge expired — refresh for a new one"
- Rate limit: 10 req/60s

#### Global Behaviors (inherited)
- JS validation (`inject_js_routes`)
- Cookie enforcement (`inject_cookie_middleware`) — `optional` mode
- User-agent blocking (`inject_user_agent_middleware`)
- Strict headers (`inject_headers_middleware`)
- `/aum` blocked (403)
- `robots.txt` misdirection

### Config
```python
COMPANY_NAME = 'Bastion Investment Group'
SITE_NAME = 'bastion'
PORT = 5009
CAPTCHA_ON_EVERY_PAGE = False
CAPTCHA_REQUIRED_PAGES = ['/strategies', '/investor-resources', '/funds', '/fund/<id>']
TIMED_CAPTCHA = True
CAPTCHA_TIME_LIMIT = 30
DOM_OBFUSCATION = True
RATE_LIMIT_ENABLED = True
MAX_REQUESTS = 10
TIME_WINDOW = 60
COOKIE_BANNER_MODE = 'optional'
GLOBAL_AUM = '$55,000,000,000'
DATA_LAYOUT = 'js_tables'
```

---

## Site 2: Landmark Property Advisors (Port 5010)

### Reference
Heitman (heitman.com) — real estate investment manager, $47B AUM

### Visual Design
- **Color scheme:** Deep forest green `#1e4d3b` primary (header, nav, CTAs), white content, warm gray `#f5f3f0` alternating section backgrounds
- **Typography:** Georgia/serif for large stat numbers and headings, clean sans-serif body text — premium real estate feel
- **Hero:** Large stat-driven sections with oversized numbers: **$47B** AUM · **60** years · **10** offices · **3** strategies · **15** solutions
- **Navigation:** `The Landmark Difference | Investment Strategies ▾ | About ▾ | Careers | Contact` + language selector (UI-only, English-only functionally)
- **Layout pattern:** Stats-first hero, full-width image sections, three-column strategy cards

**Navigation (mirrors heitman.com):** `The Landmark Difference | Investment Strategies ▾ | About ▾ | Careers | Contact` + language selector (UI-only)

**Investment Strategies dropdown:** Private Equity · Private Debt · Public Equity
**About dropdown:** Team · Sustainability

### Pages (11)
| # | Route | Template | Description |
|---|-------|----------|-------------|
| 1 | `/` | `home.html` | 5-stat hero (1 focus · 10 offices · 15 solutions · $47B AUM · 60 years) each linking to relevant page; 3 strategy cards below |
| 2 | `/landmark-difference` | `landmark_difference.html` | Philosophy, differentiators, global presence |
| 3 | `/investment-strategies` | `investment_strategies.html` | Overview of 3 RE strategies with AUM per strategy |
| 4 | `/investment-strategies/<slug>` | `strategy_detail.html` | Individual strategy detail; slugs: `private-equity`, `private-debt`, `public-equity` |
| 5 | `/about` | `about.html` | 60-year firm history timeline + 10 global office locations |
| 6 | `/about/team` | `team.html` | Paginated leadership team (5 per page) |
| 7 | `/about/sustainability` | `sustainability.html` | Sustainability / ESG overview (static) |
| 8 | `/news` | `news.html` | News listing (no separate news detail page — matches heitman.com) |
| 9 | `/careers` | `careers.html` | Open roles (static) |
| 10 | `/contact` | `contact.html` | Contact form |
| 11 | `/fingerprint-challenge` | `fingerprint_challenge.html` | Browser verification challenge page |

**AUM depth levels:**
- Level 1: `/` homepage — oversized $47B stat card
- Level 2: `/investment-strategies` — AUM by strategy (Private Equity RE / Private Debt RE / Public Equity RE)
- Level 3: `/investment-strategies/<slug>` — per-strategy AUM + fund breakdown within that strategy

### Data: `aum.json`
```json
{
  "global_aum": "$47,000,000,000",
  "by_strategy": {
    "Private Equity Real Estate": "$19,000,000,000",
    "Private Debt Real Estate": "$15,000,000,000",
    "Public Equity Real Estate": "$13,000,000,000"
  },
  "by_fund": [
    {"id": 1, "name": "Landmark Private Equity Fund III", "aum": "$9,000,000,000", "strategy": "Private Equity Real Estate"},
    {"id": 2, "name": "Landmark Value-Add Fund", "aum": "$5,500,000,000", "strategy": "Private Equity Real Estate"},
    {"id": 3, "name": "Landmark Real Estate Debt Fund II", "aum": "$8,000,000,000", "strategy": "Private Debt Real Estate"},
    {"id": 4, "name": "Landmark Mezzanine Fund", "aum": "$4,000,000,000", "strategy": "Private Debt Real Estate"},
    {"id": 5, "name": "Landmark REIT Income Fund", "aum": "$7,000,000,000", "strategy": "Public Equity Real Estate"},
    {"id": 6, "name": "Landmark Global Securities Fund", "aum": "$4,500,000,000", "strategy": "Public Equity Real Estate"}
  ]
}
```
±5% dynamic variance applied on load via `generate_dynamic_aum()`.

### Anti-Scraping Behaviors

#### 1. Rotating Session Tokens (NEW)
- `issue_token(session)` sets `session['page_token']` (UUID) and `session['page_count'] = 0`
- `validate_token(session)` decorator on all routes: increments `page_count`; if count ≥ 5, clears token, sets `session['token_expired'] = True`, returns `False`
- On token expiry: redirects to `/refresh-token`
- `/refresh-token` re-issues a new token and redirects back to referrer
- Scrapers that don't follow the redirect chain lose session state mid-crawl
- Rate limit: 4 req/60s

#### 2. Canvas/WebGL Fingerprint Blocking (NEW)
- On first visit, `base.html` includes a hidden `<canvas>` element + JavaScript that draws a standard pattern and hashes the result
- Hash is POSTed to `/verify-fingerprint`
- `/verify-fingerprint` checks hash against a blocklist of known headless browser fingerprints (Puppeteer default, Playwright default canvas hashes)
- Blocked hashes → 403 "Browser verification failed"
- Valid hashes → `session['fp_verified'] = True`
- `require_fingerprint` decorator on all routes: if `fp_verified` not in session, serve `fingerprint_challenge.html` instead of content
- Cookie banner: `mandatory` mode (blocks content until accepted)

#### Global Behaviors (inherited)
- JS validation (`inject_js_routes`)
- Cookie enforcement (`inject_cookie_middleware`) — `mandatory` mode
- User-agent blocking (`inject_user_agent_middleware`)
- Strict headers (`inject_headers_middleware`)
- `/aum` blocked (403)
- `robots.txt` misdirection

### Config
```python
COMPANY_NAME = 'Landmark Property Advisors'
SITE_NAME = 'landmark'
PORT = 5010
CAPTCHA_ON_EVERY_PAGE = False
CAPTCHA_REQUIRED_PAGES = []
ROTATING_TOKENS = True
TOKEN_PAGE_LIMIT = 5
FINGERPRINT_BLOCKING = True
RATE_LIMIT_ENABLED = True
MAX_REQUESTS = 4
TIME_WINDOW = 60
COOKIE_BANNER_MODE = 'mandatory'
GLOBAL_AUM = '$47,000,000,000'
DATA_LAYOUT = 'clean_tables'
```

---

## New Shared Utilities

### `utils/dom_obfuscator.py`
```python
generate_class_map(session) -> dict
    # Creates {semantic_name: random_5char} mapping; stores in session['class_map']
    # Returns existing map if already set for session

inject_dom_obfuscator(app)
    # Registers context processor: injects class_map into all templates
```

### `utils/timed_captcha.py`
```python
generate_timed_captcha(session) -> bytes
    # Calls generate_captcha(), sets session['captcha_issued_at'] = time.time()

validate_timed_captcha(answer, session, time_limit=30) -> Literal['ok', 'invalid', 'expired']
    # Checks elapsed time first, then answer correctness
```

### `utils/session_token.py`
```python
issue_token(session) -> str
    # Sets session['page_token'] = uuid4(), session['page_count'] = 0

validate_token(session) -> bool
    # Increments page_count; returns False and clears token if count >= TOKEN_PAGE_LIMIT

inject_token_routes(app, page_limit=5)
    # Registers GET /refresh-token: re-issues token, redirects to referrer
```

### `utils/fingerprint.py`
```python
BLOCKED_FINGERPRINTS: set[str]
    # Known headless browser canvas hashes (Puppeteer, Playwright defaults)

inject_fingerprint_routes(app)
    # Registers POST /verify-fingerprint:
    #   - hash in BLOCKED_FINGERPRINTS → 403
    #   - else → session['fp_verified'] = True, return 200
    # NOTE: /verify-fingerprint must be added to middleware bypass list
    #   alongside /set-cookie, /validate-js, /set-js-cookie

require_fingerprint(f) -> decorator
    # If fp_verified not in session: render fingerprint_challenge.html
```

### `utils/__init__.py` additions
```python
from .dom_obfuscator import generate_class_map, inject_dom_obfuscator
from .timed_captcha import generate_timed_captcha, validate_timed_captcha
from .session_token import issue_token, validate_token, inject_token_routes
from .fingerprint import inject_fingerprint_routes, require_fingerprint
```

---

## SITE_BEHAVIORS.md Additions

Two new entries appended to the existing document:

**Bastion Investment Group (Port 5009):** Dynamic DOM obfuscation (CSS class randomization per session) + timed CAPTCHA (30s expiry on data pages) + 10 req/60s rate limit

**Landmark Property Advisors (Port 5010):** Rotating session tokens (expire after 5 page views) + canvas/WebGL fingerprint blocking + 4 req/60s rate limit

---

## Data Model Extensions

`aum.json` for both sites uses the same schema as existing sites with a `by_strategy` key (matching Fortress's 6-strategy and Heitman's 3-strategy breakdown). `team.json` and `news.json` use existing schemas unchanged.

---

## Global Summary Table (Updated)

| Behavior | Bastion | Landmark |
|----------|---------|----------|
| Dynamic DOM Obfuscation | ✓ | - |
| Timed CAPTCHA (30s) | ✓ (data pages) | - |
| Rotating Session Tokens | - | ✓ |
| Canvas Fingerprint Blocking | - | ✓ |
| Rate Limiting | 10 req/60s | 4 req/60s |
| Cookie Banner | optional | mandatory |
| JS Validation | ✓ | ✓ |
| Cookie Enforcement | ✓ | ✓ |
| UA Blocking | ✓ | ✓ |
| Strict Headers | ✓ | ✓ |
| /aum Blocked | ✓ | ✓ |
| robots.txt | ✓ | ✓ |

---

## Success Criteria

1. Both sites independently deployable as Flask apps on Render
2. Bastion visually replicates fortress.com's dark/gold minimalist aesthetic
3. Landmark visually replicates heitman.com's green/serif stat-hero aesthetic
4. DOM obfuscation: CSS class names differ between sessions on Bastion
5. Timed CAPTCHA: Submitting after 30s returns expired error on Bastion
6. Token rotation: After 5 page views, Landmark redirects to `/refresh-token`
7. Fingerprint blocking: Known headless hashes return 403 on Landmark
8. All 6 global security layers active on both sites
9. AUM discoverable at 3 depth levels (homepage → strategy/IR → fund detail)
10. Leadership pagination working on both sites

---

## Tech Stack
Same as existing sites: Flask 3.0+, Jinja2, Pillow (CAPTCHA), Python 3.10+, JSON data files, Render deployment.
