# Mock Financial Services Websites — Design Spec
**Date:** 2026-05-04  
**Project:** 5 Independent Mock Financial Services Websites for Web Scraping Testing

---

## Purpose

Create 5 independent Flask-based mock financial services websites, each patterned after a real company (Fortress, Heitman, Nomura, Hokuyo Bank, Oaktree Capital), with intentional behavioral variations to test web scraping solutions. Sites feature pagination, multi-level AUM data discovery, CAPTCHAs, pop-ups, dynamic data, and rate limiting—each site with different trigger strategies to evaluate scraper robustness.

---

## Requirements

### Functional Requirements

1. **5 Separate Flask Applications**
   - Each independently deployable to Render
   - Independent data and configuration per site
   - Shared utility code for CAPTCHA, pop-ups, data generation

2. **Page Structure (~10-15 pages per site)**
   - Homepage, About, Leadership (paginated), Strategies, Investor Resources, Funds/Products, News, Contact, Data Endpoints, Footer
   - AUM data visible on pages 1, 4, 5, 6, 9 in site-specific layouts

3. **Dynamic Data (JSON-based)**
   - `data/aum.json` — Global AUM, AUM by asset class, AUM by fund
   - `data/team.json` — Leadership team with pagination support
   - `data/news.json` — News/updates
   - Data regenerated at app startup with ±5% variance

4. **Pagination**
   - Leadership team page: 5-10 members per page
   - Next/prev navigation, page indicators

5. **AUM Data Discovery (Multi-level)**
   - Level 1: Homepage teaser (global AUM)
   - Level 2: Strategies/Investor pages (AUM by asset class)
   - Level 3: Individual fund pages (detailed AUM figures)
   - Data scattered across pages in different formats (tables, JSON endpoints, JavaScript)

6. **CAPTCHAs**
   - Medium complexity (not trivial, but solvable by test code)
   - Generated using `captcha` library or similar
   - Site-specific trigger strategies (see Site Behaviors)

7. **Pop-ups**
   - Block page navigation (modal dialogs)
   - Dismissible overlays, sticky footers, auto-dismiss (site-specific)
   - Site-specific timing and behavior

8. **Request Behavior Variations**
   - Rate limiting: Some sites apply per-minute request caps
   - Artificial delays: Some sites add latency to responses
   - Dynamic data updates: Values change between visits

### Non-Functional Requirements

- **Deployability:** Each site runnable as standalone Flask app on Render
- **Maintainability:** Shared utilities to reduce code duplication
- **Testability:** Predictable behavior per site for scraper testing
- **Documentation:** Clear README for each site and overall project

---

## Site-Specific Behaviors

| Aspect | Fortress | Heitman | Nomura | Hokuyo Bank | Oaktree Capital |
|--------|----------|---------|--------|-------------|-----------------|
| **CAPTCHA Trigger** | Every page | Data pages only | Random (30%) | Never | First visit + data pages |
| **Pop-up Behavior** | Blocks nav, 2s delay | Dismissible overlay, random timing | Modal after scroll | None | Sticky footer, auto-dismiss |
| **Rate Limiting** | None | 5 req/min | None | None | 3 req/min |
| **Artificial Delays** | None | None | 1s | None | 0.5s |
| **Data Layout** | Hidden in JS tables | Tables + JSON endpoint | Scattered pages | Clean tables | AJAX-loaded content |
| **Branding Pattern** | Fortress.com | Heitman | Nomura | Hokuyo Bank | Oaktree Capital |

---

## Directory Structure

```
mock-website/
├── utils/
│   ├── __init__.py
│   ├── captcha.py              # CAPTCHA generation & validation
│   ├── popups.py               # Pop-up rendering utilities
│   ├── data_generator.py       # Dynamic AUM/team data generation
│   └── rate_limit.py           # Rate limiting middleware
├── fortress/
│   ├── app.py                  # Main Flask app
│   ├── config.py               # Site config (name, colors, behaviors)
│   ├── routes.py               # Page routes
│   ├── data/
│   │   ├── aum.json
│   │   ├── team.json
│   │   └── news.json
│   ├── templates/
│   │   ├── base.html
│   │   ├── home.html
│   │   ├── about.html
│   │   ├── leadership.html
│   │   ├── strategies.html
│   │   ├── investor_resources.html
│   │   ├── funds.html
│   │   ├── news.html
│   │   ├── contact.html
│   │   └── fund_detail.html
│   ├── static/
│   │   ├── css/
│   │   ├── js/
│   │   └── images/
│   └── requirements.txt
├── heitman/
│   ├── app.py
│   ├── config.py
│   ├── routes.py
│   ├── data/
│   ├── templates/
│   ├── static/
│   └── requirements.txt
├── nomura/
├── hokuyo/
├── oaktree/
├── README.md                   # Project overview
└── DEPLOYMENT.md               # Render deployment instructions
```

---

## Data Model

### `aum.json` Structure
```json
{
  "global_aum": "$850,000,000,000",
  "by_asset_class": {
    "Real Estate": "$350,000,000,000",
    "Credit": "$250,000,000,000",
    "Infrastructure": "$150,000,000,000",
    "Natural Resources": "$100,000,000,000"
  },
  "by_fund": [
    {
      "name": "Fund A",
      "aum": "$200,000,000,000",
      "strategy": "Real Estate"
    },
    {
      "name": "Fund B",
      "aum": "$180,000,000,000",
      "strategy": "Credit"
    }
  ]
}
```

### `team.json` Structure
```json
[
  {
    "id": 1,
    "name": "John Doe",
    "title": "CEO",
    "bio": "20+ years in asset management"
  },
  {
    "id": 2,
    "name": "Jane Smith",
    "title": "CIO",
    "bio": "Former hedge fund manager"
  }
]
```

### `news.json` Structure
```json
[
  {
    "id": 1,
    "title": "Fund announces new strategy",
    "date": "2026-05-01",
    "content": "..."
  }
]
```

---

## Page Descriptions

### 1. **Homepage**
- Company tagline, mission statement
- Global AUM teaser (e.g., "$850B under management")
- Navigation to key sections
- Fortress/Heitman/Nomura-specific branding

### 2. **About**
- Company history, leadership message
- Overview of business lines

### 3. **Leadership**
- Paginated team list (5-10 per page)
- Names, titles, bios
- Next/prev navigation
- Individual leader pages (optional)

### 4. **Our Strategies** / **Strategies Overview**
- List of strategies/funds with AUM by strategy
- Links to detailed fund pages

### 5. **Investor Resources**
- AUM breakdown by asset class (table or charts)
- Performance data
- Reports/downloads

### 6. **Funds/Products**
- List of all funds with basic AUM
- Individual fund detail pages with more data

### 7. **News/Updates**
- Blog or news listing page
- Individual news detail pages

### 8. **Contact**
- Contact form (basic, no backend processing needed)

### 9. **Data Endpoints**
- Some sites expose `/api/aum` or `/api/team` endpoints
- Others bury data only in HTML

### 10. **Footer**
- Global AUM repeated, contact info
- Copyright, site links

---

## CAPTCHA & Pop-up Implementation

### CAPTCHA
- **Trigger:** Per-site rules (every page, data pages only, random, never)
- **Type:** Medium complexity (image + text solve, or math captcha)
- **Library:** `pillow` + `captcha` or similar
- **Validation:** Server-side session validation
- **Bypass:** Solvable by test code (not blocking like Google reCAPTCHA)

### Pop-ups
- **Trigger:** Per-site timing rules
- **Styling:** CSS overlays, modals
- **Dismissal:** Varies (button click, auto-dismiss, sticky)
- **Persistence:** Session-based (reappears on new visit or after timeout)

---

## Dynamic Data Strategy

- On app startup, `data_generator.py` loads JSON and applies ±5% random variance to numeric values (AUM figures)
- Each app restart produces slightly different values
- Scrapers visiting multiple times across deployments will see variance
- Team members and news can be randomized (shuffled order, subset selection)

---

## Deployment

- Each site deployed to **Render** as independent web service
- Environment variables for port and site name
- `requirements.txt` per site (shared utils imported as package)
- GitHub Actions or manual Render dashboard deployment

---

## Success Criteria

1. ✓ 5 independently deployable Flask apps
2. ✓ Pagination working on leadership pages
3. ✓ AUM data discoverable at 3 depth levels across multiple pages
4. ✓ CAPTCHAs appearing per site-specific triggers
5. ✓ Pop-ups blocking navigation and dismissible
6. ✓ Dynamic data with ±5% variance
7. ✓ Rate limiting applied where specified
8. ✓ Each site visually distinct and realistic
9. ✓ Deployable to Render without manual configuration beyond env vars

---

## Tech Stack

- **Framework:** Flask 3.0+
- **Templating:** Jinja2
- **Data:** JSON files (loaded at runtime)
- **CAPTCHA:** `pillow` + custom logic or `captcha` library
- **Rate Limiting:** Flask-Limiter (optional, custom middleware if needed)
- **Deployment:** Render (web service)
- **Language:** Python 3.10+

---

## Risks & Mitigations

| Risk | Mitigation |
|------|-----------|
| CAPTCHA library licensing | Use open-source libraries (PIL, custom) |
| Rate limiting causing test failures | Configurable per site, off by default except specified sites |
| Data variance too high | Cap at ±5%, document behavior |
| Deployment complexity | Template Render config, automate with GitHub Actions |

