# apple-design — Tokens

## 0. PRIMITIVES

Raw scales derived from apple.com analysis. Semantic tokens reference them.

### Color Ramps

**Neutral** (cool-neutral — Apple's grays carry a very slight blue undertone)

| Step | Hex | Use |
|------|-----|-----|
| 50 | `#FFFFFF` | Pure white — primary light background |
| 100 | `#F5F5F7` | Apple gray — alt sections, card bg |
| 200 | `#E8E8ED` | Light borders, dividers |
| 300 | `#D2D2D7` | Medium borders, strong dividers |
| 400 | `#AEAEB2` | Placeholder text, disabled |
| 500 | `#8E8E93` | Tertiary text |
| 600 | `#6E6E73` | Secondary text |
| 700 | `#48484A` | Strong borders (dark mode) |
| 800 | `#3A3A3C` | Dark surfaces |
| 900 | `#1D1D1F` | Apple's near-black — primary dark text |
| 950 | `#000000` | Absolute black — Pro sections, dark hero |

**Brand** (Apple Blue)

| Step | Hex |
|------|-----|
| 50 | `#EBF3FF` |
| 100 | `#D1E6FF` |
| 200 | `#A3CDFF` |
| 300 | `#75B3FF` |
| 400 | `#2997FF` — dark mode accent |
| 500 | `#0071E3` — primary accent (light mode) |
| 600 | `#0064CA` |
| 700 | `#004F9F` |
| 800 | `#003B75` |
| 900 | `#002754` |
| 950 | `#001335` |

**Status Colors**

| Color | 50 (bg tint) | 500 (foreground) | 900 (dark tint) |
|-------|-------------|-----------------|-----------------|
| Red | `#FFF0EF` | `#FF3B30` | `#5C0A08` |
| Green | `#F0FDF5` | `#30D158` | `#0A3D1E` |
| Amber | `#FFF6EC` | `#FF9F0A` | `#5C3507` |

### Spacing Primitives

`0, 2, 4, 8, 12, 16, 24, 32, 48, 64, 96`

### Radii Primitives

`0, 8, 12, 18, 20, 980`

Note: 980 is Apple's pill radius — effectively any value ≥ height/2 produces a perfect pill. All buttons use this.

---

## 1. TYPOGRAPHY

### Font Stack

| Role | Font | Fallback | Weight | Use |
|------|------|----------|--------|-----|
| **Display / UI** | `-apple-system, BlinkMacSystemFont, "SF Pro Display"` | `"Inter", sans-serif` | 600 | Headlines, display numbers, large titles |
| **Body / Text** | `-apple-system, BlinkMacSystemFont, "SF Pro Text"` | `"Inter", sans-serif` | 400 | Body copy, labels, navigation items |
| **Mono** | `"SF Mono"` | `"JetBrains Mono", "Fira Code", monospace` | 400 | Code only (rare on marketing pages) |

### Mono Font Rules

**`mono_for_code`: false** · **`mono_for_metrics`: false**

Apple's marketing pages use the system sans-serif for all text including metrics, pricing ($999), and technical values. Mono is reserved for code contexts only, and even then is rare on apple.com marketing pages. Both flags are false — price typography like "$1,599" stays in SF Pro, styled with weight 600.

SF Pro automatically switches between SF Pro Text (body sizes ≤ 19pt) and SF Pro Display (larger sizes) — this optical sizing is handled by the system font stack. On non-Apple platforms, load Inter from Google Fonts.

### Type Scale

| Token | Size | Line Height | Letter Spacing | Weight | Use |
|-------|------|-------------|----------------|--------|-----|
| `--display` | 80px | 1.05 | -0.022em | 600 | Hero headlines, product names at monumental scale |
| `--heading` | 48px | 1.08 | -0.015em | 600 | Section headings |
| `--subheading` | 28px | 1.15 | -0.010em | 600 | Feature names, card titles |
| `--body` | 17px | 1.52 | 0em | 400 | Body copy — Apple's canonical reading size |
| `--body-sm` | 14px | 1.50 | 0em | 400 | Secondary descriptions, footnotes |
| `--caption` | 12px | 1.40 | 0.005em | 400 | Legal, timestamps, spec labels |
| `--label` | 12px | 1.30 | 0.010em | 500 | Navigation items, button labels, tags |

### Typographic Rules

- Headings at 48px+ always use weight 600 with negative tracking. Never use 700 on marketing pages.
- Body copy is always 17px, weight 400, standard line-height. Never bold body text for emphasis — use a separate headline instead.
- Letter-spacing is negative on display/heading sizes, zero on body sizes, slightly positive on caption/label. Never add positive tracking to body text.
- Maximum two font sizes per card (subheading + body). Maximum three per section (heading + body + caption).
- Price typography uses weight 600 at the nearest scale size. "$1,599" is a heading-scale element, not body.
- "Learn more →" CTA: 17px, weight 400, `--accent` color. The arrow character is `→` (Unicode), not an icon.

---

## 2. COLOR SYSTEM (Semantic Tokens)

### Primary Mode (Light)

| Token | Primitive | Hex | Role |
|-------|-----------|-----|------|
| `--background` | `{neutral.50}` | `#FFFFFF` | Page background — pure white |
| `--bg` | — | `var(--background)` | Shorthand alias |
| `--surface1` | `{neutral.100}` | `#F5F5F7` | Cards, alt sections (Apple's signature gray) |
| `--surface2` | `{neutral.200}` | `#E8E8ED` | Nested surfaces, input bg |
| `--surface3` | `{neutral.300}` | `#D2D2D7` | Tertiary wells |
| `--border` | `{neutral.200}` | `#E8E8ED` | Subtle dividers |
| `--border-visible` | `{neutral.300}` | `#D2D2D7` | Table borders, input borders |
| `--text1` | `{neutral.900}` | `#1D1D1F` | Primary text — Apple's near-black |
| `--text2` | `{neutral.600}` | `#6E6E73` | Secondary text |
| `--text3` | `{neutral.500}` | `#8E8E93` | Tertiary text — placeholders, footnotes |
| `--text4` | `{neutral.400}` | `#AEAEB2` | Disabled text |
| `--accent` | `{brand.500}` | `#0071E3` | Apple Blue — all interactive elements |
| `--accent-subtle` | `{brand.50}` | `#EBF3FF` | Tinted background for accent elements |
| `--success` | `{green.500}` | `#30D158` | Available, confirmed |
| `--warning` | `{amber.500}` | `#FF9F0A` | Caution, pending |
| `--error` | `{red.500}` | `#FF3B30` | Unavailable, error |

### Secondary Mode (Dark)

| Token | Primitive | Hex | Role |
|-------|-----------|-----|------|
| `--background` | `{neutral.950}` | `#000000` | Absolute black — Pro sections |
| `--surface1` | `{neutral.900}` | `#1D1D1F` | Primary surface on dark |
| `--surface2` | `{neutral.800}` | `#3A3A3C` | Secondary surface |
| `--surface3` | `{neutral.700}` | `#48484A` | Tertiary surface |
| `--border` | `{neutral.800}` | `#3A3A3C` | Subtle dividers |
| `--border-visible` | `{neutral.700}` | `#48484A` | Visible borders |
| `--text1` | `{neutral.100}` | `#F5F5F7` | Primary text on dark |
| `--text2` | `{neutral.500}` | `#8E8E93` | Secondary text on dark |
| `--text3` | `{neutral.600}` | `#6E6E73` | Tertiary text on dark |
| `--text4` | `{neutral.700}` | `#48484A` | Disabled text on dark |
| `--accent` | `{brand.400}` | `#2997FF` | Apple Blue — brighter on dark |
| `--accent-subtle` | `{brand.950}` | `#001335` | Accent tint on dark |
| `--success` | `{green.500}` | `#30D158` | Same system green |
| `--warning` | `{amber.500}` | `#FF9F0A` | Same system orange |
| `--error` | `{red.500}` | `#FF3B30` | Same system red |

### Accent & Status Tints

| Token | Light Mode | Dark Mode | Usage |
|-------|------------|-----------|-------|
| `--accent-subtle` | `#EBF3FF` | `#001335` | Tinted bg for selected states, focus rings |
| `--success-bg` | `#F0FDF5` | `#082B14` | Success state backgrounds |
| `--warning-bg` | `#FFF6EC` | `#2B1800` | Warning state backgrounds |
| `--error-bg` | `#FFF0EF` | `#2B0806` | Error state backgrounds |

### Color Usage Rules

- Apple Blue (`--accent`) appears **exactly once per visual unit**. Do not use it for text emphasis — only for interactive elements (links, buttons).
- `--text1` (`#1D1D1F`) is not pure black — Apple deliberately uses this near-black to reduce harshness. Never substitute `#000000` for text (reserve it for backgrounds).
- On dark sections, `--text1` is `#F5F5F7` — Apple's off-white. Pure white text (#FFFFFF) reads as harsh; use it only for very large display text (80px+) on black backgrounds.
- Semantic status colors (`--success`, `--warning`, `--error`) are Apple's system colors — they do not shift between light and dark mode. Use their bg-tint tokens (`--success-bg`) for surface contexts.

---

## 3. SPACING

### Scale (8px base)

| Token | Value | Use |
|-------|-------|-----|
| `--space-2xs` | 2px | Optical adjustments, tight icon gaps |
| `--space-xs` | 4px | Icon-to-label gap, hairline spacers |
| `--space-sm` | 8px | Between stacked text elements |
| `--space-md` | 16px | Component internal padding, row gaps |
| `--space-lg` | 24px | Card section padding, element groups |
| `--space-xl` | 32px | Between major card elements |
| `--space-2xl` | 48px | Card padding (standard), nav height |
| `--space-3xl` | 64px | Section padding (compressed) |
| `--space-4xl` | 96px | Section padding (standard) |

Apple's product pages use 80–160px vertical section padding — beyond the token scale. Use `--space-4xl` (96px) as the minimum and 160px for flagship hero sections.

---

## 4. BORDERS & RADII

### Radii Scale (Semantic → Primitive)

| Token | Value | Primitive | Use |
|-------|-------|-----------|-----|
| `--radius-element` | 8px | `{radii[1]}` | Small badges, checkboxes, micro-elements |
| `--radius-input` | 12px | `{radii[2]}` | Text fields, search bars |
| `--radius-component` | 18px | `{radii[3]}` | Cards, panels, feature blocks |
| `--radius-container` | 20px | `{radii[4]}` | Modals, sheets |
| `--radius-pill` | 980px | `{radii[5]}` | ALL buttons — no exceptions |

### Border Treatment

| Element | Border |
|---------|--------|
| Cards / Surfaces | None — depth via background color only |
| Buttons | None — pill shape, background provides identity |
| Inputs | `1px solid var(--border-visible)` default; `2px solid var(--accent)` focus |
| Tags / Chips | None — background fills |
| Modals / Sheets | None on perimeter; dividers inside use `--border` |

Apple's corner philosophy is binary: buttons are always pills (980px), everything else uses soft corners (8–20px). Sharp corners (0px) are absent from the vocabulary. The pill-first rule applies to every interactive element regardless of its content.

---

## 5. ELEVATION & SHADOWS

| Level | Light Mode | Dark Mode | Use |
|-------|-----------|----------|-----|
| **0** | None | None | Cards against matching-bg sections |
| **1** | `0 2px 8px rgba(0,0,0,0.05), 0 1px 2px rgba(0,0,0,0.06)` | `0 2px 8px rgba(0,0,0,0.30)` | Feature cards on white bg |
| **2** | `0 8px 30px rgba(0,0,0,0.08), 0 2px 8px rgba(0,0,0,0.05)` | `0 8px 30px rgba(0,0,0,0.50)` | Floating menus, popovers |
| **3** | `0 20px 60px rgba(0,0,0,0.12), 0 8px 24px rgba(0,0,0,0.08)` | `0 20px 60px rgba(0,0,0,0.70)` | Modals, dialogs |

Primary strategy: **flat**. Cards do not have shadows — background color change is the only depth signal. Level 1 shadow is permitted only when a card must sit against a same-color background (white card on white page). Level 3 is reserved for modals.

**Glass strategy (Liquid Glass):** Apple's nav bar and some overlay contexts use `backdrop-filter: blur(20px) saturate(180%)` with a semi-transparent background (`rgba(255,255,255,0.72)` light / `rgba(0,0,0,0.72)` dark). This is not a shadow — it's a material. Use only for navigation and overlay surfaces that float above content.

---

## 6. MOTION & INTERACTION

### Personality

Smooth and deliberate. Apple's interactions feel inevitable — no hesitation, no playfulness, no mechanical sharpness. Motion serves content; it never draws attention to itself. Scroll-triggered reveals use `opacity 0→1` + `translateY 20px→0` over 500ms. Hover states are fast (150ms) to feel responsive without being jumpy.

### Timing

| Type | Duration | Easing | Use |
|------|----------|--------|-----|
| **Micro** | 150ms | `cubic-bezier(0.25, 0.46, 0.45, 0.94)` | Button press, color change, opacity flicker |
| **Standard** | 300ms | `cubic-bezier(0.25, 0.46, 0.45, 0.94)` | Card expand, content show/hide, tab switch |
| **Emphasis** | 500ms | `cubic-bezier(0.28, 0.44, 0.49, 0.96)` | Section reveal, page transition, hero entrance |

### Interaction States

| Element | Default | Hover | Active | Focus | Disabled |
|---------|---------|-------|--------|-------|---------|
| Filled pill button | Solid bg | Opacity 0.85, 150ms | Scale 0.97, 100ms | 2px offset ring in `--accent` | Opacity 0.4 |
| Text-link ("Learn more") | `--accent` color | Underline + slight darken | Opacity 0.7 | 2px underline | Opacity 0.4 |
| Card | No visual change | No hover state (content-rich: product does the work) | — | — | Opacity 0.4 |
| Input | `--border-visible` border | No change | — | 2px `--accent` border, no shadow | Opacity 0.4 |

---

## 7. ICONOGRAPHY

> **⚠ Fallback disclosure.** The icons rendered in the generated preview come from the Phosphor kit (light weight) selected as the closest match to Apple's SF Symbols. They are **not** Apple's real glyphs — SF Symbols is a proprietary system and not redistributed with this skill. On Apple platforms, use SF Symbols. On web/other platforms, license-appropriate alternatives apply.

### Observed style (Apple's actual icons — SF Symbols)

| Attribute | Value |
|-----------|-------|
| Description | Proprietary Apple SF Symbols set. Thin-to-regular stroke (~1px–1.5px), perfect rounded terminals, strictly geometric construction with high internal consistency. Available in nine weights and three scales. Outline style dominates on marketing; filled variants appear in UI contexts. |
| Stroke weight | regular (~1.5px), thin in some contexts |
| Corner treatment | fully-round |
| Fill style | outline / filled (contextual) |
| Form language | strict-geometric |
| Visual density | minimal |

### Fallback kit (what the preview actually renders)

- **Kit:** Phosphor (light weight)
- **Weight / variant:** light (~1.25px)
- **Match score:** medium
- **Why this kit:** Phosphor light is the closest to SF Symbols' minimal stroke weight and rounded terminals in the free CDN pool. The humanist warmth is a slight mismatch (SF Symbols are purely geometric), but no kit offers strictly-geometric + rounded-terminals at this delicacy. Lucide (2px) and Tabler (1.5px) are too heavy.
- **CDN:** `https://unpkg.com/@phosphor-icons/web@2/src/light/style.css`
- **Usage:** `<i class="ph-light ph-{icon-name}"></i>`

### Sizes

| Context | Size |
|---------|------|
| Inline with body text (17px) | 16px |
| Buttons | 16px |
| Navigation | 20px |

### Color rule

Icons inherit `--text2` by default. Interactive icons inherit `--accent`. Status icons use their semantic color (`--success`, `--warning`, `--error`). Never give icons a color that text doesn't also use in that context.

### Don't

- Never mix SF Symbols-style icons with any other kit in the same view.
- Never claim these Phosphor icons are SF Symbols — they are a best-match fallback.
- Never use icons larger than 24px in body content (nav-level scale only).
