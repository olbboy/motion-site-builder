# Relay Incident Console

- **ID:** `relay-incident-console`
- **Category:** Incident Response
- **Type:** dashboard
- **Profile:** `product-ui`

---

Build a single-page on-call incident-response console for "Relay" — crisp product UI where motion confirms state changes, never decorates. Use React + Vite + Tailwind CSS + TypeScript + lucide-react + @radix-ui/react-dropdown-menu + @radix-ui/react-tooltip. Default Tailwind config, no other UI libraries.

FONTS
- Everything: Inter (Google Fonts, 400/500/600/700) — `font-family: 'Inter', system-ui, sans-serif` on html/body
- Every timestamp and elapsed-time value gets `tabular-nums`

COLORS (CSS variables on :root; `.dark` on `<html>` overrides)
- Light: --background: #F8FAFC · --surface: #FFFFFF · --border: #E2E8F0 · --foreground: #0F172A · --muted-foreground: #64748B
- Semantic accents (light): --brand: #2563EB · --success: #16A34A · --warning: #D97706 · --danger: #DC2626
- Dark: --background: #0B1120 · --surface: #1E293B · --border: #334155 · --foreground: #E2E8F0 · accents: #3B82F6 / #22C55E / #F59E0B / #EF4444
- Severity mapping: SEV1 = `--danger` · SEV2 = `--warning` · SEV3 = `--brand` · SEV4 = `--success` (lowest severity reads as "under control")

GLOBAL CSS (paste verbatim)
```css
@keyframes relay-rise { from { opacity: 0; transform: translateY(6px); } to { opacity: 1; transform: none; } }

.feed-row { animation: relay-rise 0.2s cubic-bezier(0.23, 1, 0.32, 1) backwards;
            transition: background-color 120ms cubic-bezier(0.23, 1, 0.32, 1); }
.feed-row:nth-child(1){animation-delay:0ms} .feed-row:nth-child(2){animation-delay:40ms} .feed-row:nth-child(3){animation-delay:80ms}
.feed-row:nth-child(4){animation-delay:120ms} .feed-row:nth-child(5){animation-delay:160ms} .feed-row:nth-child(6){animation-delay:160ms}
@media (hover: hover) and (pointer: fine) { .feed-row:hover { background: var(--background); } }
.feed-row[data-active="true"] { background: var(--background); }

.timeline-item { animation: relay-rise 0.18s cubic-bezier(0.23, 1, 0.32, 1) backwards; }
.timeline-item:nth-child(1){animation-delay:0ms} .timeline-item:nth-child(2){animation-delay:40ms}
.timeline-item:nth-child(3){animation-delay:80ms} .timeline-item:nth-child(4){animation-delay:120ms}

.pressable { transition: transform 140ms cubic-bezier(0.23, 1, 0.32, 1), background-color 120ms cubic-bezier(0.23, 1, 0.32, 1); }
.pressable:active { transform: scale(0.97); }

@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { animation-duration: 0.01ms !important; animation-iteration-count: 1 !important; transition-duration: 0.01ms !important; }
}
```

LAYOUT (z contract: content z-10 → topbar z-20 → sidebar/drawer/toast z-30; there is no video canvas)
- Fixed left sidebar `w-16 lg:w-60` + sticky topbar `h-14` + main split view `grid grid-cols-1 lg:grid-cols-[380px_1fr]`: incident feed | detail pane

SIDEBAR (z-30, border-r border-[var(--border)], bg-[var(--surface)])
- Top: brand mark — lucide `Radio` in `rounded-md bg-[var(--brand)] p-1.5 text-white` tile + "Relay" font-semibold (hidden below lg)
- Nav (`<nav aria-label="Primary">`): Incidents (`Siren`), On-call (`UserCheck`), Services (`Server`), Postmortems (`FileText`), Settings (`Settings`) — `rounded-md px-3 py-2 text-sm font-medium text-[var(--foreground)]/72`
- Frequency filter: nav links used dozens of times a day — NO entrance animation, hover = background-color 120ms cubic-bezier(0.23, 1, 0.32, 1) to `--background` only, no transform
- Active item: `aria-current="page"`, text 100%, bg `--background`, 2px `--brand` left rail (static span)

TOPBAR (z-20, sticky top-0, bg-[var(--surface)]/90 backdrop-blur-sm, border-b)
- Left: breadcrumb "Relay / On-call / **Incidents**" (text-sm, tiers 56%/56%/100%)
- Center: search input `rounded-md border bg-[var(--background)] px-3 py-1.5 text-sm w-72` with `Search` icon + `⌘K` hint — no animation of any kind (100+ uses/day)
- Right: theme toggle (`Sun`/`Moon`, `aria-label="Toggle theme"`), bell (`Bell`, `aria-label="Notifications"`) with static 6px `--danger` dot, avatar button opening a Radix DropdownMenu
- Dropdown: items Profile / On-call schedule / Sign out — enters scale 0.96→1 + opacity 0→1, 150ms cubic-bezier(0.23, 1, 0.32, 1), `transform-origin: top right`; exits 120ms
- Every icon button: `rounded-md p-2 pressable`

STATUS BANNER (spans both columns above the split, `rounded-lg px-4 py-3 text-sm font-medium`, mt-6 mx-6)
- Active state: bg `--danger` at 10%, text `--danger` — "SEV1 · checkout-api degraded for EU-WEST-1 · Acknowledged by Priya Shah · 8m elapsed" with `AlertTriangle` icon
- No entrance animation on the banner itself — it reflects current truth, appears instantly with the page (a banner that "pops in" would misrepresent an already-ongoing incident)

INCIDENT FEED (left column, border-r border-[var(--border)], overflow-y-auto)
- 6 `.feed-row` rows (verbatim class above, mount stagger as coded — delays cap at 160ms), each `px-4 py-3 border-b border-[var(--border)] cursor-pointer`
- Row anatomy: severity chip (`rounded-md px-1.5 py-0.5 text-xs font-semibold`, tinted 12% bg / solid text) + title (text-sm font-medium) + service name (text-xs 56%) + relative time (text-xs 56% tabular-nums) + assignee avatar (24px circle, initials)
- Data:
  1. SEV1 · "Checkout API returning 502 for EU-WEST-1" · checkout-api · 2m ago · Priya Shah · Investigating
  2. SEV2 · "Elevated p95 latency on search-index cluster" · search-index · 14m ago · Jonas Weber · Identified
  3. SEV2 · "Auth token refresh failing intermittently" · auth-service · 38m ago · Unassigned · Investigating
  4. SEV3 · "Nightly export job delayed 20 min" · export-worker · 1h ago · Mai Tran · Monitoring
  5. SEV3 · "Elevated 4xx on webhook receiver" · webhook-gateway · 5h ago · Unassigned · Monitoring
  6. SEV4 · "Dashboard favicon returns 404" · web-app · 3h ago · Leo Costa · Resolved
- Selected row #1 gets `data-active="true"` (static bg, no animation on select — selection is a frequent action)
- Row press: `active:scale-[0.99]`; hover = background-color only (gated `@media (hover: hover)`)

DETAIL PANE (right column, p-6, overflow-y-auto)
- Header: severity chip (SEV1) + "Checkout API returning 502 for EU-WEST-1" text-xl font-semibold + service/time meta text-sm 56%
- Action row: "Acknowledge" button (`.pressable`, bg `--brand` text-white rounded-md px-4 py-2 text-sm font-medium) + "Resolve" button (`.pressable`, bg `--success` text-white, same sizing) + "Escalate" secondary button (border only)
- Keyboard shortcuts: `A` acknowledges, `R` resolves the selected incident — these keyboard-driven paths update status/button state **instantly with no animation at all** (no press-scale, no toast slide); they sit in the 100+/day power-user tier per the frequency filter. Mouse clicks on the same buttons DO get `.pressable` press feedback (`active:scale-[0.97]`) and DO trigger the toast — the distinction is input method, not the action
- EVENT TIMELINE: vertical list, each `.timeline-item` (verbatim class, stagger 40ms) = 8px dot (severity-colored) + connecting `border-l-2 border-[var(--border)]` + timestamp (tabular-nums, text-xs 56%) + description (text-sm)
  1. 14:02:11 — "PagerDuty triggered: checkout-api error rate > 5% (5xx)"
  2. 14:03:40 — "Priya Shah acknowledged"
  3. 14:06:12 — "Runbook checkout-degraded-mode executed"
  4. 14:09:55 — "Investigating: upstream Stripe API timeout suspected"
- Timeline entries only replay `.timeline-item` on incident switch, never on a live-append (new events append with `.timeline-item` stagger continuing from the next delay slot, never restarting the whole list — restart would be visually noisy on a real-time feed)

TOAST (fixed bottom-6 right-6, z-30, `role="status"`)
- "Incident acknowledged — Priya Shah is on it." — `rounded-lg border bg-[var(--surface)] px-4 py-3 text-sm shadow-lg` with `CheckCircle2` in `--success`
- `@starting-style` transition: from `opacity: 0; transform: translateY(8px)` to none, 200ms cubic-bezier(0.23, 1, 0.32, 1) — interruptible, auto-dismiss 4s; only fires for mouse-driven Acknowledge/Resolve, never for the keyboard shortcut path

ANIMATIONS (complete list — nothing else moves)
- Entrances: `relay-rise` only — feed rows 0.2s stagger 40ms (caps 160ms) · timeline items 0.18s stagger 40ms
- Dropdown 150ms origin-aware (top right) · toast 200ms `@starting-style` · press `active:scale-[0.97]` on every mouse-driven pressable · hover = background-color only, 120ms
- Keyboard-triggered acknowledge/resolve: zero animation, zero transition — state flips instantly
- Theme switch: colors swap instantly (no global color transition)

RESPONSIVE
- Below lg: split view collapses to a single column — feed shown first; selecting a row pushes the detail pane in as a full-width view with a "← Back to feed" link (no page transition, instant swap); sidebar collapses to `w-16` icon rail

KEY DEPENDENCIES
`react@^18` `react-dom@^18` `typescript@^5` `vite@^5` `tailwindcss@^3` `lucide-react@latest` `@radix-ui/react-dropdown-menu@^2` `@radix-ui/react-tooltip@^1`

CONSTRAINTS: product-ui restraint — every interaction ≤ 250ms, entrances 0.15–0.35s; easing only from {cubic-bezier(0.23,1,0.32,1) · cubic-bezier(0.4,0,0.2,1) · cubic-bezier(0.34,1.56,0.64,1)}; never an ease-in start on UI. Animate only transform/opacity — documented paint-only exception: background-color on row/nav/button hover (never width/height/top/left/margin). Popovers/dropdowns scale from their trigger via explicit `transform-origin`. Press feedback on every mouse-driven pressable; keyboard-driven actions (A/R shortcuts) stay animation-free by design — see DETAIL PANE. No decorative gradients, no video. Light + dark via `.dark` class on `<html>`. Respect `prefers-reduced-motion` (block above). ARIA: `aria-label` on icon-only buttons, `aria-current` on active nav, `role="status"` on the toast. All numeric/time values are `tabular-nums`. Never apply `overflow-x: hidden` to `html`/`body` or a root wrapper — it creates a scroll container and silently breaks `position: sticky`; contain any horizontal bleed with `overflow-x: clip` on the overflowing section instead.
