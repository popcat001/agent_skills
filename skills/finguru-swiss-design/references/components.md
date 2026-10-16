# Finguru App Design: Components

The components the web app is built from, with the classes and styles they actually use (React + Tailwind 4, lucide-react icons, Radix for menus and tooltips). Each section names the source file. Reuse the existing component before writing a new one.

## Layout shell (`Layout.tsx`, `Sidebar.tsx`, `ResizableSidebar.tsx`)

- Two columns: a resizable sidebar on `--bg-sidebar` with a right `border-r` (`--border`), and the main area on `--bg-primary`.
- The chat column is `max-w-4xl mx-auto` with `px-6` gutters; the input is pinned to the bottom (`px-6 pb-6 pt-2`) with the disclaimer under it (`text-xs`, secondary, centered).

## Sidebar

**Mode switch (Chat | Report).** A segmented control: track `flex gap-1 p-1 rounded-xl` on a slightly darker fill; each segment `px-3 py-1.5 rounded-lg text-[13px] font-semibold`. Active segment: `bg-[var(--bg-input)] text-[var(--accent)] shadow-[0_1px_3px_var(--shadow-tint)]`. Inactive: secondary text, primary on hover.

**New chat button.** `w-full pl-2.5 pr-3 py-1.5 rounded-lg text-[13px] font-medium`, white fill, 1px border, `shadow-[0_1px_2px_var(--shadow-tint)]`. Hover: `-translate-y-px`, `shadow-[0_4px_12px_var(--shadow-tint)]`, border mixed 35% toward the accent. Leading 20×20 `rounded-md` icon tile filled with accent 12%, icon in the accent.

**Section label.** `text-[11px] font-semibold tracking-[0.08em] uppercase`, secondary color ("AGENTS", "HISTORY").

**Agent row.** `flex items-center gap-2 mx-1 px-2 py-1 rounded-lg text-[13px]`, 14px lucide icon, name `font-medium truncate`.
- Active: fill accent 12%, text and icon in the accent.
- Hover: fill accent 6%.
- Each row has a tooltip with the agent's description.

**Locked agent row (`LockedAgentRow.tsx`).** Same row, muted, with a lock icon and a **Request** action. Status capsule ("Requested", "No owner"): `rounded-full px-1.5 py-px text-[10.5px] font-semibold`; solid grey mix or a dashed border.

**User menu (`UserMenu.tsx`).** 24px round avatar filled with the accent (white initial, `text-xs font-medium`), name `text-sm font-medium`, chevron. Role badge: 9px bold uppercase, `padding 2px 7px`, `rounded-full`, accent 18% fill, accent text ("Super" / "Admin").

## Welcome screen (`WelcomeScreen.tsx`)

- Centered app logo (`w-64`), greeting `text-xl font-medium tracking-tight`, optional tagline `text-sm` secondary, `max-w-prose`.
- **Sample question card:** grid `grid-cols-1 sm:grid-cols-2 gap-3 max-w-2xl`. Card `flex items-start gap-3 px-4 py-3.5 rounded-xl text-sm leading-snug`, white fill, 1px border. 18px lucide icon in secondary that turns accent on hover. Hover: border 45% toward the accent plus `shadow-[0_4px_14px_var(--shadow-tint)]`. Press: `active:scale-[0.99]`.

## Chat input (`ChatInput.tsx`, `AttachSkillsMenu.tsx`)

- **Box:** `flex items-center gap-3 px-4 py-3 rounded-2xl`, `--bg-input` fill, 1px border, `shadow-[0_2px_12px_var(--shadow-tint)]`. On `focus-within`: border 45% toward the accent plus `0 0 0 3px var(--accent-ring)`. Transitions 200ms.
- **Textarea:** transparent, `text-sm leading-relaxed`, auto-grows to 200px, placeholder in secondary.
- **Send button:** `p-2 rounded-xl`, accent fill, white `ArrowUp` 16px; `disabled:opacity-30`. While streaming it becomes a **Stop** button (filled square). While uploading, a spinning `Loader2`.
- **"+" menu:** an icon button that opens a Radix dropdown (see Menus) with "Attach file" and a nested skills flyout.
- **Attachment chip (document):** `inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg text-xs`, white fill, 1px border, paperclip icon, name truncated at 240px, `X` remove button.
- **Image chip (pasted image):** 56px square thumbnail `rounded-lg object-cover` with a 1px border and a small round `X` overlapping its top-right corner.
- **Inline error:** `text-xs` in `--danger`, above the box, `role="alert"`.

## Messages (`MessageBubble.tsx`, `ToolIndicator.tsx`, `TodoPanel.tsx`)

- **Role label:** `text-xs font-medium` secondary ("You" / app name) above each bubble.
- **User bubble:** right-aligned, `max-w-[85%]`, `px-4 py-3 rounded-2xl text-sm`, fill `--accent-soft`, border `color-mix(in oklch, var(--accent) 18%, var(--border))`. Tinted rather than solid accent, because white text on the accent fails contrast. Pasted images render above the text (`max-h-48 rounded-lg`, 1px border, click to open). Attachments render as download chips.
- **Assistant bubble:** left-aligned, `max-w-[95%]`, `--bg-input` fill, 1px border, `.prose prose-sm` markdown. While streaming, a blinking accent `▊` cursor follows the text.
- **Tool indicator:** `flex items-center gap-2 px-3 py-2 rounded-lg text-xs`, `--hover-tint` fill, 1px border; running state shows a spinning `Loader` (13px) in the accent. Charts open below it in a framed iframe (`ChartFrame.tsx`).
- **Todo panel:** a checklist shown above the answer for multi-step tasks.
- **Feedback:** thumbs up/down under assistant messages; choosing one opens a small comment popup (`FeedbackDialog.tsx`).

## Tooltip (`Tooltip.tsx`, Radix)

`max-w-[16rem] rounded-lg px-2.5 py-1.5 text-[11px] leading-snug border shadow-lg`, white fill, primary text, with an arrow. Portalled, so it's never clipped. Every icon-only button needs one.

## Menus (Radix dropdown, `AttachSkillsMenu.tsx`)

- **Panel:** `w-64 rounded-xl p-1.5`, white fill, 1px border, shadow `0 10px 28px -6px rgba(0,0,0,.14), 0 2px 8px rgba(0,0,0,.06)`. Opens with the `menu-in` animation (140ms).
- **Item:** `flex items-start gap-2.5 rounded-lg px-2.5 py-2`. Highlighted: `--border` fill. Disabled: `opacity-40`.

## Dialog and toast (`uiDialogs.tsx`)

- **Confirm dialog:** scrim `rgba(20,16,12,.38)`; panel `min(420px, 100%)`, 22px padding, `border-radius: 16px`, 1px border, `0 24px 64px rgba(0,0,0,.28)`. Title 16px bold; message 13.5px secondary.
  - Cancel button: `8px 14px` padding, 7px radius, 1.5px border, transparent.
  - Confirm button: `8px 16px`, accent fill, or red when destructive, white `600` text.
  - Use `confirm()` / `toast()` from this module instead of `window.confirm`.
- **Toast:** bottom-center pill (`border-radius: 999px`, `10px 18px`, 13px semibold). Success is inverted (`--text-primary` fill, `--bg-primary` text) with a check icon; errors are red with an `X`.

## Banners

- **Info / onboarding (`FeedbackOnboarding.tsx`):** `flex items-start gap-3 px-4 py-3 rounded-xl`, fill accent 8% into the page background, border accent 25% into `--border`, 18px accent icon, bold `text-sm` title and secondary body, dismiss `X`.
- **Error:** same shape with `--danger-bg` / `--danger-border` and `--danger` text.

## Admin pages (`AdminConsolePage.tsx`, `AdminAccessPage.tsx`, `AgentStudioPage.tsx`)

- **Tables:** `w-full border-collapse`; header cells `text-left text-[10.5px] uppercase tracking-wider font-bold`, secondary color; rows separated by 1px `--border`, hover `--hover-tint`. Numbers use tabular figures.
- **Header actions:** small accent text links with a 12px icon (`text-[12px] font-semibold`, e.g. Regenerate, Copy link, Download).
- **Cards / panels:** white fill, 1px border, `rounded-2xl`, `0 1px 4px rgba(0,0,0,.06)`.
- **Agent Studio:** scoped under `.agent-studio-root`, with its own focus ring (`0 0 0 3px` accent 40%). The editor column is capped at 1200px. Below 1024px the preview becomes a right-side drawer over a scrim.

## Known inconsistencies (fix when touching the code)

- **Two destructive reds:** the confirm dialog and toast hard-code `#dc2626`, while the token is `--danger` (`#b4321f`). Prefer `--danger`.
- **Undefined menu token:** the menu panel uses `var(--bg-secondary, #fff)`; `--bg-secondary` isn't defined, so it always falls back. Use `--bg-input`.
- **7px radius:** dialog buttons use `borderRadius: 7`; the scale's control radius is 8px (`rounded-lg`).
- **Inline styles:** several components (`uiDialogs.tsx`, `UserMenu.tsx`) use inline `style` objects where the rest of the app uses Tailwind classes with token variables. Prefer classes.
