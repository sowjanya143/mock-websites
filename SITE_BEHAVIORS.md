# Site-Specific Anti-Scraping Behaviors

## ORIGINAL 5 SITES

### 1. Sentinel Capital Partners (Port 5000)
**Primary Obstacle: CAPTCHA on Every Page**

#### Specific Behaviors:
- **CAPTCHA Requirement**: `CAPTCHA_ON_EVERY_PAGE = True`
  - Every route checks for `session['captcha_passed']`
  - If missing, returns CAPTCHA page instead of content
  - Routes affected: `/`, `/about`, `/leadership`, `/strategies`, `/investor-resources`, `/funds`, `/fund/<id>`, `/news`, `/contact`
  
- **CAPTCHA Validation**:
  - 4-character random string image (PIL generated)
  - Noise lines and distortion
  - Case-insensitive answer validation
  - Stored in `session['captcha_answer']`
  
- **Session Management**:
  - CAPTCHA answer cleared after validation
  - Session flag: `session['captcha_passed'] = True`
  - Persists across all subsequent page views
  
- **Redirects**: After successful CAPTCHA, redirects to original referrer or home

#### Code Implementation:
```python
@require_captcha  # Decorator on all routes
def route_handler():
    # CAPTCHA passed or not required, proceed
    return render_template('...')

@app.before_request
def check_captcha():
    if request.method == 'POST' and 'captcha_answer' in request.form:
        if validate_captcha(user_answer):
            session['captcha_passed'] = True
            return redirect(request.referrer or url_for('home'))
        return jsonify({'status': 'error'}), 403
```

---

### 2. Apex Investment Group (Port 5001)
**Primary Obstacles: Rate Limiting + Selective CAPTCHA + Popups**

#### Specific Behaviors:
- **CAPTCHA on Data Pages Only**: `CAPTCHA_ON_EVERY_PAGE = False`
  - Protected routes: `/strategies`, `/investor-resources`, `/funds`, `/fund/<id>`
  - Home, about, leadership, contact: NO CAPTCHA
  - Helper function checks route against `CAPTCHA_REQUIRED_PAGES`
  
- **Rate Limiting**: 5 requests per 60 seconds per IP
  - `@rate_limit(5, 60)` decorator on all routes
  - Uses `_request_times` dict tracking per-IP timestamps
  - Sliding window algorithm (cleans old entries)
  - Returns 429 (TooManyRequests) on breach
  
- **Pop-ups**: Dismissible newsletter popup
  - Type: `'dismissible'` with no auto-dismiss
  - Trigger: `should_show_popup('data_page')` - only on data pages
  - Popup button: "Not Interested" dismissal
  - Session tracking: `session['popup_dismissed']`
  - `POST /api/dismiss-popup` endpoint
  
- **JSON API Endpoint**: `/api/aum`
  - Returns: `global_aum`, `by_asset_class`, `by_fund`
  - Used for AJAX-loaded data
  - `Config.DATA_LAYOUT = 'json_endpoint'`

#### Rate Limiting Storage:
```python
_request_times = {}  # {ip: [timestamp1, timestamp2, ...]}
# Sliding window: removes timestamps > time_window old
# If count > max_requests: raise TooManyRequests (429)
```

#### Popup Conditional:
```python
if Config.SHOW_POPUPS and should_show_popup('data_page'):
    render_popup('newsletter', auto_dismiss=False)
```

---

### 3. Meridian Global Holdings (Port 5002)
**Primary Obstacles: Random CAPTCHA + Artificial Delay + Modal Popups**

#### Specific Behaviors:
- **Random CAPTCHA**: 30% chance on every page
  - Config: `CAPTCHA_RANDOM_CHANCE = 0.30`
  - `@require_random_captcha` decorator
  - Triggers if: `random.random() < 0.30` AND `'captcha_passed' not in session`
  - Makes scraper timing unpredictable
  
- **Artificial Delay**: 1.0 second per request
  - Applied in `@app.before_request`
  - `time.sleep(1.0)` slows all responses
  - Defeats scrapers with tight timing windows
  - Config: `ARTIFICIAL_DELAY = 1.0`
  
- **Modal Pop-ups**: "Modal After Scroll"
  - Type: `'modal_after_scroll'`
  - Renders via custom `base.html` (site-specific)
  - JavaScript trigger: Appears after 30% page scroll
  - No auto-dismiss (user must close manually)
  - Intrusive modal overlay blocks content
  
- **Scattered Data Layout**: `DATA_LAYOUT = 'scattered'`
  - All numeric AUM values have ±5% variance applied
  - Data regenerated on EVERY request
  - `generate_dynamic_aum()` recursively applies variance
  - Makes data difficult to validate/compare
  
- **Custom Base Template**: Meridian's `base.html` is standalone
  - Inline CSS (not linked sheets)
  - Inline JavaScript for scroll detection
  - Not extending shared base

#### Random Captcha Logic:
```python
@app.before_request
def check_random_captcha():
    if random.random() < Config.CAPTCHA_RANDOM_CHANCE:
        if 'captcha_passed' not in session:
            return render CAPTCHA page
    return None
```

---

### 4. Premier Financial Services (Port 5003)
**Primary Obstacle: None - Baseline Control Site**

#### Specific Behaviors:
- **No CAPTCHA**: `CAPTCHA_ON_EVERY_PAGE = False`, `CAPTCHA_REQUIRED_PAGES = []`
  - All routes accessible without barriers
  - Used as performance/baseline comparison
  
- **No Rate Limiting**: `RATE_LIMIT_ENABLED = False`
  - Can make unlimited requests
  
- **No Popups**: `SHOW_POPUPS = False`
  
- **No Delays**: `ARTIFICIAL_DELAY = 0`
  
- **Clean Data Layout**: `DATA_LAYOUT = 'clean_tables'`
  - Static AUM data (no variance)
  - Consistent across all requests
  - Easy to scrape without obstacles
  
- **Uses Shared Base Template**
  - Standard HTML rendering
  - No custom styling or JavaScript

#### Routes:
```python
# All routes are bare @app.route() with no decorators
@app.route('/')
def home():
    return render_template('home.html')
```

---

### 5. Zenith Asset Management (Port 5004)
**Primary Obstacles: Dual CAPTCHA + Rate Limiting + Delays + Popups + AJAX**

#### Specific Behaviors:
- **Dual CAPTCHA Strategy**:
  - First-Visit CAPTCHA: `CAPTCHA_FIRST_VISIT = True`
    - Triggers if `'visited' not in session`
    - Forces CAPTCHA on first access to any page
  - Data-Page CAPTCHA: `CAPTCHA_DATA_PAGES = True`
    - Protected routes: `/strategies`, `/investor-resources`, `/funds`, `/fund/<id>`
    - Triggers if `'captcha_passed' not in session`
    - Combined gate: EITHER first visit OR data page protection
  
- **Rate Limiting**: 3 requests per 60 seconds (strictest)
  - `MAX_REQUESTS = 3`, `TIME_WINDOW = 60`
  - `@rate_limit(3, 60)` on all routes
  - 50% stricter than Apex (5 req/60s)
  
- **Artificial Delay**: 0.5 seconds per request
  - `ARTIFICIAL_DELAY = 0.5`
  - Slower than Meridian but faster
  - Still defeats fast scrapers
  
- **Sticky Footer Popup**: Auto-dismissing
  - Type: `'sticky_footer'`
  - Auto-dismiss: `AUTO_DISMISS_POPUP = True`
  - Auto-dismiss delay: 5000ms (5 seconds)
  - Appears on data pages: `should_show_popup('data_page')`
  - Sticky positioned (stays visible while scrolling)
  
- **AJAX-Loaded Funds Data**: `DATA_LAYOUT = 'ajax_loaded'`
  - `/api/funds` endpoint returns fund list
  - Client-side JavaScript loads data via fetch/AJAX
  - Requires JavaScript execution to display funds
  
- **Session Tracking**:
  - `session['visited'] = True` after first-visit CAPTCHA
  - `session['captcha_passed'] = True` after data-page CAPTCHA
  - Both flags required for full access
  
- **Custom Base Template**: Zenith's `base.html`
  - Inline CSS and JavaScript
  - Sticky footer HTML + inline JS auto-dismiss logic
  - Not extending shared base

#### Dual Gate Logic:
```python
@require_captcha
def route():
    # Check 1: First visit?
    if 'visited' not in session:
        show CAPTCHA, return
    
    # Check 2: Data page AND captcha not passed?
    if is_data_page and 'captcha_passed' not in session:
        show CAPTCHA, return
    
    # Proceed with route
    return render_template(...)
```

#### Session Flow:
```python
# First request to ANY page:
# session['visited'] = False → show CAPTCHA → session['visited'] = True

# Request to data page:
# session['captcha_passed'] = False → show CAPTCHA → session['captcha_passed'] = True
```

---

## NEW 4 ADVANCED SITES

### 6. Fortis Banking Group (Port 5005)
**Primary Obstacles: CAPTCHA on Data Pages + Rate Limiting**

#### Specific Behaviors:
- **CAPTCHA on Data Pages Only**: `CAPTCHA_ON_EVERY_PAGE = False`
  - Protected routes: `/strategies`, `/investor-resources`, `/funds`, `/fund/<id>`
  - Home, about, leadership, contact, news: NO CAPTCHA
  - Allows unauthenticated browsing of basic pages
  - CAPTCHA required only for sensitive financial data
  
- **CAPTCHA Validation**:
  - 4-character random string image (PIL generated)
  - Noise lines and visual distortion
  - Case-insensitive answer validation
  - Stored in `session['captcha_answer']`
  - Session flag: `session['captcha_passed'] = True`
  
- **Route Protection**:
  - `@require_captcha` decorator on data pages
  - Checks: if on protected route AND captcha_passed not in session → show CAPTCHA
  - Helper function: `require_captcha_for_page(current_path)`
  - After CAPTCHA success: redirects to referrer or home
  
- **Rate Limiting**: 7 requests per 60 seconds
  - `@rate_limit(7, 60)` on all routes
  - Moderate restriction (between Apex 5/60s and Quantum 6/60s)
  - Returns 429 on breach
  
- **Clean Data Layout**: `DATA_LAYOUT = 'clean_tables'`
  - Static AUM data (no variance)
  - Consistent across requests
  - Unlike dynamic sites

#### CAPTCHA Detection Logic:
```python
def require_captcha_for_page(current_path):
    """Check if current path requires CAPTCHA."""
    if current_path in Config.CAPTCHA_REQUIRED_PAGES:
        return True
    for page in Config.CAPTCHA_REQUIRED_PAGES:
        if page.endswith('<id>'):
            base_path = page.replace('/<id>', '')
            if current_path.startswith(base_path):
                return True
    return False

@require_captcha
@app.route('/strategies')
def strategies():
    # CAPTCHA validated by decorator
    return render_template('strategies.html')
```

---

### 7. Nexus Capital (Port 5006)
**Primary Obstacles: Honeypot Detection + Bot Fingerprinting + Fragmented Data**

#### Specific Behaviors:
- **Honeypot Form Fields**: `HONEYPOT_ENABLED = True`
  - Generated per-session: `generate_honeypot_field_name()`
  - Unique field name stored in `session['honeypot_field']`
  - Field name example: `hf_a1b2c3d4e5f6`
  - Field displayed with misleading label "Website" (CSS display:none or opacity:0 in real impl)
  
- **Honeypot Detection Logic**:
  - Contact form `POST /contact`:
    - Validates form with `validate_form_submission(request.form, session)`
    - If honeypot field filled (not empty): `return 403 Invalid submission`
    - Indicates bot behavior (bots fill all fields)
    - Real users won't fill invisible field
  
- **Artificial Delay**: 0.2 seconds per request
  - `ARTIFICIAL_DELAY = 0.2`
  - Slight delay to slow automated scripts
  - Not as intrusive as Meridian's 1.0s
  
- **Rate Limiting**: 8 requests per 60 seconds
  - `@rate_limit(8, 60)` on all routes
  - Moderate restriction (between Apex and Quantum)
  
- **Bot Detection Configuration**:
  - `STRICT_BOT_DETECTION = True`
  - `HIDDEN_LINKS = True` (prepared for future use)
  - `SHADOW_DOM = True` (prepared for future use)
  - User-agent blocking: ALL scrapers blocked
  
- **Fragmented Data Layout**: `DATA_LAYOUT = 'fragmented'`
  - Data spread across multiple pages
  - Requires visiting pages in sequence
  - Dynamic AUM variance applied per request
  
- **Contact Form Honeypot**:
  - Form includes hidden honeypot field
  - Real submission validates honeypot is empty
  - Bot fills all fields → caught by validation

#### Honeypot Flow:
```python
@app.context_processor
def inject_globals():
    honeypot = inject_honeypot_fields(session) if Config.HONEYPOT_ENABLED else None
    # honeypot = {'field_name': 'hf_a1b2c3d4e5f6', 'display_name': 'Website'}
    return {'honeypot': honeypot}

# In template (contact.html):
{% if honeypot %}
    <input type="text" name="{{ honeypot.field_name }}" style="display:none;" />
{% endif %}

@app.route('/contact', methods=['POST'])
def contact():
    if not validate_form_submission(request.form, session):
        return jsonify({'error': 'Invalid submission'}), 403
    return jsonify({'status': 'ok'}), 200
```

#### Honeypot Detection:
```python
def validate_form_submission(form_data, session):
    honeypot_field = session.get('honeypot_field')
    if not honeypot_field:
        return True
    
    # If honeypot filled → bot
    if form_data.get(honeypot_field, '').strip() != '':
        return False
    
    return True
```

---

### 8. Quantum Funds (Port 5007)
**Primary Obstacles: Geographic Blocking + VPN Detection + IP-Based Rate Limiting**

#### Specific Behaviors:
- **Country Restrictions**: `GEO_BLOCKING = True`
  - Allowed countries: `['US', 'CA', 'UK']`
  - `@allow_countries(Config.ALLOWED_COUNTRIES)` on most routes
  - Other countries get 403: "This service is not available in {country}"
  
- **IP Geolocation**: Mock implementation
  - `get_country_from_ip(ip)` - Simple mock
  - Checks if IP starts with: `127.`, `192.168.`, `10.` → returns 'US'
  - Default: returns 'UNKNOWN'
  - Ready for MaxMind GeoIP2 integration
  - Client IP from: `request.remote_addr` or `X-Forwarded-For` header
  
- **VPN Detection**: `BLOCK_VPNS = True`
  - `@block_vpn` decorator on routes
  - Known VPN IPs: `8.8.8.8`, `1.1.1.1`, `208.67.222.222` (demo)
  - Detection: if IP in VPN_IPS → 403 "VPN/proxy access not allowed"
  - Mock implementation, ready for real VPN detection service
  
- **IP-Based Rate Limiting**:
  - General limit: 6 req/60s
  - Configurable per country in future
  - `@rate_limit(6, 60)` on routes
  
- **Geofenced Data**: `DATA_LAYOUT = 'geofenced'`
  - Some AUM data accessible only from allowed countries
  - Template includes `user_country` context variable
  - Conditional display: `{% if user_country in allowed_countries %}`
  
- **Geo Check Endpoint**: `/api/check-location`
  - GET request returns:
    ```json
    {
      "ip": "192.168.1.1",
      "country": "US",
      "vpn_detected": false
    }
    ```
  - Used for testing geolocation
  - No auth required (for testing purposes)
  
- **Route Protection**:
  - Home page: `@allow_countries(['US','CA','UK'])` + `@block_vpn`
  - Other routes: `@allow_countries(['US','CA','UK'])` only
  - Contact/News: country restricted

#### Country Gating:
```python
@allow_countries(Config.ALLOWED_COUNTRIES)
@block_vpn
@rate_limit(6, 60)
@app.route('/')
def home():
    return render_template('home.html')

# Behind the scenes:
def allow_countries(allowed):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            ip = get_client_ip(request)
            country = get_country_from_ip(ip)
            if country not in allowed:
                return jsonify({'error': 'Access denied', 'message': f'...in {country}'}), 403
            return f(*args, **kwargs)
        return decorated
    return decorator
```

#### IP Detection:
```python
def get_client_ip(request):
    # Check X-Forwarded-For (for proxies/load balancers)
    if request.headers.get('X-Forwarded-For'):
        return request.headers.get('X-Forwarded-For').split(',')[0].strip()
    return request.remote_addr

def is_vpn_ip(ip):
    return ip in VPN_IPS or ip.startswith('8.8.8.8') or ip.startswith('1.1.1.1')

def get_country_from_ip(ip):
    if ip.startswith(('127.', '192.168.', '10.')):
        return 'US'
    return 'UNKNOWN'
```

---

### 9. Cipher Wealth Management (Port 5008)
**Primary Obstacles: CAPTCHA on Every Page + Artificial Delay**

#### Specific Behaviors:
- **CAPTCHA on Every Page**: `CAPTCHA_ON_EVERY_PAGE = True`
  - All routes check for `session['captcha_passed']`
  - If missing, returns CAPTCHA page instead of content
  - Routes affected: `/`, `/about`, `/leadership`, `/strategies`, `/investor-resources`, `/funds`, `/fund/<id>`, `/news`, `/contact`
  - Stricter than Sentinel: 5-character CAPTCHAs (harder to OCR)
  
- **Image CAPTCHA with Distortion**: `CAPTCHA_TYPE = 'image_ocr'`
  - 5-character random string (vs. 4 in Sentinel)
  - Enhanced distortion and noise for OCR difficulty
  - Config: `CAPTCHA_DISTORTION = True`, `CAPTCHA_LENGTH = 5`
  - PIL generated image with heavy noise lines
  - Makes automated OCR bypass extremely difficult
  
- **Rate Limiting**: 6 requests per 60 seconds (strictest)
  - Strictest rate limit across all sites
  - `MAX_REQUESTS = 6`, `TIME_WINDOW = 60`
  - Returns 429 on breach
  - Defeats concurrent scraping attempts
  
- **Artificial Delay**: 0.1 seconds per request
  - `ARTIFICIAL_DELAY = 0.1`
  - Light delay applied before all requests
  - Slightly slows rapid scraper attacks
  - Config: `@app.before_request` applies sleep
  
- **Session Management**:
  - CAPTCHA answer cleared after validation
  - Session flag: `session['captcha_passed'] = True`
  - Persists across all page views
  - After success: redirects to referrer or home
  
- **Protected Data Layout**: `DATA_LAYOUT = 'protected_tables'`
  - All data locked behind CAPTCHA gate
  - No public pages without solving CAPTCHA
  - Every page view requires new challenge

#### CAPTCHA Every Page Logic:
```python
@require_captcha
def route():
    # CAPTCHA passed or not required, proceed
    return render_template('...')

@app.before_request
def apply_delay_and_check_captcha():
    """Apply delay and check CAPTCHA submission."""
    if Config.ARTIFICIAL_DELAY > 0:
        time.sleep(Config.ARTIFICIAL_DELAY)

    if request.method == 'POST' and 'captcha_answer' in request.form:
        user_answer = request.form.get('captcha_answer', '').strip()
        if validate_captcha(user_answer):
            session['captcha_passed'] = True
            return redirect(request.referrer or url_for('home'))
        return jsonify({'status': 'error'}), 403

@require_captcha
@app.route('/')
def home():
    return render_template('home.html')
```

#### OCR Difficulty:
- 5 characters (harder to guess)
- Enhanced distortion (hard for ML models)
- Noise lines throughout image
- Random colors and backgrounds
- Makes OCR services (Tesseract, AWS Textract, etc.) much less effective

---

### 10. Bastion Investment Group (Port 5009)
**Primary Obstacles: Dynamic DOM Obfuscation + Timed CAPTCHA**

#### Specific Behaviors:
- **DOM Obfuscation**: CSS classes randomized per session
  - `generate_class_map(session)` creates random 5-char strings for semantic class names
  - Class map stored in `session['class_map']`; regenerated on new session
  - All AUM-containing elements use `{{ class_map['aum-value'] }}` instead of hardcoded names
  - Scrapers using CSS selectors find different class names each session
  
- **Timed CAPTCHA**: 30s expiry on data pages
  - Applied on data pages: `/what-we-do`, `/investors`, `/financial-advisors`
  - `session['captcha_issued_at']` set when CAPTCHA generated
  - `validate_timed_captcha(answer)` checks elapsed > 30s → expired; wrong answer → invalid; correct → ok
  - Countdown timer in UI shows remaining time
  
- **Rate Limiting**: 10 requests per 60 seconds
  - `@rate_limit(10, 60)` on all routes
  - Moderate restriction (between Zenith's 3 and Apex's 5)
  
- **Cookie Banner**: Optional mode (non-blocking)
- **Global layers**: JS validation, cookie enforcement, UA blocking, strict headers, /aum blocked, robots.txt

#### Config snippet:
```python
COMPANY_NAME = 'Bastion Investment Group'
ROTATING_TOKENS = False
TIMED_CAPTCHA = True
CAPTCHA_TIME_LIMIT = 30
DOM_OBFUSCATION = True
MAX_REQUESTS = 10
COOKIE_BANNER_MODE = 'optional'
GLOBAL_AUM = '$55,000,000,000'
```

---

### 11. Landmark Property Advisors (Port 5010)
**Primary Obstacles: Rotating Session Tokens + Canvas/WebGL Fingerprint Blocking**

#### Specific Behaviors:
- **Rotating Session Tokens**: Expire after 5 page views
  - `issue_token(session)` sets `session['page_token']` (UUID) and `session['page_count'] = 0`
  - `@require_token(5)` decorator on ALL routes increments page_count
  - After 5 page views, token expires and redirects to `/refresh-token`
  - `/refresh-token` re-issues token and redirects back to referrer
  - Scrapers lose session state mid-crawl if they don't handle token refresh
  
- **Canvas/WebGL Fingerprint Blocking**: Detects headless browsers
  - On first visit, `base.html` includes hidden `<canvas>` + JavaScript fingerprint check
  - Hash POSTed to `/verify-fingerprint`
  - Known headless hashes (Puppeteer, Playwright defaults) return 403
  - Valid hashes stored in `session['fp_verified'] = True`
  - `require_fingerprint` decorator on all routes renders challenge if not verified
  
- **Rate Limiting**: 4 requests per 60 seconds (strictest)
  - `@rate_limit(4, 60)` on all routes
  - Defeats concurrent scraping attempts
  
- **Cookie Banner**: Mandatory mode (blocks content until accepted)
- **NO CAPTCHA** (key difference - uses fingerprint instead)
- **Global layers**: JS validation, cookie enforcement, UA blocking, strict headers, /aum blocked, robots.txt

#### Config snippet:
```python
COMPANY_NAME = 'Landmark Property Advisors'
ROTATING_TOKENS = True
TOKEN_PAGE_LIMIT = 5
FINGERPRINT_BLOCKING = True
MAX_REQUESTS = 4
COOKIE_BANNER_MODE = 'mandatory'
GLOBAL_AUM = '$47,000,000,000'
```

---

## GLOBAL FEATURES (All 11 Sites)

### 1. JavaScript Requirement
**Implemented**: `require_javascript` decorator + `inject_js_routes(app)`

**Behavior**:
- Every route decorated with `@require_javascript`
- First request to any page without JS validation:
  - Redirects to `/validate-js`
  - Generates token: `session['js_token']`
  - Renders `validate-js.html`
- JavaScript in page POSTs token to `/set-js-cookie`:
  - Server validates token matches session
  - Sets `session['js_validated'] = True`
  - Returns redirect URL
- Client redirects to original page
- Subsequent requests allowed

**Benefits**:
- Blocks headless browsers (curl, requests library, scrapy, selenium without JS)
- Proves real browser execution
- Can't bypass with simple HTTP requests

---

### 2. Cookie Enforcement
**Implemented**: `inject_cookie_middleware(app)`

**Behavior**:
- Middleware intercepts ALL requests
- Checks for `site_session_cookie`
- Missing cookie:
  - Returns 403 with redirect to `/set-cookie`
  - `/set-cookie` sets cookie with random value
  - Redirects to referrer or home
- Cookie persists for 24 hours
- HttpOnly flag set (can't access via JS in prod)

**Benefits**:
- Blocks requests from tools that don't handle cookies
- Requires stateful session management
- Defeats simple curl/wget requests

---

### 3. User-Agent Blocking
**Implemented**: `inject_user_agent_middleware(app)`

**Blocked Patterns** (case-insensitive):
- `requests`, `curl`, `wget`, `python`, `httpx`
- `scrapy`, `selenium`, `headless`, `phantom`
- `bot`, `crawler`, `spider`
- `java`, `c#`, `powershell`, `go-http-client`
- `ruby`, `perl`, `node`, `axios`, `fetch`
- Empty user agent

**Behavior**:
- Middleware checks on every request
- Match found: 403 "Access denied"
- Real browsers (Chrome, Firefox, Safari, Edge) pass through

**Benefits**:
- Stops most automated scripts
- Easy for real users to bypass (add user-agent header)
- Defeats bots that don't spoof user-agent

---

### 4. Strict Headers Validation
**Implemented**: `inject_headers_middleware(app)`

**Required Headers**:
- `User-Agent` - Browser identification
- `Accept` - MIME types accepted

**Behavior**:
- Middleware checks on every request
- Missing header: 403 "Invalid request headers"
- Allows requests to bypass routes: `/set-cookie`, `/validate-js`, `/set-js-cookie`

**Benefits**:
- Simple HTTP requests (curl, requests lib) often lack these
- Real browsers always send these headers
- Lightweight security check

---

### 5. /aum Route Blocked
**Implemented**: Route handler on all sites

**Behavior**:
```python
@app.route('/aum')
def aum_blocked():
    return jsonify({'error': 'Access denied'}), 403
```

**Response**: 403 Forbidden with JSON error message

**Benefits**:
- Direct AUM data access prevented
- Forces scrapers to go through site pages
- Can be combined with site-specific obstacles

---

### 6. robots.txt Misdirection
**Implemented**: Route handler on all sites

**Content** (example):
```
User-agent: *
Disallow: /
Disallow: /api
Disallow: /admin
Crawl-delay: 999999
Sitemap: /fake-sitemap.xml
```

**Variations by Site**:
- **Sentinel, Apex, Meridian, Premier, Zenith, Fortis**: Standard disallow all
- **Nexus, Quantum**: Very strict (Disallow: /)
- **Cipher**: API-specific (Disallow: /api, Disallow: /)

**Benefits**:
- Legitimate crawlers respect robots.txt
- Prevents indexing
- Fake sitemap points to non-existent data
- Crawl-delay of 999999 seconds discourages bots

---

## Summary Table: Behaviors by Site

| Behavior | Sentinel | Apex | Meridian | Premier | Zenith | Fortis | Nexus | Quantum | Cipher | Bastion | Landmark |
|----------|----------|------|----------|---------|--------|--------|-------|---------|--------|---------|----------|
| **CAPTCHA Strategies** |
| Every Page CAPTCHA | ✓ | - | - | - | - | - | - | - | ✓ | - | - |
| Data Pages CAPTCHA | - | ✓ | - | - | ✓ | ✓ | - | - | - | ✓ | - |
| Random CAPTCHA (30%) | - | - | ✓ | - | - | - | - | - | - | - | - |
| First-Visit + Data | - | - | - | - | ✓ | - | - | - | - | - | - |
| Timed CAPTCHA (30s) | - | - | - | - | - | - | - | - | - | ✓ | - |
| **Rate Limiting** |
| 3 req/60s | - | - | - | - | ✓ | - | - | - | - | - | - |
| 4 req/60s | - | - | - | - | - | - | - | - | - | - | ✓ |
| 5 req/60s | - | ✓ | - | - | - | - | - | - | - | - | - |
| 6 req/60s | - | - | - | - | - | - | - | ✓ | ✓ | - | - |
| 7 req/60s | - | - | - | - | - | ✓ | - | - | - | - | - |
| 8 req/60s | - | - | - | - | - | - | ✓ | - | - | - | - |
| 10 req/60s | - | - | - | - | - | - | - | - | - | ✓ | - |
| **Delays & Popups** |
| Artificial Delay | - | - | 1.0s | - | 0.5s | - | 0.2s | - | 0.1s | - | - |
| Dismissible Popup | - | ✓ | - | - | - | - | - | - | - | - | - |
| Modal Popup | - | - | ✓ | - | - | - | - | - | - | - | - |
| Sticky Auto-Dismiss | - | - | - | - | ✓ | - | - | - | - | - | - |
| **Auth & Detection** |
| Honeypot Forms | - | - | - | - | - | - | ✓ | - | - | - | - |
| DOM Obfuscation | - | - | - | - | - | - | - | - | - | ✓ | - |
| Rotating Tokens | - | - | - | - | - | - | - | - | - | - | ✓ |
| Canvas Fingerprint | - | - | - | - | - | - | - | - | - | - | ✓ |
| GeoIP Blocking | - | - | - | - | - | - | - | ✓ | - | - | - |
| VPN Detection | - | - | - | - | - | - | - | ✓ | - | - | - |
| **Data Presentation** |
| JSON Endpoint | - | ✓ | - | - | - | - | - | - | - | - | - |
| AJAX Loading | - | - | - | - | ✓ | - | - | - | - | - | - |
| Scattered Layout | - | - | ✓ | - | - | - | - | - | - | - | - |
| Fragmented Layout | - | - | - | - | - | - | ✓ | - | - | - | - |
| Geofenced Data | - | - | - | - | - | - | - | ✓ | - | - | - |
| Protected Tables | - | - | - | - | - | - | - | - | ✓ | - | - |
| **Cookie Banner** |
| Optional | - | - | - | - | - | - | - | - | - | ✓ | - |
| Mandatory | - | - | - | - | - | - | - | - | - | - | ✓ |
| **Global Features** |
| JS Validation | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Cookie Enforcement | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| UA Blocking | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Strict Headers | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| /aum Blocked | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| robots.txt | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |

---

## Attack Layers (Defense in Depth)

### Layer 1: Basic Request Filtering (All Sites)
1. User-Agent blocking - Rejects known scrapers
2. Strict headers validation - Requires browser headers
3. Cookie enforcement - Requires session cookie

**Bypass difficulty**: Easy (add headers, handle cookies)

### Layer 2: JavaScript Gate (All Sites)
1. Requires client-side JS execution
2. Token exchange proves execution
3. Blocks headless browsers

**Bypass difficulty**: Medium (need JS engine like Selenium/Playwright)

### Layer 3: Site-Specific Obstacles
1. **Sentinel**: CAPTCHA on every page
2. **Apex**: Rate limiting + selective CAPTCHA + popups
3. **Meridian**: Random CAPTCHA + delays
4. **Premier**: None (baseline)
5. **Zenith**: Multi-gate CAPTCHA + delays + AJAX
6. **Fortis**: CAPTCHA on data pages + rate limiting
7. **Nexus**: Honeypot detection
8. **Quantum**: GeoIP blocking + VPN detection
9. **Cipher**: CAPTCHA on every page + artificial delay
10. **Bastion**: DOM obfuscation + timed CAPTCHA + rate limiting
11. **Landmark**: Rotating tokens + canvas fingerprint blocking + strict rate limiting

**Bypass difficulty**: Hard to Very Hard (varies by site)

### Combined Defense

A scraper must:
1. ✓ Handle cookies properly
2. ✓ Send realistic headers (User-Agent, Accept)
3. ✓ Execute JavaScript (or obtain token)
4. ✓ Pass site-specific obstacles (CAPTCHA, auth, honeypot, etc.)
5. ✓ Handle rate limiting (backoff, rotation)

**Total bypass difficulty**: Hard to Extremely Hard (layered approach)

