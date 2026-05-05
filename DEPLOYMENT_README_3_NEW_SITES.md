# Deployment Guide - 3 New Mock Financial Websites

## Quick Overview

Three new professional mock financial websites are ready for deployment:

| Site | Port | URL (Local) | Reference | Status |
|------|------|-----------|-----------|--------|
| **Fortis Banking Group** | 5005 | http://localhost:5005 | peachtreegroup.com | ✅ Ready |
| **Nexus Capital** | 5006 | http://localhost:5006 | shadowpartners.com.my | ✅ Ready |
| **Cipher Wealth Management** | 5008 | http://localhost:5008 | growthpoint.com.au | ✅ Ready |

---

## What's Inside Each Site

### Fortis Banking Group (Port 5005)
**Peachtree Modern Design** - Warm terracotta accents, real estate focused
- **Business:** Real estate with 3 verticals (Investments, Credit & Lending, Investment Services)
- **AUM:** $6 billion
- **Unique Features:**
  - Track record display (104 deals, $10.6B lending, 1,200+ properties)
  - Awards/certifications (INC 5000, Hilton Award)
  - Media mentions section (Bloomberg, CNBC)
  - Special data file: `awards.json`
- **Color Scheme:** Navy (#1a3a52) + Warm Accent (#c07a3f)

### Nexus Capital (Port 5006)
**Shadow Elegant Design** - Dark charcoal, sophisticated private equity
- **Business:** Private equity with philosophy-driven approach
- **AUM:** $420 billion
- **Unique Features:**
  - 3 investment philosophy cards (Time-Tested Value, Catalytic, Risk-Based)
  - Investment products overview (Wholesale, Customized Mandates)
  - Differentiators messaging
  - Special data file: `mandates.json`
- **Color Scheme:** Charcoal (#2d2d2d) + Silver/Gold accents

### Cipher Wealth Management (Port 5008)
**Growth Premium Design** - Vibrant teal/orange, investor relations focus
- **Business:** Property investment with investor communications
- **AUM:** $5.4 billion
- **Unique Features:**
  - Portfolio metrics (WACR 6.7%, WALE 5.6 years, 95% occupancy)
  - Property portfolio carousel (5 featured properties)
  - Investor centre section
  - Special data file: `properties.json`
- **Color Scheme:** Teal (#0d7377) + Orange (#ff8c42)

---

## Files Created

### New Data Files
```
fortis/data/awards.json              ← Certifications & media mentions
nexus/data/mandates.json             ← Investment mandates & offerings
cipher/data/properties.json          ← 5 featured properties with metrics
```

### Updated Data Files
```
fortis/data/aum.json                 ← Vertical-based structure
nexus/data/aum.json                  ← Philosophy-based allocation
cipher/data/aum.json                 ← Portfolio metrics (WACR, WALE, etc)
```

### New Templates
```
fortis/templates/base.html           ← Fortis-specific base with peachtree CSS
nexus/templates/base.html            ← Nexus-specific base with shadow CSS
cipher/templates/base.html           ← Cipher-specific base with growth CSS

fortis/templates/home.html           ← 3 verticals layout
nexus/templates/home.html            ← 3 philosophy cards layout
cipher/templates/home.html           ← Investor relations layout + carousel
```

### CSS Stylesheets
```
fortis/static/css/peachtree-modern.css       (470 lines)
nexus/static/css/shadow-elegant.css          (490 lines)
cipher/static/css/growth-premium.css         (480 lines)
```

### Deployment Files (Already exist)
```
fortis/app.py
fortis/config.py
fortis/Procfile              → web: cd fortis && python app.py
fortis/runtime.txt           → python-3.14.3
fortis/requirements.txt      → Flask, Pillow, Werkzeug, PyJWT

[Same for nexus and cipher]
```

---

## Step-by-Step Deployment

### Option 1: Local Testing First

```bash
# Test Fortis
cd fortis
python app.py
# Visit http://localhost:5005

# Test Nexus  
cd nexus
python app.py
# Visit http://localhost:5006

# Test Cipher
cd cipher
python app.py
# Visit http://localhost:5008
```

Verify:
- [ ] Homepage loads
- [ ] CSS styling displays
- [ ] Navigation menu works
- [ ] Data renders (no blank pages)
- [ ] No console errors
- [ ] Responsive on mobile

### Option 2: Deploy to Render.com (Recommended)

#### Step 1: Prepare GitHub
```bash
git add .
git commit -m "Add Fortis, Nexus, Cipher sites with new designs and data"
git push origin main
```

#### Step 2: Create Render Services (Do this 3 times)

For **Fortis**:
1. Go to https://dashboard.render.com
2. Click **New +** → **Web Service**
3. Connect GitHub repository
4. Fill in:
   ```
   Name: Fortis Banking Group
   Build Command: pip install -r fortis/requirements.txt
   Start Command: cd fortis && python app.py
   Environment: Python 3
   Plan: Free (to start)
   ```
5. Environment Variables:
   ```
   SECRET_KEY = your-secret-key-here
   DEBUG = False
   ```
6. Click **Create Web Service**
7. Wait for deployment (2-3 minutes)
8. Access at: https://fortis-banking.onrender.com

Repeat for **Nexus**:
- Build: `pip install -r nexus/requirements.txt`
- Start: `cd nexus && python app.py`
- URL: https://nexus-capital.onrender.com

Repeat for **Cipher**:
- Build: `pip install -r cipher/requirements.txt`
- Start: `cd cipher && python app.py`
- URL: https://cipher-wealth.onrender.com

#### Step 3: Configure Custom Domains (Optional)

In Render dashboard for each service:
1. Go to **Settings** tab
2. Under **Custom Domain**, add your domain
3. Update DNS records to CNAME pointing to Render

---

## Configuration Files

### requirements.txt (All sites)
```
Flask==3.0.0
Pillow==11.1.0
Werkzeug==3.0.1
PyJWT==2.12.1
```

### Procfile
```
web: cd {site_name} && python app.py
```

### runtime.txt
```
python-3.14.3
```

---

## Environment Variables

Generate a secure SECRET_KEY:
```python
import secrets
print(secrets.token_urlsafe(32))
```

Set in Render dashboard:
- `SECRET_KEY` = your generated key
- `DEBUG` = False (production)

---

## Post-Deployment Checklist

For each site (Fortis, Nexus, Cipher):

- [ ] Site loads at HTTPS URL
- [ ] Homepage displays without errors
- [ ] CSS styling applies correctly
- [ ] All images/icons load
- [ ] Navigation menu functional
- [ ] Data tables/cards render
- [ ] No 404 errors in console
- [ ] Mobile responsive (test at 375px)
- [ ] Performance: Load time < 2 seconds
- [ ] Green HTTPS lock icon

---

## Testing Each Site

### Fortis Homepage Should Show:
- Company name and tagline
- Capital metrics cards (Raised, Deployed, Returned, AUM)
- 3 business vertical cards
- Awards/recognition section
- Featured funds table

### Nexus Homepage Should Show:
- Company name and tagline
- Global AUM ($420B)
- 3 philosophy cards
- Investment products section
- Differentiators messaging

### Cipher Homepage Should Show:
- Company name and tagline
- Featured announcement
- Company mission statement
- 4 portfolio metrics cards
- 5 properties in carousel
- Investor centre links
- Latest news feed

---

## Troubleshooting

### "ModuleNotFoundError: No module named 'flask'"
```bash
pip install -r {site}/requirements.txt
```

### "Port already in use"
```bash
# Find and kill process
lsof -i :5005
kill -9 <PID>
```

### "TemplateNotFound"
- Check `templates/` directory exists
- Verify file names (case-sensitive)
- Ensure base.html is in correct location

### "Static files not loading (404)"
- Check CSS file path in base.html
- Verify static directory structure
- Use browser DevTools to see actual request URL

### "JSON decode error"
```bash
# Validate JSON files
python -m json.tool fortis/data/aum.json
```

### Deployment fails on Render
1. Check build logs in Render dashboard
2. Verify requirements.txt is in site directory
3. Test locally first
4. Ensure Procfile is correct
5. Check Python version compatibility

---

## Monitoring & Maintenance

### Daily (Week 1)
- Check Render logs for errors
- Verify uptime
- Test homepage loads

### Weekly (Week 2+)
- Review error logs
- Check performance metrics
- Test all main pages
- Verify data loads

### Monthly
- Update dependencies (security)
- Review performance trending
- Security audit
- Check all links work

---

## Quick Commands

### Local Testing
```bash
cd fortis && python app.py      # Fortis on :5005
cd nexus && python app.py       # Nexus on :5006
cd cipher && python app.py      # Cipher on :5008
```

### Git Deployment
```bash
git add .
git commit -m "Deploy new sites"
git push origin main  # Auto-deploys to Render
```

### Check API
```bash
curl https://fortis-banking.onrender.com/
curl https://nexus-capital.onrender.com/
curl https://cipher-wealth.onrender.com/
```

---

## Key Stats

| Metric | Value |
|--------|-------|
| **Build Time (per site)** | ~30s |
| **Local Test Time** | 5-10 min |
| **Render Deployment Time** | 2-3 min |
| **Total Time (all 3 sites)** | ~45 min |
| **Monthly Cost (Render Free)** | $0 |
| **Monthly Cost (Render Standard)** | $21 (all 3 sites) |
| **Storage per Site** | ~2MB (data + code) |
| **Typical Load Time** | <1 second |

---

## Success Criteria

✅ All sites deployed successfully when:

- [ ] Fortis accessible: https://fortis-banking.onrender.com
- [ ] Nexus accessible: https://nexus-capital.onrender.com
- [ ] Cipher accessible: https://cipher-wealth.onrender.com
- [ ] All pages load without 500 errors
- [ ] CSS displays correctly
- [ ] Data renders (tables/cards visible)
- [ ] HTTPS enabled (green lock)
- [ ] Responsive on mobile

---

## Documentation Files

For more detailed information:

- **DEPLOYMENT_GUIDE_NEW_SITES.md** - Comprehensive guide
- **QUICK_DEPLOYMENT_CHECKLIST.md** - Quick reference checklist
- **DESIGN_SYSTEM_SUMMARY.md** - Design documentation
- **PREMIER_MODERN_MINIMAL.md** - Design reference
- **SENTINEL_CORPORATE_MODULAR.md** - Design reference
- **APEX_GLASSMORPHISM.md** - Design reference

---

## Support Links

- Render Documentation: https://docs.render.com/
- Flask Documentation: https://flask.palletsprojects.com/
- GitHub Pages: https://pages.github.com/
- Python Docs: https://docs.python.org/

---

## Next Steps

1. **Today:** Review this guide and test locally
2. **Tomorrow:** Deploy all 3 sites to Render
3. **Week 1:** Monitor logs and verify functionality
4. **Week 2+:** Routine maintenance and monitoring

---

**Deployment Status:** ✅ READY TO DEPLOY

All files prepared. Follow the steps above to get your 3 new professional mock financial websites live!

**Questions?** Check the detailed guides or documentation files listed above.

Good luck! 🚀
