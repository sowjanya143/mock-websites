# Mock Financial Services Websites - Render Deployment Guide

This guide provides step-by-step instructions for deploying all 9 mock financial services websites to Render.com.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Sites Overview](#sites-overview)
3. [General Deployment Setup](#general-deployment-setup)
4. [Deploying Each Site](#deploying-each-site)
5. [Verification](#verification)
6. [Troubleshooting](#troubleshooting)

---

## Prerequisites

Before deploying to Render, ensure you have:

- **GitHub Account**: Create one at https://github.com if you don't have one
- **Render Account**: Sign up for free at https://render.com
- **Repository Pushed**: This repository must be pushed to GitHub (public or private)
- **Git Bash or Terminal**: For running commands locally

### Local Testing (Recommended)

Before deploying, test the applications locally:

```bash
# Test each site in separate terminal windows
cd sentinel && python app.py  # Port 5000
cd apex && python app.py      # Port 5001
cd meridian && python app.py  # Port 5002
cd premier && python app.py   # Port 5003
cd zenith && python app.py    # Port 5004
cd fortis && python app.py    # Port 5005
cd nexus && python app.py     # Port 5006
cd quantum && python app.py   # Port 5007
cd cipher && python app.py    # Port 5008
```

---

## Sites Overview

### Original 5 Sites

| Site | Port | Key Features |
|------|------|--------------|
| **Sentinel Capital Partners** | 5000 | CAPTCHA on every page |
| **Apex Investment Group** | 5001 | CAPTCHA on data pages, rate limiting |
| **Meridian Global Holdings** | 5002 | Random CAPTCHA, scattered data, delays |
| **Premier Financial Services** | 5003 | Clean baseline (no obstacles) |
| **Zenith Asset Management** | 5004 | All obstacles combined |

### New Advanced Anti-Scraping Sites

| Site | Port | Key Features |
|------|------|--------------|
| **Fortis Banking Group** | 5005 | JWT authentication, login required, session timeout |
| **Nexus Capital** | 5006 | Honeypot detection, bot fingerprinting, fragmented data |
| **Quantum Funds** | 5007 | Geographic blocking, VPN detection, IP-based restrictions |
| **Cipher Wealth Management** | 5008 | API key requirement, encrypted responses, HMAC signing |

### Global Features (All 9 Sites)
- JavaScript requirement (client-side validation)
- Cookie enforcement
- User-agent blocking (scraper detection)
- STRICT_HEADERS validation
- /aum endpoint blocked (403)
- robots.txt with misdirection

---

## General Deployment Setup

### Required Files for Each Site

Each site directory contains:

1. **`{site}/Procfile`** - Defines how to start the web process
   ```
   web: cd {site} && python app.py
   ```

2. **`{site}/runtime.txt`** - Specifies Python version (if applicable)
   ```
   python-3.14.3
   ```

3. **`{site}/requirements.txt`** - Python dependencies
   ```
   Flask==3.0.0
   Pillow==11.1.0
   Werkzeug==3.0.1
   PyJWT==2.8.1
   ```

4. **`{site}/.env.example`** - Environment variables template

### App Configuration

Each `app.py` has been configured to:
- Read the `PORT` environment variable (Render sets this dynamically)
- Bind to `0.0.0.0` to accept external connections
- Default to port 5000, 5001, 5002, 5003, or 5004 respectively

```python
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Adjust per site
    app.run(debug=Config.DEBUG, host='0.0.0.0', port=port)
```

---

## Deploying Each Site

### Step 1: Log In to Render

1. Go to https://render.com
2. Click **Sign Up** or **Sign In**
3. You can use your GitHub account for authentication

### Step 2: Create a New Web Service for Each Site

Repeat the following steps for each of the 5 sites (Sentinel, Apex, Meridian, Premier, Zenith):

#### 2.1 Create Web Service

1. Click the **"New +"** button in the top-right corner
2. Select **"Web Service"**
3. Click **"Connect a repository"**

#### 2.2 Connect Your GitHub Repository

1. Select your GitHub account or organization
2. Search for the repository containing the mock-website
3. Click **"Connect"** next to the correct repository

#### 2.3 Configure Web Service Settings

Fill in the deployment form with site-specific details:

**For Sentinel Capital Partners (Port 5000):**

| Field | Value |
|-------|-------|
| **Name** | `sentinel-mock-website` |
| **Environment** | `Python 3` |
| **Region** | `Oregon (US West)` (or your preferred) |
| **Branch** | `main` |
| **Build Command** | `pip install -r sentinel/requirements.txt` |
| **Start Command** | `cd sentinel && python app.py` |
| **Plan** | `Free` |

**For Apex Investment Group (Port 5001):**

| Field | Value |
|-------|-------|
| **Name** | `apex-mock-website` |
| **Build Command** | `pip install -r apex/requirements.txt` |
| **Start Command** | `cd apex && python app.py` |

**For Meridian Global Holdings (Port 5002):**

| Field | Value |
|-------|-------|
| **Name** | `meridian-mock-website` |
| **Build Command** | `pip install -r meridian/requirements.txt` |
| **Start Command** | `cd meridian && python app.py` |

**For Premier Financial Services (Port 5003):**

| Field | Value |
|-------|-------|
| **Name** | `premier-mock-website` |
| **Build Command** | `pip install -r premier/requirements.txt` |
| **Start Command** | `cd premier && python app.py` |

**For Zenith Asset Management (Port 5004):**

| Field | Value |
|-------|-------|
| **Name** | `zenith-mock-website` |
| **Build Command** | `pip install -r zenith/requirements.txt` |
| **Start Command** | `cd zenith && python app.py` |

**For Fortis Banking Group (Port 5005):**

| Field | Value |
|-------|-------|
| **Name** | `fortis-mock-website` |
| **Build Command** | `pip install -r fortis/requirements.txt` |
| **Start Command** | `cd fortis && python app.py` |

**For Nexus Capital (Port 5006):**

| Field | Value |
|-------|-------|
| **Name** | `nexus-mock-website` |
| **Build Command** | `pip install -r nexus/requirements.txt` |
| **Start Command** | `cd nexus && python app.py` |

**For Quantum Funds (Port 5007):**

| Field | Value |
|-------|-------|
| **Name** | `quantum-mock-website` |
| **Build Command** | `pip install -r quantum/requirements.txt` |
| **Start Command** | `cd quantum && python app.py` |

**For Cipher Wealth Management (Port 5008):**

| Field | Value |
|-------|-------|
| **Name** | `cipher-mock-website` |
| **Build Command** | `pip install -r cipher/requirements.txt` |
| **Start Command** | `cd cipher && python app.py` |

### Step 3: Add Environment Variables

After creating each web service:

1. Go to the service dashboard on Render
2. Click on the **"Environment"** tab (left sidebar)
3. Click **"Add Environment Variable"** and add:

| Key | Value | Notes |
|-----|-------|-------|
| `FLASK_ENV` | `production` | Sets Flask to production mode |
| `DEBUG` | `False` | Disables debug mode for security |
| `SECRET_KEY` | `[generate-random-string]` | See below |
| `PORT` | `5000` | Render assigns automatically; optional |

#### Generate SECRET_KEY

Generate a secure random secret key using Python:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Or use: https://www.randomkeygen.com/ (Fort Knox section)

### Step 4: Deploy

#### 4.1 Automatic Deployment

After creating the web service, Render will automatically:
1. Pull your code from GitHub
2. Install dependencies
3. Build and start the application

**First deployment typically takes 5-10 minutes.**

#### 4.2 Manual Deployment

If auto-deploy is enabled and you've made changes:
1. Push your code to GitHub
2. Render will automatically detect the push and start building
3. Check the **"Logs"** tab to monitor

#### 4.3 Monitor Deployment

1. Go to your web service dashboard on Render
2. Click the **"Logs"** tab
3. Watch for build and startup messages
4. Look for: `Running on http://0.0.0.0:PORT`

---

## Verification

### For Each Site

Once deployment is complete:

#### 5.1 Access the Application

1. Go to the web service dashboard on Render
2. Copy the **URL** from the top
3. Open this URL in your browser

#### 5.2 Verification Checklist

- [ ] **Home page loads** - Verify site branding appears
- [ ] **Site-specific features work**:
  - **Sentinel**: CAPTCHA displays on every page
  - **Apex**: CAPTCHA displays on data pages; rate limiting active
  - **Meridian**: Random CAPTCHA may appear; scattered AUM data
  - **Premier**: Clean interface loads; no security obstacles
  - **Zenith**: All obstacles combined (CAPTCHA, pop-ups, rate limiting)
- [ ] **AUM data loads** - Verify financial data displays
- [ ] **Leadership page** - Navigate to /leadership and verify team data
- [ ] **Pagination works** - Verify pagination controls
- [ ] **All routes accessible**:
  - `/` (Home)
  - `/about` (About)
  - `/leadership` (Leadership)
  - `/strategies` (Strategies)
  - `/investor-resources` (Resources)
  - `/funds` (Funds)
  - `/news` (News)
  - `/contact` (Contact)

#### 5.3 Common Verification Issues

| Issue | Solution |
|-------|----------|
| CAPTCHA image doesn't display | Verify Pillow in requirements.txt |
| 502 Bad Gateway | Check logs for errors; verify PORT configuration |
| Page styling off | Verify static files are served correctly |
| Routes return 404 | Check Flask route definitions in app.py |
| Rate limiting too strict | Adjust MAX_REQUESTS/TIME_WINDOW in config.py |

---

## Troubleshooting

### View Logs

1. Go to web service dashboard on Render
2. Click **"Logs"** tab
3. Look for error patterns

### Common Issues

#### "ModuleNotFoundError: No module named 'flask'"

**Cause**: Dependencies not installed
**Solution**:
- Verify `{site}/requirements.txt` exists with all dependencies
- Check Build Command in Render: `pip install -r {site}/requirements.txt`
- Trigger redeploy by pushing a new commit

#### "Address already in use"

**Cause**: Port conflict
**Solution**:
- Verify app.py uses `os.environ.get('PORT', 5000)`
- Ensure Start Command is: `cd {site} && python app.py`
- Render will automatically assign available PORT

#### "502 Bad Gateway"

**Cause**: Application crashed or not responding
**Solution**:
1. Check logs for errors
2. Verify all routes and templates exist
3. Verify environment variables are set
4. Push a new commit to trigger redeploy

#### "CAPTCHA image won't display"

**Cause**: Pillow not installed
**Solution**:
- Verify `Pillow==10.0.0` in `{site}/requirements.txt`
- Check logs for PIL/ImageDraw errors
- Trigger rebuild via redeploy

#### "Template not found"

**Cause**: Templates in wrong location
**Solution**:
- Verify `{site}/templates/` has all template files
- Check app.py for correct template loader configuration

#### "Static files not loading"

**Cause**: Flask not serving static files
**Solution**:
- Static files should be in `{site}/static/`
- Use relative paths in HTML: `{{ url_for('static', filename='css/main.css') }}`
- Ensure static files are committed to Git

### Rebuild and Redeploy

**Option 1: Push to GitHub**
```bash
git add .
git commit -m "Deployment updates"
git push origin main
```

**Option 2: Manual Redeploy in Render Dashboard**
1. Go to web service dashboard
2. Click **"Manual Deploy"** button
3. Select **"Deploy latest"**

### Environment Variable Issues

If variables aren't being read:
1. Verify variables in Render dashboard (Environment tab)
2. Ensure names match exactly (case-sensitive):
   - `FLASK_ENV` (not `Flask_Env`)
   - `DEBUG` (not `Debug`)
   - `SECRET_KEY` (not `SECRET_KEY_SITE`)
3. Redeploy after changing variables
4. Check logs for confirmation

---

## After Successful Deployment

1. **Document URLs** - Note live URLs for all 5 sites
2. **Run Integration Tests** - Test all features thoroughly
3. **Monitor Performance** - Use Render's analytics
4. **Set Up Custom Domains** (optional) - Add custom domains per site
5. **Enable Auto-Deploy** (recommended) - Automatic deployment on GitHub push

---

## Reference

### Deployment Commands Quick Reference

```bash
# Deploy Sentinel
Build: pip install -r sentinel/requirements.txt
Start: cd sentinel && python app.py

# Deploy Apex
Build: pip install -r apex/requirements.txt
Start: cd apex && python app.py

# Deploy Meridian
Build: pip install -r meridian/requirements.txt
Start: cd meridian && python app.py

# Deploy Premier
Build: pip install -r premier/requirements.txt
Start: cd premier && python app.py

# Deploy Zenith
Build: pip install -r zenith/requirements.txt
Start: cd zenith && python app.py
```

### Site Configuration Files

- **Sentinel**: `sentinel/config.py`
- **Apex**: `apex/config.py`
- **Meridian**: `meridian/config.py`
- **Premier**: `premier/config.py`
- **Zenith**: `zenith/config.py`

### Useful Resources

- [Render Python Deployment](https://render.com/docs/deploy-python)
- [Environment Variables](https://render.com/docs/environment-variables)
- [Static Files](https://render.com/docs/static-files)
- [Custom Domains](https://render.com/docs/custom-domains)
- [Flask Documentation](https://flask.palletsprojects.com)
- [Render Support](https://render.com/support)

---

**Last Updated**: 2026-05-04
**Version**: 1.0
**Python Version**: 3.11.7
