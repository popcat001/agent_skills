# Finguru App Design: Tokens

Every value here is taken from the running Finguru app (rtb_v3 repo). The source of truth there is `framework/web/frontend/src/index.css` (`:root`), with the eight base colors overridden per project by `web/project-config.ts` (`theme`). If this file and `index.css` ever disagree, `index.css` wins; update this file.

## 1. Color

### Base tokens (project-configurable)

These eight are set by `project-config.ts` `theme`, so a rebrand changes them in one place.

| Token | Finguru value | `theme` key | Role |
|-------|---------------|-------------|------|
| `--bg-primary` | `#faf8f5` | `bgPrimary` | Page background (main chat area) |
| `--bg-sidebar` | `#f5f0eb` | `bgSidebar` | Sidebar, slightly warmer and darker than the page |
| `--bg-input` | `#ffffff` | `bgInput` | Raised surfaces: chat input, cards, assistant bubbles, menus, dialogs |
| `--text-primary` | `#1a1a1a` | `textPrimary` | Body text, headings |
| `--text-secondary` | `#6b6b6b` | `textSecondary` | Labels, captions, idle icons, placeholders |
| `--accent` | `#e07a3a` | `accent` | Brand orange: active states, primary actions, links, focus |
| `--accent-hover` | `#c96a2e` | `accentHover` | Hover on accent fills |
| `--border` | `#e8e2db` | `border` | 1px warm hairline on every surface |

### Derived tokens (follow the base tokens automatically)

Computed with `color-mix(in oklch, …)`, so they track whatever accent and surface a project configures. Use these instead of hard-coding tints.

| Token | Definition | Use |
|-------|------------|-----|
| `--accent-soft` | accent 10% into `--bg-input` | User message bubble fill |
| `--accent-ring` | accent 40% transparent | Focus outline / focus glow |
| `--hover-tint` | text-primary 4% transparent | Neutral hover fill, tool-indicator background, table row hover |
| `--shadow-tint` | accent 12% transparent | Color of the soft warm shadows |
| `--success` | `#2f7d4f` | Success text/icons |
| `--danger` | `#b4321f` | Destructive text/icons, errors |
| `--danger-bg` | danger 7% into `--bg-input` | Error banner fill |
| `--danger-border` | danger 22% into `--bg-input` | Error banner border |

### Inline accent mixes in common use

These recur in components but aren't named tokens yet. Use the same percentages for consistency.

| Mix | Use |
|-----|-----|
| `color-mix(in oklch, var(--accent) 6%, transparent)` | Hover fill on sidebar rows |
| `color-mix(in oklch, var(--accent) 12%, transparent)` | Active sidebar row fill; icon tile behind "New chat" |
| `color-mix(in oklch, var(--accent) 18%, transparent)` | "Super" / "Admin" badge fill |
| `color-mix(in oklch, var(--accent) 35–45%, var(--border))` | Border on hover for cards and the chat input |
| `color-mix(in srgb, var(--accent) 8%, var(--bg-primary))` + 25% border | Onboarding/info banner |

### Color rules

- Warm neutrals only. The page, sidebar and border are all warm (beige/sand); never introduce cool greys or pure `#f5f5f5`-style neutrals.
- The accent marks *state and action*: the active agent, the active segment, the primary button, focus, the streaming cursor, hover on a card's icon. It is never a large fill; at most a 10–18% tint.
- One status color each: `--success`, `--danger`. No warning token exists yet; if you need one, add it to `index.css` first.
- There is **no dark mode**. Don't add `dark:` variants piecemeal.

## 2. Typography

**Font: Geist Variable**, bundled with `@fontsource-variable/geist` (imported in `index.css`). It is bundled rather than loaded from Google Fonts because the backend CSP is `font-src 'self' data:`. Fallback: `-apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif`. There is one font for everything; no display face and no monospace role in the UI.

### Scale (what the app actually uses)

Dense, small UI text. The workhorse is 13px.

| Role | Size | Weight | Extra | Where |
|------|------|--------|-------|-------|
| Welcome headline | 20px (`text-xl`) | 500 | `tracking-tight` | Landing greeting |
| Page title | 18–22px | 600–700 | | Admin Console / Agent Studio headers |
| Dialog title | 16px | 700 | | Confirm dialog |
| Body / chat text | 14px (`text-sm`) | 400 | line-height 1.65 in `.prose` | Messages, sample questions, banners |
| UI text | 13px (`text-[13px]`) | 500–600 | | Sidebar rows, buttons, menu items, dialog buttons |
| Small UI / captions | 12px (`text-xs` / `text-[12px]`) | 400–600 | | Tool indicators, toolbars, meta lines, links in headers |
| Section label | 11px | 600 | uppercase, `tracking-[0.08em]` | Sidebar "AGENTS", "HISTORY" |
| Micro label | 10–10.5px | 600–700 | uppercase, `tracking-wider` | Table headers, sub-group labels, pills |
| Badge | 9px | 700 | uppercase, letter-spacing 0.3px | "Super" / "Admin" |

### Weights

Three weights only: **500** (medium: rows, names), **600** (semibold: buttons, labels, prose headings), **700** (bold: dialog titles, badges, table headers).

### Prose (assistant answers, `.prose` in `index.css`)

- Line-height 1.65; paragraphs have 0.75em gap and `text-wrap: pretty`.
- Headings are small and weight 600: h1 1.25em, h2 1.125em, h3 1em, with -0.01em tracking and `text-wrap: balance`.
- Tables use **tabular numbers** (`font-variant-numeric: tabular-nums`) so ARR/unit columns line up. Header cells get a 3% text-color wash and no wrapping; rows hover with `--hover-tint`.
- Blockquote: 3px `--border` left rule, secondary text color.

## 3. Spacing

Tailwind's default 4px scale. Common values:

| Use | Value |
|-----|-------|
| Chat column | `max-w-4xl`, centered; page gutter `px-6` |
| Chat input box | `px-4 py-3`, `gap-3` |
| Message bubble | `px-4 py-3` |
| Sidebar padding | `px-4`; rows `px-2 py-1`, list `gap-0.5` |
| Card (sample question) | `px-4 py-3.5`, grid `gap-3` |
| Menu panel | `p-1.5`; items `px-2.5 py-2` |
| Dialog | 22px padding; button row `gap-2.5` |
| Chips / pills | `px-2.5 py-1` (chips), `px-1.5 py-px` (pills) |

## 4. Radius

| Value | Tailwind | Use |
|-------|----------|-----|
| 6px | `rounded-md` | Small icon tiles (the "New chat" icon), inline controls |
| 7–8px | `rounded-lg` | **Default**: rows, buttons, tool indicators, chips, tooltips, menu items |
| 12px | `rounded-xl` | Cards (sample questions), menus, banners, segmented control track |
| 16px | `rounded-2xl` | The chat input box, message bubbles, dialogs |
| 999px | `rounded-full` | Avatars, pills, badges, toasts, status dots |

`rounded-lg` is the most used radius in the app (about 50 uses), then `rounded-md`/`rounded-full`, `rounded-xl` and `rounded-2xl`.

## 5. Elevation

Shadows are soft and **warm**: resting surfaces use the accent-tinted `--shadow-tint`, never grey drop shadows. Floating layers (menus, dialogs, toasts) use neutral dark shadows because they sit over arbitrary content.

| Level | Shadow | Use |
|-------|--------|-----|
| Flat | none, 1px `--border` | Sidebar rows, tables, bubbles |
| Resting | `0 1px 2px var(--shadow-tint)` / `0 1px 3px var(--shadow-tint)` | "New chat" button, active segment |
| Raised | `0 2px 12px var(--shadow-tint)` | Chat input box |
| Hover lift | `0 4px 12–14px var(--shadow-tint)` | Cards and "New chat" on hover |
| Menu | `0 10px 28px -6px rgba(0,0,0,.14), 0 2px 8px rgba(0,0,0,.06)` | Dropdown menus |
| Tooltip | Tailwind `shadow-lg` | Tooltips |
| Dialog | `0 24px 64px rgba(0,0,0,.28)` over a `rgba(20,16,12,.38)` scrim | Confirm dialog |
| Toast | `0 6px 24px rgba(0,0,0,.22)` | Toast |

## 6. Motion

| What | Value |
|------|-------|
| Color / background hover | 150ms (`duration-150`) |
| Border / shadow / lift | 200ms (`duration-200`) |
| Menu open | `menu-in` keyframe: fade + 4px rise + scale 0.98 → 1, 140ms, `cubic-bezier(0.16, 1, 0.3, 1)` |
| Hover lift | `hover:-translate-y-px` (buttons), shadow grows |
| Press | `active:scale-[0.99]` (cards, buttons) or `active:scale-95` (icon buttons) |
| Streaming | `.streaming-cursor` blinking `▊` in the accent; `animate-spin` loaders in the accent |
| Drawer | Agent Studio preview: 280ms `cubic-bezier(0.22, 1, 0.36, 1)` |

`index.css` honours `prefers-reduced-motion` globally (durations collapse to ~0).

## 7. Focus

One focus ring everywhere: `outline: 2px solid var(--accent-ring); outline-offset: 2px` on `:focus-visible` (buttons, links). Text inputs show focus by tinting the container border toward the accent and adding `0 0 0 3px var(--accent-ring)` (the chat input's `focus-within` style).

## 8. Icons

**lucide-react**, stroke icons at the default weight. Sizes: 12–13px inline in small UI, 14px sidebar agent icons, 16px buttons, 18px card and banner icons. Icons inherit `currentColor`: secondary text color at rest, accent on hover/active. Agent icons are named in each `agent.yaml` (`icon:`).

## 9. Layers (z-index)

| Layer | z-index |
|-------|---------|
| Menus | 30 |
| Tooltips | 50 |
| Agent Studio drawer / scrim | 150 / 140 |
| Dialog | 400 |
| Toast | 500 |
