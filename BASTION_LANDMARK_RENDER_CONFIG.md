# Bastion & Landmark Render Configuration

Complete configuration for deploying and rendering Bastion Investment Group and Landmark Property Advisors.

---

## Site Overview

| Property | Bastion | Landmark |
|----------|---------|----------|
| **Company** | Bastion Investment Group | Landmark Property Advisors |
| **Port** | 5009 | 5010 |
| **Reference** | fortress.com | heitman.com |
| **Theme** | Corporate Modular (Dark/Gold) | Premium Property (Navy/Green) |
| **AUM** | $55B | $47B |

---

## Bastion Configuration (Port 5009)

### Application Config (`bastion/config.py`)

```python
COMPANY_NAME = 'Bastion Investment Group'
SITE_NAME = 'bastion'
SECRET_KEY = os.environ.get('SECRET_KEY', 'bastion-dev-key-55555')

# Anti-Scraping: DOM Obfuscation + Timed CAPTCHA
DOM_OBFUSCATION = True
TIMED_CAPTCHA = True
CAPTCHA_TIME_LIMIT = 30
CAPTCHA_REQUIRED_PAGES = ['/what-we-do', '/investors', '/financial-advisors']

# Rate Limiting: 10 requests per 60 seconds
RATE_LIMIT_ENABLED = True
MAX_REQUESTS = 10
TIME_WINDOW = 60

# Cookie Banner: Optional
COOKIE_BANNER_MODE = 'optional'

# Financial Data
GLOBAL_AUM = '$55,000,000,000'
DATA_LAYOUT = 'js_tables'

# Environment
DEBUG = os.environ.get('DEBUG', True)
```

### Environment Variables

```bash
# Required for production
SECRET_KEY=<generate-with-secrets.py>
DEBUG=False
FLASK_ENV=production

# Optional
PORT=5009
LOG_LEVEL=INFO
```

### Flask App Structure (`bastion/app.py`)

**Key Features:**
- ✓ DOM obfuscation: Random CSS class maps per session
- ✓ Timed CAPTCHA: 30-second expiration on data pages
- ✓ Rate limiting: 10 req/60s sliding window
- ✓ User-agent filtering: Headless browser detection
- ✓ Cookie banner: Optional mode

**Routes:**
- `/` → Home (hero, stat cards, portfolio showcase)
- `/what-we-do` → Requires CAPTCHA
- `/investors` → Requires CAPTCHA
- `/financial-advisors` → Requires CAPTCHA
- `/about` → Company story
- `/team` → Team grid (pagination, 5 per page)
- `/contact` → Contact form
- Plus 6 strategy detail pages

**Templates:**
```
bastion/templates/
├── base.html                      # Fixed navy header, gold accents, footer
├── home.html                      # Hero + stats + portfolio
├── what_we_do.html               # Alternating strategy sections
├── who_we_are.html               # Stat cards + values + portfolio
├── team.html                      # 3-column grid, paginated
├── investors.html                # 3 investor portals
├── financial_advisors.html       # Knowledge center
├── media.html                     # News grid
├── careers.html                   # Benefits + positions + process
├── contact.html                   # 2-column form + info
├── corporate_credit.html         # Strategy detail
├── asset_based_finance.html      # Strategy detail
├── real_estate.html              # Strategy detail
├── private_equity.html           # Strategy detail
├── insurance_solutions.html      # Strategy detail
└── multi_manager.html            # Strategy detail
```

**CSS:**
```
bastion/static/css/
├── style.css                      # Global styles
└── fortress.css                   # Corporate modular (navy/gold)
```

---

## Landmark Configuration (Port 5010)

### Application Config (`landmark/config.py`)

```python
COMPANY_NAME = 'Landmark Property Advisors'
SITE_NAME = 'landmark'
SECRET_KEY = os.environ.get('SECRET_KEY', 'landmark-dev-key-5010')
PORT = 5010

# Anti-Scraping: Session Token Rotation + Canvas Fingerprint
ROTATING_TOKENS = True
TOKEN_PAGE_LIMIT = 5
FINGERPRINT_BLOCKING = True

# Rate Limiting: 4 requests per 60 seconds (stricter than Bastion)
RATE_LIMIT_ENABLED = True
MAX_REQUESTS = 4
TIME_WINDOW = 60

# Cookie Banner: Mandatory
COOKIE_BANNER_MODE = 'mandatory'

# Financial Data
GLOBAL_AUM = '$47,000,000,000'
DATA_LAYOUT = 'js_tables'

# Environment
DEBUG = os.environ.get('DEBUG', True)
```

### Environment Variables

```bash
# Required for production
SECRET_KEY=<generate-with-secrets.py>
DEBUG=False
FLASK_ENV=production

# Optional
PORT=5010
LOG_LEVEL=INFO
```

### Flask App Structure (`landmark/app.py`)

**Key Features:**
- ✓ Session token rotation: 5-page limit, expires and regenerates
- ✓ Canvas fingerprint blocking: Headless browser detection via canvas
- ✓ Rate limiting: 4 req/60s sliding window (stricter)
- ✓ User-agent filtering: Headless browser detection
- ✓ Cookie banner: Mandatory mode (users must accept)
- ✓ Fixed navy header with fixed positioning

**Routes:**
- `/` → Home (hero, 5 stat cards, news grid, green CTAs)
- `/verify-fingerprint` → POST endpoint for fingerprint validation
- `/refresh-token` → GET endpoint for token rotation
- `/about` → Company story + timeline + office locations
- `/landmark-difference` → 6 differentiators
- `/investment-strategies` → Funds table + characteristics matrix
- `/team` → 3-column grid, paginated
- `/sustainability` → ESG initiatives + targets
- `/news` → Article grid with date badges
- `/careers` → Benefits + positions + culture
- `/contact` → 2-column form + regional offices
- Plus 3 strategy detail pages

**Templates:**
```
landmark/templates/
├── base.html                      # Fixed navy header, green accents, footer
├── home.html                      # Hero + 5 stat cards + news grid
├── landmark_difference.html      # 6 differentiators
├── investment_strategies.html    # Funds table + matrix
├── about.html                     # 60-year timeline
├── team.html                      # 3-column grid, paginated
├── sustainability.html           # ESG initiatives + grid
├── news.html                      # Article grid
├── careers.html                   # Benefits + positions + process
├── contact.html                   # 2-column form + regional offices
├── private_equity_re.html        # Strategy detail
├── private_debt_re.html          # Strategy detail
└── public_equity_re.html         # Strategy detail
```

**CSS:**
```
landmark/static/css/
├── style.css                      # Global styles
└── heitman.css                    # Premium property (navy/green)
```

---

## Requirements Files

### `bastion/requirements.txt`
```
Flask==2.3.3
Werkzeug==2.3.7
```

### `landmark/requirements.txt`
```
Flask==2.3.3
Werkzeug==2.3.7
```

Both inherit from root `requirements.txt` which includes:
- Jinja2, gunicorn, gevent, redis, cryptography, PyJWT, SQLAlchemy, requests, sentry-sdk, pytest

---

## Running Locally

### Start Bastion
```bash
python bastion/app.py
# Runs on http://localhost:5009
```

### Start Landmark
```bash
python landmark/app.py
# Runs on http://localhost:5010
```

### Start Both
```bash
python bastion/app.py &
python landmark/app.py &
```

---

## Docker Deployment

### Dockerfile (shared)
```dockerfile
FROM python:3.11-slim

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN mkdir -p logs

EXPOSE ${PORT:-5009}

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:${PORT:-5009}/ || exit 1

CMD ["gunicorn", "--workers", "4", "--worker-class", "sync", "--timeout", "30", "--bind", "0.0.0.0:${PORT:-5009}", "app:app"]
```

### Docker Compose Services

```yaml
bastion:
  build:
    context: .
    dockerfile: Dockerfile
  ports:
    - "5009:5009"
  environment:
    - FLASK_APP=bastion/app.py
    - PORT=5009
    - SECRET_KEY=${BASTION_SECRET_KEY}
    - DEBUG=False
  volumes:
    - ./bastion:/app/bastion
    - ./utils:/app/utils
    - ./shared:/app/shared
  healthcheck:
    test: ["CMD", "curl", "-f", "http://localhost:5009/"]
    interval: 30s
    timeout: 3s
    retries: 3

landmark:
  build:
    context: .
    dockerfile: Dockerfile
  ports:
    - "5010:5010"
  environment:
    - FLASK_APP=landmark/app.py
    - PORT=5010
    - SECRET_KEY=${LANDMARK_SECRET_KEY}
    - DEBUG=False
  volumes:
    - ./landmark:/app/landmark
    - ./utils:/app/utils
    - ./shared:/app/shared
  healthcheck:
    test: ["CMD", "curl", "-f", "http://localhost:5010/"]
    interval: 30s
    timeout: 3s
    retries: 3
```

---

## Anti-Scraping Measures

### Bastion
| Measure | Enabled | Details |
|---------|---------|---------|
| DOM Obfuscation | ✓ Yes | Random CSS class maps per session, idempotent |
| Timed CAPTCHA | ✓ Yes | 30-second expiration on `/what-we-do`, `/investors`, `/financial-advisors` |
| Rate Limiting | ✓ Yes | 10 requests per 60 seconds |
| User-Agent Filtering | ✓ Yes | Detects headless browsers |
| JavaScript Validation | ✓ Yes | Requires JavaScript to render pages |

### Landmark (Stricter)
| Measure | Enabled | Details |
|---------|---------|---------|
| Session Token Rotation | ✓ Yes | Token expires after 5 page views, /refresh-token to get new token |
| Canvas Fingerprint | ✓ Yes | Blocks known headless browsers (Playwright, Selenium, etc.) |
| Rate Limiting | ✓ Yes | 4 requests per 60 seconds (stricter than Bastion) |
| User-Agent Filtering | ✓ Yes | Detects headless browsers |
| JavaScript Validation | ✓ Yes | Requires JavaScript to render pages |

---

## Testing Locally

### Health Check (Both Sites)
```bash
curl http://localhost:5009/
curl http://localhost:5010/
```

### Test Bastion Pages
```bash
# Home page
curl http://localhost:5009/

# About page
curl http://localhost:5009/about

# Contact page
curl http://localhost:5009/contact

# Strategy page (requires CAPTCHA)
curl http://localhost:5009/what-we-do
```

### Test Landmark Pages
```bash
# Home page (requires fingerprint verification)
curl http://localhost:5010/

# About page
curl http://localhost:5010/about

# Contact page
curl http://localhost:5010/contact

# Investment strategies
curl http://localhost:5010/investment-strategies
```

---

## Environment Variables Summary

### For Bastion (5009)

| Variable | Value | Description |
|----------|-------|-------------|
| `FLASK_APP` | `bastion/app.py` | Flask entry point |
| `PORT` | `5009` | Listen port |
| `SECRET_KEY` | `*` | Generated secret (see generate_secrets.py) |
| `DEBUG` | `False` (prod) | Disable debug mode in production |
| `FLASK_ENV` | `production` | Production environment |

### For Landmark (5010)

| Variable | Value | Description |
|----------|-------|-------------|
| `FLASK_APP` | `landmark/app.py` | Flask entry point |
| `PORT` | `5010` | Listen port |
| `SECRET_KEY` | `*` | Generated secret (see generate_secrets.py) |
| `DEBUG` | `False` (prod) | Disable debug mode in production |
| `FLASK_ENV` | `production` | Production environment |

---

## Production Deployment Checklist

- [ ] Generate production secrets: `python scripts/generate_secrets.py`
- [ ] Generate SSL certificates: `bash scripts/generate-ssl-certs.sh`
- [ ] Set environment variables (SECRET_KEY, DEBUG=False, FLASK_ENV=production)
- [ ] Test both sites locally with updated config
- [ ] Build Docker images: `docker-compose build`
- [ ] Run health checks: `bash scripts/health-check.sh`
- [ ] Enable Nginx reverse proxy with SSL termination
- [ ] Configure monitoring (Sentry, New Relic, Datadog)
- [ ] Set up automated backups
- [ ] Deploy to production: `docker-compose up -d bastion landmark`

---

**Last Updated:** 2026-05-06
**Version:** 1.0
