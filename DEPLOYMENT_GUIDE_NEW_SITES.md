# Deployment Guide: New Mock Financial Websites

## Overview

This guide covers deployment of the 3 newly built mock financial websites:

1. **Fortis Banking Group** (Port 5005)
2. **Nexus Capital** (Port 5006)
3. **Cipher Wealth Management** (Port 5008)

All sites follow the same deployment architecture as existing sites (Sentinel, Apex, Premier, Zenith, Meridian).

---

## Quick Summary

| Site | Port | Framework | Status | Data | Templates |
|------|------|-----------|--------|------|-----------|
| Fortis Banking Group | 5005 | Flask | Production-Ready | ✅ | ✅ |
| Nexus Capital | 5006 | Flask | Production-Ready | ✅ | ✅ |
| Cipher Wealth Management | 5008 | Flask | Production-Ready | ✅ | ✅ |

---

## Prerequisites

Before deploying, ensure you have:

- Python 3.14.3 or compatible version
- Git for version control
- Render.com account (or compatible hosting platform)
- Basic knowledge of Flask applications
- Environment variables management

---

## Local Development Setup

### 1. Clone Repository

```bash
git clone https://github.com/your-org/mock-website.git
cd mock-website
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
# For Fortis
cd fortis && pip install -r requirements.txt

# For Nexus
cd nexus && pip install -r requirements.txt

# For Cipher
cd cipher && pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create `.env` file in each site directory:

```bash
# fortis/.env
SECRET_KEY=your-fortis-secret-key-here
DEBUG=True
PORT=5005

# nexus/.env
SECRET_KEY=your-nexus-secret-key-here
DEBUG=True
PORT=5006

# cipher/.env
SECRET_KEY=your-cipher-secret-key-here
DEBUG=True
PORT=5008
```

### 5. Run Locally

```bash
# Fortis
cd fortis && python app.py
# Access at http://localhost:5005

# Nexus
cd nexus && python app.py
# Access at http://localhost:5006

# Cipher
cd cipher && python app.py
# Access at http://localhost:5008
```

---

## Production Deployment (Render.com)

### Prerequisites for Render Deployment

1. Render.com account
2. GitHub repository with all site code
3. GitHub Personal Access Token

### Step-by-Step Deployment

#### 1. Create New Web Service on Render

For each site (Fortis, Nexus, Cipher):

1. Log in to [Render Dashboard](https://dashboard.render.com)
2. Click **New +** → **Web Service**
3. Connect your GitHub repository
4. Select the repository branch (main)

#### 2. Configure Each Service

**Fortis Banking Group:**

```
Name: Fortis Banking Group
Region: Oregon (or closest to your users)
Branch: main
Build Command: pip install -r fortis/requirements.txt
Start Command: cd fortis && python app.py
Environment: Python 3
Plan: Free or Standard
```

**Environment Variables:**
```
SECRET_KEY=your-production-fortis-secret-key
DEBUG=False
PORT=5005
```

**Nexus Capital:**

```
Name: Nexus Capital
Region: Oregon (or closest to your users)
Branch: main
Build Command: pip install -r nexus/requirements.txt
Start Command: cd nexus && python app.py
Environment: Python 3
Plan: Free or Standard
```

**Environment Variables:**
```
SECRET_KEY=your-production-nexus-secret-key
DEBUG=False
PORT=5006
```

**Cipher Wealth Management:**

```
Name: Cipher Wealth Management
Region: Oregon (or closest to your users)
Branch: main
Build Command: pip install -r cipher/requirements.txt
Start Command: cd cipher && python app.py
Environment: Python 3
Plan: Free or Standard
```

**Environment Variables:**
```
SECRET_KEY=your-production-cipher-secret-key
DEBUG=False
PORT=5008
```

#### 3. Custom Domain Setup (Optional)

For each service:

1. Go to **Settings** tab
2. Scroll to **Custom Domain**
3. Add your custom domain (e.g., `fortis.yourdomain.com`)
4. Configure DNS records as shown in Render instructions

**DNS Configuration:**
```
Type: CNAME
Name: fortis (or nexus, cipher)
Value: [provided-by-render]
TTL: 3600
```

#### 4. Deploy

- Render auto-deploys on every push to main branch
- Manual deploy: Click **Deploy latest commit** on service dashboard
- Check deployment status in **Deploys** tab
- Monitor logs in **Logs** tab

---

## File Structure for Deployment

Each new site follows this structure:

```
fortis/
├── app.py              # Flask application
├── config.py           # Configuration settings
├── requirements.txt    # Python dependencies
├── Procfile           # Deployment configuration
├── runtime.txt        # Python version
├── static/
│   ├── css/
│   │   ├── style.css
│   │   └── peachtree-modern.css
│   └── js/
│       └── common.js
├── templates/
│   ├── base.html
│   ├── home.html
│   ├── strategies.html
│   ├── about.html
│   ├── leadership.html
│   ├── funds.html
│   ├── news.html
│   ├── contact.html
│   └── [...other templates]
└── data/
    ├── aum.json
    ├── team.json
    ├── news.json
    ├── awards.json (Fortis only)
    ├── mandates.json (Nexus only)
    └── properties.json (Cipher only)

nexus/
├── [Same structure as Fortis]

cipher/
├── [Same structure as Fortis]
```

---

## Dependencies & Requirements

### Python Packages (All 3 Sites)

```
Flask==3.0.0               # Web framework
Pillow==11.1.0            # Image processing (for CAPTCHA)
Werkzeug==3.0.1           # WSGI utilities
PyJWT==2.12.1             # JWT authentication
```

### Optional but Recommended

```
python-dotenv==1.0.0      # Environment variable management
gunicorn==21.2.0          # Production WSGI server
```

To add these, update `requirements.txt`:

```bash
Flask==3.0.0
Pillow==11.1.0
Werkzeug==3.0.1
PyJWT==2.12.1
python-dotenv==1.0.0
gunicorn==21.2.0
```

Update Procfile for production:

```
web: cd fortis && gunicorn app:app
web: cd nexus && gunicorn app:app
web: cd cipher && gunicorn app:app
```

---

## Configuration Files

### Procfile

```
web: cd fortis && python app.py
```

**For Production with Gunicorn:**
```
web: cd fortis && gunicorn app:app -w 4 -b 0.0.0.0:$PORT
```

### runtime.txt

```
python-3.14.3
```

Specify exact Python version for consistent deployments.

### requirements.txt

List all Python dependencies with pinned versions:

```
Flask==3.0.0
Pillow==11.1.0
Werkzeug==3.0.1
PyJWT==2.12.1
```

---

## Environment Variables

### Required Variables

```
SECRET_KEY              # Session encryption key (generate random)
DEBUG                  # False in production, True in development
PORT                   # 5005 (Fortis), 5006 (Nexus), 5008 (Cipher)
```

### Optional Variables

```
FLASK_ENV              # production or development
FLASK_APP              # app.py
LOG_LEVEL              # INFO, DEBUG, WARNING
```

### Generate Secure SECRET_KEY

```python
import secrets
print(secrets.token_urlsafe(32))
```

Output example: `abcdef1234567890_XYZABC-defghijk`

---

## Health Checks & Monitoring

### Render Health Check

Render automatically sends GET requests to `/` to verify service health.

**Add to app.py if needed:**

```python
@app.route('/health')
def health():
    return jsonify({'status': 'healthy'}), 200
```

### Monitoring Deployment

1. **Logs Tab**: Real-time application logs
2. **Metrics Tab**: CPU, memory, response times
3. **Events Tab**: Deployment history and status
4. **Integrations**: Connect to monitoring services (DataDog, New Relic, etc.)

---

## Testing Before Deployment

### 1. Local Testing

```bash
# Start local Flask server
cd fortis && python app.py

# Test homepage
curl http://localhost:5005/

# Test API endpoints
curl http://localhost:5005/api/funds

# Test CSS loads
# Visit in browser: http://localhost:5005/
# Check browser DevTools → Network → CSS loads successfully
```

### 2. Check All Templates

```bash
# Verify template rendering
python -c "
from app import app
with app.app_context():
    templates = [
        'home.html', 'about.html', 'leadership.html',
        'strategies.html', 'funds.html', 'news.html', 'contact.html'
    ]
    from flask import render_template
    for t in templates:
        render_template(t)
        print(f'✓ {t}')
"
```

### 3. Verify Data Files

```bash
# Check JSON data loads correctly
python -c "
import json
files = ['data/aum.json', 'data/team.json', 'data/news.json']
for f in files:
    with open(f) as file:
        data = json.load(file)
        print(f'✓ {f} - {len(data)} items')
"
```

### 4. CSS & Static Files

```bash
# Verify static files are served
ls -la static/css/
ls -la static/js/
```

---

## Troubleshooting

### Common Issues & Solutions

#### 1. "ModuleNotFoundError: No module named 'flask'"

**Solution:**
```bash
pip install -r requirements.txt
```

#### 2. "Port already in use"

**Solution:**
```bash
# Find process using port 5005
lsof -i :5005

# Kill process
kill -9 <PID>

# Or use different port
PORT=5009 python app.py
```

#### 3. "TemplateNotFound: home.html"

**Solution:**
- Verify `templates/` directory exists
- Check file spelling (case-sensitive)
- Ensure templates are in correct subdirectory

#### 4. "JSON decode error in aum.json"

**Solution:**
```bash
# Validate JSON syntax
python -m json.tool data/aum.json
```

#### 5. "Static files not loading (404)"

**Solution:**
```bash
# Verify static directory structure
find static/ -type f

# In production, ensure static path is correct
# Check URL_FOR in templates generates correct paths
```

#### 6. Deployment Build Fails on Render

**Solution:**
1. Check build command in Render settings
2. Verify `requirements.txt` is in site directory
3. Check Python version compatibility
4. Review build logs in Render dashboard
5. Test locally first: `pip install -r requirements.txt`

---

## Monitoring & Maintenance

### Daily Checks

```bash
# Check service status
curl https://fortis-banking.onrender.com/

# Check response time
time curl https://fortis-banking.onrender.com/

# Monitor logs
# View in Render dashboard → Logs tab
```

### Weekly Maintenance

1. **Review error logs** for 500 errors or exceptions
2. **Check uptime** in Render dashboard
3. **Verify data files** are loading correctly
4. **Test key routes**: /, /about, /strategies, /funds
5. **Check CSS/JS** loads without 404s

### Monthly Tasks

1. **Update dependencies** (security patches)
2. **Review performance metrics**
3. **Audit access logs** for suspicious activity
4. **Test all forms** and API endpoints
5. **Backup data files** if needed

---

## Security Checklist

- [ ] SECRET_KEY is unique and strong
- [ ] DEBUG=False in production
- [ ] HTTPS enabled (automatic on Render)
- [ ] No sensitive data in code (use env vars)
- [ ] No hardcoded API keys or passwords
- [ ] robots.txt configured
- [ ] CORS headers set appropriately
- [ ] Security headers enabled (X-Frame-Options, etc.)
- [ ] Rate limiting enabled
- [ ] CAPTCHA and cookie requirements configured

---

## Scaling & Performance

### If Performance Degrades

1. **Upgrade Render Plan:**
   - Free → Standard ($7/month)
   - Standard → Pro ($25/month)

2. **Enable Caching:**
   - Browser caching (static files)
   - Server-side session caching

3. **Optimize Database Queries:**
   - Verify JSON data loads efficiently
   - Cache API responses

4. **CDN Integration:**
   - Serve static files from CDN
   - Reduce origin server load

---

## Rollback Procedure

If deployment fails:

1. **Check Render Dashboard:**
   - Go to service → Deploys tab
   - Identify last working deployment

2. **Redeploy Previous Version:**
   - Click on previous deploy
   - Click "Redeploy"
   - Wait for service to restart

3. **Or Manual Revert:**
   - Push previous commit to GitHub
   - Render auto-deploys latest commit
   ```bash
   git revert HEAD
   git push origin main
   ```

---

## Accessing Deployed Sites

Once deployed on Render:

```
Fortis Banking Group:    https://fortis-banking.onrender.com
Nexus Capital:           https://nexus-capital.onrender.com
Cipher Wealth Management: https://cipher-wealth.onrender.com
```

Or with custom domains:

```
Fortis Banking Group:    https://fortis.yourdomain.com
Nexus Capital:           https://nexus.yourdomain.com
Cipher Wealth Management: https://cipher.yourdomain.com
```

---

## Automation & CI/CD

### GitHub Actions Workflow (Optional)

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Render

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Notify Render
        run: |
          curl -X POST https://api.render.com/deploy/srv-${{ secrets.RENDER_FORTIS_ID }}?key=${{ secrets.RENDER_API_KEY }}
```

---

## Support & Documentation

### Useful Links

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Render Documentation](https://docs.render.com/)
- [Python Package Index](https://pypi.org/)
- [GitHub Pages](https://pages.github.com/)

### Getting Help

1. Check application logs in Render dashboard
2. Review this deployment guide troubleshooting section
3. Search GitHub Issues for similar problems
4. Contact Render support for infrastructure issues

---

## Summary

All 3 new websites (Fortis, Nexus, Cipher) are production-ready and follow the same deployment architecture:

- ✅ Flask-based Python applications
- ✅ Modern CSS designs (Peachtree, Shadow Elegant, Growth Premium)
- ✅ Comprehensive data files (JSON-based)
- ✅ Responsive templates
- ✅ Security features (CAPTCHA, rate limiting, cookies)
- ✅ Easy deployment to Render.com

**Deployment Time:** ~5 minutes per site
**Estimated Cost:** Free tier or $7-25/month per service on Render
**Uptime SLA:** 99.9% with Standard plan

---

**Last Updated:** 2026-05-05
**Status:** Deployment-Ready
