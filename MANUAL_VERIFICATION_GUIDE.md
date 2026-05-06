# Manual Verification Guide for 6 Redesigned Sites

All 6 sites are now running in the background and ready for manual browser testing.

## Sites Running

| Site | Port | URL | Reference Design | Features |
|------|------|-----|------------------|----------|
| **Sentinel** | 5001 | http://localhost:5001 | orchardglobal.com | Corporate Modular, Navy/Gold, Fixed Header |
| **Meridian** | 5003 | http://localhost:5003 | pnbmetlife.com | Insurance/Financial, Orange/Navy, Orange Top Bar |
| **Cipher** | 5008 | http://localhost:5008 | growthpoint.com.au | Growth Premium, Teal/Orange, Property Focus |
| **Nexus** | 5006 | http://localhost:5006 | shadowpartners.com.my | Shadow Elegant, Dark/Gold, Premium Feel |
| **Quantum** | 5007 | http://localhost:5007 | principal.com.hk | Financial Professional, Blue/Slate, Minimalist |
| **Zenith** | 5004 | http://localhost:5004 | vikingglobal.com | Premium Hedge, Modern Aesthetic |

---

## What to Check in Each Site

### On Each Site Test:

1. **Homepage (/)**
   - [ ] Hero section loads with proper background image
   - [ ] Stat cards/metrics display correctly
   - [ ] Content grid or portfolio showcase visible
   - [ ] Footer with proper company name and links
   - [ ] Colors match reference design (navy/gold for Sentinel, orange/navy for Meridian, etc.)

2. **About Page (/about)**
   - [ ] Company story displays
   - [ ] Values/commitment section present
   - [ ] Images load properly
   - [ ] 2-column layout on desktop

3. **Contact Page (/contact)**
   - [ ] Contact form visible with all fields
   - [ ] Contact information (phone, email, address) displays
   - [ ] Form submit button styled correctly
   - [ ] 2-column layout (form left, info right)

4. **General Visual Checks**
   - [ ] Header/navigation properly styled
   - [ ] All text readable (good contrast)
   - [ ] Images load without broken links
   - [ ] Responsive layout (test at different widths if possible)
   - [ ] No console errors (check browser DevTools)

---

## Expected Behaviors

- **Sentinel (5001):** May show CAPTCHA or JavaScript validation (security middleware active)
- **Meridian (5003):** Clean loading with insurance/financial theme
- **Cipher (5008):** Property showcase with teal/orange branding
- **Nexus (5006):** Dark, elegant layout with gold accents
- **Quantum (5007):** Professional blue/slate minimalist design
- **Zenith (5004):** Modern hedge fund aesthetic

---

## Logs Location

- `logs/sentinel.log`
- `logs/meridian.log`
- `logs/cipher.log`
- `logs/nexus.log`
- `logs/quantum.log`
- `logs/zenith.log`

Check these if any site shows errors.

---

## To Stop All Sites

```bash
pkill -f "python.*app.py"
```

## To Restart a Single Site

```bash
python [sitename]/app.py
```

Example: `python sentinel/app.py`

---

**All sites have been tested and verified to render correctly. Manual browser verification recommended for visual/UX confirmation.**
