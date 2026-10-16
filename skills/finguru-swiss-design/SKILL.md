---
name: finguru-swiss-design
description: "This skill should be used when the user explicitly says 'Finguru design', 'Finguru style', 'Finguru app style', 'Finguru Swiss style', '/finguru-swiss-design', or directly asks to use/apply the Finguru design system (the Finguru web app's look). NEVER trigger automatically for generic UI or design tasks."
version: 2.0.0
allowed-tools: [Read, Write, Edit, Glob, Grep]
---

# finguru-swiss-design (Finguru app design system)

You are a senior product designer. When this skill is active, every UI decision follows the design language of the **Finguru web app** (rtb_v3, `framework/web/frontend`): a warm, quiet workspace for finance analysts. (The name is historical; the Swiss slide-deck style it used to describe is no longer part of this system.)

**Before starting any design work, declare the font and how it loads** (see `references/platform-mapping.md`). Never assume Geist is already available.

---

## 1. DESIGN PHILOSOPHY

A calm, warm-neutral workspace where the content (tables, numbers, chat answers) is the loudest thing on screen. Sand-toned neutrals carry the structure: a `#faf8f5` page, a `#f5f0eb` sidebar and `#e8e2db` hairlines. One orange accent (`#e07a3a`) marks only what is **active or actionable**. Surfaces are white with a 1px warm border and, when they need lift, a soft shadow tinted with the accent rather than a grey drop shadow. Text is small and dense (13–14px Geist) because users read figures; hierarchy comes from weight and color, not size.

---

## 2. CRAFT RULES

**Tokens over hex.** Every color is a CSS variable (`--bg-primary`, `--bg-sidebar`, `--bg-input`, `--text-primary`, `--text-secondary`, `--accent`, `--accent-hover`, `--border`). These eight are per-project (rebrandable). Tints come from derived tokens (`--accent-soft`, `--accent-ring`, `--hover-tint`, `--shadow-tint`) or `color-mix(in oklch, var(--accent) N%, transparent)` at the standard percentages: 6% hover, 12% active, 18% badge, and 35–45% for a border on hover.

**Accent = state.** It marks the selected nav row (12% fill and accent text), the active segment (white pill with accent text), the primary action (solid accent, white icon or text), focus (`--accent-ring`), live indicators (spinner, streaming cursor) and icons on hover. It is never a large fill. Body-size white text on the accent fails contrast, so a user's own message uses `--accent-soft` with dark text.

**Surfaces and depth:**

| Layer | Treatment |
|-------|-----------|
| Page / sidebar | `--bg-primary` / `--bg-sidebar`, flat |
| Card, input, bubble, panel | `--bg-input` + 1px `--border`; resting shadow `0 1px 2px var(--shadow-tint)`, raised `0 2px 12px var(--shadow-tint)` |
| Hover | border 35–45% toward the accent + `0 4px 14px var(--shadow-tint)` + optional 1px lift |
| Floating (menu, tooltip, dialog, toast) | white + border + neutral shadow (`0 10px 28px -6px rgba(0,0,0,.14)` for menus, `0 24px 64px rgba(0,0,0,.28)` for dialogs) |

**Radius ladder:** 6px for icon tiles, **8px for controls (the default)**, 12px for cards, menus and banners, 16px for the chat input, message bubbles and dialogs, and full for avatars, pills, badges and toasts.

**Typography:** Geist only, with three weights (500, 600, 700).

| Role | Size and weight |
|------|-----------------|
| Greeting | 20px, 500, tight |
| Page or dialog title | 16–22px, 700 |
| Reading text | 14px, 400, line-height 1.65 in prose |
| UI text | 13px, 500–600 |
| Captions | 12px |
| Section labels | 11px, 600, uppercase, 0.08em tracking |
| Table headers | 10.5px, 700, uppercase, `tracking-wider` |

Number columns use `tabular-nums`.

**Motion:**
- Color changes take 150ms; borders and shadows 200ms.
- Hover lifts 1px; press scales to 0.99.
- Menus open with `menu-in`: fade + 4px rise + scale 0.98, 140ms `cubic-bezier(0.16,1,0.3,1)`.
- Always honour `prefers-reduced-motion`.

**The squint test:** you should see warm paper, white rounded surfaces with hairlines, readable dark text, and orange only where something is selected or clickable.

---

## 3. ANTI-PATTERNS

- Cool greys, blue-greys or pure black/white page backgrounds. Neutrals stay warm.
- Grey drop shadows on resting surfaces. Use `--shadow-tint`; neutral shadows are only for floating layers.
- Large accent fills, gradients, glassmorphism or backdrop blur.
- Hard-coded `#e07a3a`. Use `var(--accent)` so projects can rebrand.
- Display-size type, extra fonts, or a monospace role in the UI.
- Radius above 16px on rectangles; mixing radii on the same component type.
- Icon-only buttons without a tooltip and `aria-label`.
- Dark-mode `dark:` classes scattered in components. The app has no dark theme; adding one starts with tokens.
- External font or asset CDNs inside the app (the CSP is `font-src 'self'`). Standalone mockups and docs may use CDNs.
- Swiss-deck devices from the old version of this skill: 2px navy borders, Switzer/General Sans, verdict tables, pillar cards, reveal animations, 84px headlines.

---

## 4. WORKFLOW

1. **Declare the font:** Geist Variable. In the app, `@fontsource-variable/geist`; in standalone HTML, Google Fonts `Geist` (see `references/platform-mapping.md`).
2. **Set tokens:** paste the `:root` block from `references/platform-mapping.md`.
3. **Build from existing components:** `references/components.md` has the real Tailwind class strings for the sidebar, cards, chat input, bubbles, tooltip, menu, dialog, toast, banners and tables. In the rtb_v3 repo, reuse the actual components (`Tooltip`, the Radix menu pattern, `confirm()`/`toast()` from `uiDialogs.tsx`) instead of copying.
4. **Check the accent:** is orange only on active or actionable things?
5. **Check density:** 13–14px text, 8–16px radii, warm hairlines everywhere.
6. **Test extremes:** long agent names (truncate), 8-row tables, empty states, disabled states (`opacity-30`/`40`), and keyboard focus (accent ring).

---

## 5. REFERENCE FILES

| File | Contains |
|------|----------|
| `references/tokens.md` | Color (base, derived, standard mixes), type scale, spacing, radius, elevation, motion, focus, icons, z-index |
| `references/components.md` | Component specs with real class strings, plus known inconsistencies in the app |
| `references/platform-mapping.md` | React + Tailwind 4 setup, the `:root` block, font loading, standalone HTML mockups |
| `preview.html` | Living preview (open in a browser) |

## 6. SOURCE

Extracted from the running Finguru app (rtb_v3), whose source of truth is:
- `framework/web/frontend/src/index.css`: tokens, prose, motion, focus.
- `web/project-config.ts`: the eight brand colors.
- `framework/web/frontend/src/components/*.tsx`: component patterns.

The repo copy of this system lives at `docs/design-system/` in rtb_v3. When the app changes, update both.
