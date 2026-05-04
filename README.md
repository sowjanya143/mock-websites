# Mock Financial Services Websites

A collection of 5 independent Flask-based mock financial services websites, each designed to demonstrate different web interaction patterns and security challenges.

## Overview

This project contains the following mock financial services sites:

### 1. **Fortress Bank**
A banking website with CAPTCHA protection on login attempts.

### 2. **Heitman Investment Group**
Investment services platform featuring interactive pop-ups and user engagement elements.

### 3. **Nomura Trading**
A trading platform with complex rate limiting and request throttling.

### 4. **Hokuyo Bank**
A Japanese-themed banking service with unique behavioral patterns.

### 5. **Oaktree Capital**
A capital management firm with advanced anti-scraping features.

## Site-Specific Behaviors

Each site is independently deployable and exhibits unique characteristics:

- **Fortress Bank**: CAPTCHA verification system on authentication
- **Heitman Investment Group**: Requires interaction with dynamic pop-ups before accessing content
- **Nomura Trading**: Implements rate limiting to prevent high-frequency requests
- **Hokuyo Bank**: Specialized behavioral patterns and data presentation
- **Oaktree Capital**: Advanced anti-bot detection and anti-scraping measures

## Project Structure

```
mock-website/
├── fortress/              # Fortress Bank Flask app
├── heitman/              # Heitman Investment Group Flask app
├── nomura/               # Nomura Trading Flask app
├── hokuyo/               # Hokuyo Bank Flask app
├── oaktree/              # Oaktree Capital Flask app
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
# Fortress Bank (port 5001)
python fortress/app.py

# Heitman Investment Group (port 5002)
python heitman/app.py

# Nomura Trading (port 5003)
python nomura/app.py

# Hokuyo Bank (port 5004)
python hokuyo/app.py

# Oaktree Capital (port 5005)
python oaktree/app.py
```

Visit each site in your browser:
- Fortress: http://localhost:5001
- Heitman: http://localhost:5002
- Nomura: http://localhost:5003
- Hokuyo: http://localhost:5004
- Oaktree: http://localhost:5005

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
