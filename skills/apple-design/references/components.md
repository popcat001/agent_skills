# apple-design — Components

## 1. BUTTONS

### Variants

| Variant | Background | Text | Border | Radius | Height |
|---------|-----------|------|--------|--------|--------|
| Primary (dark) | `#000000` / `--text1` on dark sections | `#FFFFFF` | None | 980px | 48px |
| Primary (blue) | `#0071E3` / `--accent` | `#FFFFFF` | None | 980px | 48px |
| Ghost (outline) | Transparent | `#FFFFFF` | `1px solid rgba(255,255,255,0.6)` | 980px | 48px |
| Text link | Transparent | `--accent` | None | 0 | auto |

### Specs

| Property | Value |
|----------|-------|
| Height (large) | 48px |
| Height (small) | 36px |
| Padding (large) | 14px 24px |
| Padding (small) | 9px 18px |
| Font | `-apple-system, "SF Pro Text", Inter` weight 400, 17px |
| Font (small) | 15px |
| Min touch target | 44px |

### States

| State | Change |
|-------|--------|
| **Hover** | Opacity 0.85, transition 150ms ease-out |
| **Active / Pressed** | `transform: scale(0.97)`, 100ms |
| **Disabled** | Opacity 0.4, cursor not-allowed |
| **Focus** | `outline: 2px solid var(--accent); outline-offset: 2px` |

**Text link ("Learn more →"):** The arrow is Unicode `→` (U+2192), same font, same size. It does not have spacing from the text — it sits tight. On hover: underline.

---

## 2. CARDS / SURFACES

### Product Card
- Background: varies per section (`--background`, `--surface1`, or brand color)
- Border: none
- Radius: 18px (`--radius-component`)
- Padding: 48px
- Shadow: none (depth via section bg difference)

### Feature Card
- Background: `--surface1` (#F5F5F7 light / #1D1D1F dark)
- Border: none
- Radius: 18px
- Padding: 32px
- Shadow: `0 2px 8px rgba(0,0,0,0.05)` — only when card is white-on-white

### Specification Card (comparison table)
- Background: `--surface1`
- Border: `1px solid var(--border)`
- Radius: 18px
- Padding: 32px
- Shadow: none

### Content Layout
- Headline: `--subheading` (28px), `--text1`, weight 600, -0.010em tracking
- Description: `--body` (17px), `--text2`, weight 400
- CTA: `--body` (17px), `--accent`, "Learn more →"
- Internal spacing: `--space-md` (16px) between headline and body, `--space-lg` (24px) before CTA

---

## 3. INPUTS

### Text Field

| Property | Value |
|----------|-------|
| Height | 44px |
| Background | `--surface2` (#E8E8ED) |
| Border (default) | `1px solid var(--border-visible)` |
| Border (focus) | `2px solid var(--accent)` |
| Border (error) | `1px solid var(--error)` |
| Radius | 12px (`--radius-input`) |
| Padding | 10px 14px |
| Font | 17px, weight 400 |
| Placeholder color | `--text3` |

### Search Bar
- Background: `rgba(142,142,147,0.12)` (Apple's system fill)
- Border: none
- Radius: 10px
- Left icon: magnifying glass, `--text3`
- Height: 36px

### Label
- Position: above field, 8px gap
- Font: 14px, weight 400, `--text2`

### States

| State | Treatment |
|-------|-----------|
| **Default** | `--border-visible` border |
| **Focus** | `2px solid var(--accent)`, no shadow ring |
| **Error** | `1px solid var(--error)`. Error text below in `--error`, 12px |
| **Disabled** | Opacity 0.4, no interaction |

---

## 4. LISTS / DATA ROWS

### Standard Row

| Property | Value |
|----------|-------|
| Min height | 44px |
| Padding | 12px 16px |
| Divider | `1px solid var(--border)` bottom, inset-left 16px |
| Label font | 17px, weight 400, `--text1` |
| Value font | 17px, weight 400, `--text2` |
| Accessory | Chevron right in `--text3`, 12px |

### Interaction States

| State | Treatment |
|-------|-----------|
| **Default** | Transparent background |
| **Pressed** | `--surface1` background, instant |
| **Selected** | `--accent-subtle` background, `--accent` indicator |

### Specification Row (feature comparison)
- Left: feature name, `--text2`, 15px
- Right: value, `--text1`, 15px, weight 400
- Checkmark: `--success` for included, `--text4` for excluded
- Divider: `1px solid var(--border)`

---

## 5. NAVIGATION / TAB BAR

### Global Nav (apple.com header)

| Property | Value |
|----------|-------|
| Height | 44px |
| Background | `rgba(255,255,255,0.72)` light / `rgba(0,0,0,0.72)` dark |
| Backdrop filter | `blur(20px) saturate(180%)` |
| Border bottom | `1px solid rgba(0,0,0,0.08)` light / `rgba(255,255,255,0.08)` dark |
| Font | 12px, weight 400, `--text1` |
| Item spacing | 24px between nav items |
| Active item | `--text1`, no underline |
| Position | `position: sticky; top: 0; z-index: 100` |

### Tab States

| State | Treatment |
|-------|-----------|
| **Active** | `--text1`, weight 400 |
| **Inactive** | `--text2`, weight 400 |
| **Hover** | `--text1`, opacity transition 150ms |

---

## 6. TAGS / CHIPS

| Property | Value |
|----------|-------|
| Height | 28px |
| Padding | 5px 12px |
| Radius | 8px (`--radius-element`) |
| Font | 12px, weight 500 |
| Background | `--surface2` |
| Text color | `--text2` |
| Border | None |

### Selected State
- Background: `--accent-subtle`
- Text: `--accent`
- Border: none

### Availability Tags (product pages)
- "Available" → `--success-bg` bg, `--success` text
- "Coming soon" → `--warning-bg` bg, `--warning` text
- "Out of stock" → `--error-bg` bg, `--error` text

---

## 7. OVERLAYS

### Modal / Dialog

| Property | Value |
|----------|-------|
| Background | `--background` |
| Radius | 20px (`--radius-container`) |
| Shadow | `0 20px 60px rgba(0,0,0,0.12), 0 8px 24px rgba(0,0,0,0.08)` |
| Backdrop | `rgba(0,0,0,0.4)`, backdrop-filter `blur(8px)` |
| Max width | 560px |
| Padding | 32px |
| Close button | ✕ glyph, top-right, 20px, `--text3`, no border |

### Dropdown / Popover

| Property | Value |
|----------|-------|
| Background | `rgba(255,255,255,0.90)` with `backdrop-filter: blur(20px)` |
| Radius | 12px |
| Shadow | `0 8px 30px rgba(0,0,0,0.08)` |
| Border | `1px solid rgba(0,0,0,0.08)` |
| Item height | 36px |
| Item padding | 8px 14px |
| Selected indicator | `--accent-subtle` background, `--accent` text |

---

## 8. STATE PATTERNS

### Empty State
- Layout: centered, 96px+ top padding
- No icon (avoid decorative elements — Apple's marketing pages use space, not icons, as the empty signal)
- Headline: 28px, weight 600, `--text2`
- Description: 17px, `--text3`, 2 lines max
- CTA: text-link "Learn more →" or filled pill button, 24px below description

### Loading
- Inline: activity spinner, 20px, `--text3` color, 2px stroke, SVG arc
- Full screen: fade-in of content (opacity 0→1 over 300ms), no skeleton

### Error
- Inline (field): `--error` text, 12px, below the field, 4px gap
- Screen-level: 48px emoji or status icon in `--error`, followed by 28px heading, 17px description, CTA

### Disabled
- Opacity 0.4, no interaction, layout preserved
- No hover/focus states

---

## 9. TOGGLE / SWITCH

### Specs

| Property | Value |
|----------|-------|
| Track width | 51px |
| Track height | 31px |
| Track radius | 980px (pill) |
| Thumb size | 27px |
| Thumb radius | 50% |
| Thumb offset (from edge) | 2px |
| Label position | Right of toggle |
| Label gap | 10px |
| Label font | 17px, weight 400, `--text1` |

### States

| State | Track Background | Thumb |
|-------|-----------------|-------|
| **Off** | `--surface3` (`#D2D2D7`) | `#FFFFFF`, subtle shadow |
| **On** | `--success` (`#30D158`) | `#FFFFFF`, subtle shadow |
| **Hover** | Slight opacity shift | — |
| **Disabled** | Opacity 0.4 | — |
| **Focus** | `outline: 2px solid var(--accent); outline-offset: 2px` | — |

---

## 10. PROGRESS BAR

### Specs

| Property | Value |
|----------|-------|
| Height | 4px |
| Track radius | 980px |
| Track background | `--surface2` |
| Fill color | `--accent` (default), semantic variants available |
| Fill radius | 980px |
| Label position | Above, `--caption`, `--text2` |

### Circular Progress (Activity Ring)
- SVG ring, `stroke-linecap: round`
- Track: `--surface2`
- Fill: semantic color (`--success` for activity, `--accent` for general)
- Stroke width: 8px for large (80px ring), 4px for small (40px)

### Semantic Fill Colors

| Variant | Fill |
|---------|------|
| Default | `--accent` |
| Activity / Move | `#FF2D55` (Apple's Move ring red) |
| Exercise | `#30D158` (Apple's Exercise ring green) |
| Stand | `#5AC8FA` (Apple's Stand ring blue) |
| Storage | `--accent` |

---

## 11. DATA TABLE

### Header Row

| Property | Value |
|----------|-------|
| Height | 40px |
| Background | `--surface1` |
| Font | 12px, weight 600, `--text2` |
| Text transform | uppercase, letter-spacing 0.06em |
| Cell padding | 12px 16px |
| Border bottom | `1px solid var(--border-visible)` |

### Body Row

| Property | Value |
|----------|-------|
| Height | 48px |
| Font | 15px, weight 400, `--text1` |
| Cell padding | 12px 16px |
| Row divider | `1px solid var(--border)` |

### Row States

| State | Treatment |
|-------|-----------|
| **Default** | Transparent |
| **Hover** | `--surface1` background |
| **Selected** | `--accent-subtle` background |

---

## 12. TOOLTIP

| Property | Value |
|----------|-------|
| Background | `rgba(58,58,60,0.95)` (`--surface2` dark) |
| Text color | `#F5F5F7` |
| Font | 12px, weight 400 |
| Radius | 8px |
| Padding | 6px 10px |
| Max width | 280px |
| Delay (show) | 400ms |
| Shadow | `0 4px 12px rgba(0,0,0,0.2)` |
