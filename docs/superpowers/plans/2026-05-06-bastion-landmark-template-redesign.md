# Bastion & Landmark Template Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rebuild all 23 Bastion and Landmark HTML templates with distinctive, photography-driven layouts matching Fortress.com and Heitman.com reference sites.

**Architecture:** Rewrite all 23 templates with completely new HTML structures (not card-based grids). Bastion uses portfolio showcases on all pages, stat overlays, and alternating image-text layouts. Landmark maintains fixed navy header across all pages with minimal design and alternating content sections. Each template is self-contained with inline CSS and Unsplash image URLs. No component inheritance—each page's structure is unique to its purpose.

**Tech Stack:** Flask Jinja2 templates, Unsplash API (direct image URLs), CSS (Bastion gold/dark, Landmark green/navy), existing utils (DOM obfuscation, rate limiting, CAPTCHA, token rotation, fingerprint blocking).

---

## PHASE 1: Base Templates & Shared Components

### Task 1: Bastion base.html with Gold Header and Footer

**Files:**
- Modify: `bastion/templates/base.html`

- [ ] **Step 1: Replace base.html with new header/footer structure**

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}{{ company_name }}{% endblock %}</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            background: #fff;
            color: #333;
        }

        /* Header */
        header {
            background: #1a1a1a;
            padding: 20px 0;
            position: sticky;
            top: 0;
            z-index: 100;
            border-bottom: 3px solid #c8a96e;
        }

        header .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        header .logo {
            font-size: 20px;
            font-weight: bold;
            color: white;
            text-decoration: none;
        }

        header nav {
            display: flex;
            gap: 40px;
        }

        header nav a {
            color: white;
            text-decoration: none;
            font-size: 14px;
            text-transform: uppercase;
            letter-spacing: 1px;
            transition: color 0.3s;
        }

        header nav a:hover {
            color: #c8a96e;
        }

        /* Footer */
        footer {
            background: #1a1a1a;
            color: white;
            padding: 60px 0;
            margin-top: 80px;
        }

        footer .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
        }

        footer .footer-top {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 40px;
            margin-bottom: 40px;
            padding-bottom: 40px;
            border-bottom: 1px solid #333;
        }

        footer .footer-section h4 {
            font-size: 14px;
            color: #c8a96e;
            margin-bottom: 15px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        footer .footer-section ul {
            list-style: none;
        }

        footer .footer-section ul li {
            margin-bottom: 10px;
        }

        footer .footer-section ul li a {
            color: #ccc;
            text-decoration: none;
            font-size: 13px;
            transition: color 0.3s;
        }

        footer .footer-section ul li a:hover {
            color: #c8a96e;
        }

        /* Newsletter */
        footer .newsletter {
            margin-bottom: 40px;
        }

        footer .newsletter h4 {
            font-size: 14px;
            color: #c8a96e;
            margin-bottom: 15px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        footer .newsletter form {
            display: flex;
            gap: 10px;
        }

        footer .newsletter input {
            flex: 1;
            padding: 12px;
            border: none;
            background: #333;
            color: white;
        }

        footer .newsletter input::placeholder {
            color: #999;
        }

        footer .newsletter button {
            padding: 12px 24px;
            background: #c8a96e;
            border: none;
            color: white;
            cursor: pointer;
            font-weight: bold;
            transition: background 0.3s;
        }

        footer .newsletter button:hover {
            background: #b39860;
        }

        footer .footer-bottom {
            text-align: center;
            font-size: 12px;
            color: #999;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
        }

        @media (max-width: 768px) {
            header nav {
                gap: 20px;
                font-size: 12px;
            }

            footer .footer-top {
                grid-template-columns: 1fr;
            }

            footer .newsletter form {
                flex-direction: column;
            }
        }
    </style>
    {% block extra_css %}{% endblock %}
</head>
<body>
    <header>
        <div class="container">
            <a href="/" class="logo">{{ company_name }}</a>
            <nav>
                <a href="/what-we-do">What We Do</a>
                <a href="/who-we-are">Who We Are</a>
                <a href="/investors">Investors</a>
                <a href="/media">Media</a>
                <a href="/careers">Careers</a>
                <a href="/contact">Contact</a>
            </nav>
        </div>
    </header>

    {% block content %}{% endblock %}

    <footer>
        <div class="container">
            <div class="footer-top">
                <div class="footer-section">
                    <h4>Company</h4>
                    <ul>
                        <li><a href="/who-we-are">About Us</a></li>
                        <li><a href="/who-we-are/team">Team</a></li>
                        <li><a href="/careers">Careers</a></li>
                        <li><a href="/contact">Contact</a></li>
                    </ul>
                </div>
                <div class="footer-section">
                    <h4>Investments</h4>
                    <ul>
                        <li><a href="/what-we-do">Strategies</a></li>
                        <li><a href="/investors">For Investors</a></li>
                        <li><a href="/financial-advisors">For Advisors</a></li>
                        <li><a href="/media">News</a></li>
                    </ul>
                </div>
                <div class="footer-section newsletter">
                    <h4>Subscribe</h4>
                    <form method="POST" action="/subscribe">
                        <input type="email" placeholder="Your email" name="email" required>
                        <button type="submit">Subscribe</button>
                    </form>
                </div>
            </div>
            <div class="footer-bottom">
                <p>&copy; 2024 {{ company_name }}. All rights reserved. | <a href="/privacy" style="color: #999;">Privacy</a> | <a href="/disclaimer" style="color: #999;">Disclaimer</a></p>
            </div>
        </div>
    </footer>
</body>
</html>
```

- [ ] **Step 2: Test base.html renders without errors**

Run: `cd /c/Users/vboddeti/sandbox/mock-website && python -c "from bastion.app import app; app.test_client().get('/')"`
Expected: No template errors

- [ ] **Step 3: Commit**

```bash
git add bastion/templates/base.html
git commit -m "feat: rebuild Bastion base template with gold header and footer"
```

---

### Task 2: Landmark base.html with Navy Fixed Header

**Files:**
- Modify: `landmark/templates/base.html`

- [ ] **Step 1: Replace base.html with navy fixed header and footer**

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}{{ company_name }}{% endblock %}</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: Georgia, 'Times New Roman', serif;
            background: #fff;
            color: #333;
            padding-top: 120px;
        }

        /* Fixed Header */
        header {
            position: fixed;
            top: 0;
            width: 100%;
            background: #001f3f;
            color: white;
            z-index: 200;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        }

        header .top-bar {
            padding: 15px 0;
            text-align: center;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }

        header .top-bar .tagline {
            font-size: 11px;
            letter-spacing: 2px;
            text-transform: uppercase;
            color: #ccc;
        }

        header .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            height: 70px;
        }

        header .logo {
            font-size: 24px;
            font-weight: bold;
            color: white;
            text-decoration: none;
            letter-spacing: 3px;
        }

        header nav {
            display: flex;
            gap: 40px;
        }

        header nav a {
            color: white;
            text-decoration: none;
            font-size: 13px;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Arial, sans-serif;
            transition: color 0.3s;
        }

        header nav a:hover {
            color: #4a7c6b;
        }

        /* Footer */
        footer {
            background: #001f3f;
            color: white;
            padding: 60px 0;
        }

        footer .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
        }

        footer .footer-top {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 40px;
            margin-bottom: 40px;
            padding-bottom: 40px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }

        footer .footer-section h4 {
            font-size: 12px;
            color: #4a7c6b;
            margin-bottom: 15px;
            text-transform: uppercase;
            letter-spacing: 1px;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Arial, sans-serif;
        }

        footer .footer-section ul {
            list-style: none;
        }

        footer .footer-section ul li {
            margin-bottom: 10px;
        }

        footer .footer-section ul li a {
            color: #bbb;
            text-decoration: none;
            font-size: 12px;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Arial, sans-serif;
            transition: color 0.3s;
        }

        footer .footer-section ul li a:hover {
            color: #4a7c6b;
        }

        /* Newsletter */
        footer .newsletter {
            margin-bottom: 40px;
        }

        footer .newsletter h4 {
            font-size: 12px;
            color: #4a7c6b;
            margin-bottom: 15px;
            text-transform: uppercase;
            letter-spacing: 1px;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Arial, sans-serif;
        }

        footer .newsletter form {
            display: flex;
            gap: 10px;
        }

        footer .newsletter input {
            flex: 1;
            padding: 12px;
            border: none;
            background: rgba(255, 255, 255, 0.1);
            color: white;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Arial, sans-serif;
        }

        footer .newsletter input::placeholder {
            color: #999;
        }

        footer .newsletter button {
            padding: 12px 24px;
            background: #4a7c6b;
            border: none;
            color: white;
            cursor: pointer;
            font-weight: bold;
            transition: background 0.3s;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Arial, sans-serif;
        }

        footer .newsletter button:hover {
            background: #5a8d7b;
        }

        footer .footer-bottom {
            text-align: center;
            font-size: 11px;
            color: #999;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Arial, sans-serif;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
        }

        @media (max-width: 768px) {
            body {
                padding-top: 140px;
            }

            header nav {
                gap: 20px;
                font-size: 11px;
            }

            footer .footer-top {
                grid-template-columns: 1fr;
            }

            footer .newsletter form {
                flex-direction: column;
            }
        }
    </style>
    {% block extra_css %}{% endblock %}
</head>
<body>
    <header>
        <div class="top-bar">
            <div class="tagline">FIVE DECADES SERVING CLIENTS</div>
        </div>
        <div class="container">
            <a href="/" class="logo">LANDMARK</a>
            <nav>
                <a href="/landmark-difference">The Landmark Difference</a>
                <a href="/investment-strategies">Investment Strategies</a>
                <a href="/about">About</a>
                <a href="/careers">Careers</a>
                <a href="/contact">Contact</a>
            </nav>
        </div>
    </header>

    {% block content %}{% endblock %}

    <footer>
        <div class="container">
            <div class="footer-top">
                <div class="footer-section">
                    <h4>Company</h4>
                    <ul>
                        <li><a href="/about">About Us</a></li>
                        <li><a href="/about/team">Team</a></li>
                        <li><a href="/careers">Careers</a></li>
                        <li><a href="/contact">Contact</a></li>
                    </ul>
                </div>
                <div class="footer-section">
                    <h4>Investments</h4>
                    <ul>
                        <li><a href="/investment-strategies">Strategies</a></li>
                        <li><a href="/landmark-difference">Our Difference</a></li>
                        <li><a href="/about/sustainability">Sustainability</a></li>
                        <li><a href="/news">News</a></li>
                    </ul>
                </div>
                <div class="footer-section newsletter">
                    <h4>Subscribe</h4>
                    <form method="POST" action="/subscribe">
                        <input type="email" placeholder="Your email" name="email" required>
                        <button type="submit">Subscribe</button>
                    </form>
                </div>
            </div>
            <div class="footer-bottom">
                <p>&copy; 2024 {{ company_name }}. All rights reserved. | <a href="/privacy" style="color: #999;">Privacy</a> | <a href="/disclaimer" style="color: #999;">Disclaimer</a></p>
            </div>
        </div>
    </footer>
</body>
</html>
```

- [ ] **Step 2: Test base.html renders without errors**

Run: `cd /c/Users/vboddeti/sandbox/mock-website && python -c "from landmark.app import app; app.test_client().get('/')"`
Expected: No template errors

- [ ] **Step 3: Commit**

```bash
git add landmark/templates/base.html
git commit -m "feat: rebuild Landmark base template with navy fixed header"
```

---

### Task 3: Bastion home.html with Hero and Stat Cards

See full template code in detailed spec. Creates homepage with full-page hero, 3 clickable stat cards, 6 strategy cards (2-column), featured funds (2-column), 8 portfolio company logos, CTA section.

- [ ] **Step 1: Create home.html following template structure from spec**
- [ ] **Step 2: Test homepage renders (curl http://localhost:5009/)**
- [ ] **Step 3: Commit**

---

### Task 4: Bastion what_we_do.html with Alternating Sections

See full template code in detailed spec. Creates strategies overview with hero, alternating 2-column image-text sections for each strategy, portfolio showcase.

- [ ] **Step 1: Create what_we_do.html following template structure from spec**
- [ ] **Step 2: Test page renders (curl http://localhost:5009/what-we-do)**
- [ ] **Step 3: Commit**

---

## PHASE 2: Remaining Bastion Templates (Tasks 5-11)

### Task 5: Bastion Strategy Detail Pages (6 files: corporate_credit.html, asset_based_finance.html, real_estate.html, private_equity.html, insurance_solutions.html, multi_manager.html)

**Files:**
- Create: `bastion/templates/what_we_do/[strategy].html` (6 files total)

Each strategy detail page structure:
- Full-page hero with strategy-specific Unsplash image
- Large serif heading with strategy name
- Alternating 3-block content sections (text-left-image-right, image-left-text-right, text-left-image-right)
- Fund details section showing funds for this strategy
- Portfolio showcase section (8-12 company logos)
- Related strategies CTA at bottom
- Use same gold border/accent styling as home

- [ ] **Step 1: Create 6 strategy detail templates following spec layout**
- [ ] **Step 2: Test each renders without error (curl http://localhost:5009/what-we-do/[strategy-name])**
- [ ] **Step 3: Commit all 6 files**

```bash
git add bastion/templates/what_we_do/*.html
git commit -m "feat: add Bastion strategy detail pages with alternating content"
```

---

### Task 6: Bastion who_we_are.html

**Files:**
- Create: `bastion/templates/who_we_are.html`

Structure per spec:
- Full-page hero with office building Unsplash image
- 4 large stat cards (clickable): assets, companies, returns, people
- 2-column section: image-left, mission/vision text-right
- 4 full-width value cards (NOT grid)
- Impact statement section with background color block
- Portfolio showcase section
- Newsletter CTA

- [ ] **Step 1: Create who_we_are.html following spec**
- [ ] **Step 2: Test renders (curl http://localhost:5009/who-we-are)**
- [ ] **Step 3: Commit**

---

### Task 7: Bastion who_we_are/team.html

**Files:**
- Create: `bastion/templates/who_we_are/team.html`

Structure per spec:
- Full-page hero with team gathering image
- 3-column team grid with large professional headshots
- Each card: photo, name, title, bio, social links
- Pagination below (5 per page)
- "Join our team" CTA linking to careers
- Portfolio showcase section

- [ ] **Step 1: Create team.html following spec**
- [ ] **Step 2: Test renders and pagination**
- [ ] **Step 3: Commit**

---

### Task 8: Bastion investors.html

**Files:**
- Create: `bastion/templates/investors.html`

Structure per spec:
- Full-page hero with investor meeting imagery
- 3 distinct portal sections (Institutional, FA, Insurance): Large boxes with image-left, features-right layout
- Resource library: 4 downloadable items with icons (2-column)
- FAQ accordion section
- Portfolio showcase
- Contact CTA

- [ ] **Step 1: Create investors.html following spec**
- [ ] **Step 2: Test renders**
- [ ] **Step 3: Commit**

---

### Task 9: Bastion financial_advisors.html

**Files:**
- Create: `bastion/templates/financial_advisors.html`

Structure per spec:
- Full-page hero with advisory/planning imagery
- Knowledge center: 6 resources in 2-column with images
- Benefits: 4 boxes, 2x2 grid with icons
- Positioning statement with background color block
- Advisor success story: image-left, testimonial-right
- Portfolio showcase
- Contact form

- [ ] **Step 1: Create financial_advisors.html following spec**
- [ ] **Step 2: Test renders**
- [ ] **Step 3: Commit**

---

### Task 10: Bastion media.html and careers.html

**Files:**
- Create: `bastion/templates/media.html`
- Create: `bastion/templates/careers.html`

**media.html per spec:**
- Full-page hero with news/press imagery
- News articles: 2-column layout (image-top, headline/excerpt/date below, left gold border)
- Press resources section with icons
- Media contact box (gold background)
- Portfolio showcase

**careers.html per spec:**
- Full-page hero with team/culture imagery
- Career narrative: 2-3 paragraphs with alternating image-left/text-right pairings
- Benefits grid: 6 items, 2-column, with icons
- Open positions: Large cards, 1 per row, with details and apply button
- Application process: 4 steps horizontal
- Portfolio showcase

- [ ] **Step 1: Create media.html and careers.html following spec**
- [ ] **Step 2: Test both render (curl http://localhost:5009/media and /careers)**
- [ ] **Step 3: Commit both**

---

### Task 11: Bastion contact.html

**Files:**
- Create: `bastion/templates/contact.html`

Structure per spec:
- Full-page hero with minimal office/workspace imagery
- 2-column layout: contact form (left), contact info + regional offices (right)
- 4 office location cards: address, phone, map link
- Newsletter signup form in gold box
- No portfolio showcase (contact page only)

- [ ] **Step 1: Create contact.html following spec**
- [ ] **Step 2: Test renders (curl http://localhost:5009/contact)**
- [ ] **Step 3: Commit**

---

## PHASE 3: Landmark Templates (Tasks 12-23)

### Task 12: Landmark home.html with Navy Header and Stat Cards

**Files:**
- Create: `landmark/templates/home.html`

Structure per spec:
- Full-screen hero: Real estate/architecture photography background
- Centered white text overlay: "Investment focus: real estate"
- 5 large clickable stat cards below hero (each links to relevant page):
  - $47B AUM → /investment-strategies
  - 50+ Years → /about
  - Global Presence → /about
  - 3 Strategies → /investment-strategies
  - [Team/offices count] → /about/team
- 3-column strategy cards with images and metrics
- News grid: 3-4 items, 2-column, with images
- CTA section

- [ ] **Step 1: Create home.html following spec**
- [ ] **Step 2: Test renders (curl http://localhost:5010/)**
- [ ] **Step 3: Commit**

---

### Task 13: Landmark landmark_difference.html

**Files:**
- Create: `landmark/templates/landmark_difference.html`

Structure per spec:
- Hero: Architecture photo with "The Landmark Difference" text overlay
- 6 differentiators with alternating image-left/text-right and text-left/image-right layout
- Global presence: 5 office location cards with office building images
- Track record: Table or metrics display
- Core values: 5 values in 2-column layout (serif headings)

- [ ] **Step 1: Create landmark_difference.html following spec**
- [ ] **Step 2: Test renders**
- [ ] **Step 3: Commit**

---

### Task 14: Landmark investment_strategies.html

**Files:**
- Create: `landmark/templates/investment_strategies.html`

Structure per spec:
- Hero with real estate/urban development imagery
- 3 strategy cards (2-column + 1 below): image-top, name, metrics, description, learn-more link
- Funds table: Comparison of funds (scrollable on mobile)
- Fund characteristics matrix: Interactive comparison
- CTA: "Speak with an advisor"

- [ ] **Step 1: Create investment_strategies.html following spec**
- [ ] **Step 2: Test renders**
- [ ] **Step 3: Commit**

---

### Task 15: Landmark Strategy Detail Pages (3 files: private_equity_re.html, private_debt_re.html, public_equity_re.html)

**Files:**
- Create: `landmark/templates/investment_strategies/[strategy].html` (3 files total)

Each strategy detail page structure:
- Hero with strategy-specific real estate imagery
- Overview: 4 stat cards with key metrics
- Approach: Alternating image-text blocks (2-3 sections)
- Fund details: Funds in this strategy with performance data
- Investment characteristics: Grid or list
- Case study: Image-left, description-right (real estate project example)

- [ ] **Step 1: Create 3 strategy detail templates following spec**
- [ ] **Step 2: Test each renders without error**
- [ ] **Step 3: Commit all 3 files**

---

### Task 16: Landmark about.html

**Files:**
- Create: `landmark/templates/about.html`

Structure per spec:
- Hero with company headquarters/campus imagery
- 60-year timeline: Horizontal timeline with 8 key milestones (year, event, image)
- 4 office regions: Large cards with office photos, names, addresses
- 6 core values: 3x2 grid with icons and short descriptions
- Culture section: 2-3 paragraphs with integrated team/office photos

- [ ] **Step 1: Create about.html with timeline (use CSS for horizontal timeline)**
- [ ] **Step 2: Test renders**
- [ ] **Step 3: Commit**

---

### Task 17: Landmark about/team.html

**Files:**
- Create: `landmark/templates/about/team.html`

Structure per spec:
- Hero with team gathering image
- Team grid: 3 columns with large professional headshots (image-first)
- Each card: Photo, name, title, bio, social links
- Pagination below (5 per page)
- Culture section: 2 paragraphs with team/office photos
- "Join us" CTA to careers

- [ ] **Step 1: Create team.html following spec**
- [ ] **Step 2: Test renders and pagination**
- [ ] **Step 3: Commit**

---

### Task 18: Landmark about/sustainability.html

**Files:**
- Create: `landmark/templates/about/sustainability.html`

Structure per spec:
- Hero with environmental/green imagery
- 4 sustainability initiatives: Alternating image-left/text-right and text-left/image-right
  - Each: Heading, description, metrics, image
- ESG targets: 3-column grid (Environmental, Social, Governance) with metrics/icons
- Impact statement section with background color
- Commitment messaging

- [ ] **Step 1: Create sustainability.html following spec**
- [ ] **Step 2: Test renders**
- [ ] **Step 3: Commit**

---

### Task 19: Landmark news.html

**Files:**
- Create: `landmark/templates/news.html`

Structure per spec:
- Hero with media/press imagery
- News articles: 2-column layout (image-top, headline, date, category, excerpt)
- Filter buttons: By category (optional)
- Press contact section: Green background box with details
- Archive link (optional)

- [ ] **Step 1: Create news.html following spec**
- [ ] **Step 2: Test renders**
- [ ] **Step 3: Commit**

---

### Task 20: Landmark careers.html

**Files:**
- Create: `landmark/templates/careers.html`

Structure per spec:
- Hero with team/culture imagery
- Benefits grid: 6 benefits, 2-column, with icons
- Open positions: Large cards, 1 per row, full-width with details and apply button
- Application process: 4 steps shown horizontally
- Culture section: 2-3 paragraphs with integrated team/office photos

- [ ] **Step 1: Create careers.html following spec**
- [ ] **Step 2: Test renders**
- [ ] **Step 3: Commit**

---

### Task 21: Landmark contact.html

**Files:**
- Create: `landmark/templates/contact.html`

Structure per spec:
- Hero with office/workspace imagery
- 2-column: Contact form (left), Contact info (right)
- 4 regional office cards: Address, phone, office photo, map link
- Newsletter signup in green background box
- Hours of operation

- [ ] **Step 1: Create contact.html following spec**
- [ ] **Step 2: Test renders**
- [ ] **Step 3: Commit**

---

## PHASE 4: Verification and Testing (Task 22)

### Task 22: Port Verification and Visual Testing

**Files:**
- No files modified
- Test: Both ports serve without errors

- [ ] **Step 1: Start both Flask apps on correct ports**

Bastion: `python bastion/app.py` (port 5009)
Landmark: `python landmark/app.py` (port 5010)

- [ ] **Step 2: Test all Bastion pages load without errors**

Run: `curl -s http://localhost:5009/` and verify HTML renders with no errors

Test each page:
- http://localhost:5009/
- http://localhost:5009/what-we-do
- http://localhost:5009/what-we-do/corporate-credit (+ other strategies)
- http://localhost:5009/who-we-are
- http://localhost:5009/who-we-are/team
- http://localhost:5009/investors
- http://localhost:5009/financial-advisors
- http://localhost:5009/media
- http://localhost:5009/careers
- http://localhost:5009/contact

Expected: All pages return HTML with 200 status, no Jinja2 template errors

- [ ] **Step 3: Test all Landmark pages load without errors**

Test each page:
- http://localhost:5010/
- http://localhost:5010/landmark-difference
- http://localhost:5010/investment-strategies
- http://localhost:5010/investment-strategies/private-equity-re (+ other strategies)
- http://localhost:5010/about
- http://localhost:5010/about/team
- http://localhost:5010/about/sustainability
- http://localhost:5010/news
- http://localhost:5010/careers
- http://localhost:5010/contact

Expected: All pages return HTML with 200 status, no Jinja2 template errors

- [ ] **Step 4: Verify DOM obfuscation still active**

Test: Load Bastion home, inspect page source, verify `{{ aum_data }}` is rendered with actual data (not template syntax visible), and CSS class names are obfuscated (random 5-char strings)

- [ ] **Step 5: Verify rate limiting still active**

Test: Make 11 rapid requests to http://localhost:5009/ (exceeds 10 req/60s limit), verify 429 response on 11th request

- [ ] **Step 6: Verify anti-scraping still active**

Test Landmark: Navigate to http://localhost:5010/, should render fingerprint verification. Check session has fingerprint challenge.

- [ ] **Step 7: Commit**

```bash
git commit --allow-empty -m "test: verify all 23 templates render and anti-scraping measures active"
```

---

## Success Criteria

✅ All 23 templates deploy and render without errors on correct ports
✅ Each page has distinctive visual structure (not generic cards)
✅ Bastion pages clearly show portfolio showcase section on every page (except contact)
✅ Landmark pages maintain consistent navy fixed header across all pages
✅ Stat cards are clickable/interactive where specified in spec
✅ Images load from Unsplash without broken links
✅ Mobile responsive at 768px and 480px breakpoints
✅ DOM obfuscation still functions (random class names per session)
✅ Rate limiting still functions (10 req/60s Bastion, 4 req/60s Landmark)
✅ Anti-scraping measures active (CAPTCHA on Bastion, fingerprint on Landmark)
✅ Pagination works on team pages (5 items per page)
✅ Newsletter forms in footer accept email input
✅ All links navigate to correct pages
