# Fortress Mock Financial Website - Render Deployment Guide

This guide provides step-by-step instructions for deploying the Fortress mock financial website to Render.com.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Prepare Fortress for Deployment](#step-1-prepare-fortress-for-deployment)
3. [Create Render Web Service](#step-2-create-render-web-service)
4. [Configure Environment Variables](#step-3-add-environment-variables)
5. [Deploy](#step-4-deploy)
6. [Verify Deployment](#step-5-verify)
7. [Troubleshooting](#step-6-troubleshooting)

---

## Prerequisites

Before deploying to Render, ensure you have:

- **GitHub Account**: Create one at https://github.com if you don't have one
- **Render Account**: Sign up for free at https://render.com
- **Repository Pushed**: This repository must be pushed to GitHub (public or private)
- **Git Bash or Terminal**: For running commands locally

### Local Testing (Optional but Recommended)

Before deploying, test the application locally:

```bash
cd fortress
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Visit http://localhost:5000 to verify the app works.

---

## Step 1: Prepare Fortress for Deployment

The Fortress site has been configured for Render deployment. Verify the following files exist:

### Required Files

1. **`fortress/Procfile`** - Defines how to start the web process
   ```
   web: cd fortress && python app.py
   ```

2. **`fortress/runtime.txt`** - Specifies Python version
   ```
   python-3.11.7
   ```

3. **`fortress/requirements.txt`** - Python dependencies
   ```
   Flask==3.0.0
   Pillow==10.0.0
   Werkzeug==3.0.1
   ```

4. **`fortress/.env.example`** - Environment variables template
   - Copy this to set environment variables in Render dashboard

### App Configuration

The `fortress/app.py` has been updated to:
- Read the `PORT` environment variable (Render sets this dynamically)
- Bind to `0.0.0.0` to accept external connections
- Default to port 5000 if PORT is not set

```python
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=Config.DEBUG, host='0.0.0.0', port=port)
```

---

## Step 2: Create Render Web Service

### 2.1 Log In to Render

1. Go to https://render.com
2. Click **Sign Up** or **Sign In**
3. You can use your GitHub account for authentication

### 2.2 Create a New Web Service

1. Click the **"New +"** button in the top-right corner
2. Select **"Web Service"**
3. Click **"Connect a repository"**

### 2.3 Connect Your GitHub Repository

1. Select your GitHub account or organization
2. Search for the repository containing the mock-website
3. Click **"Connect"** next to the correct repository

### 2.4 Configure Web Service Settings

Fill in the following details on the deployment form:

| Field | Value |
|-------|-------|
| **Name** | `fortress-mock-website` (or your preferred name) |
| **Environment** | `Python 3` |
| **Region** | `Oregon (US West)` (or your preferred region) |
| **Branch** | `main` (or your deployment branch) |
| **Build Command** | `pip install -r fortress/requirements.txt` |
| **Start Command** | `cd fortress && python app.py` |
| **Plan** | `Free` (for testing and development) |

### 2.5 Review Configuration

The form should look like this:
- **Name**: fortress-mock-website
- **Environment**: Python 3
- **Build Command**: pip install -r fortress/requirements.txt
- **Start Command**: cd fortress && python app.py
- **Auto-Deploy**: Yes (checked)
- **Plan**: Free

---

## Step 3: Add Environment Variables

After creating the web service, you need to configure environment variables.

### 3.1 Access Environment Variables

1. Go to your Fortress web service dashboard on Render
2. Click on the **"Environment"** tab (left sidebar)

### 3.2 Add Environment Variables

Click **"Add Environment Variable"** and add the following variables:

| Key | Value | Notes |
|-----|-------|-------|
| `FLASK_ENV` | `production` | Sets Flask to production mode |
| `DEBUG` | `False` | Disables debug mode for security |
| `SECRET_KEY` | `[generate-random-string]` | See below for generation instructions |
| `PORT` | `5000` | Optional - Render assigns automatically |

### 3.3 Generate SECRET_KEY

Generate a secure random secret key using Python:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

This will output something like: `a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6a7b8c9d0e`

Copy this value and paste it into the `SECRET_KEY` environment variable in Render.

Alternatively, use this quick generator:
- Go to: https://www.randomkeygen.com/ (Fort Knox section)
- Copy the generated key

### 3.4 Save Environment Variables

Click **"Save"** to apply the environment variables. The service will redeploy automatically.

---

## Step 4: Deploy

### 4.1 Manual Deployment (if needed)

If auto-deploy is enabled and you've made changes:
1. Push your code to GitHub
2. Render will automatically detect the push and start building
3. Check the **"Logs"** tab to monitor the deployment

### 4.2 Initial Deployment

After creating the web service, Render will automatically:
1. Pull your code from GitHub
2. Install dependencies from `requirements.txt`
3. Build the application
4. Start the application using the **Start Command**

**First deployment typically takes 5-10 minutes.** Subsequent deployments are faster.

### 4.3 Monitor Deployment

1. Go to your web service dashboard on Render
2. Click the **"Logs"** tab
3. Watch for build and startup messages
4. Look for: `Running on http://0.0.0.0:PORT` (indicates successful startup)

---

## Step 5: Verify Deployment

Once the deployment is complete and the service is running, verify the application works correctly.

### 5.1 Access the Application

1. Go to your web service dashboard on Render
2. Copy the **URL** from the top (format: `https://fortress-mock-website.onrender.com`)
3. Open this URL in your browser

### 5.2 Verification Checklist

- [ ] **Home page loads** - Visit the home page and verify the Fortress branding appears
- [ ] **CAPTCHA displays** - Verify the CAPTCHA image appears on the first visit
- [ ] **CAPTCHA submission** - Enter the CAPTCHA answer and verify access is granted
- [ ] **AUM data loads** - Verify Assets Under Management data displays correctly
- [ ] **Leadership page** - Navigate to /leadership and verify team member data loads
- [ ] **Pagination works** - Verify pagination controls work on the leadership page
- [ ] **All routes accessible** - Test key routes:
  - `/` (Home)
  - `/about` (About)
  - `/leadership` (Leadership)
  - `/strategies` (Strategies)
  - `/investor-resources` (Resources)
  - `/funds` (Funds)
  - `/news` (News)
  - `/contact` (Contact)

### 5.3 Common Verification Issues

| Issue | Solution |
|-------|----------|
| CAPTCHA image doesn't display | Verify Pillow is installed (in requirements.txt) |
| 502 Bad Gateway error | Check logs for errors; ensure PORT is configured |
| Page loads but styling is off | Verify static files are being served correctly |
| Routes return 404 | Check Flask route definitions in app.py |

---

## Step 6: Troubleshooting

### 6.1 View Logs

The most useful troubleshooting tool is the application logs:

1. Go to your web service dashboard on Render
2. Click the **"Logs"** tab
3. Scroll through logs to find errors or warnings
4. Common log patterns:
   - `Build started` - Initial build phase
   - `Running on` - Application successfully started
   - `ERROR` - Application errors (highlighted in red)
   - `WARNING` - Application warnings (highlighted in yellow)

### 6.2 Common Deployment Issues

#### Issue: "ModuleNotFoundError: No module named 'flask'"

**Cause**: Dependencies not installed
**Solution**:
- Verify `fortress/requirements.txt` exists and has all dependencies
- Check Build Command in Render: `pip install -r fortress/requirements.txt`
- Manually trigger a redeploy by pushing a new commit

#### Issue: "Address already in use" or "Port 5000 already in use"

**Cause**: Port conflict
**Solution**:
- Verify app.py uses `os.environ.get('PORT', 5000)`
- Ensure Start Command is: `cd fortress && python app.py`
- Render will automatically assign an available PORT

#### Issue: "502 Bad Gateway" error

**Cause**: Application crashed or not responding
**Solution**:
1. Check logs for errors
2. Verify all routes and templates exist
3. Verify environment variables are set correctly
4. Trigger a manual redeploy: push a commit to GitHub

#### Issue: "CAPTCHA image won't display"

**Cause**: PIL/Pillow not installed or ImageDraw error
**Solution**:
- Verify `Pillow==10.0.0` is in `fortress/requirements.txt`
- Check logs for PIL/ImageDraw errors
- Trigger a rebuild: `pip install -r fortress/requirements.txt`

#### Issue: "Template not found" error

**Cause**: Templates in wrong location or jinja2 loader misconfigured
**Solution**:
- Verify `fortress/templates/` directory has all template files
- Check that `app.py` has correct ChoiceLoader configuration
- Verify shared templates are in `shared/templates/`

#### Issue: "Static files not loading" (CSS/JS not displaying)

**Cause**: Flask not serving static files correctly
**Solution**:
- Static files should be in `fortress/static/`
- Verify paths in HTML templates are relative: `{{ url_for('static', filename='css/main.css') }}`
- For Render, ensure static files are committed to Git (not in .gitignore)

### 6.3 Rebuild and Redeploy

If you make changes and want to force a redeploy:

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

### 6.4 Check Python Version

If you encounter version-specific issues:

```bash
# In Render logs, you'll see the Python version used
# Verify it matches fortress/runtime.txt
python-3.11.7
```

### 6.5 Environment Variable Issues

If environment variables aren't being read:

1. Verify variables are set in Render dashboard (Environment tab)
2. Ensure variable names match exactly (case-sensitive):
   - `FLASK_ENV` (not `Flask_Env` or `flask_env`)
   - `DEBUG` (not `Debug` or `debug`)
   - `SECRET_KEY` (not `SECRET_KEY_FORTRESS`)
3. Redeploy after changing environment variables
4. Check logs for confirmation that variables are loaded

---

## Next Steps

### After Successful Fortress Deployment

1. **Document the URL** - Note your live URL for testing and sharing
2. **Run Integration Tests** - Test all features thoroughly
3. **Monitor Performance** - Use Render's analytics to monitor CPU, memory, and requests
4. **Set Up Custom Domain** (optional) - In Render settings, add a custom domain
5. **Enable Auto-Deploy** (recommended) - Automatic deployment on GitHub push

### Deploying Other Sites

Repeat this process for the other mock financial websites:
- Heitman
- Nomura
- Hokuyo
- Oaktree

Each site has its own `requirements.txt`, templates, and data files. The deployment process is identical.

---

## Reference

### Useful Render Documentation
- [Render Python Deployment](https://render.com/docs/deploy-python)
- [Environment Variables](https://render.com/docs/environment-variables)
- [Static Files](https://render.com/docs/static-files)
- [Custom Domains](https://render.com/docs/custom-domains)

### Fortress Site Documentation
- Configuration: `fortress/config.py`
- Routes: `fortress/app.py`
- Templates: `fortress/templates/`
- Static files: `fortress/static/`
- Data files: `fortress/data/`

### Troubleshooting Resources
- Check logs in Render dashboard
- Review this DEPLOYMENT.md guide
- Check Flask documentation: https://flask.palletsprojects.com
- Render support: https://render.com/support

---

## Support

If you encounter issues not covered in this guide:

1. **Check the logs** - Most issues are visible in Render logs
2. **Review this guide** - Use the troubleshooting section
3. **Check error messages** - Error messages often indicate the solution
4. **Verify configuration** - Double-check settings match this guide
5. **Contact Render support** - https://render.com/support

---

**Last Updated**: 2026-05-04
**Fortress Version**: 1.0
**Python Version**: 3.11.7
