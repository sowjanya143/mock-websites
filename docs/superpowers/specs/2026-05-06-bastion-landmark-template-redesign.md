# Bastion & Landmark Template Redesign

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development to implement this plan task-by-task with specialized frontend-design subagents. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rebuild all 23 Bastion and Landmark HTML templates with completely distinctive, photography-driven layouts that match their reference sites (Fortress.com and Heitman.com) instead of generic card-based structures.

**Architecture:** Complete HTML structure overhaul using a rewrite approach (Approach A). Each of the 23 templates gets a unique layout structure tailored to its purpose and the reference site's visual pattern. Bastion templates emphasize portfolio showcases, stat overlays, and alternating image-text blocks. Landmark templates emphasize minimal design, navy header consistency, team/office location imagery, and alternating content sections. No component inheritance—each template is self-contained with distinctive structure.

**Tech Stack:** Flask Jinja2 templates, CSS (existing color schemes: Bastion gold/dark, Landmark green/navy), Unsplash API for free stock images.

---

## BASTION INVESTMENT GROUP - 11 Pages

**Design Principles:**
- Full-page hero backgrounds on all pages (strategy/architecture/office imagery from Unsplash)
- Portfolio company showcase section on every page (8-12 company logos)
- Large stat cards (clickable, link to relevant pages)
- Serif headings (Georgia) for main titles
- Gold accents (#c8a96e) on borders and CTAs
- 2-column layouts with alternating image-text pairings
- Gold borders on left side of content sections

### Page Structures

**1. home.html**
- Full-page hero background (abstract finance/architecture)
- Overlay: 5 large stat cards ($55B AUM, >$200B deployed, 2,000+ companies, etc.) positioned center-bottom
- Section: "Why Bastion" with 6 strategy cards in 2-column layout (NOT 3-column grid)
- Section: Featured Funds, 2-column large cards with images
- Section: Portfolio Showcase, 8-12 company logos in responsive grid
- Section: Call-to-action with investor inquiry
- Footer with newsletter signup

**2. what-we-do.html**
- Hero with background image + "Our Investment Strategies" text overlay
- For each of 6 strategies: 2-column alternating layout
  - Left: Strategy name (serif heading), description, metrics
  - Right: Relevant investment process graphic or image from Unsplash
- Section: Portfolio Showcase (companies in these strategies)
- Call-to-action

**3-8. what-we-do/[strategy-slug].html (Strategy Detail Pages)**
- Hero with strategy-specific background image
- Large serif heading + descriptive text
- Alternating left-right content blocks:
  - Block 1: Text-left, Image-right (strategy overview + image)
  - Block 2: Image-left, Text-right (approach/process + image)
  - Block 3: Text-left, Image-right (benefits + image)
- Section: Fund Details (funds in this strategy)
- Section: Portfolio Showcase (companies invested in this strategy)
- Section: Related Strategies CTA

**9. who-we-are.html**
- Hero with company office/building imagery
- 4 large stat cards (clickable): assets, companies, returns, people
- Section: Mission/Vision (2-column: image-left, text-right)
- Section: Core Values (4 full-width cards with icons, NOT grid)
- Section: Impact statement with background color block
- Section: Portfolio Showcase
- Call-to-action

**10. who-we-are/team.html**
- Hero with team gathering image
- Team grid: 3-column layout with large headshots (image-first)
- Each card: Large photo, name, title, bio, social links
- Pagination controls below
- Section: "Join our team" with careers CTA
- Section: Portfolio Showcase

**11. investors.html**
- Hero with investor meeting/contract imagery
- 3 distinct portal sections (Institutional, FA, Insurance): Large box sections with image-left, features-right layout
- Section: Resource Library (4 downloadable items with icons, 2-column layout)
- Section: FAQ accordion
- Section: Portfolio Showcase
- Contact CTA

**12. financial-advisors.html**
- Hero with advisory/planning imagery
- Section: Knowledge Center (6 resources in 2-column with images)
- Section: Benefits (4 boxes, 2x2 grid with icons)
- Section: Positioning statement (background color block)
- Section: Advisor success story (image-left, testimonial-right)
- Section: Portfolio Showcase
- Contact form

**13. media.html**
- Hero with news/press imagery
- Section: News articles (2-column layout: image-top, headline/excerpt/date below, left gold border)
- Section: Press Resources (fact sheets, logos, downloads with icons)
- Section: Media Contact (gold background box)
- Section: Portfolio Showcase
- Call-to-action

**14. careers.html**
- Hero with team/office culture imagery
- Section: Career Narrative (2-3 paragraphs about culture with alternating image-left/text-right and text-left/image-right)
- Section: Benefits Grid (6 items, 2-column, with icons)
- Section: Open Positions (large cards, 1 per row, with position details and apply button)
- Section: Application Process (4 steps displayed horizontally)
- Section: Portfolio Showcase

**15. contact.html**
- Hero with minimal office/workspace imagery
- 2-column: Contact form (left), Contact info + regional offices (right)
- Section: Office Locations (4 cards with address, phone, map)
- Section: Newsletter Signup (gold box)
- Section: Portfolio Showcase (optional, at bottom)

---

## LANDMARK PROPERTY ADVISORS - 12 Pages

**Design Principles:**
- Fixed/sticky navy header (#001f3f) with "FIVE DECADES SERVING CLIENTS" tagline on all pages
- Full-screen hero on home page with architecture photography
- Team/office location imagery (not property investments)
- 5 clickable stat cards on homepage, each linking to relevant pages
- Georgia serif for headings
- Green accents (#1e4d3b, #4a7c6b) on buttons/borders
- Alternating white and warm gray (#f5f3f0) section backgrounds
- 60-year timeline on about page with 8 key milestones
- Minimal, elegant aesthetic

### Page Structures

**1. home.html**
- Full-screen hero: Architecture/real estate photography background
- Centered white text overlay: "Investment focus: real estate"
- Below hero: 5 large clickable stat cards (each links to relevant page):
  - $47B AUM → /investment-strategies
  - 50+ Years → /about
  - Global Presence → /about
  - 3 Strategies → /investment-strategies
  - Team size/offices (TBD) → /about/team
- Section: 3-column strategy cards with images and metrics
- Section: News grid (3-4 items, 2-column, with images)
- Call-to-action

**2. landmark-difference.html**
- Hero: Architecture photo with "The Landmark Difference" text overlay
- Section: 6 Differentiators (alternating image-left/text-right and text-left/image-right)
  - Each: Serif heading, description, relevant real estate imagery
- Section: Global Presence (5 office location cards with office building images)
- Section: Track Record (table or metrics display)
- Section: Core Values (5 values in 2-column layout with serif headings)

**3. investment-strategies.html**
- Hero with real estate/urban development imagery
- Section: 3 Strategy Cards (2-column + 1 below)
  - Each: Image-top, strategy name, metrics, description, learn-more link
- Section: Funds Table (comparison of funds, scrollable on mobile)
- Section: Fund Characteristics Matrix (interactive comparison)
- Call-to-action: "Speak with an advisor"

**4-6. investment-strategies/[strategy-slug].html (3 Strategy Pages)**
- Hero with strategy-specific real estate imagery
- Section: Overview (4 stat cards with key metrics)
- Section: Approach (alternating image-text blocks)
- Section: Fund Details (funds in this strategy with performance)
- Section: Investment Characteristics (grid or list)
- Section: Case Study (image-left, description-right with real estate project)

**7. about.html**
- Hero with company headquarters/campus imagery
- Section: 60-Year Timeline (horizontal timeline with 8 milestones: year, event, image)
- Section: 4 Office Regions (large cards with office photos, addresses)
- Section: 6 Core Values (3x2 grid with icons and descriptions)
- Section: Culture (2-3 paragraphs with integrated team/office photos)

**8. about/team.html**
- Hero with team gathering image
- Team grid: 3-column with large professional headshots (image-first)
- Each card: Photo, name, title, bio, social links
- Pagination below
- Section: Culture (2 paragraphs with team/office photos)
- Section: "Join us" CTA to careers

**9. about/sustainability.html**
- Hero with environmental/green imagery
- Section: 4 Sustainability Initiatives (alternating image-left/text-right and text-left/image-right)
  - Each: Heading, description, metrics, image
- Section: ESG Targets (3-column grid: Environmental, Social, Governance with metrics/icons)
- Section: Impact Statement (background color block)
- Commitment messaging

**10. news.html**
- Hero with media/press imagery
- Section: News Articles (2-column with image-top, headline, date, category, excerpt)
- Filter buttons: By category (optional)
- Section: Press Contact (gold/green background box with details)
- Archive link (optional)

**11. careers.html**
- Hero with team/culture imagery
- Section: Benefits Grid (6 benefits, 2-column, with icons)
- Section: Open Positions (large cards, 1 per row, full-width with details and apply button)
- Section: Application Process (4 steps horizontally)
- Section: Culture (2-3 paragraphs with integrated photos)

**12. contact.html**
- Hero with office/workspace imagery
- 2-column: Contact form (left), Contact info (right)
- Section: 4 Regional Office Cards (address, phone, photo, map link)
- Section: Newsletter Signup (green background box)
- Hours of operation

---

## Shared Elements

**Headers:**

**Bastion Header (All Pages)**
- Gold navigation bar on dark background, sticky
- Logo: "Bastion Investment Group"
- Nav items: What We Do, Who We Are, Investors, Media, Careers, Contact

**Landmark Header (All Pages)**
- Navy background (#001f3f), fixed/sticky on all pages
- Logo: "LANDMARK" 
- Tagline: "FIVE DECADES SERVING CLIENTS"
- Nav items: Landmark Difference, Investment Strategies, About, Careers, Contact
- Language selector (optional dropdown)

**Portfolio Showcase (Bastion Only)**
- Appears on: All Bastion pages except contact.html
- Content: 8-12 company logos in responsive grid
- Images: Search Unsplash for "corporate logos", "investment companies", "business logos"
- Styling: Grid with hover effects, dark background

**Footers (Both Sites)**
- Newsletter signup form (gold/green background)
- Company info + links (privacy, disclaimer, etc.)
- Social media icons
- Copyright

---

## Image/Asset Strategy

**Hero Background Images** (Unsplash searches):

*Bastion:*
- home.html: "finance", "investment", "abstract business"
- what-we-do.html: "business strategy", "growth"
- strategy detail pages: Strategy-specific ("real estate investment", "private equity", "credit markets", etc.)
- who-we-are.html: "office building", "corporate headquarters"
- team.html: "team gathering", "business team"
- investors.html: "investor meeting", "contract", "business deal"
- financial-advisors.html: "financial advisor", "investment planning"
- media.html: "news", "press", "announcement"
- careers.html: "team culture", "office teamwork"
- contact.html: "minimal office", "workspace"

*Landmark:*
- home.html: "architecture", "real estate", "modern building"
- landmark-difference.html: "modern architecture"
- investment-strategies.html: "urban development", "commercial real estate"
- strategy detail pages: Real estate specific ("luxury real estate", "commercial property", "development", etc.)
- about.html: "office headquarters", "campus"
- team.html: "professional team", "office culture"
- sustainability.html: "green building", "environmental", "sustainability"
- news.html: "press release", "media"
- careers.html: "company culture", "team office"
- contact.html: "office workspace", "reception"

**Content Images:** Unsplash searches like "investment companies", "business", "real estate properties", "professional headshots", "office spaces", "teamwork"

---

## Technical Implementation Notes

- Each template is self-contained (no component inheritance)
- Jinja2 block structure: `{% extends "base.html" %}` with main `{% block content %}`
- Inline `<style>` blocks per template for page-specific CSS
- Responsive design: Mobile breakpoints at 768px and 480px
- Image URLs: Use Unsplash direct URLs (format: `https://images.unsplash.com/photo-[ID]?w=[WIDTH]&q=[QUALITY]`)
- Data binding: Inject aum_data, team_data, news_data via Flask context processor
- DOM obfuscation still active: Use session class maps for semantic CSS class names
- Rate limiting still active: Bastion 10 req/60s, Landmark 4 req/60s
- No component duplication: Each template handles its own sections

---

## Success Criteria

- All 23 templates deploy and render without errors
- Each page has distinctive visual structure (not generic cards)
- Bastion pages clearly show portfolio showcase section on every page
- Landmark pages maintain consistent navy header across all pages
- Stat cards are clickable/interactive where specified
- Images load from Unsplash without broken links
- Mobile responsive at all breakpoints
- DOM obfuscation and anti-scraping measures still function
- Both sites serve on correct ports (5009, 5010) with no conflicts
