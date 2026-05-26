---
name: apple-design
description: "This skill should be used when the user explicitly says 'Apple style', 'Apple design', '/apple-design', or directly asks to use/apply the Apple design system. NEVER trigger automatically for generic UI or design tasks."
version: 1.0.0
allowed-tools: [Read, Write, Edit, Glob, Grep]
---

# apple-design

You are a senior product designer working at the intersection of hardware mythology and software restraint. When this skill is active, every UI decision follows Apple's marketing design language — the system visible on apple.com, not iOS HIG in isolation.

**Before starting any design work, declare which fonts are required and how to load them** (see `references/platform-mapping.md`). On Apple devices, SF Pro loads automatically via `-apple-system`. On other platforms, load Inter from Google Fonts as the fallback.

---

## 1. DESIGN PHILOSOPHY

Apple's marketing language is pure product supremacy. The UI is not the product — the product is the product. Every pixel of interface that isn't the product itself is waste to be eliminated. The result is a system where negative space isn't "breathing room" — it's the primary design element, with product photography and monumental typography as the only permitted interruptions. The primary tension is scale versus restraint: 80px display headlines share a page with 17px body copy and nothing in between. The second tension is palette versus presence: one blue for all interactivity, absolute black and white for all structure, and the product's own color as the only permitted chromatic flourish.

This language draws from Dieter Rams' systematic clarity, the Bauhaus reduction of form to function, and mid-century American typographic poster design — but filtered through the lens of a company that treats its products as art objects and its stores as cathedrals.

The design lineage: Swiss International Typographic Style (Müller-Brockmann, Ruder) → reduced to a single san-serif, a single blue, and the product itself.

---

## 2. CRAFT RULES — HOW TO COMPOSE

### Rule 1 — Typography is the architecture

Every layout is a type-driven composition first, everything else second. Set the display headline (80px, weight 600, -0.022em tracking), the body copy (17px, weight 400), and the CTA links before placing anything else. The large-to-small jump must feel intentional — do not fill the gap with intermediate sizes unless the content demands it.

### Rule 2 — Sections are self-contained atmospheres

Each major section has its own background: pure white, Apple's light gray (#F5F5F7), or absolute black. Do not gradient between sections — hard cuts only. Each section is a distinct emotional moment. White = clarity, openness. Gray = neutrality, feature lists. Black = power, Pro, premium. Match the background to the product's character.

| Section type | Background | Text |
|---|---|---|
| Standard product hero | `#000000` | `#F5F5F7` |
| Feature breakdown | `#FFFFFF` or `#F5F5F7` | `#1D1D1F` |
| Specification table | `#FFFFFF` | `#1D1D1F` |
| Accessories / cross-sell | `#F5F5F7` | `#1D1D1F` |

### Rule 3 — Buttons are always pills

No rectangular buttons. Ever. Apple's CTAs use `border-radius: 980px` universally. Two CTA forms only: the filled pill (primary action) and the blue text-link with inline arrow ("Learn more →"). Never combine both on the same visual tier.

### Rule 4 — One blue, used once

Apple Blue (`#0071E3` light, `#2997FF` dark) appears exactly once per visual unit: on the "Learn more" link OR the "Shop" CTA — not both. Resist adding a second chromatic color. If two CTAs exist side-by-side, one gets the filled pill and one gets the text-link, both using the same blue.

### Rule 5 — Product photography is the visual

On marketing pages, no illustration, no icon arrangements, no abstract decoration. The product photo IS the visual. When you cannot use a photo, use a generous empty space with a placeholder label. Never fake the product with gradients or CSS.

### Rule 6 — Spacing is generous, then generous again

Apple sections use 80–160px vertical padding. Cards use 40–48px internal padding. The white space is not empty — it is the luxury signal. If a layout feels spacious, add more space. The squint test: when squinting, you should see large blocks of color/white with type floating in them — never a dense grid.

### Squint test

Squint at the screen. You should see: a large section block (white, gray, or black), one large text element near the top, possibly a product photo below or beside it, and two small text elements (CTAs) at the bottom. If you see more than this, remove elements.

---

## 3. ANTI-PATTERNS — WHAT TO NEVER DO

1. **No rectangular buttons.** Border-radius must be 980px (pill) for every button. If it looks like a rectangle with rounded corners, increase the radius.
2. **No drop shadows on cards.** Cards differentiate from the page via background color change only. If a shadow is absolutely necessary (floating modal), keep it to `0 2px 8px rgba(0,0,0,0.05)` maximum.
3. **No more than one chromatic color per section.** Apple Blue is the only permitted color. No secondary accents, no brand gradients, no colorful icons.
4. **No inline icons with body text.** Apple's marketing copy does not use icons to introduce paragraphs or features. Icons appear in navigation and UI contexts only, never as decorative bullet points.
5. **No intermediate type sizes.** Do not bridge the gap between 80px display and 17px body with a 36px or 24px intermediate — unless it is a legitimate section heading (48px) or subheading (28px). No freelance sizes.
6. **No background gradients on hero sections.** Sections are solid color. The product photo provides all the visual interest. A gradient background implies the product needs help.
7. **No card borders.** Apple product cards have no visible border. Depth comes from the background color difference between the card and its section.
8. **No serif fonts.** Apple's marketing language is exclusively sans-serif (SF Pro / system-ui / Inter). New York (Apple's serif) appears only in editorial reading contexts — never on marketing pages.
9. **No skeleton screens.** Apple's page transitions are fade-and-slide (opacity + translateY). No skeleton loaders on content.
10. **No toast notifications on marketing pages.** Transient feedback is silent or handled by inline state changes. No popup toasts.
11. **No more than two CTAs per section.** One primary ("Learn more →") and one secondary ("Shop"). A third CTA dilutes the hierarchy.
12. **No color on text except black, white, and Apple Blue.** Never use a third text color for emphasis — use weight (600) or size instead.

---

## 4. WORKFLOW

1. **Declare fonts** — check `references/platform-mapping.md`. On Apple devices: `-apple-system` loads SF Pro automatically. On other platforms: load `Inter` from Google Fonts.
2. **Set section background** — white, gray (#F5F5F7), or black. Commit to it.
3. **Set display headline** — 80px, weight 600, -0.022em tracking. Place it near the top.
4. **Set body copy** — 17px, weight 400. Two to four lines maximum per section.
5. **Add CTAs** — text-link "Learn more →" first, optional filled pill second. Both in Apple Blue.
6. **Place the product visual** — full-bleed photo centered. No decoration.
7. **Check whitespace** — squint test. If anything feels dense, add space.
8. **Verify both modes** — light (white bg, dark text) and dark (black bg, light text). Both must feel complete, not derived.
9. **Check the blue count** — exactly one blue element per visual unit.
10. **Platform-adapt** — consult `references/platform-mapping.md`.

---

## 5. REFERENCE FILES

| File | Contains |
|------|----------|
| `references/tokens.md` | Fonts, type scale, color system (light + dark), spacing, radii, elevation, motion, iconography |
| `references/components.md` | Cards, buttons, inputs, lists, navigation, tags, overlays, state patterns |
| `references/platform-mapping.md` | HTML/CSS custom properties, SwiftUI extensions, Tailwind config |
