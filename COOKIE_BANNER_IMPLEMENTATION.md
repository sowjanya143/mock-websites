# Cookie Banner Implementation

## Overview

A three-tier cookie consent management system has been implemented across the mock financial websites with varying enforcement levels to simulate different GDPR compliance approaches.

## Architecture

### Core Components

1. **`utils/cookie_banner.py`** - Cookie banner management utility
   - `require_cookie_acceptance(mode)` - Decorator (minimal implementation, relies on context processor)
   - `inject_cookie_banner_routes(app, mode)` - Injects `/accept-cookies`, `/reject-cookies`, `/dismiss-banner` endpoints
   - `is_cookie_accepted(session)` - Checks if user accepted cookies
   - `is_banner_dismissed(session)` - Checks if user dismissed banner (optional mode)
   - Context processor injects template variables: `cookie_accepted`, `cookie_dismissed`, `banner_mode`, `banner_shown`

2. **`shared/templates/cookie_banner.html`** - Reusable banner template
   - Conditionally displays based on: `banner_shown and not cookie_accepted and not cookie_dismissed`
   - Two UI modes: **mandatory** (Accept/Reject buttons, dark overlay) vs **optional** (Accept/Dismiss buttons, light overlay)
   - Embedded CSS and JavaScript for styling and interaction
   - CSS-based page blocking in mandatory mode (opacity, pointer-events, z-index)
   - Overlay has z-index 9998, banner has z-index 9999

3. **Integration in `base.html`**
   - Cookie banner included at bottom of page via `{% include 'cookie_banner.html' %}`
   - Displays for all pages automatically when conditions are met

### Cookies Set

When `/accept-cookies` is called:
- `site_session_cookie` (24-hour, HttpOnly) - Session tracking
- `cookie_consent` (1-year) - Consent preference tracking

When `/reject-cookies` is called:
- `cookie_consent` (1-year, value='rejected') - Tracks rejection

When `/dismiss-banner` is called (optional mode):
- `site_session_cookie` (24-hour, HttpOnly) - Session tracking

## Site Configuration

### Mandatory Mode (Data Blocked Until Acceptance)
- **Sentinel Capital Partners** (Port 5000)
- **Apex Investment Group** (Port 5001)

**Behavior:**
- Banner displays on all page loads until cookies accepted
- Page content faded/disabled (opacity 0.5, pointer-events none)
- Only "Accept & Continue" and "Reject" buttons available
- Dark overlay (rgba(0,0,0,0.5)) behind banner
- Page reloads after acceptance to fully enable content
- Rejection hides banner but keeps page blocked until Accept is clicked

### Optional Mode (Data Visible, Banner Dismissible)
- **Meridian Global Holdings** (Port 5002)
- **Premier Financial Services** (Port 5003)
- **Zenith Asset Management** (Port 5004)

**Behavior:**
- Banner displays at bottom of page on initial visit
- Page content fully accessible and interactive
- "Accept" and "Dismiss" buttons available
- Light overlay (rgba(0,0,0,0.3)) behind banner
- Dismissing banner hides it but doesn't set acceptance flag
- Accepting sets flag and reloads page
- Banner won't reappear if either acceptance or dismissal flag is set

### No Banner (CAPTCHA-Based Alternative)
- **Fortis Banking Group** (Port 5005)
- **Nexus Capital** (Port 5006)
- **Quantum Funds** (Port 5007)
- **Cipher Wealth Management** (Port 5008)

**Behavior:**
- No cookie banner; uses CAPTCHA obstacles instead
- Traditional set-cookie middleware (no explicit consent UI)
- Anti-scraping focus via CAPTCHA, rate limiting, bot detection

## Flow Diagrams

### Mandatory Mode Flow
```
User visits page
  ↓
Banner shows (page content faded)
  ├→ User clicks "Accept & Continue"
  │   ↓
  │   POST /accept-cookies
  │   ↓
  │   session['cookie_accepted'] = True
  │   ↓
  │   Page reloads
  │   ↓
  │   Banner hidden, content fully visible
  │
  └→ User clicks "Reject"
      ↓
      POST /reject-cookies
      ↓
      Banner hidden, page remains blocked
      ↓
      User must eventually click "Accept" to proceed
```

### Optional Mode Flow
```
User visits page
  ↓
Page loads normally with banner at bottom
  ├→ User clicks "Accept"
  │   ↓
  │   POST /accept-cookies
  │   ↓
  │   session['cookie_accepted'] = True
  │   ↓
  │   Page reloads
  │   ↓
  │   Banner hidden
  │
  └→ User clicks "Dismiss"
      ↓
      POST /dismiss-banner
      ↓
      session['cookie_dismissed'] = True
      ↓
      Banner hidden, page remains accessible
      ↓
      Banner won't reappear (dismissed flag persists)
```

## Session State Variables

- **`session['cookie_accepted']`** - Boolean, True if user clicked Accept
- **`session['cookie_dismissed']`** - Boolean, True if user dismissed banner (optional mode)
- **`session['cookie_rejected']`** - Boolean, True if user clicked Reject (mandatory mode)
- **`session['banner_token']`** - String, unique token for tracking sessions

## CSS Classes and Attributes

### Data Attributes on Body
- `data-cookie-mode` - Set to 'mandatory' or 'optional' by JavaScript
- `data-cookie-accepted` - Set to 'true' or 'false' by JavaScript

### CSS Selectors for Blocking
```css
/* Disable interaction in mandatory mode */
body[data-cookie-mode="mandatory"]:not([data-cookie-accepted="true"]) main,
body[data-cookie-mode="mandatory"]:not([data-cookie-accepted="true"]) nav,
body[data-cookie-mode="mandatory"]:not([data-cookie-accepted="true"]) .main-content {
    pointer-events: none;
    opacity: 0.5;
}
```

## JavaScript Functions

### `acceptCookies()`
- POSTs to `/accept-cookies`
- Sets `data-cookie-accepted="true"` on body
- Reloads page for mandatory mode to fully enable content

### `rejectCookies()`
- POSTs to `/reject-cookies`
- Hides banner (in mandatory mode, page stays blocked)
- Sets `data-cookie-accepted="false"` on body

### `dismissBanner()`
- POSTs to `/dismiss-banner`
- Sets `data-cookie-accepted="true"` on body (allows interaction in optional mode)
- Hides banner

## Testing Checklist

### Mandatory Mode (Sentinel, Apex)
- [ ] Page loads with banner displayed
- [ ] Page content is faded/disabled
- [ ] "Accept & Continue" button works and reloads page
- [ ] "Reject" button hides banner but keeps page blocked
- [ ] After accepting, banner doesn't reappear on subsequent visits
- [ ] After rejecting, banner still appears on refresh until Accept is clicked
- [ ] Cookies are set correctly (`site_session_cookie`, `cookie_consent`)

### Optional Mode (Meridian, Premier, Zenith)
- [ ] Page loads normally with banner at bottom
- [ ] Page content is fully interactive
- [ ] "Accept" button works and reloads page
- [ ] "Dismiss" button hides banner without reloading
- [ ] After accepting or dismissing, banner doesn't reappear
- [ ] Cookies are set correctly when accepting
- [ ] Session cookies are set when dismissing

### No Banner Sites (Fortis, Nexus, Quantum, Cipher)
- [ ] No cookie banner appears
- [ ] CAPTCHA or other obstacles appear as configured
- [ ] Sites remain fully functional

## Browser Compatibility

- Modern browsers (Chrome, Firefox, Safari, Edge) with ES6 support
- CSS Grid and Flexbox required for layout
- Fetch API required for banner interactions
- LocalStorage not used (relies on sessions)

## Future Enhancements

1. LocalStorage fallback for session persistence across tabs
2. Analytics integration to track banner interaction rates
3. Geolocation-based banner mode selection (mandatory for EU, optional for US)
4. Multi-language banner text
5. Custom banner styling per site
6. A/B testing different button text and layouts
