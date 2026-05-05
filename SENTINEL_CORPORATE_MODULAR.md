# Sentinel Capital Partners - Corporate Modular Design

## Overview

Sentinel has been redesigned with a **Corporate Modular** aesthetic - inspired by institutional corporate design (Orchard Global reference). Professional, premium, and structured with gold accents for sophistication and trust.

## Design Philosophy

### Core Principles
1. **Modularity** - Self-contained card components that compose the layout
2. **Corporate** - Professional, trustworthy, institutional appearance
3. **Premium** - Gold accents and refined details signal quality
4. **Structure** - Clear hierarchy with consistent spacing and alignment
5. **Elegance** - Navy blue and gold color scheme conveys sophistication

## Color Scheme

```
Primary Color:     #0f2b4d (Deep Navy)
Secondary Color:   #1a3a5c (Navy Light)
Dark Color:        #0a1f35 (Navy Dark)
Accent Color:      #d4af37 (Gold)
Background:        #ffffff (White)
Light BG:          #f7f8fa (Light Gray)
Border Color:      #e8eaef (Light Border)
Text Dark:         #1a1a1a (Black)
Text Muted:        #666666 (Gray)
```

## Typography

- **Font Family**: System fonts (Segoe UI, -apple-system, BlinkMacSystemFont, Helvetica Neue)
- **Headings**: 700 weight, letter-spacing -0.8px for h2 (42px)
- **Body**: 14px, line-height 1.7
- **Navigation**: 13px, uppercase, letter-spacing 0.3px

## Key Design Elements

### Header
- Sticky navy background with subtle box shadow
- Logo with animated gold dot after text (using ::after)
- Nav links with smooth gold underline animation on hover
- Uppercase, letter-spaced navigation for professional tone

### Hero Section
- Navy gradient background (135deg blend)
- Large bold typography (54px h1)
- Company name watermark in background (opacity 0.05)
- AUM display as bordered card with gold border
- Centered layout with ample padding (120px)

### Content Sections
- Full-width sections with 100px padding
- Section headings (42px) with gold bottom bar
- Consistent borders between sections
- Organized data presentation with modular structure

### Modular Cards
- Grid layout (repeat auto-fit minmax 350px)
- Gold top border that scales on hover (scaleX transform)
- Subtle shadow that increases on hover
- Lift effect on hover (translateY -6px)
- 40px padding with responsive adjustment

### Data Tables
- Navy header background with white text
- Uppercase column headings
- Hover state: light gray background + left gold border
- 20px padding in header, 18px in body
- Last row has no bottom border

### Stat Boxes
- Light gray background by default
- Center-aligned statistics
- Gold number text (large, 48px)
- Hover effect: background changes to navy, text turns white
- Responsive grid (repeat auto-fit minmax 250px)

### Buttons
- Navy background with gold accent
- Sliding background reveal on hover (::before element)
- Uppercase, letter-spaced text
- Smooth transition effects
- No border radius (sharp edges for corporate feel)

### Footer
- Navy background matching header
- White text with proper opacity
- Gold accent for global AUM display
- Professional spacing and typography

### Dividers
- Light gray horizontal lines
- 80px margin top/bottom for section separation

## Responsive Design

### Breakpoints
- **Desktop**: 1220px container width (primary layout)
- **Tablet/Mobile**: 768px (adjusted spacing and typography)

### Features
- Flexible hero section padding (70px → 20px on mobile)
- Grid changes to single column on mobile
- Navigation gap reduces from 35px to 15px
- Hero background watermark scales down (300px → 120px font-size)

## Technical Implementation

### CSS Features
- CSS variables for theming (:root properties)
- CSS Grid for responsive layouts (auto-fit, minmax)
- Flexbox for navigation and centering
- Transform-based animations (scaleX, translateY)
- Cubic-bezier timing (0.4, 0, 0.2, 1) for smooth motion
- GPU-accelerated transforms (translate, scale)
- Box-shadow for depth effects

### Performance
- No external images required
- Pure CSS design
- Minimal animations (0.35s transitions)
- Optimized shadows and effects
- ~500 lines CSS

## Browser Support
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+
- Mobile browsers (iOS Safari, Chrome Mobile)

## Design Highlights

### 1. Premium Appearance
- Navy and gold color combination signals institutional wealth
- Gold accents throughout (borders, text, animations)
- Refined spacing and alignment
- Clean, uncluttered layout

### 2. Visual Hierarchy
- Large section headings (42px) with gold underlines
- Card-based modular layout for easy scanning
- Stat boxes draw attention with large numbers
- Data tables organized with navy header

### 3. Interactive Polish
- Smooth transitions on all interactive elements
- Card lift effect creates depth on hover
- Button background slide animation
- Nav link underline width transition

### 4. Professional Tone
- Navy and white color palette conveys trust
- Gold accents convey premium quality
- No rounded corners (sharp, institutional feel)
- Consistent uppercase typography in navigation

## Customization

### Easy CSS Variables
```css
:root {
    --navy: #0f2b4d;
    --navy-light: #1a3a5c;
    --navy-dark: #0a1f35;
    --accent-gold: #d4af37;
    --white: #ffffff;
    --gray-light: #f7f8fa;
    --gray-medium: #e8eaef;
    --text-dark: #1a1a1a;
    --text-muted: #666666;
}
```

## Comparison: Sentinel vs Apex vs Premier

| Aspect | Sentinel | Apex | Premier |
|--------|----------|------|---------|
| **Theme** | Corporate Modular | Glassmorphism | Modern Minimalist |
| **Colors** | Navy/Gold | Purple gradient | Blue/Gray/Black |
| **Background** | White with gradient hero | Gradient blur | Clean white |
| **Complexity** | Moderate (modular cards) | Moderate (blur effects) | Minimal (pure design) |
| **Tone** | Professional & institutional | Modern & playful | Clean & institutional |
| **Accents** | Gold throughout | Purple | Blue |
| **Card Style** | Modular with gold border | Glass with blur | Minimal with borders |

## Files

### New Files
- `/sentinel/static/css/corporate-modular.css` - Complete corporate modular stylesheet
- `/sentinel/templates/base.html` - Sentinel-specific base template

### Modified Files
- `/sentinel/templates/home.html` - Removed inline styles, uses corporate-modular CSS
- `/sentinel/templates/strategies.html` - Removed inline styles, uses corporate-modular CSS

## Testing Checklist

- [x] Templates render without errors
- [x] Corporate modular CSS loads correctly
- [x] Hero section displays properly with watermark
- [x] Gold accents visible throughout
- [x] Data tables styled with navy header
- [x] Navigation underline animation works
- [x] Responsive on mobile (max-width: 768px)
- [x] Buttons are interactive with background reveal
- [x] Cards have hover lift effect
- [x] Footer displays correctly
- [x] Professional appearance maintained
- [x] Institutional tone conveyed through colors

## Deployment Notes

The corporate-modular.css file requires:
- No external dependencies
- No font imports (system fonts only)
- Modern browser CSS support
- No JavaScript enhancements needed

The design is self-contained and production-ready.
