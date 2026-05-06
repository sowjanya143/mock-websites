# Mock Websites Suite - Deployment Guide

## Overview

This repository contains 23 mock financial websites built with Flask, organized into a unified deployment system. All sites share common utilities and anti-scraping measures while maintaining distinctive designs.

## 23 Mock Websites

### New Sites (2026)
1. **Bastion Investment Group** (Port 5009) - Fortress.com replica
   - Dark/Gold theme (#1a1a1a + #c8a96e)
   - DOM obfuscation + Timed CAPTCHA
   - Rate limiting: 10 req/60s
   - Portfolio showcase on all pages
   - [Layout: 11 pages with alternating sections, hero images]

2. **Landmark Property Advisors** (Port 5010) - Heitman.com replica
   - Navy/Green theme (#001f3f + #4a7c6b)
   - Rotating tokens + Canvas fingerprint blocking
   - Rate limiting: 4 req/60s (strictest)
   - Fixed header on all pages
   - [Layout: 12 pages with timeline, ESG grid, minimal design]

### Existing Sites (Ports 5000-5008)
3. Apex (5000)
4. Sentinel (5001)
5. Cipher (5002)
6. Fortis (5003)
7-23. [17 additional sites on ports 5004-5008 and beyond]

---

## Prerequisites

- Docker & Docker Compose (v3.8+)
- Python 3.11+ (for local development)
- Git
- OpenSSL (for SSL certificate generation)
- 4GB RAM minimum (8GB recommended for all 23 sites)
- 10GB disk space

---

## Quick Start

### 1. Clone Repository
```bash
git clone <repository-url>
cd mock-website
```

### 2. Setup Environment
```bash
# Copy environment template
cp .env.production.example .env.production

# Generate production secret keys
python scripts/generate_secrets.py

# Edit .env.production with your settings
nano .env.production
```

### 3. Generate SSL Certificates
```bash
bash scripts/generate-ssl-certs.sh
```

### 4. Build and Deploy with Docker
```bash
# Build Docker images
docker-compose build

# Start all 23 sites
docker-compose up -d

# Verify all services are running
docker-compose ps

# Check logs
docker-compose logs -f
```

### 5. Access Sites
- **Bastion**: https://bastion.local or http://localhost:5009
- **Landmark**: https://landmark.local or http://localhost:5010
- **Others**: http://localhost:5000-5008

---

## Architecture

### Directory Structure
```
mock-website/
├── bastion/                 # New 2026 site
│   ├── app.py              # Flask application
│   ├── config.py           # Configuration
│   ├── data/               # JSON data files
│   ├── static/css          # Stylesheets
│   └── templates/          # 11 HTML templates
├── landmark/               # New 2026 site
│   ├── app.py
│   ├── config.py
│   ├── data/
│   ├── static/css
│   └── templates/          # 12 HTML templates
├── apex/                   # Existing site
├── sentinel/               # Existing site
├── cipher/                 # Existing site
├── fortis/                 # Existing site
├── utils/                  # Shared utilities
│   ├── dom_obfuscator.py   # DOM class obfuscation
│   ├── timed_captcha.py    # Time-limited CAPTCHA
│   ├── session_token.py    # Rotating tokens
│   ├── fingerprint.py      # Canvas fingerprinting
│   └── __init__.py
├── shared/                 # Shared templates/static
├── nginx.conf              # Nginx reverse proxy
├── docker-compose.yml      # Docker composition
├── Dockerfile              # Container definition
├── requirements.txt        # Python dependencies
└── scripts/                # Deployment scripts
    ├── generate-ssl-certs.sh
    ├── generate_secrets.py
    ├── health-check.sh
    └── backup.sh
```

### Utilities Architecture

**Shared Anti-Scraping Utilities:**
```python
# dom_obfuscator.py - Random CSS class name mapping per session
generate_class_map(session) -> {'aum-value': 'x7k2p', ...}

# timed_captcha.py - Time-limited CAPTCHA challenges
generate_timed_captcha(session) -> image_base64
validate_timed_captcha(answer, session, time_limit=30) -> 'ok'|'expired'|'invalid'

# session_token.py - Rotating tokens (5-page limit)
issue_token(session, page_limit=5) -> token_uuid
validate_token(session, page_limit=5) -> True|False

# fingerprint.py - Canvas fingerprint blocking
inject_fingerprint_routes(app) -> /verify-fingerprint endpoint
require_fingerprint(f) -> decorator
```

### Network Architecture
```
┌─────────────────────────────────────┐
│         Client Browser              │
└────────────────┬────────────────────┘
                 │ HTTPS (443)
                 ▼
┌─────────────────────────────────────┐
│      NGINX Reverse Proxy            │
│   (Rate Limiting, SSL/TLS, Cache)   │
└────┬────────┬────────┬───────┬──────┘
     │        │        │       │
   HTTP/    HTTP/    HTTP/    HTTP/
   5009     5010     5000    5001-5008
     │        │        │       │
     ▼        ▼        ▼       ▼
┌──────┐ ┌──────┐ ┌─────┐ ┌──────────┐
│Bastion│ │Landmark│ │Apex│ │Sentinel..│
│5009   │ │5010   │ │5000│ │5001-5008 │
└──────┘ └──────┘ └─────┘ └──────────┘
   │        │        │       │
   └────────┴────────┴───────┘
            │
      ┌─────▼─────┐
      │  Shared   │
      │  Utils    │
      └───────────┘
```

---

## Configuration Files

### docker-compose.yml
Orchestrates all 23 sites as separate services with:
- Individual ports (5000-5010+)
- Volume mounts for code and data
- Health checks every 30 seconds
- Environment variable injection
- Network isolation

### nginx.conf
Reverse proxy with:
- SSL/TLS termination
- Rate limiting (per-site)
- Request logging
- Static asset caching
- Upstream load balancing

### .env.production
Production secrets and configuration:
- SECRET_KEY for each site
- Database and Redis URLs
- Logging levels
- Anti-scraping settings
- Rate limit thresholds
- Monitoring/observability keys

---

## Deployment Scenarios

### Scenario 1: Local Development (All 23 Sites)
```bash
# Start with docker-compose
docker-compose up -d

# Logs from all sites
docker-compose logs -f

# Stop all sites
docker-compose down
```

### Scenario 2: Production Deployment (Cloud)

#### AWS EC2
```bash
# SSH into EC2 instance
ssh -i key.pem ec2-user@instance-ip

# Clone repo
git clone <repo> && cd mock-website

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh && sh get-docker.sh

# Setup environment
cp .env.production.example .env.production
# Edit with production secrets

# Generate SSL (or use ACM)
bash scripts/generate-ssl-certs.sh

# Deploy
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d

# Verify
docker-compose ps
```

#### Kubernetes
```bash
# Build and push images
docker build -t myregistry/mock-websites:latest .
docker push myregistry/mock-websites:latest

# Deploy with Helm
helm install mock-websites ./helm \
  --set image.repository=myregistry/mock-websites \
  --set image.tag=latest \
  --values values-prod.yaml

# Verify
kubectl get pods -n mock-websites
```

#### Docker Swarm
```bash
# Initialize swarm
docker swarm init

# Deploy stack
docker stack deploy -c docker-compose.yml mock-websites

# Check services
docker service ls
docker service ps mock-websites_bastion
```

### Scenario 3: Selective Deployment (Subset of Sites)

```bash
# Deploy only Bastion and Landmark
docker-compose up -d bastion landmark

# Deploy only legacy sites (5000-5008)
docker-compose up -d apex sentinel cipher fortis
```

---

## Monitoring & Health Checks

### Built-in Health Checks
Each service has health checks that run every 30s:
```bash
# View health status
docker-compose ps

# Check specific service
docker inspect <container-id> | jq '.[0].State.Health'
```

### Logging
```bash
# View logs for all sites
docker-compose logs

# View logs for specific site
docker-compose logs bastion
docker-compose logs landmark

# Real-time logs
docker-compose logs -f bastion

# Last 100 lines
docker-compose logs --tail=100 landmark
```

### Monitoring Integration
Configure in .env.production:
- **Sentry** (Error tracking): SENTRY_DSN
- **New Relic** (Performance): NEW_RELIC_LICENSE_KEY
- **Datadog** (Infrastructure): DATADOG_API_KEY

---

## Anti-Scraping Measures

### Bastion (DOM Obfuscation + Timed CAPTCHA)
```
1. User requests page
2. Server generates random CSS class map: {'aum-value': 'x7k2p'}
3. HTML rendered with obfuscated classes
4. CAPTCHA challenge on /what-we-do, /investors, /financial-advisors
5. CAPTCHA expires after 30 seconds
6. Rate limit: 10 requests/60 seconds
```

### Landmark (Rotating Tokens + Fingerprint Blocking)
```
1. User loads page
2. Canvas fingerprint challenge
3. Headless browser hashes blocked (known signatures)
4. Session token issued (valid for 5 pages)
5. Token expires when page limit reached
6. New token required to continue
7. Rate limit: 4 requests/60 seconds (strictest)
```

---

## Backup & Recovery

### Backup
```bash
# Backup all site data
bash scripts/backup.sh

# Creates timestamped backup
# artifacts/mock-websites-backup-2026-05-06.tar.gz

# Backup specific site
docker cp bastion_container:/app/bastion/data ./backups/
```

### Recovery
```bash
# Restore from backup
tar -xzf artifacts/mock-websites-backup-2026-05-06.tar.gz

# Restart services
docker-compose restart bastion landmark
```

---

## Scaling

### Horizontal Scaling (Multiple Nodes)
```yaml
# docker-compose.prod.yml
version: '3.8'
services:
  bastion:
    deploy:
      replicas: 3  # 3 replicas of Bastion
      placement:
        constraints: [node.role == worker]
  
  landmark:
    deploy:
      replicas: 2  # 2 replicas of Landmark
```

### Vertical Scaling (More Resources)
```yaml
services:
  bastion:
    environment:
      - WORKERS=8          # Increase worker processes
      - WORKER_CLASS=gevent  # Use async workers
```

---

## Security Checklist

- [ ] Generate production SECRET_KEYs (not default values)
- [ ] Enable SSL/TLS certificates (not self-signed)
- [ ] Configure firewall rules (only allow 80, 443, 22)
- [ ] Rotate secrets regularly (every 90 days)
- [ ] Enable HTTP security headers
- [ ] Configure CORS properly (not *)
- [ ] Setup monitoring/alerting
- [ ] Regular backups (daily)
- [ ] Rate limiting enabled
- [ ] Anti-scraping active
- [ ] Logs centralized (ELK, Splunk, etc.)
- [ ] Vulnerability scanning (Snyk, Trivy)

---

## Troubleshooting

### Service Won't Start
```bash
# Check logs
docker-compose logs bastion

# Check health
docker-compose ps

# Restart service
docker-compose restart bastion

# Rebuild and restart
docker-compose build bastion
docker-compose up -d bastion
```

### Port Already in Use
```bash
# Find process using port
lsof -i :5009

# Kill process
kill -9 <PID>

# Or change port in docker-compose.yml
```

### Connection Issues
```bash
# Test connectivity
docker exec bastion curl -f http://localhost:5009/

# Check network
docker network inspect mock-websites

# View network logs
docker-compose logs nginx
```

---

## Maintenance

### Regular Tasks
- **Daily**: Monitor logs and alerts
- **Weekly**: Backup data
- **Monthly**: Security patches, dependency updates
- **Quarterly**: Certificate renewal, secret rotation

### Updates
```bash
# Update dependencies
pip install --upgrade -r requirements.txt

# Rebuild images
docker-compose build --no-cache

# Deploy updates (zero-downtime)
docker-compose up -d --no-deps bastion
```

---

## Support & Documentation

- **README**: Overview and quick start
- **SITE_BEHAVIORS.md**: Detailed security behaviors for each site
- **DEPLOYMENT.md**: This file (deployment guide)
- **CODE**: Inline comments and docstrings
- **Issues**: GitHub issue tracker

---

## License

All 23 mock websites are part of the mock-website suite. Refer to LICENSE file.

---

**Last Updated**: 2026-05-06  
**Total Sites**: 23  
**Total Ports**: 5000-5010+ (11 ports documented)
