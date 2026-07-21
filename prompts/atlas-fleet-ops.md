# Atlas Fleet Ops

- **ID:** `atlas-fleet-ops`
- **Category:** Logistics
- **Type:** dashboard
- **Profile:** `product-ui`

---

Build a single-page logistics fleet-operations dashboard for "Atlas" — live vehicle status without a real map dependency, motion used only to draw the eye to what changed. Use React + Vite + Tailwind CSS + TypeScript + lucide-react + @radix-ui/react-dropdown-menu. Default Tailwind config, no other UI libraries.

FONTS
- Everything: Inter (Google Fonts, 400/500/600) — `font-family: 'Inter', system-ui, sans-serif` on html/body
- All KPI values, ETAs, and timestamps get `tabular-nums`

COLORS (CSS variables on :root; `.dark` on `<html>` overrides)
- Light: --background: #F8FAFC · --surface: #FFFFFF · --border: #E2E8F0 · --foreground: #0F172A · --muted-foreground: #64748B
- Semantic accents (light): --brand: #2563EB · --success: #16A34A · --warning: #D97706 · --danger: #DC2626
- Dark: --background: #0B1120 · --surface: #1E293B · --border: #334155 · --foreground: #E2E8F0 · accents: #3B82F6 / #22C55E / #F59E0B / #EF4444
- Vehicle status mapping: En route = `--success` · Idle = `--warning` · Alert = `--danger`

GLOBAL CSS (paste verbatim)
```css
@keyframes atlas-rise { from { opacity: 0; transform: translateY(6px); } to { opacity: 1; transform: none; } }
@keyframes atlas-pulse { 0% { transform: scale(1); opacity: 0.55; } 70% { transform: scale(2.2); opacity: 0; } 100% { transform: scale(2.2); opacity: 0; } }

.vehicle-row { animation: atlas-rise 0.2s cubic-bezier(0.23, 1, 0.32, 1) backwards;
               transition: background-color 120ms cubic-bezier(0.23, 1, 0.32, 1); }
.vehicle-row:nth-child(1){animation-delay:0ms} .vehicle-row:nth-child(2){animation-delay:40ms} .vehicle-row:nth-child(3){animation-delay:80ms}
.vehicle-row:nth-child(4){animation-delay:120ms} .vehicle-row:nth-child(5){animation-delay:160ms} .vehicle-row:nth-child(6){animation-delay:200ms}
@media (hover: hover) and (pointer: fine) { .vehicle-row:hover { background: var(--background); } }
.vehicle-row[data-active="true"] { background: var(--background); }

.map-dot { position: relative; }
.map-dot::after { content: ""; position: absolute; inset: -6px; border-radius: 9999px; background: currentColor;
                  animation: atlas-pulse 1.8s linear infinite; }

.detail-drawer { transform: translateX(100%); transition: transform 220ms cubic-bezier(0.23, 1, 0.32, 1); }
.detail-drawer[data-state="open"] { transform: translateX(0); }

.pressable { transition: transform 140ms cubic-bezier(0.23, 1, 0.32, 1); }
.pressable:active { transform: scale(0.97); }

@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { animation-duration: 0.01ms !important; animation-iteration-count: 1 !important; transition-duration: 0.01ms !important; }
  .map-dot::after { animation: none; opacity: 0.35; transform: scale(1.4); }
}
```

LAYOUT (z contract: content z-10 → topbar z-20 → drawer/toast z-30; the map is a styled div, no map library)
- Fixed left sidebar `w-16 lg:w-60` + sticky topbar `h-14` + main `grid grid-cols-1 lg:grid-cols-[320px_1fr] gap-4 p-6`: vehicle list | KPI row + map panel; detail drawer overlays from the right on selection

SIDEBAR (z-30, border-r border-[var(--border)], bg-[var(--surface)])
- Top: brand mark — lucide `Navigation` in `rounded-md bg-[var(--brand)] p-1.5 text-white` tile + "Atlas" font-semibold (hidden below lg)
- Nav (`<nav aria-label="Primary">`): Fleet map (`Map`), Vehicles (`Truck`), Routes (`Route`), Drivers (`Users`), Settings (`Settings`)
- Frequency filter: hover = background-color 120ms only; active item gets static 2px `--brand` left rail

TOPBAR (z-20, sticky top-0, bg-[var(--surface)]/90 backdrop-blur-sm, border-b, flex justify-between px-6)
- Left: breadcrumb "Atlas / **Fleet map**"
- Right: theme toggle (`Sun`/`Moon`), bell (`Bell`) with static 6px `--danger` dot, avatar button opening a Radix DropdownMenu (Profile / Sign out, scale 0.96→1 + opacity 150ms, `transform-origin: top right`)

VEHICLE LIST (left column, `rounded-xl border border-[var(--border)] bg-[var(--surface)] overflow-y-auto`)
- Header: "Fleet — 6 active" text-sm font-medium p-4 border-b
- 6 `.vehicle-row` rows (verbatim class, stagger 40ms), each `px-4 py-3 border-b border-[var(--border)] cursor-pointer`
- Row anatomy: status chip (`rounded-md px-1.5 py-0.5 text-xs font-semibold`, tinted 12% bg / solid text) + vehicle ID (font-mono text-sm font-medium) + driver name (text-xs 56%) + route or last-stop note (text-xs 56%)
- Data:
  1. En route · RT-2201 · Marcus Webb · Depot 4 → Client Site B · ETA 12 min
  2. Idle · RT-1187 · Dana Osei · Last stop Depot 2 · 34 min ago
  3. Alert · RT-3390 · Felix Ngata · Geofence breach on Corridor 9
  4. En route · RT-0745 · Priya Shah · Depot 1 → Warehouse C · ETA 27 min
  5. Idle · RT-2810 · Yusuf Demir · Last stop Depot 3 · 8 min ago
  6. En route · RT-4402 · Ana Fuentes · Depot 4 → Client Site A · ETA 6 min
- Selected row #3 gets `data-active="true"` (static, no animation on select); press `active:scale-[0.99]`; hover = background-color only

KPI ROW (top of right column, `grid grid-cols-2 lg:grid-cols-4 gap-4`)
- Cards `rounded-xl border border-[var(--border)] bg-[var(--surface)] p-4`, label text-xs 56% + value text-2xl font-semibold tabular-nums
1. "Active vehicles" → `42`
2. "On-time rate" → `96.4%` (`--success` value text)
3. "Avg delivery time" → `34 min`
4. "Open alerts" → `3` (`--danger` value text)
- No count-up animation — these values refresh on a live poll; per the frequency filter, frequently-updating numbers stay `tabular-nums` and static, they don't perform on every refresh

MAP PANEL (`rounded-xl border border-[var(--border)] bg-[var(--surface)] p-4 mt-4 h-[420px] relative overflow-hidden`)
- Background: static CSS grid pattern (`background-image: linear-gradient(var(--border) 1px, transparent 1px), linear-gradient(90deg, var(--border) 1px, transparent 1px); background-size: 32px 32px`) — a styled placeholder, no map library, no imagery
- Each active vehicle plotted as a `.map-dot` (8px solid circle, `text-[var(--success)]` / `text-[var(--warning)]` / `text-[var(--danger)]` per status) positioned absolutely at a fixed `top`/`left` percentage per vehicle; the pulsing ring (`::after`) uses `currentColor` so it always matches the dot's status color
- Only En route and Alert vehicles pulse (they need attention or are actively moving); Idle vehicles render a plain static dot, no `::after` ring — pulsing every dot on a busy map would be visual noise
- Under `prefers-reduced-motion: reduce`, the ring freezes as a static 1.4×-scale halo at 35% opacity instead of disappearing — the status cue survives, only the looping motion stops

DETAIL DRAWER (`.detail-drawer`, fixed right-0 top-14 bottom-0 w-full sm:w-96 bg-[var(--surface)] border-l border-[var(--border)] p-6 z-30, translates in on selection)
- Header: status chip + "RT-3390" font-mono text-lg font-semibold + close `X` button (`.pressable`)
- Body: driver "Felix Ngata" + route "Corridor 9" + issue "Geofence breach detected 14:41:02" (text-sm text-[var(--danger)]) + "Contact driver" (`.pressable`, bg `--brand` text-white rounded-md px-4 py-2 text-sm font-medium) + "Dismiss alert" secondary button

TOAST (fixed bottom-6 right-6, z-30, `role="status"`)
- "Alert dismissed — RT-3390." — `rounded-lg border bg-[var(--surface)] px-4 py-3 text-sm shadow-lg` with `CheckCircle2` in `--success`
- `@starting-style`: from `opacity: 0; transform: translateY(8px)`, 200ms cubic-bezier(0.23, 1, 0.32, 1), auto-dismiss 3.5s

ANIMATIONS (complete list — nothing else moves)
- Entrances: `atlas-rise` — vehicle rows 0.2s stagger 40ms (caps 200ms)
- Map dot pulse: `atlas-pulse` 1.8s linear infinite, scale 1→2.2 + opacity 0.55→0, only on En route/Alert dots; frozen to a static halo under reduced motion
- Detail drawer slide: translateX 220ms cubic-bezier(0.23, 1, 0.32, 1)
- Avatar dropdown: 150ms scale-from-trigger · toast 200ms `@starting-style` · press `active:scale-[0.97]` on every pressable · hover = background-color only, 120ms
- KPI values and status chips: fully static, no animation

RESPONSIVE
- Below lg: vehicle list and KPI/map stack into a single column (list first, map below); detail drawer becomes full-width; sidebar collapses to `w-16` icon rail

KEY DEPENDENCIES
`react@^18` `react-dom@^18` `typescript@^5` `vite@^5` `tailwindcss@^3` `lucide-react@latest` `@radix-ui/react-dropdown-menu@^2`

CONSTRAINTS: product-ui restraint — every interaction ≤ 250ms, entrances 0.15–0.35s; easing only from {cubic-bezier(0.23,1,0.32,1) · cubic-bezier(0.4,0,0.2,1) · cubic-bezier(0.34,1.56,0.64,1)} plus `linear` for the constant map-dot pulse; never an ease-in start. Animate only transform/opacity — documented paint-only exception: background-color on row hover (never width/height/top/left/margin; the drawer moves via `transform`, never `right`). Popovers/dropdowns scale from their trigger via explicit `transform-origin`. Press feedback on every pressable. No real map library, no decorative gradients beyond the static grid pattern, no video. Light + dark via `.dark`. Respect `prefers-reduced-motion` (block above; the map-dot ring gets an explicit frozen-halo override rather than vanishing). ARIA: `aria-label` on icon-only buttons, `role="status"` on the toast, `aria-current` on active nav. Never apply `overflow-x: hidden` to `html`/`body` or a root wrapper — it creates a scroll container and silently breaks `position: sticky`; contain any horizontal bleed with `overflow-x: clip` on the overflowing section instead.
