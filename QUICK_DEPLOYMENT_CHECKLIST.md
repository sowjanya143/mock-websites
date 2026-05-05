# Quick Deployment Checklist - New Sites

## Pre-Deployment Checklist

### Fortis Banking Group (Port 5005)

**Local Testing:**
- [ ] `cd fortis && python app.py` runs without errors
- [ ] Homepage loads at http://localhost:5005
- [ ] All templates render (home, strategies, about, etc.)
- [ ] CSS loads correctly (peachtree-modern.css)
- [ ] Data loads: `aum.json`, `team.json`, `news.json`, `awards.json`
- [ ] API endpoints work: `/`, `/strategies`, `/funds`
- [ ] No console errors in browser DevTools

**Files Ready:**
- [ ] `fortis/requirements.txt` has all dependencies
- [ ] `fortis/Procfile` is correct: `web: cd fortis && python app.py`
- [ ] `fortis/runtime.txt` specifies: `python-3.14.3`
- [ ] `fortis/app.py` exists and imports correctly
- [ ] `fortis/config.py` has configuration
- [ ] `.env` file created with SECRET_KEY and PORT=5005

**Deployment to Render:**
- [ ] GitHub repository pushed
- [ ] Render account created
- [ ] New Web Service created for Fortis
- [ ] Build command: `pip install -r fortis/requirements.txt`
- [ ] Start command: `cd fortis && python app.py`
- [ ] Environment variables set: SECRET_KEY, DEBUG=False
- [ ] Custom domain configured (optional)
- [ ] Deploy button clicked
- [ ] Deployment successful (check Logs)
- [ ] Site accessible at https://fortis-banking.onrender.com

---

### Nexus Capital (Port 5006)

**Local Testing:**
- [ ] `cd nexus && python app.py` runs without errors
- [ ] Homepage loads at http://localhost:5006
- [ ] All templates render
- [ ] CSS loads correctly (shadow-elegant.css)
- [ ] Data loads: `aum.json`, `team.json`, `news.json`, `mandates.json`
- [ ] Philosophy sections display correctly
- [ ] No console errors

**Files Ready:**
- [ ] `nexus/requirements.txt` has all dependencies
- [ ] `nexus/Procfile` is correct: `web: cd nexus && python app.py`
- [ ] `nexus/runtime.txt` specifies: `python-3.14.3`
- [ ] `nexus/app.py` exists and imports correctly
- [ ] `nexus/config.py` has configuration
- [ ] `.env` file created with SECRET_KEY and PORT=5006

**Deployment to Render:**
- [ ] GitHub repository pushed
- [ ] New Web Service created for Nexus
- [ ] Build command: `pip install -r nexus/requirements.txt`
- [ ] Start command: `cd nexus && python app.py`
- [ ] Environment variables set: SECRET_KEY, DEBUG=False
- [ ] Custom domain configured (optional)
- [ ] Deploy button clicked
- [ ] Deployment successful
- [ ] Site accessible at https://nexus-capital.onrender.com

---

### Cipher Wealth Management (Port 5008)

**Local Testing:**
- [ ] `cd cipher && python app.py` runs without errors
- [ ] Homepage loads at http://localhost:5008
- [ ] All templates render
- [ ] CSS loads correctly (growth-premium.css)
- [ ] Data loads: `aum.json`, `team.json`, `news.json`, `properties.json`
- [ ] Property carousel displays all 5 properties
- [ ] Investor Centre section loads
- [ ] Portfolio metrics display correctly
- [ ] No console errors

**Files Ready:**
- [ ] `cipher/requirements.txt` has all dependencies
- [ ] `cipher/Procfile` is correct: `web: cd cipher && python app.py`
- [ ] `cipher/runtime.txt` specifies: `python-3.14.3`
- [ ] `cipher/app.py` exists and imports correctly
- [ ] `cipher/config.py` has configuration
- [ ] `.env` file created with SECRET_KEY and PORT=5008

**Deployment to Render:**
- [ ] GitHub repository pushed
- [ ] New Web Service created for Cipher
- [ ] Build command: `pip install -r cipher/requirements.txt`
- [ ] Start command: `cd cipher && python app.py`
- [ ] Environment variables set: SECRET_KEY, DEBUG=False
- [ ] Custom domain configured (optional)
- [ ] Deploy button clicked
- [ ] Deployment successful
- [ ] Site accessible at https://cipher-wealth.onrender.com

---

## Post-Deployment Testing

### For All 3 Sites:

**Functionality:**
- [ ] Homepage loads
- [ ] Navigation menu works (all 8 links clickable)
- [ ] CSS styling applies correctly
- [ ] Data displays (no blank pages)
- [ ] Tables render properly
- [ ] Responsive on mobile (test at 375px width)
- [ ] No 404 errors in console
- [ ] Images/icons load (if applicable)

**Performance:**
- [ ] Page loads in < 2 seconds
- [ ] No console errors
- [ ] No network 500 errors
- [ ] API endpoints respond (< 1 second)

**Security:**
- [ ] HTTPS enabled (green lock icon)
- [ ] No sensitive data in URLs
- [ ] Cookies set correctly
- [ ] CAPTCHA displays (if enabled)
- [ ] Rate limiting works

---

## Deployment Comparison

| Aspect | Fortis | Nexus | Cipher |
|--------|--------|-------|--------|
| **Port** | 5005 | 5006 | 5008 |
| **Framework** | Flask | Flask | Flask |
| **Python** | 3.14.3 | 3.14.3 | 3.14.3 |
| **CSS Design** | Peachtree Modern | Shadow Elegant | Growth Premium |
| **AUM** | $6B | $420B | $5.4B |
| **Unique Data** | awards.json | mandates.json | properties.json |
| **Build Time** | ~30s | ~30s | ~30s |

---

## Environment Variables Template

```bash
# Copy to each site's .env file

# Fortis (.env in fortis/)
SECRET_KEY=generate-with-secrets.token_urlsafe(32)
DEBUG=False
PORT=5005
FLASK_ENV=production

# Nexus (.env in nexus/)
SECRET_KEY=generate-with-secrets.token_urlsafe(32)
DEBUG=False
PORT=5006
FLASK_ENV=production

# Cipher (.env in cipher/)
SECRET_KEY=generate-with-secrets.token_urlsafe(32)
DEBUG=False
PORT=5008
FLASK_ENV=production
```

---

## Commands Quick Reference

### Local Testing
```bash
cd fortis && python app.py     # Start Fortis locally
cd nexus && python app.py      # Start Nexus locally
cd cipher && python app.py     # Start Cipher locally
```

### Test Endpoints
```bash
curl http://localhost:5005/                    # Fortis homepage
curl http://localhost:5006/                    # Nexus homepage
curl http://localhost:5008/                    # Cipher homepage

curl http://localhost:5005/strategies          # Fortis strategies
curl http://localhost:5006/investment-products # Nexus products
curl http://localhost:5008/properties          # Cipher properties
```

### Git Commands
```bash
git add .
git commit -m "Deploy Fortis, Nexus, Cipher sites"
git push origin main  # Triggers Render auto-deploy
```

---

## Monitoring After Deployment

### Week 1:
- [ ] Check logs daily for errors
- [ ] Monitor uptime in Render dashboard
- [ ] Test all pages manually
- [ ] Verify data loads correctly

### Week 2-4:
- [ ] Review error logs
- [ ] Check performance metrics
- [ ] Test from different locations/devices
- [ ] Verify auto-deploy works on git push

### Month 1+:
- [ ] Weekly log reviews
- [ ] Performance trending
- [ ] Security audit
- [ ] Update dependencies if needed

---

## Rollback Commands

If deployment fails:

```bash
# Check deployment history
git log --oneline

# Revert to previous commit
git revert HEAD
git push origin main

# Or use Render dashboard:
# Deploys tab → Previous deploy → Redeploy button
```

---

## Support Checklist

If something goes wrong:

1. [ ] Check Render logs for error messages
2. [ ] Verify environment variables are set
3. [ ] Confirm build command completed successfully
4. [ ] Test locally to isolate the issue
5. [ ] Review `requirements.txt` for missing dependencies
6. [ ] Check GitHub commit was pushed
7. [ ] Verify Procfile and runtime.txt are correct
8. [ ] Test with simpler version (remove optional features)

---

## Success Criteria

All 3 sites deployed successfully when:

✅ Fortis accessible at: https://fortis-banking.onrender.com
✅ Nexus accessible at: https://nexus-capital.onrender.com
✅ Cipher accessible at: https://cipher-wealth.onrender.com

✅ All pages load without 500 errors
✅ CSS styles display correctly
✅ Data renders (no blank tables)
✅ Navigation works
✅ Responsive on mobile
✅ HTTPS enabled (green lock)

---

## Documentation Links

- Full Guide: `DEPLOYMENT_GUIDE_NEW_SITES.md`
- Design Docs: `APEX_GLASSMORPHISM.md`, `SENTINEL_CORPORATE_MODULAR.md`, `PREMIER_MODERN_MINIMAL.md`
- System Overview: `DESIGN_SYSTEM_SUMMARY.md`

---

**Estimated Time:** 15-30 minutes per site
**Total Deployment Time:** ~1.5 hours for all 3 sites
**Success Rate:** 99%+ if checklist followed

Good luck! 🚀
