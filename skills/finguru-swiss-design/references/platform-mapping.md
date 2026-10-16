# Finguru App Design: Platform Mapping

The Finguru app is React + Tailwind CSS 4 + CSS custom properties, with lucide-react icons and Radix primitives (dropdown menu, tooltip). This file covers working inside the rtb_v3 app and building standalone mockups or docs in the same style.

## 1. Inside the rtb_v3 app

- **Tokens:** already defined in `framework/web/frontend/src/index.css` (`:root`). The eight base colors come from `web/project-config.ts` `theme`. Don't redefine them; reference them in Tailwind arbitrary values:
  `bg-[var(--bg-input)]`, `text-[var(--text-secondary)]`, `border-[var(--border)]`, `shadow-[0_2px_12px_var(--shadow-tint)]`, `hover:bg-[color-mix(in_oklch,var(--accent)_6%,transparent)]`.
- **Font:** `@import "@fontsource-variable/geist";` is already at the top of `index.css`. Never add Google Fonts or other CDNs: the backend CSP is `font-src 'self' data:`.
- **Icons:** `import { TrendingUp } from "lucide-react"`, sized 12–18px, `currentColor`.
- **Reuse:** `Tooltip.tsx`, the Radix menu in `AttachSkillsMenu.tsx`, `confirm()` / `toast()` from `uiDialogs.tsx`, and `.prose` for markdown answers.

## 2. Standalone HTML (mockups, docs, previews)

```html
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Geist:wght@400;500;600;700&display=swap">
<!-- Tailwind v4 browser build lets you paste the app's class strings verbatim -->
<script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4.1.7/dist/index.global.js"
        integrity="sha384-VvC4TMG9RMvzPM9UKRYpGbP8G/4qVHiSANfgSa0qX+d3QGIXX3wB8KIuBmCU8fjZ" crossorigin="anonymous"></script>
<script src="https://unpkg.com/lucide@0.511.0/dist/umd/lucide.min.js"
        integrity="sha384-YCxwI7HW+hlnktW3yOnKN44k9F/E859McBSCz+NoK45Sww88vGY9Kqfdo794td6J" crossorigin="anonymous"></script>
<!-- <i data-lucide="trending-up"></i> … then call lucide.createIcons() -->
```

### `:root` block (copy of the app's `index.css`, Finguru theme)

```css
:root {
  --bg-primary: #faf8f5;
  --bg-sidebar: #f5f0eb;
  --bg-input: #ffffff;
  --text-primary: #1a1a1a;
  --text-secondary: #6b6b6b;
  --accent: #e07a3a;
  --accent-hover: #c96a2e;
  --border: #e8e2db;
  --accent-soft: color-mix(in oklch, var(--accent) 10%, var(--bg-input));
  --accent-ring: color-mix(in oklch, var(--accent) 40%, transparent);
  --hover-tint: color-mix(in oklch, var(--text-primary) 4%, transparent);
  --shadow-tint: color-mix(in oklch, var(--accent) 12%, transparent);
  --success: #2f7d4f;
  --danger: #b4321f;
  --danger-bg: color-mix(in oklch, var(--danger) 7%, var(--bg-input));
  --danger-border: color-mix(in oklch, var(--danger) 22%, var(--bg-input));
}
body {
  margin: 0;
  font-family: "Geist", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  background-color: var(--bg-primary);
  color: var(--text-primary);
  -webkit-font-smoothing: antialiased;
}
:where(button, a):focus-visible { outline: 2px solid var(--accent-ring); outline-offset: 2px; }
@keyframes menu-in { from { opacity: 0; transform: translateY(4px) scale(.98); } to { opacity: 1; transform: none; } }
@media (prefers-reduced-motion: reduce) { *, *::before, *::after { animation-duration: .01ms !important; transition-duration: .01ms !important; } }
```

(The app loads the bundled family name `"Geist Variable"`; standalone pages use Google's `"Geist"`.)

`preview.html` in this skill is a complete example built this way.

## 3. Other projects on the same framework

Another project rebrands by setting `theme` in its own `web/project-config.ts`. The derived tokens and every component follow automatically. A mockup for that project swaps the eight base values in the `:root` block above and changes nothing else.
