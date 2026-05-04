# Mock Financial Services Websites

A collection of 5 independent Flask-based mock financial services websites, each designed to demonstrate different web interaction patterns and security challenges.

## Overview

This project contains the following mock financial services sites:

### 1. **Sentinel Capital Partners** (Port 5000)
CAPTCHA protection on every page for maximum security.

### 2. **Apex Investment Group** (Port 5001)
CAPTCHA on data pages, JSON endpoints, and rate limiting.

### 3. **Meridian Global Holdings** (Port 5002)
Random CAPTCHA, scattered AUM data, and artificial delays.

### 4. **Premier Financial Services** (Port 5003)
Baseline clean site with no obstacles.

### 5. **Zenith Asset Management** (Port 5004)
All obstacles combined - comprehensive anti-scraping and security measures.

## Site-Specific Behaviors

Each site is independently deployable and exhibits unique characteristics:

- **Sentinel Capital Partners**: CAPTCHA verification on every page
- **Apex Investment Group**: CAPTCHA on data pages, rate limiting enabled
- **Meridian Global Holdings**: Random CAPTCHA, scattered AUM data, artificial delays
- **Premier Financial Services**: Clean interface, no security obstacles (control site)
- **Zenith Asset Management**: Maximum security - combined CAPTCHA, pop-ups, rate limiting, and delays

## Project Structure

```
mock-website/
├── sentinel/             # Sentinel Capital Partners Flask app (port 5000)
├── apex/                 # Apex Investment Group Flask app (port 5001)
├── meridian/             # Meridian Global Holdings Flask app (port 5002)
├── premier/              # Premier Financial Services Flask app (port 5003)
├── zenith/               # Zenith Asset Management Flask app (port 5004)
├── shared/               # Shared utilities module
│   ├── captcha.py        # CAPTCHA generation and validation
│   ├── popups.py         # Pop-up management utilities
│   ├── data_generator.py # Mock data generation
│   ├── rate_limit.py     # Rate limiting utilities
│   └── __init__.py
├── requirements-shared.txt # Shared dependencies
├── .gitignore            # Git ignore patterns
├── .claudeignore         # Claude Code ignore patterns
└── README.md             # This file
```

## Local Development Setup

### Prerequisites
- Python 3.8 or higher
- pip or uv package manager

### Installation

1. **Create and activate a virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. **Install shared dependencies:**
   ```bash
   pip install -r requirements-shared.txt
   ```

3. **Install site-specific dependencies (if any):**
   ```bash
   pip install -r fortress/requirements.txt
   pip install -r heitman/requirements.txt
   # ... repeat for other sites
   ```

### Running Sites Locally

Each site runs independently on its own port:

```bash
# Sentinel Capital Partners (port 5000)
python sentinel/app.py

# Apex Investment Group (port 5001)
python apex/app.py

# Meridian Global Holdings (port 5002)
python meridian/app.py

# Premier Financial Services (port 5003)
python premier/app.py

# Zenith Asset Management (port 5004)
python zenith/app.py
```

Visit each site in your browser:
- Sentinel: http://localhost:5000
- Apex: http://localhost:5001
- Meridian: http://localhost:5002
- Premier: http://localhost:5003
- Zenith: http://localhost:5004

## Deployment to Render

Each site is independently deployable to Render as a separate web service.

### Deployment Steps

1. **Push to GitHub** (each site in its own repository or as a subdirectory)
2. **Create a new Web Service on Render**
3. **Configure:**
   - Build command: `pip install -r requirements.txt`
   - Start command: `gunicorn app:app` or `python app.py`
   - Port: 10000 (Render's default external port maps to your app's port)

### Environment Variables

Set the following in Render's dashboard for each service:
- `FLASK_ENV=production`
- Any site-specific variables (see individual site documentation)

## Shared Utilities

The `shared/` directory contains reusable components:

### `captcha.py`
Generates and validates CAPTCHA challenges.
```python
from shared.captcha import generate_captcha, verify_captcha
```

### `popups.py`
Manages dynamic pop-up content and user interaction tracking.
```python
from shared.popups import create_popup, dismiss_popup
```

### `data_generator.py`
Generates realistic mock financial data (accounts, transactions, rates, etc.).
```python
from shared.data_generator import generate_mock_accounts, generate_transactions
```

### `rate_limit.py`
Implements rate limiting for API endpoints.
```python
from shared.rate_limit import rate_limit_decorator
```

## Dependencies

### Shared Requirements
- **Flask 3.0.0**: Web framework
- **Pillow 10.0.0**: Image generation for CAPTCHA

### Additional Site-Specific Requirements
Each site may have additional dependencies listed in their respective `requirements.txt` files.

## Development Notes

- Each site is a self-contained Flask application
- Shared code is in the `shared/` module and imported as needed
- Sites are designed to be independently deployable without interdependencies
- Mock data is generated fresh on app startup (or can be persisted in optional SQLite databases)

## Contributing

When adding new features:
1. Place shared utilities in `shared/`
2. Keep site-specific code in their respective directories
3. Update this README with any new deployments or features
4. Ensure each site remains independently deployable

## License

This project is provided as-is for educational and testing purposes.
