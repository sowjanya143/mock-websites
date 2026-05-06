# Deployment Checklist for 23 Mock Websites

## Pre-Deployment Validation

### 1. Code Quality
- [ ] All 23 sites tested locally (Bastion, Landmark, + 6 existing sites + 15 others)
- [ ] No uncommitted changes: `git status`
- [ ] All tests passing: `pytest tests/`
- [ ] Linting passes: `flake8 . pylint .`
- [ ] No security issues: `bandit -r . -ll`
- [ ] Dependencies updated: `pip list --outdated`

### 2. Configuration
- [ ] `.env.production` created with all 23 sites' SECRET_KEYs
- [ ] SSL certificates generated: `bash scripts/generate-ssl-certs.sh`
- [ ] nginx.conf configured for all 23 sites
- [ ] docker-compose.yml includes all services
- [ ] Health checks configured (30s interval)
- [ ] Logging configured (centralized, rotated)

### 3. Security Verification
- [ ] No secrets in code or commits
- [ ] `.gitignore` includes `.env.production`, `ssl/`, `backups/`
- [ ] All databases configured with strong passwords
- [ ] Rate limiting enabled:
  - Bastion: 10 req/60s ✓
  - Landmark: 4 req/60s ✓
- [ ] CORS properly configured (not * unless dev)
- [ ] HTTPS only (redirect HTTP → HTTPS)
- [ ] Security headers configured (HSTS, X-Frame-Options, etc.)

### 4. Anti-Scraping Validation
- **Bastion:**
  - [ ] DOM obfuscation active: Random class maps per session
  - [ ] Timed CAPTCHA working: 30-second expiration
  - [ ] Portfolio showcase on: home, what-we-do, who-we-are, team, investors, financial-advisors, media, careers

- **Landmark:**
  - [ ] Canvas fingerprint challenge active on all pages
  - [ ] Session token rotation working (5-page limit)
  - [ ] Rotating tokens issue: /refresh-token endpoint
  - [ ] Headless browser detection active

### 5. Data Integrity
- [ ] All JSON data files present (aum.json, team.json, news.json)
- [ ] Data files validated for correct JSON format
- [ ] No sensitive data in JSON files
- [ ] Static assets (CSS, images) properly linked

### 6. Template Verification
- **Bastion (11 templates):**
  - [ ] base.html (gold header, footer)
  - [ ] home.html (hero, stat cards, portfolio)
  - [ ] what_we_do.html (alternating sections)
  - [ ] who_we_are.html (stat cards, values)
  - [ ] team.html (3-column grid, pagination)
  - [ ] investors.html (3 portals)
  - [ ] financial_advisors.html (knowledge center)
  - [ ] media.html (news grid)
  - [ ] careers.html (benefits, positions)
  - [ ] contact.html (form, offices)
  - [ ] 6 Strategy detail pages (corporate_credit, asset_based_finance, etc.)

- **Landmark (12 templates):**
  - [ ] base.html (navy header, fixed)
  - [ ] home.html (hero, 5 stat cards)
  - [ ] landmark_difference.html (6 differentiators)
  - [ ] investment_strategies.html (funds table)
  - [ ] 3 Strategy detail pages
  - [ ] about.html (60-year timeline)
  - [ ] team.html (3-column grid)
  - [ ] sustainability.html (ESG grid)
  - [ ] news.html (article grid)
  - [ ] careers.html (benefits, positions)
  - [ ] contact.html (form, offices)

### 7. Database & Redis (if applicable)
- [ ] Database migrations run: `python -m migrate`
- [ ] Database indexed for performance
- [ ] Redis connection configured
- [ ] Redis persistence enabled (AOF or RDB)
- [ ] Database backups automated

## Deployment Steps

### Phase 1: Pre-Deployment (Dev Environment)
```bash
[ ] 1. Clone repository
      git clone <repo>
      cd mock-website

[ ] 2. Setup environment
      python -m venv venv
      source venv/bin/activate  # or venv\Scripts\activate on Windows
      pip install -r requirements.txt

[ ] 3. Generate secrets
      python scripts/generate_secrets.py

[ ] 4. Generate SSL certificates
      bash scripts/generate-ssl-certs.sh

[ ] 5. Test locally (all sites)
      docker-compose up -d
      bash scripts/health-check.sh

[ ] 6. Verify anti-scraping active
      # Test CAPTCHA on Bastion
      curl http://localhost:5009/what-we-do
      
      # Test fingerprint on Landmark
      curl http://localhost:5010/

[ ] 7. Run tests
      pytest tests/ -v
      pytest --cov=. tests/
```

### Phase 2: Staging Deployment
```bash
[ ] 1. Deploy to staging environment
      docker-compose -f docker-compose.yml -f docker-compose.staging.yml up -d

[ ] 2. Verify all 23 sites running
      docker-compose ps
      
[ ] 3. Check logs for errors
      docker-compose logs -f
      
[ ] 4. Run health checks
      bash scripts/health-check.sh
      
[ ] 5. Test user flows
      # Test on each site: homepage → page → page
      # Verify rate limiting
      # Verify anti-scraping
      
[ ] 6. Verify monitoring/alerting
      # Check Sentry, New Relic, Datadog

[ ] 7. Test backup/restore
      bash scripts/backup.sh
      # Verify backup file created
```

### Phase 3: Production Deployment
```bash
[ ] 1. Final production checks
      # All code committed
      # All tests passing
      # All staging tests passed
      # All security checks passed

[ ] 2. Create production backup
      ssh prod-server
      bash /app/scripts/backup.sh

[ ] 3. Pull latest code
      git pull origin main

[ ] 4. Update dependencies (if needed)
      pip install -r requirements.txt

[ ] 5. Rebuild Docker images
      docker-compose build

[ ] 6. Deploy with zero downtime
      # Update one service at a time
      docker-compose up -d bastion
      docker-compose up -d landmark
      # ... repeat for all sites

[ ] 7. Verify production sites
      # Visit each site's homepage
      # Check status codes
      
[ ] 8. Run production health checks
      bash scripts/health-check.sh
      
[ ] 9. Monitor logs
      docker-compose logs -f
      
[ ] 10. Verify monitoring alerts
       # Ensure monitoring active
       # Check for any anomalies
```

## Post-Deployment Verification

### Functionality Tests
- [ ] **Bastion**: 
  - [ ] Homepage loads with portfolio showcase
  - [ ] CAPTCHA appears on /what-we-do after 3 page visits
  - [ ] Rate limiting blocks at >10 req/60s
  - [ ] Team pagination works (5 per page)

- [ ] **Landmark**:
  - [ ] Homepage loads with navy header (fixed)
  - [ ] Fingerprint challenge blocks headless browsers
  - [ ] Token rotation works (expires after 5 pages)
  - [ ] News grid displays correctly
  - [ ] ESG sustainability grid visible on /about/sustainability

### Performance Metrics
- [ ] Homepage load time < 2 seconds (all sites)
- [ ] Static assets cached (CSS, JS, images)
- [ ] Database queries optimized (< 100ms)
- [ ] Memory usage within limits
- [ ] CPU usage normal (< 70%)

### Security Verification
- [ ] SSL certificate valid (all sites)
- [ ] HTTP → HTTPS redirect working
- [ ] Security headers present:
  - [ ] Strict-Transport-Security
  - [ ] X-Content-Type-Options
  - [ ] X-Frame-Options
  - [ ] Content-Security-Policy
- [ ] CORS headers correct
- [ ] Rate limiting blocking abuse (test with Apache Bench)
- [ ] Anti-scraping active (DOM obfuscation, CAPTCHA, fingerprint)

### Monitoring & Logging
- [ ] Application logs flowing to central store
- [ ] Error tracking (Sentry) receiving events
- [ ] Performance monitoring (New Relic) active
- [ ] Infrastructure monitoring (Datadog) collecting metrics
- [ ] Alerts configured and triggering on threshold breach
- [ ] Backup running on schedule (daily)

## Rollback Plan

If deployment fails:

```bash
# 1. Identify failed service
   docker-compose ps | grep -v "Up"

# 2. Check recent changes
   git log --oneline -5

# 3. Rollback to previous version
   git checkout <previous-commit>
   docker-compose build
   docker-compose up -d

# 4. Verify rollback successful
   bash scripts/health-check.sh

# 5. Investigate root cause
   docker-compose logs <service-name>
   
# 6. Fix issue and redeploy
```

## Maintenance Schedule

### Daily
- [ ] Check monitoring dashboards
- [ ] Review error logs (Sentry)
- [ ] Verify backups completed

### Weekly
- [ ] Review performance metrics
- [ ] Check security alerts
- [ ] Update base images

### Monthly
- [ ] Dependency security updates
- [ ] Certificate renewal (if needed)
- [ ] Database optimization
- [ ] Disaster recovery drill

### Quarterly
- [ ] Full security audit
- [ ] Penetration testing
- [ ] Performance optimization
- [ ] Documentation update

## Emergency Contacts

- **On-Call**: [Your team details]
- **Incident Channel**: [Slack/Teams channel]
- **Status Page**: [Your status page URL]
- **Escalation**: [Manager details]

## Sign-Off

- [ ] QA Team Approval: _______________  Date: ____
- [ ] Security Team Approval: _______________  Date: ____
- [ ] DevOps/Infrastructure: _______________  Date: ____
- [ ] Product Owner: _______________  Date: ____
- [ ] Deployment Lead: _______________  Date: ____

---

**Deployment Date**: ________________  
**Deployed By**: ________________  
**Version**: ________________  
**Notes**: ________________________________________________

---

## Quick Reference

### Useful Commands
```bash
# View all running services
docker-compose ps

# View logs for specific site
docker-compose logs -f bastion

# Restart specific service
docker-compose restart landmark

# Stop all services
docker-compose down

# Health check
bash scripts/health-check.sh

# Backup
bash scripts/backup.sh

# Generate secrets
python scripts/generate_secrets.py

# Test rate limiting
ab -n 20 -c 1 http://localhost:5009/
```

### Key Ports
- Bastion: 5009 (Fortress replica, DOM + CAPTCHA)
- Landmark: 5010 (Heitman replica, fingerprint + tokens)
- Apex: 5000
- Sentinel: 5001
- Cipher: 5002
- Fortis: 5003
- Others: 5004-5008

### Key Features
- 23 total mock websites
- Anti-scraping on Bastion & Landmark
- Rate limiting per site
- Health checks every 30 seconds
- Centralized logging
- Automated backups
- SSL/TLS termination via Nginx

---

**Deployment Configuration Version**: 1.0  
**Last Updated**: 2026-05-06
