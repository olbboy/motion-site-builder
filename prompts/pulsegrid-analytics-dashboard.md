# PulseGrid Analytics

- **ID:** `pulsegrid-analytics-dashboard`
- **Category:** Dashboard
- **Type:** dashboard
- **Profile:** `product-ui`

---

Build a single-page subscription-analytics dashboard for "PulseGrid" — crisp, fast SaaS product UI where motion is feedback, not spectacle. Use React + Vite + Tailwind CSS + TypeScript + lucide-react + recharts + @radix-ui/react-dropdown-menu. Default Tailwind config, no other UI libraries.

FONTS
- Everything: Inter (Google Fonts, 400/500/600/700) — load via `<link>` in index.html; `font-family: 'Inter', system-ui, sans-serif` on html/body
- Every metric and table number gets `tabular-nums`

COLORS (CSS variables on :root; `.dark` on `<html>` overrides)
- Light: --background: #F8FAFC · --surface: #FFFFFF · --border: #E2E8F0 · --foreground: #0F172A · --muted-foreground: #64748B
- Semantic accents (light): --brand: #2563EB · --success: #16A34A · --warning: #D97706 · --danger: #DC2626
- Dark: --background: #0F172A · --surface: #1E293B · --border: #334155 · --foreground: #E2E8F0 · accents: #3B82F6 / #22C55E / #F59E0B / #EF4444
- Text hierarchy = foreground at opacity tiers 100% / 72% / 56% / 40%, never extra hues

GLOBAL CSS (paste verbatim)
```css
@keyframes ui-rise { from { opacity: 0; transform: translateY(6px); } to { opacity: 1; transform: none; } }

.stat { animation: ui-rise 0.22s cubic-bezier(0.23, 1, 0.32, 1) backwards;
        transition: transform 140ms cubic-bezier(0.23, 1, 0.32, 1), box-shadow 140ms cubic-bezier(0.23, 1, 0.32, 1); }
.stat:active { transform: scale(0.98); }
@media (hover: hover) and (pointer: fine) { .stat:hover { transform: translateY(-2px); box-shadow: 0 8px 24px rgb(15 23 42 / 0.08); } }

.row { animation: ui-rise 0.2s cubic-bezier(0.23, 1, 0.32, 1) backwards;
       transition: background-color 120ms cubic-bezier(0.23, 1, 0.32, 1); }
.row:nth-child(1){animation-delay:0ms} .row:nth-child(2){animation-delay:40ms} .row:nth-child(3){animation-delay:80ms}
.row:nth-child(4){animation-delay:120ms} .row:nth-child(5){animation-delay:160ms} .row:nth-child(6){animation-delay:200ms}
@media (hover: hover) { .row:hover { background: var(--background); } }

.panel { animation: ui-rise 0.28s cubic-bezier(0.23, 1, 0.32, 1) backwards; animation-delay: 160ms; }

@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { animation-duration: 0.01ms !important; animation-iteration-count: 1 !important; transition-duration: 0.01ms !important; }
}
```

LAYOUT (z contract: content z-10 → topbar z-20 → sidebar/dropdown/toast z-30; there is no video canvas)
- Fixed left sidebar `w-16 lg:w-60` + sticky topbar `h-14` + main `p-6 max-w-7xl` grid: stat row → chart panel → table

SIDEBAR (z-30, border-r border-[var(--border)], bg-[var(--surface)])
- Top: brand mark — lucide `Activity` in a `rounded-md bg-[var(--brand)] p-1.5 text-white` tile + "PulseGrid" font-semibold (hidden below lg)
- Nav (`<nav aria-label="Primary">`): Dashboard (`LayoutDashboard`), Revenue (`LineChart`), Customers (`Users`), Billing (`CreditCard`), Settings (`Settings`) — `rounded-md px-3 py-2 text-sm font-medium text-[var(--foreground)]/72`
- Frequency filter: nav links are used dozens of times a day — NO entrance animation, NO transform on hover; hover = background-color 120ms cubic-bezier(0.23, 1, 0.32, 1) to `--background` only
- Active item: `aria-current="page"`, text 100%, bg `--background`, 2px `--brand` left rail (a static absolutely-positioned span, not animated)

TOPBAR (z-20, sticky top-0, bg-[var(--surface)]/90 backdrop-blur-sm, border-b)
- Left: breadcrumb "Workspaces / Acme Inc / **Overview**" (text-sm, tiers 56%/56%/100%)
- Center: search input `rounded-md border bg-[var(--background)] px-3 py-1.5 text-sm w-72` with `Search` icon + `⌘K` kbd hint — no animation of any kind (100+ uses/day)
- Right: theme toggle (`Sun`/`Moon`, `aria-label="Toggle theme"`), bell (`Bell`, `aria-label="Notifications"`) with a static 6px `--danger` dot, avatar button opening a Radix DropdownMenu
- Dropdown: items Profile / Workspace settings / Sign out — enters scale 0.96→1 + opacity 0→1, 150ms cubic-bezier(0.23, 1, 0.32, 1), `transform-origin: top right` (scales from the trigger, never from center); exits 120ms
- Every icon button: `rounded-md p-2`, hover background-color 120ms, `active:scale-[0.98]`

STAT ROW — 4 `.stat` cards (verbatim class above), `grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-4`, stagger via `animation-delay: 0 / 40ms / 80ms / 120ms`
1. "MRR" → `$128.4k` (text-2xl font-semibold tabular-nums) + `+8.2%` text-xs font-medium text-[var(--success)]
2. "Active subscribers" → `9,412` + `+312 this month` (success)
3. "Churn" → `2.1%` + `−0.4 pt` (success — down is good)
4. "Trial → paid" → `38%` + `−2.1 pt` (text-[var(--danger)])
- Each card: label text-sm text-[var(--muted-foreground)], `rounded-xl border border-[var(--border)] bg-[var(--surface)] p-5 text-left`

CHART PANEL (`.panel`, rounded-xl border bg-[var(--surface)] p-5)
- Header row: "Monthly recurring revenue" font-medium + range pills `7D / 30D / 90D` — active pill `bg-[var(--brand)] text-white`, inactive `text-[var(--foreground)]/56`; `rounded-md px-2.5 py-1 text-xs font-medium`, transition background-color 120ms, `active:scale-[0.98]`; only the active pill's colors change — no sliding indicator
- recharts `<AreaChart>` h-72, 30 points trending 96→128: area stroke `var(--brand)` strokeWidth 2, gradient fill `var(--brand)` 12% → 0%, CartesianGrid dashed `var(--border)`, axes text-xs 56%, tooltip = surface card, `isAnimationActive={false}` on every series — the panel animates, the chart doesn't perform
- Export button (top right, `Download` icon + "Export", rounded-md border px-3 py-1.5 text-sm, `active:scale-[0.98]`) → triggers the toast

TABLE PANEL (`.panel`, mt-6) — "Recent subscriptions"
- 6 `.row` rows (verbatim class above — mount stagger 40ms apart): columns Customer / Plan / MRR (tabular-nums) / Status
- Data: Halcyon Labs · Scale · $1,290 · Active — Northwind · Growth · $490 · Active — Kite & Co · Growth · $490 · Past due — Lumen Studio · Starter · $99 · Active — Vanta Point · Scale · $1,290 · Trialing — Ondo Works · Starter · $99 · Active
- Status chips: `rounded-md px-2 py-0.5 text-xs font-medium` — Active = success at 12% bg / success text · Past due = danger tint · Trialing = warning tint
- Rows are clickable (`cursor-pointer`, press `active:scale-[0.99]`); hover = background-color only (gated `@media (hover: hover)`)

TOAST (fixed bottom-6 right-6, z-30)
- "Report exported — check your email." — `rounded-lg border bg-[var(--surface)] px-4 py-3 text-sm shadow-lg` with `CheckCircle2` in `--success`
- Enter via CSS `@starting-style`: from `opacity: 0; transform: translateY(8px)` to none, 200ms cubic-bezier(0.23, 1, 0.32, 1) — interruptible transition, NOT a keyframe that restarts; auto-dismiss after 4s (exit = same transition reversed); `role="status"`

ANIMATIONS (complete list — nothing else moves)
- Entrances: `ui-rise` only — stats 0.22s / rows 0.2s / panels 0.28s, stagger 40ms, all cubic-bezier(0.23, 1, 0.32, 1)
- Dropdown 150ms origin-aware · toast 200ms @starting-style · press `active:scale-[0.98]` on every pressable · hover = background-color/box-shadow only, 120–140ms
- Theme switch: colors swap instantly (no global color transition)

RESPONSIVE
- Below lg: sidebar collapses to `w-16` icon rail (labels hidden, `aria-label` stays on each link); search hides below md (icon button instead); stat grid 1 → 2 → 4 columns; table scrolls horizontally in an `overflow-x-auto` wrapper

KEY DEPENDENCIES
`react@^18` `react-dom@^18` `typescript@^5` `vite@^5` `tailwindcss@^3` `lucide-react@latest` `recharts@^2` `@radix-ui/react-dropdown-menu@^2`

CONSTRAINTS: product-ui restraint — every interaction ≤ 250ms, entrances 0.15–0.35s; easing only from {cubic-bezier(0.23,1,0.32,1) · cubic-bezier(0.4,0,0.2,1) · cubic-bezier(0.34,1.56,0.64,1)}; never an ease-in start on UI. Animate only transform/opacity — documented paint-only exceptions: background-color on row/pill/nav hover, box-shadow on card hover (never width/height/top/left/margin). No decorative gradients, no video, no hero drama — the UI appears, it doesn't perform. Light + dark via `.dark` class on `<html>`. Respect `prefers-reduced-motion` (block above). ARIA labels on all icon-only buttons, `aria-current` on active nav, `role="status"` on the toast. All numeric UI is `tabular-nums`. Never apply `overflow-x: hidden` to `html`/`body` or a root wrapper — it creates a scroll container and silently breaks `position: sticky`; contain any horizontal bleed with `overflow-x: clip` on the overflowing section instead.
