# apple-design — Platform Mapping

## 1. HTML / CSS / WEB

### Font Loading

Apple's SF Pro is a system font — it loads automatically on Apple devices via `-apple-system`. For all other platforms, load Inter as the fallback:

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://unpkg.com/@phosphor-icons/web@2/src/light/style.css">
```

### CSS Custom Properties — Light Mode (Primary)

```css
:root {
  /* Colors */
  --background: #FFFFFF;
  --bg: var(--background);
  --surface1: #F5F5F7;
  --surface2: #E8E8ED;
  --surface3: #D2D2D7;
  --border: #E8E8ED;
  --border-visible: #D2D2D7;
  --text1: #1D1D1F;
  --text2: #6E6E73;
  --text3: #8E8E93;
  --text4: #AEAEB2;
  --accent: #0071E3;
  --accent-subtle: #EBF3FF;
  --success: #30D158;
  --success-bg: #F0FDF5;
  --warning: #FF9F0A;
  --warning-bg: #FFF6EC;
  --error: #FF3B30;
  --error-bg: #FFF0EF;

  /* Fonts */
  --font-display: -apple-system, BlinkMacSystemFont, "SF Pro Display", "Inter", sans-serif;
  --font-body: -apple-system, BlinkMacSystemFont, "SF Pro Text", "Inter", sans-serif;
  --font-mono: "SF Mono", "JetBrains Mono", "Fira Code", monospace;

  /* Type Scale */
  --text-display: 80px;
  --text-heading: 48px;
  --text-subheading: 28px;
  --text-body: 17px;
  --text-body-sm: 14px;
  --text-caption: 12px;
  --text-label: 12px;

  /* Letter Spacing (apply per token) */
  --ls-display: -0.022em;
  --ls-heading: -0.015em;
  --ls-subheading: -0.010em;
  --ls-body: 0em;
  --ls-label: 0.010em;

  /* Spacing */
  --space-2xs: 2px;
  --space-xs: 4px;
  --space-sm: 8px;
  --space-md: 16px;
  --space-lg: 24px;
  --space-xl: 32px;
  --space-2xl: 48px;
  --space-3xl: 64px;
  --space-4xl: 96px;

  /* Radii */
  --radius-element: 8px;
  --radius-input: 12px;
  --radius-component: 18px;
  --radius-container: 20px;
  --radius-pill: 980px;
  /* Alias for buttons — always pill */
  --radius-buttons: 980px;
  --radius-cards: 18px;
  --radius-tags: 8px;
  --radius-modals: 20px;

  /* Motion */
  --ease-fast: cubic-bezier(0.25, 0.46, 0.45, 0.94);
  --ease-medium: cubic-bezier(0.25, 0.46, 0.45, 0.94);
  --ease-slow: cubic-bezier(0.28, 0.44, 0.49, 0.96);
  --duration-fast: 150ms;
  --duration-medium: 300ms;
  --duration-slow: 500ms;

  /* Shadows */
  --shadow-1: 0 2px 8px rgba(0,0,0,0.05), 0 1px 2px rgba(0,0,0,0.06);
  --shadow-2: 0 8px 30px rgba(0,0,0,0.08), 0 2px 8px rgba(0,0,0,0.05);
  --shadow-3: 0 20px 60px rgba(0,0,0,0.12), 0 8px 24px rgba(0,0,0,0.08);

  /* Glass (Liquid Glass — navigation and overlays only) */
  --glass-bg-light: rgba(255,255,255,0.72);
  --glass-bg-dark: rgba(0,0,0,0.72);
  --glass-filter: blur(20px) saturate(180%);
}
```

### CSS Custom Properties — Dark Mode

```css
[data-theme="dark"] {
  --background: #000000;
  --bg: var(--background);
  --surface1: #1D1D1F;
  --surface2: #3A3A3C;
  --surface3: #48484A;
  --border: #3A3A3C;
  --border-visible: #48484A;
  --text1: #F5F5F7;
  --text2: #8E8E93;
  --text3: #6E6E73;
  --text4: #48484A;
  --accent: #2997FF;
  --accent-subtle: #001335;
  --success-bg: #082B14;
  --warning-bg: #2B1800;
  --error-bg: #2B0806;
  --shadow-1: 0 2px 8px rgba(0,0,0,0.30), 0 1px 2px rgba(0,0,0,0.40);
  --shadow-2: 0 8px 30px rgba(0,0,0,0.50), 0 2px 8px rgba(0,0,0,0.40);
  --shadow-3: 0 20px 60px rgba(0,0,0,0.70), 0 8px 24px rgba(0,0,0,0.50);
}
```

### System Preference Auto-Dark

```css
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    /* Same overrides as [data-theme="dark"] above */
    --background: #000000;
    --surface1: #1D1D1F;
    /* ... */
  }
}
```

### Utility Classes

```css
/* Typography */
.display { font-family: var(--font-display); font-size: var(--text-display); font-weight: 600; line-height: 1.05; letter-spacing: -0.022em; }
.heading  { font-family: var(--font-display); font-size: var(--text-heading);  font-weight: 600; line-height: 1.08; letter-spacing: -0.015em; }
.subheading { font-family: var(--font-display); font-size: var(--text-subheading); font-weight: 600; line-height: 1.15; letter-spacing: -0.010em; }
.body     { font-family: var(--font-body); font-size: var(--text-body);     font-weight: 400; line-height: 1.52; }
.body-sm  { font-family: var(--font-body); font-size: var(--text-body-sm);  font-weight: 400; line-height: 1.50; }
.caption  { font-family: var(--font-body); font-size: var(--text-caption);  font-weight: 400; line-height: 1.40; letter-spacing: 0.005em; }
.label    { font-family: var(--font-body); font-size: var(--text-label);    font-weight: 500; line-height: 1.30; letter-spacing: 0.010em; }

/* Buttons */
.btn {
  display: inline-flex; align-items: center; justify-content: center;
  padding: 14px 24px; border-radius: var(--radius-pill); border: none;
  font-family: var(--font-body); font-size: 17px; font-weight: 400;
  cursor: pointer; text-decoration: none;
  transition: opacity var(--duration-fast) var(--ease-fast),
              transform var(--duration-fast) var(--ease-fast);
}
.btn:hover  { opacity: 0.85; }
.btn:active { transform: scale(0.97); }
.btn:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }

.btn-primary { background: var(--text1); color: var(--background); }
.btn-blue    { background: var(--accent); color: #FFFFFF; }
.btn-outline { background: transparent; color: #FFFFFF; border: 1px solid rgba(255,255,255,0.6); }
.btn-sm      { padding: 9px 18px; font-size: 15px; }

/* Text link CTA */
.link-cta {
  color: var(--accent); text-decoration: none;
  font-size: 17px; font-weight: 400;
  transition: opacity var(--duration-fast) var(--ease-fast);
}
.link-cta:hover { text-decoration: underline; opacity: 0.85; }

/* Cards */
.card {
  background: var(--surface1);
  border-radius: var(--radius-component);
  padding: var(--space-2xl);
}
.card-feature {
  background: var(--background);
  border-radius: var(--radius-component);
  padding: var(--space-xl);
  box-shadow: var(--shadow-1);
}

/* Glass nav */
.glass-nav {
  background: var(--glass-bg-light);
  backdrop-filter: var(--glass-filter);
  -webkit-backdrop-filter: var(--glass-filter);
  border-bottom: 1px solid rgba(0,0,0,0.08);
}
[data-theme="dark"] .glass-nav {
  background: var(--glass-bg-dark);
  border-bottom: 1px solid rgba(255,255,255,0.08);
}
```

---

## 2. SWIFTUI

```swift
import SwiftUI

// MARK: — Color System
extension Color {
  // Backgrounds
  static let appBackground = Color(.systemBackground)
  static let appSurface1   = Color(.secondarySystemBackground)
  static let appSurface2   = Color(.tertiarySystemBackground)

  // Text
  static let text1 = Color(.label)
  static let text2 = Color(.secondaryLabel)
  static let text3 = Color(.tertiaryLabel)
  static let text4 = Color(.quaternaryLabel)

  // Accent
  static let appAccent = Color(.systemBlue)          // #0071E3 light / #2997FF dark
  static let appAccentSubtle = Color(.systemBlue).opacity(0.1)

  // Status
  static let appSuccess = Color(.systemGreen)         // #30D158
  static let appWarning = Color(.systemOrange)        // #FF9F0A
  static let appError   = Color(.systemRed)           // #FF3B30
}

// MARK: — Typography
extension Font {
  static let appDisplay    = Font.system(size: 80, weight: .semibold, design: .default)
  static let appHeading    = Font.system(size: 48, weight: .semibold, design: .default)
  static let appSubheading = Font.system(size: 28, weight: .semibold, design: .default)
  static let appBody       = Font.system(size: 17, weight: .regular, design: .default)
  static let appBodySm     = Font.system(size: 14, weight: .regular, design: .default)
  static let appCaption    = Font.system(size: 12, weight: .regular, design: .default)
  static let appLabel      = Font.system(size: 12, weight: .medium, design: .default)
}

// MARK: — Spacing
extension CGFloat {
  static let space2xs: CGFloat = 2
  static let spaceXS:  CGFloat = 4
  static let spaceSM:  CGFloat = 8
  static let spaceMD:  CGFloat = 16
  static let spaceLG:  CGFloat = 24
  static let spaceXL:  CGFloat = 32
  static let space2XL: CGFloat = 48
  static let space3XL: CGFloat = 64
  static let space4XL: CGFloat = 96
}

// MARK: — Radius
extension CGFloat {
  static let radiusElement:   CGFloat = 8
  static let radiusInput:     CGFloat = 12
  static let radiusComponent: CGFloat = 18
  static let radiusContainer: CGFloat = 20
}

// MARK: — Button Style
struct ApplePillButtonStyle: ButtonStyle {
  var variant: Variant = .primary
  enum Variant { case primary, blue, outline }

  func makeBody(configuration: Configuration) -> some View {
    configuration.label
      .font(.system(size: 17, weight: .regular))
      .padding(.horizontal, 24)
      .padding(.vertical, 14)
      .background(bgColor(configuration.isPressed))
      .foregroundColor(fgColor)
      .clipShape(Capsule())
      .opacity(configuration.isPressed ? 0.85 : 1.0)
      .scaleEffect(configuration.isPressed ? 0.97 : 1.0)
      .animation(.easeOut(duration: 0.15), value: configuration.isPressed)
  }

  private func bgColor(_ pressed: Bool) -> Color {
    switch variant {
    case .primary: return .primary
    case .blue:    return .appAccent
    case .outline: return .clear
    }
  }
  private var fgColor: Color {
    switch variant {
    case .primary: return Color(.systemBackground)
    case .blue:    return .white
    case .outline: return .white
    }
  }
}

// MARK: — Card Modifier
struct AppleCardStyle: ViewModifier {
  func body(content: Content) -> some View {
    content
      .background(Color(.secondarySystemBackground))
      .clipShape(RoundedRectangle(cornerRadius: .radiusComponent, style: .continuous))
  }
}

extension View {
  func appleCard() -> some View { modifier(AppleCardStyle()) }
}
```

---

## 3. TAILWIND CONFIG

```javascript
// tailwind.config.js
module.exports = {
  darkMode: ['selector', '[data-theme="dark"]'],
  theme: {
    extend: {
      colors: {
        background: 'var(--background)',
        surface1:   'var(--surface1)',
        surface2:   'var(--surface2)',
        surface3:   'var(--surface3)',
        border:     'var(--border)',
        'border-visible': 'var(--border-visible)',
        text1: 'var(--text1)',
        text2: 'var(--text2)',
        text3: 'var(--text3)',
        text4: 'var(--text4)',
        accent: 'var(--accent)',
        'accent-subtle': 'var(--accent-subtle)',
        success: 'var(--success)',
        warning: 'var(--warning)',
        error:   'var(--error)',
        // Apple system grays
        'neutral-50':  '#FFFFFF',
        'neutral-100': '#F5F5F7',
        'neutral-200': '#E8E8ED',
        'neutral-300': '#D2D2D7',
        'neutral-400': '#AEAEB2',
        'neutral-500': '#8E8E93',
        'neutral-600': '#6E6E73',
        'neutral-700': '#48484A',
        'neutral-800': '#3A3A3C',
        'neutral-900': '#1D1D1F',
        'neutral-950': '#000000',
        // Apple Blue
        'brand-400': '#2997FF',
        'brand-500': '#0071E3',
        'brand-600': '#0064CA',
      },
      fontFamily: {
        display: ['-apple-system', 'BlinkMacSystemFont', '"SF Pro Display"', '"Inter"', 'sans-serif'],
        body:    ['-apple-system', 'BlinkMacSystemFont', '"SF Pro Text"', '"Inter"', 'sans-serif'],
        mono:    ['"SF Mono"', '"JetBrains Mono"', '"Fira Code"', 'monospace'],
      },
      fontSize: {
        display:    ['80px', { lineHeight: '1.05', letterSpacing: '-0.022em', fontWeight: '600' }],
        heading:    ['48px', { lineHeight: '1.08', letterSpacing: '-0.015em', fontWeight: '600' }],
        subheading: ['28px', { lineHeight: '1.15', letterSpacing: '-0.010em', fontWeight: '600' }],
        body:       ['17px', { lineHeight: '1.52' }],
        'body-sm':  ['14px', { lineHeight: '1.50' }],
        caption:    ['12px', { lineHeight: '1.40', letterSpacing: '0.005em' }],
        label:      ['12px', { lineHeight: '1.30', letterSpacing: '0.010em', fontWeight: '500' }],
      },
      spacing: {
        '2xs': '2px',
        xs:    '4px',
        sm:    '8px',
        md:    '16px',
        lg:    '24px',
        xl:    '32px',
        '2xl': '48px',
        '3xl': '64px',
        '4xl': '96px',
      },
      borderRadius: {
        element:   '8px',
        input:     '12px',
        component: '18px',
        container: '20px',
        pill:      '980px',
      },
      boxShadow: {
        1: '0 2px 8px rgba(0,0,0,0.05), 0 1px 2px rgba(0,0,0,0.06)',
        2: '0 8px 30px rgba(0,0,0,0.08), 0 2px 8px rgba(0,0,0,0.05)',
        3: '0 20px 60px rgba(0,0,0,0.12), 0 8px 24px rgba(0,0,0,0.08)',
      },
      transitionTimingFunction: {
        'apple-fast':   'cubic-bezier(0.25, 0.46, 0.45, 0.94)',
        'apple-slow':   'cubic-bezier(0.28, 0.44, 0.49, 0.96)',
      },
      transitionDuration: {
        fast:   '150ms',
        medium: '300ms',
        slow:   '500ms',
      },
    },
  },
}
```
