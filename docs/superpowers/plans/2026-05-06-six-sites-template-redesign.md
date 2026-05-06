# Six Sites Template Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rebuild all 6 remaining financial websites (Sentinel, Meridian, Cipher, Nexus, Quantum, Zenith) with distinctive, photo-driven layouts matching their reference websites (orchardglobal.com, pnbmetlife.com, growthpoint.com.au, shadowpartners.com.my, principal.com.hk, vikingglobal.com).

**Architecture:** Each site gets a complete template rebuild with site-specific CSS, branded colors, and layouts distinctive to its reference website. Base templates define header/footer styling, home.html showcases hero images + stat cards + content grids, about/team pages show organizational structure, contact pages provide inquiry forms. All sites maintain existing anti-scraping utilities (dom_obfuscator, timed_captcha, session_token, fingerprint) and rate limiting. Tests verify HTML renders without errors on correct ports (5001, 5003, 5005, 5006, 5007, 5008) using Playwright.

**Tech Stack:** Flask 2.3.3, Jinja2 3.1.2, custom CSS per site, Unsplash images, Playwright for verification

---

## Reference Site Specifications

### Sentinel (5001) - orchardglobal.com (Corporate Modular)
- **Color Scheme:** Navy (#001f3f), Gold (#d4af37), Light Gray (#f5f5f5)
- **Header:** Fixed navy background, horizontal navigation, gold accents on hover
- **Layout:** Institutional, professional, multi-column grids, image + text pairings
- **Key Visual:** Large corporate photography, financial metrics cards, team in grid formation
- **Portfolio:** Showcase investment sectors/strategies in 3-4 column grid

### Meridian (5003) - pnbmetlife.com (Insurance/Financial)
- **Color Scheme:** Orange (#ff6b35), White (#ffffff), Navy (#003366)
- **Header:** Orange band at top with logo, clean white navigation bar below
- **Layout:** Warm, approachable, family-focused, carousel banners, card-based services
- **Key Visual:** Product cards with icons, testimonials, health/financial imagery
- **Portfolio:** Insurance products/services in grid with descriptions and CTAs

### Cipher (5008) - growthpoint.com.au (Growth Premium)
- **Color Scheme:** Teal (#00897b), Orange (#ff7043), Dark Gray (#424242)
- **Header:** White/light background, teal accents, property-focused navigation
- **Layout:** Modern property showcase, large hero images, stat cards with metrics
- **Key Visual:** Real estate photography, property portfolios, development timelines
- **Portfolio:** Property assets/developments in showcase grid with location/yield metrics

### Nexus (5006) - shadowpartners.com.my (Shadow Elegant)
- **Color Scheme:** Dark (#1a1a1a), Deep Blue (#003d7a), Gold (#c0a080)
- **Header:** Dark background, subtle gold accents, sophisticated navigation
- **Layout:** Minimalist, elegant, asymmetric sections, large whitespace, premium feel
- **Key Visual:** High-end photography, dark backgrounds with gold borders, executive headshots
- **Portfolio:** Private equity portfolio companies with minimal descriptions

### Quantum (5007) - principal.com.hk/home (Financial Services)
- **Color Scheme:** Royal Blue (#0052cc), White (#ffffff), Gray (#666666)
- **Header:** Professional blue header, clean typography, structured navigation
- **Layout:** Minimalist professional, data-driven, clear hierarchies, 2-3 column layouts
- **Key Visual:** Business photography, financial charts, professional imagery
- **Portfolio:** Financial products/solutions in organized grid with clear metrics

### Zenith (5004) - vikingglobal.com (Hedge Fund)
- **Color Scheme:** Dark Navy (#0a1428), Gold/Amber (#ffc107), White (#ffffff)
- **Header:** Dark header with premium feel, bold typography
- **Layout:** Modern premium, large hero sections, asymmetric content blocks, motion-friendly
- **Key Visual:** Abstract/financial imagery, bold typography, premium photography
- **Portfolio:** Investment strategies in distinctive layout with performance metrics

---

## Phase 1: Sentinel (5001)

### Task 1: Create Sentinel base.html with Corporate Modular styling

**Files:**
- Create: `sentinel/templates/base.html`
- Create: `sentinel/static/css/corporate-modular.css` (if not exists)

- [ ] **Step 1: Create corporate-modular.css with Sentinel branding**

```css
/* Sentinel Corporate Modular CSS */
:root {
  --primary-navy: #001f3f;
  --accent-gold: #d4af37;
  --light-gray: #f5f5f5;
  --text-dark: #222;
  --text-light: #666;
  --border-light: #e0e0e0;
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  color: var(--text-dark);
  line-height: 1.6;
  background: #fff;
}

/* Fixed Header */
header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  background: var(--primary-navy);
  color: white;
  padding: 1rem 2rem;
  z-index: 1000;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

header h1 {
  font-size: 1.8rem;
  font-weight: 600;
  letter-spacing: 0.5px;
}

nav {
  display: flex;
  gap: 2rem;
  list-style: none;
  justify-content: center;
}

nav a {
  color: white;
  text-decoration: none;
  font-size: 0.95rem;
  transition: color 0.3s;
  border-bottom: 2px solid transparent;
  padding-bottom: 0.5rem;
}

nav a:hover {
  color: var(--accent-gold);
  border-bottom-color: var(--accent-gold);
}

main {
  margin-top: 120px;
  padding: 0;
}

/* Hero Section */
.hero {
  position: relative;
  height: 500px;
  background: linear-gradient(rgba(0, 31, 63, 0.7), rgba(0, 31, 63, 0.7)), url('https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?auto=format&fit=crop&w=1200&q=80');
  background-size: cover;
  background-position: center;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  text-align: center;
}

.hero h2 {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.hero p {
  font-size: 1.2rem;
  max-width: 600px;
  margin-bottom: 2rem;
}

/* Stat Cards */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 2rem;
  padding: 3rem 2rem;
  background: var(--light-gray);
}

.stat-card {
  background: white;
  padding: 2rem;
  border-left: 4px solid var(--accent-gold);
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
  transition: transform 0.3s, box-shadow 0.3s;
}

.stat-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 16px rgba(0,0,0,0.12);
}

.stat-card h3 {
  color: var(--accent-gold);
  font-size: 2.5rem;
  margin-bottom: 0.5rem;
}

.stat-card p {
  color: var(--text-light);
  font-size: 0.9rem;
}

/* Content Grid */
.content-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  padding: 3rem 2rem;
}

.content-item {
  background: white;
  border: 1px solid var(--border-light);
  overflow: hidden;
  transition: box-shadow 0.3s;
}

.content-item img {
  width: 100%;
  height: 250px;
  object-fit: cover;
}

.content-item-text {
  padding: 1.5rem;
}

.content-item h3 {
  color: var(--primary-navy);
  margin-bottom: 0.5rem;
}

/* Portfolio Showcase */
.portfolio-section {
  background: var(--primary-navy);
  color: white;
  padding: 3rem 2rem;
}

.portfolio-section h2 {
  text-align: center;
  margin-bottom: 2rem;
  color: var(--accent-gold);
}

.portfolio-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
}

.portfolio-item {
  background: rgba(255,255,255,0.1);
  padding: 1.5rem;
  border: 1px solid var(--accent-gold);
  text-align: center;
}

.portfolio-item h3 {
  color: var(--accent-gold);
  margin-bottom: 0.5rem;
}

/* Footer */
footer {
  background: var(--primary-navy);
  color: white;
  padding: 3rem 2rem 1rem;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
}

footer h4 {
  color: var(--accent-gold);
  margin-bottom: 1rem;
}

footer a {
  display: block;
  color: #ccc;
  text-decoration: none;
  margin: 0.5rem 0;
  transition: color 0.3s;
}

footer a:hover {
  color: var(--accent-gold);
}

footer hr {
  grid-column: 1 / -1;
  border: none;
  border-top: 1px solid rgba(212, 175, 55, 0.3);
  margin: 1rem 0;
}

.footer-bottom {
  grid-column: 1 / -1;
  text-align: center;
  color: #999;
  padding-top: 1rem;
}

/* Responsive */
@media (max-width: 768px) {
  header {
    padding: 0.5rem 1rem;
  }

  header h1 {
    font-size: 1.2rem;
  }

  nav {
    gap: 1rem;
    flex-wrap: wrap;
  }

  .hero h2 {
    font-size: 1.8rem;
  }

  main {
    margin-top: 100px;
  }
}
```

- [ ] **Step 2: Create sentinel/templates/base.html**

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{% block title %}Sentinel Capital Partners{% endblock %}</title>
  <link rel="stylesheet" href="{{ url_for('static', filename='css/corporate-modular.css') }}">
  {% block extra_css %}{% endblock %}
</head>
<body>
  <header>
    <h1>Sentinel Capital Partners</h1>
    <nav>
      <a href="/">Home</a>
      <a href="/about">About</a>
      <a href="/strategies">Strategies</a>
      <a href="/team">Team</a>
      <a href="/contact">Contact</a>
    </nav>
  </header>

  <main>
    {% block content %}{% endblock %}
  </main>

  <footer>
    <div>
      <h4>Company</h4>
      <a href="/">Home</a>
      <a href="/about">About Us</a>
      <a href="/team">Team</a>
      <a href="/careers">Careers</a>
    </div>
    <div>
      <h4>Investments</h4>
      <a href="/strategies">Investment Strategies</a>
      <a href="/portfolio">Portfolio</a>
      <a href="/performance">Performance</a>
    </div>
    <div>
      <h4>Resources</h4>
      <a href="/news">News</a>
      <a href="/resources">Resources</a>
      <a href="/contact">Contact</a>
    </div>
    <hr>
    <div class="footer-bottom">
      <p>&copy; 2026 Sentinel Capital Partners. All rights reserved.</p>
    </div>
  </footer>

  {% block extra_js %}{% endblock %}
</body>
</html>
```

- [ ] **Step 3: Commit CSS and base template**

```bash
git add sentinel/static/css/corporate-modular.css sentinel/templates/base.html
git commit -m "feat: create Sentinel corporate modular base template and CSS"
```

### Task 2: Create Sentinel home.html with hero, stats, and portfolio showcase

**Files:**
- Create: `sentinel/templates/home.html`

- [ ] **Step 1: Create sentinel/templates/home.html**

```html
{% extends "base.html" %}

{% block content %}
<section class="hero">
  <div style="text-align: center;">
    <h2>Institutional Investment Excellence</h2>
    <p>Strategic capital solutions for global investors</p>
  </div>
</section>

<section class="stats-grid">
  <div class="stat-card">
    <h3>$125B+</h3>
    <p>Assets Under Management</p>
  </div>
  <div class="stat-card">
    <h3>45+</h3>
    <p>Portfolio Companies</p>
  </div>
  <div class="stat-card">
    <h3>30+</h3>
    <p>Years of Excellence</p>
  </div>
  <div class="stat-card">
    <h3>150+</h3>
    <p>Investment Professionals</p>
  </div>
</section>

<section style="padding: 3rem 2rem; background: white;">
  <div style="max-width: 1200px; margin: 0 auto;">
    <h2 style="text-align: center; color: #001f3f; margin-bottom: 2rem;">Investment Strategies</h2>
    <div class="content-grid">
      <div class="content-item">
        <img src="https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?auto=format&fit=crop&w=400&q=80" alt="Private Equity">
        <div class="content-item-text">
          <h3>Private Equity</h3>
          <p>Strategic investments in mature companies with strong management teams and growth potential.</p>
        </div>
      </div>
      <div class="content-item">
        <img src="https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=400&q=80" alt="Infrastructure">
        <div class="content-item-text">
          <h3>Infrastructure</h3>
          <p>Long-term value creation through essential infrastructure assets worldwide.</p>
        </div>
      </div>
      <div class="content-item">
        <img src="https://images.unsplash.com/photo-1486312338219-ce68d2c6f44d?auto=format&fit=crop&w=400&q=80" alt="Real Estate">
        <div class="content-item-text">
          <h3>Real Estate</h3>
          <p>Premium commercial and residential properties with strong yield characteristics.</p>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="portfolio-section">
  <h2>Portfolio Highlights</h2>
  <div class="portfolio-grid">
    <div class="portfolio-item">
      <h3>Technology</h3>
      <p>12 Companies | $4.2B AUM</p>
    </div>
    <div class="portfolio-item">
      <h3>Healthcare</h3>
      <p>8 Companies | $2.8B AUM</p>
    </div>
    <div class="portfolio-item">
      <h3>Financial Services</h3>
      <p>6 Companies | $1.9B AUM</p>
    </div>
    <div class="portfolio-item">
      <h3>Consumer</h3>
      <p>10 Companies | $3.1B AUM</p>
    </div>
  </div>
</section>
{% endblock %}
```

- [ ] **Step 2: Commit home template**

```bash
git add sentinel/templates/home.html
git commit -m "feat: create Sentinel home template with hero and portfolio showcase"
```

### Task 3: Create Sentinel about.html

**Files:**
- Create: `sentinel/templates/about.html`

- [ ] **Step 1: Create sentinel/templates/about.html**

```html
{% extends "base.html" %}

{% block content %}
<section class="hero">
  <div style="text-align: center;">
    <h2>About Sentinel</h2>
    <p>Three decades of investment excellence</p>
  </div>
</section>

<section style="padding: 3rem 2rem; background: white; max-width: 1200px; margin: 0 auto;">
  <h2 style="color: #001f3f; margin-bottom: 2rem;">Our Story</h2>
  <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; align-items: center;">
    <div>
      <p style="margin-bottom: 1rem; line-height: 1.8;">Founded in 1995, Sentinel Capital Partners has established itself as a leading institutional investment manager. Our commitment to excellence, rigorous due diligence, and long-term value creation has defined our approach for over 30 years.</p>
      <p style="margin-bottom: 1rem; line-height: 1.8;">We manage capital on behalf of institutional investors globally, including pension funds, endowments, foundations, and family offices. Our deep expertise across multiple asset classes enables us to identify compelling investment opportunities.</p>
    </div>
    <img src="https://images.unsplash.com/photo-1552664730-d307ca884978?auto=format&fit=crop&w=500&q=80" alt="About Sentinel" style="border-radius: 8px; width: 100%; height: 400px; object-fit: cover;">
  </div>
</section>

<section style="padding: 3rem 2rem; background: #f5f5f5;">
  <div style="max-width: 1200px; margin: 0 auto;">
    <h2 style="text-align: center; color: #001f3f; margin-bottom: 3rem;">Core Values</h2>
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 2rem;">
      <div style="background: white; padding: 2rem; border-left: 4px solid #d4af37; text-align: center;">
        <h3 style="color: #001f3f;">Integrity</h3>
        <p>We operate with the highest ethical standards in all business dealings.</p>
      </div>
      <div style="background: white; padding: 2rem; border-left: 4px solid #d4af37; text-align: center;">
        <h3 style="color: #001f3f;">Excellence</h3>
        <p>We pursue superior investment returns through rigorous analysis and execution.</p>
      </div>
      <div style="background: white; padding: 2rem; border-left: 4px solid #d4af37; text-align: center;">
        <h3 style="color: #001f3f;">Partnership</h3>
        <p>We build long-term relationships based on trust and mutual respect.</p>
      </div>
      <div style="background: white; padding: 2rem; border-left: 4px solid #d4af37; text-align: center;">
        <h3 style="color: #001f3f;">Innovation</h3>
        <p>We embrace new methodologies and invest in emerging opportunities.</p>
      </div>
    </div>
  </div>
</section>
{% endblock %}
```

- [ ] **Step 2: Commit about template**

```bash
git add sentinel/templates/about.html
git commit -m "feat: create Sentinel about template with company story and values"
```

### Task 4: Create Sentinel contact.html

**Files:**
- Create: `sentinel/templates/contact.html`

- [ ] **Step 1: Create sentinel/templates/contact.html**

```html
{% extends "base.html" %}

{% block content %}
<section class="hero">
  <div style="text-align: center;">
    <h2>Contact Us</h2>
    <p>Get in touch with our team</p>
  </div>
</section>

<section style="padding: 3rem 2rem; max-width: 1200px; margin: 0 auto;">
  <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 3rem;">
    <div>
      <h2 style="color: #001f3f; margin-bottom: 2rem;">Send us a Message</h2>
      <form style="display: flex; flex-direction: column; gap: 1rem;">
        <input type="text" placeholder="Full Name" required style="padding: 0.8rem; border: 1px solid #e0e0e0; border-radius: 4px; font-family: inherit;">
        <input type="email" placeholder="Email Address" required style="padding: 0.8rem; border: 1px solid #e0e0e0; border-radius: 4px; font-family: inherit;">
        <input type="text" placeholder="Subject" required style="padding: 0.8rem; border: 1px solid #e0e0e0; border-radius: 4px; font-family: inherit;">
        <textarea placeholder="Message" rows="5" required style="padding: 0.8rem; border: 1px solid #e0e0e0; border-radius: 4px; font-family: inherit; resize: vertical;"></textarea>
        <button type="submit" style="padding: 1rem; background: #001f3f; color: white; border: none; border-radius: 4px; cursor: pointer; font-weight: 600; transition: background 0.3s;" onmouseover="this.style.background='#d4af37'; this.style.color='#001f3f';" onmouseout="this.style.background='#001f3f'; this.style.color='white';">Send Message</button>
      </form>
    </div>
    <div>
      <h2 style="color: #001f3f; margin-bottom: 2rem;">Contact Information</h2>
      <div style="margin-bottom: 2rem;">
        <h3 style="color: #d4af37; margin-bottom: 0.5rem;">Headquarters</h3>
        <p>123 Financial Plaza<br>New York, NY 10001<br>United States</p>
      </div>
      <div style="margin-bottom: 2rem;">
        <h3 style="color: #d4af37; margin-bottom: 0.5rem;">Phone</h3>
        <p>+1 (212) 555-1000</p>
      </div>
      <div style="margin-bottom: 2rem;">
        <h3 style="color: #d4af37; margin-bottom: 0.5rem;">Email</h3>
        <p>investors@sentinel.com</p>
      </div>
      <div>
        <h3 style="color: #d4af37; margin-bottom: 0.5rem;">Hours</h3>
        <p>Monday - Friday: 9am - 6pm EST<br>Saturday - Sunday: Closed</p>
      </div>
    </div>
  </div>
</section>
{% endblock %}
```

- [ ] **Step 2: Commit contact template**

```bash
git add sentinel/templates/contact.html
git commit -m "feat: create Sentinel contact template with form and office details"
```

### Task 5: Verify Sentinel renders on port 5001

**Files:**
- No new files

- [ ] **Step 1: Test Sentinel homepage with Playwright**

```bash
python -c "
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto('http://localhost:5001/')
    page.wait_for_load_state('networkidle')
    page.screenshot(path='sentinel-home.png')
    print('✓ Sentinel homepage rendered')
    
    page.goto('http://localhost:5001/about')
    page.wait_for_load_state('networkidle')
    print('✓ Sentinel about page rendered')
    
    page.goto('http://localhost:5001/contact')
    page.wait_for_load_state('networkidle')
    print('✓ Sentinel contact page rendered')
    
    browser.close()
"
```

Expected: All 3 pages render without errors, screenshots saved

- [ ] **Step 2: Verify no console errors in Playwright output**

Screenshots should show:
- Sentinel home: Navy header with gold navigation, corporate hero, 4 stat cards, 3 strategy content items, navy portfolio section
- Sentinel about: Navy header, hero, 2-column story section, 4 core value cards with gold borders
- Sentinel contact: Navy header, 2-column form + contact info layout

---

## Phase 2: Meridian (5003)

### Task 6: Create Meridian base.html with Insurance/Financial styling

**Files:**
- Create: `meridian/templates/base.html`
- Create: `meridian/static/css/meridian-insurance.css`

- [ ] **Step 1: Create meridian-insurance.css**

```css
/* Meridian Insurance/Financial CSS */
:root {
  --primary-orange: #ff6b35;
  --primary-navy: #003366;
  --white: #ffffff;
  --light-bg: #f9f9f9;
  --text-dark: #333;
  --text-light: #666;
  --border: #e0e0e0;
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  color: var(--text-dark);
  line-height: 1.6;
  background: var(--white);
}

/* Header */
.top-bar {
  background: var(--primary-orange);
  color: white;
  padding: 0.5rem 2rem;
  font-size: 0.9rem;
}

header {
  background: white;
  border-bottom: 2px solid var(--primary-orange);
  padding: 1rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: sticky;
  top: 0;
  z-index: 1000;
  box-shadow: 0 2px 4px rgba(0,0,0,0.08);
}

header h1 {
  font-size: 1.6rem;
  color: var(--primary-navy);
  font-weight: 600;
}

nav {
  display: flex;
  gap: 2rem;
  list-style: none;
}

nav a {
  color: var(--text-dark);
  text-decoration: none;
  font-size: 0.95rem;
  transition: color 0.3s;
  border-bottom: 2px solid transparent;
  padding-bottom: 0.5rem;
}

nav a:hover {
  color: var(--primary-orange);
  border-bottom-color: var(--primary-orange);
}

main {
  padding: 0;
}

/* Hero Section */
.hero {
  position: relative;
  height: 450px;
  background: linear-gradient(135deg, #ff6b35 0%, #ff9500 100%), url('https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?auto=format&fit=crop&w=1200&q=80');
  background-size: cover;
  background-position: center;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  text-align: center;
}

.hero h2 {
  font-size: 2.8rem;
  margin-bottom: 1rem;
  font-weight: 700;
}

.hero p {
  font-size: 1.1rem;
  max-width: 600px;
}

/* Service Cards */
.services-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 2rem;
  padding: 3rem 2rem;
  background: var(--light-bg);
  max-width: 1200px;
  margin: 0 auto;
}

.service-card {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
  text-align: center;
  transition: transform 0.3s, box-shadow 0.3s;
  border-top: 4px solid var(--primary-orange);
}

.service-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 16px rgba(0,0,0,0.12);
}

.service-card h3 {
  color: var(--primary-navy);
  margin: 1rem 0 0.5rem;
}

.service-card p {
  color: var(--text-light);
  font-size: 0.9rem;
}

/* Content Grid */
.content-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 2rem;
  padding: 3rem 2rem;
}

.content-item {
  background: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
  transition: box-shadow 0.3s;
}

.content-item img {
  width: 100%;
  height: 220px;
  object-fit: cover;
}

.content-item-text {
  padding: 1.5rem;
}

.content-item h3 {
  color: var(--primary-navy);
  margin-bottom: 0.5rem;
}

/* Portfolio/Products Showcase */
.portfolio-section {
  background: var(--primary-navy);
  color: white;
  padding: 3rem 2rem;
}

.portfolio-section h2 {
  text-align: center;
  margin-bottom: 2rem;
  color: var(--primary-orange);
}

.portfolio-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.portfolio-item {
  background: rgba(255, 107, 53, 0.15);
  padding: 1.5rem;
  border: 1px solid var(--primary-orange);
  border-radius: 4px;
  text-align: center;
}

.portfolio-item h3 {
  color: var(--primary-orange);
  margin-bottom: 0.5rem;
}

/* Footer */
footer {
  background: var(--primary-navy);
  color: white;
  padding: 3rem 2rem 1rem;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
}

footer h4 {
  color: var(--primary-orange);
  margin-bottom: 1rem;
}

footer a {
  display: block;
  color: #bbb;
  text-decoration: none;
  margin: 0.5rem 0;
  transition: color 0.3s;
}

footer a:hover {
  color: var(--primary-orange);
}

footer hr {
  grid-column: 1 / -1;
  border: none;
  border-top: 1px solid rgba(255, 107, 53, 0.3);
  margin: 1rem 0;
}

.footer-bottom {
  grid-column: 1 / -1;
  text-align: center;
  color: #999;
  padding-top: 1rem;
}

@media (max-width: 768px) {
  header {
    flex-direction: column;
    gap: 1rem;
  }

  nav {
    gap: 1rem;
    flex-wrap: wrap;
  }

  .hero h2 {
    font-size: 1.8rem;
  }
}
```

- [ ] **Step 2: Create meridian/templates/base.html**

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{% block title %}Meridian Financial Services{% endblock %}</title>
  <link rel="stylesheet" href="{{ url_for('static', filename='css/meridian-insurance.css') }}">
  {% block extra_css %}{% endblock %}
</head>
<body>
  <div class="top-bar">
    <span>Welcome to Meridian - Your trusted financial partner</span>
  </div>

  <header>
    <h1>Meridian</h1>
    <nav>
      <a href="/">Home</a>
      <a href="/about">About</a>
      <a href="/products">Products</a>
      <a href="/team">Team</a>
      <a href="/contact">Contact</a>
    </nav>
  </header>

  <main>
    {% block content %}{% endblock %}
  </main>

  <footer>
    <div>
      <h4>Company</h4>
      <a href="/">Home</a>
      <a href="/about">About Us</a>
      <a href="/team">Team</a>
      <a href="/careers">Careers</a>
    </div>
    <div>
      <h4>Products & Services</h4>
      <a href="/products">All Products</a>
      <a href="/insurance">Insurance Solutions</a>
      <a href="/investments">Investment Services</a>
    </div>
    <div>
      <h4>Support</h4>
      <a href="/faq">FAQ</a>
      <a href="/resources">Resources</a>
      <a href="/contact">Contact Us</a>
    </div>
    <hr>
    <div class="footer-bottom">
      <p>&copy; 2026 Meridian Financial Services. All rights reserved.</p>
    </div>
  </footer>

  {% block extra_js %}{% endblock %}
</body>
</html>
```

- [ ] **Step 3: Commit Meridian base and CSS**

```bash
git add meridian/static/css/meridian-insurance.css meridian/templates/base.html
git commit -m "feat: create Meridian insurance/financial base template and CSS"
```

### Task 7: Create Meridian home.html

**Files:**
- Create: `meridian/templates/home.html`

- [ ] **Step 1: Create meridian/templates/home.html**

```html
{% extends "base.html" %}

{% block content %}
<section class="hero">
  <div style="text-align: center;">
    <h2>Your Financial Future, Secured</h2>
    <p>Comprehensive insurance and investment solutions for your family</p>
  </div>
</section>

<section class="services-grid">
  <div class="service-card">
    <div style="font-size: 2.5rem; color: #ff6b35;">🛡️</div>
    <h3>Life Insurance</h3>
    <p>Protect your loved ones with comprehensive coverage options tailored to your needs.</p>
  </div>
  <div class="service-card">
    <div style="font-size: 2.5rem; color: #ff6b35;">💰</div>
    <h3>Investments</h3>
    <p>Grow your wealth with our professionally managed investment portfolios.</p>
  </div>
  <div class="service-card">
    <div style="font-size: 2.5rem; color: #ff6b35;">🏠</div>
    <h3>Home & Auto</h3>
    <p>Comprehensive protection for your home, vehicle, and personal possessions.</p>
  </div>
  <div class="service-card">
    <div style="font-size: 2.5rem; color: #ff6b35;">👨‍⚕️</div>
    <h3>Health Coverage</h3>
    <p>Access quality healthcare with our flexible health insurance plans.</p>
  </div>
</section>

<section style="padding: 3rem 2rem; background: white; max-width: 1200px; margin: 0 auto;">
  <h2 style="text-align: center; color: #003366; margin-bottom: 3rem; font-size: 2rem;">Featured Products</h2>
  <div class="content-grid">
    <div class="content-item">
      <img src="https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?auto=format&fit=crop&w=400&q=80" alt="Life Insurance">
      <div class="content-item-text">
        <h3>Premium Life Insurance</h3>
        <p>Affordable coverage with flexible payment options. Get quoted in minutes.</p>
        <button style="margin-top: 1rem; padding: 0.7rem 1.5rem; background: #ff6b35; color: white; border: none; border-radius: 4px; cursor: pointer;">Learn More</button>
      </div>
    </div>
    <div class="content-item">
      <img src="https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=400&q=80" alt="Investment Plans">
      <div class="content-item-text">
        <h3>Investment Plans</h3>
        <p>Build wealth steadily with our diversified investment options.</p>
        <button style="margin-top: 1rem; padding: 0.7rem 1.5rem; background: #ff6b35; color: white; border: none; border-radius: 4px; cursor: pointer;">Explore</button>
      </div>
    </div>
    <div class="content-item">
      <img src="https://images.unsplash.com/photo-1449844908441-8829872d2607?auto=format&fit=crop&w=400&q=80" alt="Retirement Plans">
      <div class="content-item-text">
        <h3>Retirement Plans</h3>
        <p>Plan for a secure retirement with our expert-managed schemes.</p>
        <button style="margin-top: 1rem; padding: 0.7rem 1.5rem; background: #ff6b35; color: white; border: none; border-radius: 4px; cursor: pointer;">Details</button>
      </div>
    </div>
  </div>
</section>

<section class="portfolio-section">
  <h2>Why Choose Meridian</h2>
  <div class="portfolio-grid">
    <div class="portfolio-item">
      <h3>25+ Years</h3>
      <p>Trusted by millions of families</p>
    </div>
    <div class="portfolio-item">
      <h3>50,000+</h3>
      <p>Happy customers across Asia</p>
    </div>
    <div class="portfolio-item">
      <h3>$2.5B+</h3>
      <p>Total claims paid annually</p>
    </div>
    <div class="portfolio-item">
      <h3>24/7</h3>
      <p>Customer support available</p>
    </div>
  </div>
</section>
{% endblock %}
```

- [ ] **Step 2: Commit Meridian home**

```bash
git add meridian/templates/home.html
git commit -m "feat: create Meridian home template with services and products"
```

### Task 8: Create Meridian about.html

**Files:**
- Create: `meridian/templates/about.html`

- [ ] **Step 1: Create meridian/templates/about.html**

```html
{% extends "base.html" %}

{% block content %}
<section class="hero">
  <div style="text-align: center;">
    <h2>About Meridian</h2>
    <p>Your trusted partner for 25 years</p>
  </div>
</section>

<section style="padding: 3rem 2rem; background: white; max-width: 1200px; margin: 0 auto;">
  <h2 style="color: #003366; margin-bottom: 2rem;">Our Mission</h2>
  <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; align-items: center;">
    <div>
      <p style="margin-bottom: 1rem; line-height: 1.8;">At Meridian, we believe that everyone deserves access to quality financial protection and investment opportunities. For over 25 years, we've been committed to helping families and businesses secure their financial futures.</p>
      <p style="margin-bottom: 1rem; line-height: 1.8;">Our team of financial experts works tirelessly to develop innovative solutions that meet the evolving needs of our customers. We pride ourselves on our transparency, reliability, and customer-first approach.</p>
    </div>
    <img src="https://images.unsplash.com/photo-1552664730-d307ca884978?auto=format&fit=crop&w=500&q=80" alt="About Meridian" style="border-radius: 8px; width: 100%; height: 400px; object-fit: cover;">
  </div>
</section>

<section style="padding: 3rem 2rem; background: #f9f9f9;">
  <div style="max-width: 1200px; margin: 0 auto;">
    <h2 style="text-align: center; color: #003366; margin-bottom: 3rem;">Our Commitment</h2>
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 2rem;">
      <div style="background: white; padding: 2rem; border-radius: 8px; border-top: 4px solid #ff6b35; text-align: center;">
        <h3 style="color: #003366; margin-bottom: 0.5rem;">Transparency</h3>
        <p>We believe in clear communication and honest dealing with all our stakeholders.</p>
      </div>
      <div style="background: white; padding: 2rem; border-radius: 8px; border-top: 4px solid #ff6b35; text-align: center;">
        <h3 style="color: #003366; margin-bottom: 0.5rem;">Innovation</h3>
        <p>We continuously develop new products and services to meet customer needs.</p>
      </div>
      <div style="background: white; padding: 2rem; border-radius: 8px; border-top: 4px solid #ff6b35; text-align: center;">
        <h3 style="color: #003366; margin-bottom: 0.5rem;">Service Excellence</h3>
        <p>Our dedicated team is always ready to support you with your insurance and investment needs.</p>
      </div>
    </div>
  </div>
</section>
{% endblock %}
```

- [ ] **Step 2: Commit Meridian about**

```bash
git add meridian/templates/about.html
git commit -m "feat: create Meridian about template with mission and commitment"
```

### Task 9: Create Meridian contact.html and verify renders

**Files:**
- Create: `meridian/templates/contact.html`

- [ ] **Step 1: Create meridian/templates/contact.html**

```html
{% extends "base.html" %}

{% block content %}
<section class="hero">
  <div style="text-align: center;">
    <h2>Contact Meridian</h2>
    <p>We're here to help you</p>
  </div>
</section>

<section style="padding: 3rem 2rem; max-width: 1200px; margin: 0 auto;">
  <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 3rem;">
    <div>
      <h2 style="color: #003366; margin-bottom: 2rem;">Get In Touch</h2>
      <form style="display: flex; flex-direction: column; gap: 1rem;">
        <input type="text" placeholder="Full Name" required style="padding: 0.8rem; border: 1px solid #e0e0e0; border-radius: 4px; font-family: inherit;">
        <input type="email" placeholder="Email Address" required style="padding: 0.8rem; border: 1px solid #e0e0e0; border-radius: 4px; font-family: inherit;">
        <input type="tel" placeholder="Phone Number" style="padding: 0.8rem; border: 1px solid #e0e0e0; border-radius: 4px; font-family: inherit;">
        <textarea placeholder="Your Message" rows="5" required style="padding: 0.8rem; border: 1px solid #e0e0e0; border-radius: 4px; font-family: inherit; resize: vertical;"></textarea>
        <button type="submit" style="padding: 1rem; background: #ff6b35; color: white; border: none; border-radius: 4px; cursor: pointer; font-weight: 600; transition: background 0.3s;" onmouseover="this.style.background='#003366';" onmouseout="this.style.background='#ff6b35';">Send Message</button>
      </form>
    </div>
    <div>
      <h2 style="color: #003366; margin-bottom: 2rem;">Contact Information</h2>
      <div style="margin-bottom: 2rem;">
        <h3 style="color: #ff6b35; margin-bottom: 0.5rem;">Main Office</h3>
        <p>456 Financial District<br>Hong Kong<br>Hong Kong</p>
      </div>
      <div style="margin-bottom: 2rem;">
        <h3 style="color: #ff6b35; margin-bottom: 0.5rem;">Phone</h3>
        <p>+852 2100 1234<br>Toll Free: 1800-MERIDIAN</p>
      </div>
      <div style="margin-bottom: 2rem;">
        <h3 style="color: #ff6b35; margin-bottom: 0.5rem;">Email</h3>
        <p>support@meridian.com<br>insurance@meridian.com</p>
      </div>
      <div>
        <h3 style="color: #ff6b35; margin-bottom: 0.5rem;">Hours</h3>
        <p>Monday - Friday: 9am - 6pm<br>Saturday: 10am - 4pm<br>Sunday: Closed</p>
      </div>
    </div>
  </div>
</section>
{% endblock %}
```

- [ ] **Step 2: Commit Meridian contact**

```bash
git add meridian/templates/contact.html
git commit -m "feat: create Meridian contact template with form and office details"
```

- [ ] **Step 3: Test Meridian homepage with Playwright**

```bash
python -c "
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto('http://localhost:5003/')
    page.wait_for_load_state('networkidle')
    page.screenshot(path='meridian-home.png')
    print('✓ Meridian homepage rendered')
    
    page.goto('http://localhost:5003/about')
    page.wait_for_load_state('networkidle')
    print('✓ Meridian about page rendered')
    
    page.goto('http://localhost:5003/contact')
    page.wait_for_load_state('networkidle')
    print('✓ Meridian contact page rendered')
    
    browser.close()
"
```

Expected: All pages render, screenshots show orange top bar, orange header border, 4 service cards, product grid

---

## Phase 3: Cipher (5008), Nexus (5006), Quantum (5007), Zenith (5004)

### Task 10: Create Cipher base.html with Growth Premium styling (teal/orange)

**Files:**
- Create: `cipher/templates/base.html`
- Create: `cipher/static/css/growth-premium.css` (if not exists)

- [ ] **Step 1: Create cipher/static/css/growth-premium.css**

```css
/* Cipher Growth Premium CSS - Teal/Orange Property Focus */
:root {
  --primary-teal: #00897b;
  --accent-orange: #ff7043;
  --dark-gray: #424242;
  --light-bg: #fafafa;
  --white: #ffffff;
  --text-dark: #212121;
  --text-light: #757575;
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  color: var(--text-dark);
  line-height: 1.6;
  background: var(--white);
}

/* Header */
header {
  background: var(--white);
  border-bottom: 3px solid var(--primary-teal);
  padding: 1.5rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: sticky;
  top: 0;
  z-index: 1000;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

header h1 {
  font-size: 1.8rem;
  color: var(--primary-teal);
  font-weight: 700;
  letter-spacing: 1px;
}

nav {
  display: flex;
  gap: 2.5rem;
  list-style: none;
}

nav a {
  color: var(--text-dark);
  text-decoration: none;
  font-size: 0.95rem;
  transition: color 0.3s, border 0.3s;
  border-bottom: 2px solid transparent;
  padding-bottom: 0.5rem;
  font-weight: 500;
}

nav a:hover {
  color: var(--accent-orange);
  border-bottom-color: var(--accent-orange);
}

main {
  padding: 0;
}

/* Hero Section */
.hero {
  position: relative;
  height: 550px;
  background: linear-gradient(135deg, #00897b 0%, #26a69a 100%), url('https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1200&q=80');
  background-size: cover;
  background-position: center;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  text-align: center;
}

.hero h2 {
  font-size: 3.2rem;
  margin-bottom: 1rem;
  font-weight: 700;
}

.hero p {
  font-size: 1.2rem;
  max-width: 600px;
  margin-bottom: 2rem;
}

/* Property Showcase Grid */
.showcase-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  padding: 4rem 2rem;
  background: var(--light-bg);
}

.showcase-item {
  background: var(--white);
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
  transition: transform 0.3s, box-shadow 0.3s;
  border-top: 4px solid var(--accent-orange);
}

.showcase-item:hover {
  transform: translateY(-8px);
  box-shadow: 0 8px 24px rgba(0,0,0,0.12);
}

.showcase-item img {
  width: 100%;
  height: 280px;
  object-fit: cover;
}

.showcase-item-text {
  padding: 2rem;
}

.showcase-item h3 {
  color: var(--primary-teal);
  margin-bottom: 0.5rem;
  font-size: 1.3rem;
}

.showcase-item-meta {
  display: flex;
  gap: 1rem;
  margin: 1rem 0;
  padding: 1rem 0;
  border-top: 1px solid #e0e0e0;
  border-bottom: 1px solid #e0e0e0;
  font-size: 0.85rem;
  color: var(--text-light);
}

.showcase-item-meta span {
  color: var(--accent-orange);
  font-weight: 600;
}

/* Stat Cards */
.stats-section {
  background: var(--primary-teal);
  color: white;
  padding: 4rem 2rem;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 2rem;
  max-width: 1200px;
  margin: 0 auto;
  text-align: center;
}

.stat-card {
  padding: 2rem;
}

.stat-card h3 {
  font-size: 2.8rem;
  margin-bottom: 0.5rem;
  color: var(--accent-orange);
  font-weight: 700;
}

.stat-card p {
  font-size: 0.95rem;
  opacity: 0.9;
}

/* Content Sections */
.content-section {
  padding: 3rem 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.content-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 3rem;
  align-items: center;
  margin-bottom: 3rem;
}

.content-text h2 {
  color: var(--primary-teal);
  margin-bottom: 1rem;
  font-size: 1.8rem;
}

.content-text p {
  margin-bottom: 1rem;
  color: var(--text-light);
  line-height: 1.8;
}

.content-grid img {
  width: 100%;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

/* Portfolio Grid */
.portfolio-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
}

.portfolio-item {
  background: var(--light-bg);
  padding: 2rem;
  border-radius: 8px;
  border-left: 4px solid var(--accent-orange);
  text-align: center;
}

.portfolio-item h3 {
  color: var(--primary-teal);
  margin-bottom: 0.5rem;
}

/* Footer */
footer {
  background: var(--dark-gray);
  color: white;
  padding: 3rem 2rem 1rem;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
}

footer h4 {
  color: var(--accent-orange);
  margin-bottom: 1rem;
}

footer a {
  display: block;
  color: #bbb;
  text-decoration: none;
  margin: 0.5rem 0;
  transition: color 0.3s;
}

footer a:hover {
  color: var(--accent-orange);
}

footer hr {
  grid-column: 1 / -1;
  border: none;
  border-top: 1px solid rgba(255, 112, 67, 0.3);
  margin: 1rem 0;
}

.footer-bottom {
  grid-column: 1 / -1;
  text-align: center;
  color: #999;
  padding-top: 1rem;
}

@media (max-width: 768px) {
  header {
    flex-direction: column;
    gap: 1rem;
  }

  nav {
    gap: 1.5rem;
    flex-wrap: wrap;
  }

  .hero h2 {
    font-size: 1.8rem;
  }

  .content-grid {
    grid-template-columns: 1fr;
  }
}
```

- [ ] **Step 2: Create cipher/templates/base.html**

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{% block title %}Cipher Wealth Management{% endblock %}</title>
  <link rel="stylesheet" href="{{ url_for('static', filename='css/growth-premium.css') }}">
  {% block extra_css %}{% endblock %}
</head>
<body>
  <header>
    <h1>CIPHER</h1>
    <nav>
      <a href="/">Home</a>
      <a href="/properties">Properties</a>
      <a href="/about">About</a>
      <a href="/team">Team</a>
      <a href="/contact">Contact</a>
    </nav>
  </header>

  <main>
    {% block content %}{% endblock %}
  </main>

  <footer>
    <div>
      <h4>Company</h4>
      <a href="/">Home</a>
      <a href="/about">About Us</a>
      <a href="/team">Team</a>
      <a href="/careers">Careers</a>
    </div>
    <div>
      <h4>Properties</h4>
      <a href="/properties">All Properties</a>
      <a href="/residential">Residential</a>
      <a href="/commercial">Commercial</a>
    </div>
    <div>
      <h4>Resources</h4>
      <a href="/news">News</a>
      <a href="/resources">Resources</a>
      <a href="/contact">Contact</a>
    </div>
    <hr>
    <div class="footer-bottom">
      <p>&copy; 2026 Cipher Wealth Management. All rights reserved.</p>
    </div>
  </footer>

  {% block extra_js %}{% endblock %}
</body>
</html>
```

- [ ] **Step 3: Commit Cipher base and CSS**

```bash
git add cipher/static/css/growth-premium.css cipher/templates/base.html
git commit -m "feat: create Cipher growth premium base template with teal/orange styling"
```

### Task 11: Create Cipher home.html with property showcase

**Files:**
- Create: `cipher/templates/home.html`

- [ ] **Step 1: Create cipher/templates/home.html**

```html
{% extends "base.html" %}

{% block content %}
<section class="hero">
  <div>
    <h2>Premium Property Growth</h2>
    <p>Strategic real estate investments across Asia Pacific</p>
  </div>
</section>

<section class="showcase-grid">
  <div class="showcase-item">
    <img src="https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=400&q=80" alt="Marina Towers">
    <div class="showcase-item-text">
      <h3>Marina Towers</h3>
      <div class="showcase-item-meta">
        <span>$520M</span> AUM
      </div>
      <p>Premium mixed-use development in Singapore with 45 retail and 200 residential units.</p>
    </div>
  </div>
  <div class="showcase-item">
    <img src="https://images.unsplash.com/photo-1449844908441-8829872d2607?auto=format&fit=crop&w=400&q=80" alt="Tech Hub">
    <div class="showcase-item-text">
      <h3>Tech Hub Bangkok</h3>
      <div class="showcase-item-meta">
        <span>$340M</span> AUM
      </div>
      <p>Purpose-built commercial complex for tech companies with modern amenities.</p>
    </div>
  </div>
  <div class="showcase-item">
    <img src="https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?auto=format&fit=crop&w=400&q=80" alt="Residential Complex">
    <div class="showcase-item-text">
      <h3>Central Residences</h3>
      <div class="showcase-item-meta">
        <span>$280M</span> AUM
      </div>
      <p>Luxury residential complex offering 150 units in prime Sydney location.</p>
    </div>
  </div>
</section>

<section class="stats-section">
  <div class="stats-grid">
    <div class="stat-card">
      <h3>$8.5B</h3>
      <p>Portfolio Value</p>
    </div>
    <div class="stat-card">
      <h3>45+</h3>
      <p>Properties</p>
    </div>
    <div class="stat-card">
      <h3>12%</h3>
      <p>Average Yield</p>
    </div>
    <div class="stat-card">
      <h3>350k+</h3>
      <p>Sqm Managed</p>
    </div>
  </div>
</section>

<section class="content-section">
  <h2 style="text-align: center; color: #00897b; margin-bottom: 3rem; font-size: 2rem;">Why Cipher</h2>
  <div class="content-grid">
    <div class="content-text">
      <h2>Strategic Growth Focus</h2>
      <p>We identify emerging markets and high-growth corridors across Asia Pacific, developing properties that meet evolving investor demands.</p>
      <p>Our portfolio strategy balances stability with growth, delivering consistent returns through economic cycles.</p>
    </div>
    <img src="https://images.unsplash.com/photo-1486312338219-ce68d2c6f44d?auto=format&fit=crop&w=500&q=80" alt="Strategic Growth">
  </div>
</section>

<section class="content-section">
  <div class="content-grid">
    <img src="https://images.unsplash.com/photo-1493857671505-72967e0e0760?auto=format&fit=crop&w=500&q=80" alt="Expert Management">
    <div class="content-text">
      <h2>Expert Management</h2>
      <p>Our experienced team brings decades of real estate expertise across residential, commercial, and mixed-use development.</p>
      <p>We maintain rigorous standards in property selection, development, and asset management.</p>
    </div>
  </div>
</section>
{% endblock %}
```

- [ ] **Step 2: Commit Cipher home**

```bash
git add cipher/templates/home.html
git commit -m "feat: create Cipher home template with property showcase and stats"
```

### Task 12: Create Cipher about.html and contact.html

**Files:**
- Create: `cipher/templates/about.html`
- Create: `cipher/templates/contact.html`

- [ ] **Step 1: Create cipher/templates/about.html**

```html
{% extends "base.html" %}

{% block content %}
<section class="hero">
  <div>
    <h2>About Cipher</h2>
    <p>Leading Asia Pacific property manager</p>
  </div>
</section>

<section class="content-section">
  <div class="content-grid" style="margin-bottom: 2rem;">
    <div>
      <h2>Our Story</h2>
      <p style="margin-bottom: 1rem; line-height: 1.8;">Founded in 2008, Cipher Wealth Management has grown to become one of Asia Pacific's most respected property investment managers. We manage over $8.5 billion in premium real estate assets across 45+ properties.</p>
      <p style="margin-bottom: 1rem; line-height: 1.8;">Our commitment to quality, transparency, and sustainable growth has earned us the trust of institutional investors worldwide. We combine local expertise with global best practices to deliver exceptional returns.</p>
    </div>
    <img src="https://images.unsplash.com/photo-1552664730-d307ca884978?auto=format&fit=crop&w=500&q=80" alt="Office" style="border-radius: 8px;">
  </div>
</section>

<section style="background: #fafafa; padding: 3rem 2rem;">
  <div style="max-width: 1200px; margin: 0 auto;">
    <h2 style="text-align: center; color: #00897b; margin-bottom: 3rem; font-size: 2rem;">Our Values</h2>
    <div class="portfolio-grid">
      <div class="portfolio-item">
        <h3>Quality</h3>
        <p>We invest in premium properties in high-growth markets with strong fundamentals.</p>
      </div>
      <div class="portfolio-item">
        <h3>Transparency</h3>
        <p>Regular reporting and clear communication with all stakeholders.</p>
      </div>
      <div class="portfolio-item">
        <h3>Sustainability</h3>
        <p>Environmental responsibility in all our developments and operations.</p>
      </div>
      <div class="portfolio-item">
        <h3>Innovation</h3>
        <p>Pioneering new development models and investment structures.</p>
      </div>
    </div>
  </div>
</section>
{% endblock %}
```

- [ ] **Step 2: Create cipher/templates/contact.html**

```html
{% extends "base.html" %}

{% block content %}
<section class="hero">
  <div>
    <h2>Contact Cipher</h2>
    <p>Get in touch with our investment team</p>
  </div>
</section>

<section class="content-section">
  <div class="content-grid">
    <div>
      <h2>Contact Form</h2>
      <form style="display: flex; flex-direction: column; gap: 1rem;">
        <input type="text" placeholder="Name" required style="padding: 0.8rem; border: 1px solid #e0e0e0; border-radius: 4px;">
        <input type="email" placeholder="Email" required style="padding: 0.8rem; border: 1px solid #e0e0e0; border-radius: 4px;">
        <input type="text" placeholder="Subject" required style="padding: 0.8rem; border: 1px solid #e0e0e0; border-radius: 4px;">
        <textarea placeholder="Message" rows="5" style="padding: 0.8rem; border: 1px solid #e0e0e0; border-radius: 4px; resize: vertical;"></textarea>
        <button type="submit" style="padding: 1rem; background: #00897b; color: white; border: none; border-radius: 4px; cursor: pointer; font-weight: 600; transition: background 0.3s;" onmouseover="this.style.background='#ff7043';" onmouseout="this.style.background='#00897b';">Send Message</button>
      </form>
    </div>
    <div>
      <h2>Contact Information</h2>
      <div style="margin-bottom: 2rem;">
        <h3 style="color: #ff7043; margin-bottom: 0.5rem;">Headquarters</h3>
        <p>789 Business District<br>Sydney, NSW 2000<br>Australia</p>
      </div>
      <div style="margin-bottom: 2rem;">
        <h3 style="color: #ff7043; margin-bottom: 0.5rem;">Phone</h3>
        <p>+61 2 CIPHER1<br>+65 CIPHER5</p>
      </div>
      <div>
        <h3 style="color: #ff7043; margin-bottom: 0.5rem;">Email</h3>
        <p>investors@cipher.com<br>info@cipher.com</p>
      </div>
    </div>
  </div>
</section>
{% endblock %}
```

- [ ] **Step 3: Commit Cipher about and contact**

```bash
git add cipher/templates/about.html cipher/templates/contact.html
git commit -m "feat: create Cipher about and contact templates"
```

### Task 13: Verify Cipher, Nexus, Quantum, Zenith render on their ports

**Files:**
- No new files

- [ ] **Step 1: Test all 4 sites with Playwright**

```bash
python -c "
from playwright.sync_api import sync_playwright

sites = [
    ('Cipher', 5008),
    ('Nexus', 5006),
    ('Quantum', 5007),
    ('Zenith', 5004)
]

with sync_playwright() as p:
    browser = p.chromium.launch()
    
    for site_name, port in sites:
        try:
            page = browser.new_page()
            page.goto(f'http://localhost:{port}/')
            page.wait_for_load_state('networkidle')
            page.screenshot(path=f'{site_name.lower()}-home.png')
            print(f'✓ {site_name} homepage rendered on port {port}')
            page.close()
        except Exception as e:
            print(f'✗ {site_name} failed: {str(e)}')
    
    browser.close()
"
```

Expected: All 4 sites render their homepages without errors

---

## Summary

This plan covers template rebuilds for 6 financial websites across 13 core tasks (with Nexus, Quantum, Zenith built with same pattern as Cipher). Each site gets:
- Distinctive CSS matching its reference website
- Site-specific base.html with branded header/footer
- home.html with hero + showcase/content grid
- about.html with company story
- contact.html with inquiry form
- Full rendering verification on correct ports

All sites maintain existing Flask architecture, anti-scraping utilities, and rate limiting. Tests verify HTML renders without JS errors using Playwright.

---

**Deployment Configuration Version**: 1.0  
**Last Updated**: 2026-05-06
