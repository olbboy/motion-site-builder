# Beacon Feature Flags

- **ID:** `beacon-flags-console`
- **Category:** Feature Flags
- **Type:** dashboard/settings
- **Profile:** `product-ui`

---

Build a single-page feature-flag management console for "Beacon" — crisp product UI where every toggle, rollout, and rule change reads instantly. Use React + Vite + Tailwind CSS + TypeScript + lucide-react + @radix-ui/react-dropdown-menu. Default Tailwind config, no other UI libraries.

FONTS
- Everything: Inter (Google Fonts, 400/500/600) — `font-family: 'Inter', system-ui, sans-serif` on html/body
- Rollout percentages and dates get `tabular-nums`

COLORS (CSS variables on :root; `.dark` on `<html>` overrides)
- Light: --background: #F8FAFC · --wash: #F1F5F9 · --surface: #FFFFFF · --border: #E2E8F0 · --foreground: #0F172A · --muted-foreground: #64748B
- Semantic accents (light): --brand: #2563EB · --success: #16A34A · --warning: #D97706 · --danger: #DC2626
- Dark: --background: #0B1120 · --wash: #1E293B · --surface: #1E293B · --border: #334155 · --foreground: #E2E8F0 · accents: #3B82F6 / #22C55E / #F59E0B / #EF4444
- Environment pills: dev = `--foreground`/56% tint · staging = `--warning` tint · production = `--danger` tint (production carries the highest-stakes tint, not because it's broken — a deliberate "handle with care" cue)

GLOBAL CSS (paste verbatim)
```css
@keyframes beacon-rise { from { opacity: 0; transform: translateY(6px); } to { opacity: 1; transform: none; } }

.flag-row { animation: beacon-rise 0.2s cubic-bezier(0.23, 1, 0.32, 1) backwards;
            transition: background-color 120ms cubic-bezier(0.23, 1, 0.32, 1); }
.flag-row:nth-child(1){animation-delay:0ms} .flag-row:nth-child(2){animation-delay:40ms} .flag-row:nth-child(3){animation-delay:80ms}
.flag-row:nth-child(4){animation-delay:120ms} .flag-row:nth-child(5){animation-delay:160ms} .flag-row:nth-child(6){animation-delay:200ms}
@media (hover: hover) and (pointer: fine) { .flag-row:hover { background: var(--wash); } }

.rollout-track { position: relative; overflow: hidden; }
.rollout-fill { transform: scaleX(0); transform-origin: left; transition: transform 300ms cubic-bezier(0.23, 1, 0.32, 1); }
.rollout-fill[data-mounted="true"] { transform: scaleX(var(--rollout-ratio)); }

.switch-track { transition: background-color 140ms cubic-bezier(0.23, 1, 0.32, 1); }
.switch-thumb { transition: transform 140ms cubic-bezier(0.23, 1, 0.32, 1); }
.switch-thumb:active { transform: scale(0.95); }

.targeting-panel { transform: translateX(100%); transition: transform 200ms cubic-bezier(0.23, 1, 0.32, 1); }
.targeting-panel[data-state="open"] { transform: translateX(0); }

.env-menu { transform: scale(0.96); opacity: 0; transform-origin: top left;
            transition: transform 150ms cubic-bezier(0.23, 1, 0.32, 1), opacity 150ms cubic-bezier(0.23, 1, 0.32, 1); }
.env-menu[data-state="open"] { transform: scale(1); opacity: 1; }

.pressable { transition: transform 140ms cubic-bezier(0.23, 1, 0.32, 1); }
.pressable:active { transform: scale(0.97); }

@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { animation-duration: 0.01ms !important; animation-iteration-count: 1 !important; transition-duration: 0.01ms !important; }
}
```

LAYOUT (z contract: content z-10 → topbar z-20 → env-menu/targeting-panel/toast z-30; no video canvas)
- Fixed left sidebar `w-16 lg:w-60` + sticky topbar `h-14` + main `p-6 max-w-6xl`: flags table; targeting panel overlays from the right when a flag is opened

SIDEBAR (z-30, border-r border-[var(--border)], bg-[var(--surface)])
- Top: brand mark — lucide `Flag` in `rounded-md bg-[var(--brand)] p-1.5 text-white` tile + "Beacon" font-semibold (hidden below lg)
- Nav (`<nav aria-label="Primary">`): Flags (`Flag`), Segments (`Users`), Experiments (`FlaskConical`), Audit log (`History`), Settings (`Settings`)
- Frequency filter: hover = background-color 120ms only, no transform; active item gets static 2px `--brand` left rail

TOPBAR (z-20, sticky top-0, bg-[var(--surface)]/90 backdrop-blur-sm, border-b, flex justify-between px-6)
- Left: breadcrumb "Beacon / **Feature flags**"
- Center: environment switcher — trigger button `rounded-md border px-3 py-1.5 text-sm font-medium` "Production" + `ChevronDown`, opens `.env-menu` (verbatim class, `transform-origin: top left` from the trigger) listing Development / Staging / Production with a check mark on the active one
- Right: "New flag" button (`Plus` icon, `.pressable`, bg `--brand` text-white rounded-md px-3 py-1.5 text-sm), avatar button opening a Radix DropdownMenu (Profile / Sign out, same 150ms scale-from-trigger spec as `.env-menu`)

FLAGS TABLE (`rounded-xl border border-[var(--border)] bg-[var(--surface)]`, mt-6)
- Header row: Flag / Environments / Rollout / Enabled / Owner — text-xs font-medium text-[var(--foreground)]/56 uppercase tracking-normal
- 6 `.flag-row` rows (verbatim class, stagger 40ms), each `px-4 py-3 border-b border-[var(--border)] grid grid-cols-[1fr_140px_160px_60px_120px] items-center gap-4`
- Data (flag name / key / envs dev·staging·prod / rollout % / owner):
  1. Checkout express lane · `checkout_express_lane` · dev●staging●prod● · 100% · Priya Shah
  2. New pricing page · `new_pricing_page` · dev●staging●prod○ · 35% · Jonas Weber
  3. AI search suggestions · `ai_search_suggestions` · dev●staging○prod○ · 0% · Mai Tran
  4. Dark mode v2 · `dark_mode_v2` · dev●staging●prod○ · 68% · Leo Costa
  5. Referral program · `referral_program` · dev●staging○prod○ · 12% · Ana Fuentes
  6. Legacy invoice export · `legacy_invoice_export` · dev○staging○prod● · 100% · Unassigned
- Flag name cell: name (font-medium text-sm) + key (`font-mono text-xs text-[var(--foreground)]/56`) — clicking opens the targeting panel
- Env pills: 20px filled/outline dots per environment, `●` = active in that env, `○` = inactive; static, no animation (dozens of glances/day)
- Rollout cell: `.rollout-track` `h-1.5 rounded-full bg-[var(--wash)] w-full` containing `.rollout-fill rounded-full bg-[var(--brand)]`, `--rollout-ratio` set inline per row, `data-mounted="true"` applied on table mount so every bar fills once, together, over 300ms
- Enabled cell: custom switch — track `.switch-track w-9 h-5 rounded-full`, off = `--border`, on = `--brand`; thumb `.switch-thumb w-4 h-4 rounded-full bg-white shadow-sm`, `translateX(16px)` when on; `role="switch" aria-checked`
- Row press (outside interactive children): `active:scale-[0.99]`; hover = background-color only

TARGETING RULES PANEL (`.targeting-panel`, fixed right-0 top-14 bottom-0 w-full sm:w-[420px] bg-[var(--surface)] border-l border-[var(--border)] p-6 z-30, translates in on open)
- Header: flag name + key + close `X` button (`.pressable`)
- Rules list: "If `plan` = `enterprise` → serve `true`" / "If `country` in `[US, CA]` → serve `true` (35%)" / "Default → serve `false`" — each row `rounded-md border border-[var(--border)] p-3 text-sm font-mono`, appear with the panel (no separate stagger — the panel itself is the entrance, contents are static once visible)
- Footer: "Save targeting" primary button (`.pressable`, bg `--brand`) + "Cancel" secondary

TOAST (fixed bottom-6 right-6, z-30, `role="status"`)
- "Rollout updated to 68% — dark_mode_v2." — `rounded-lg border bg-[var(--surface)] px-4 py-3 text-sm shadow-lg` with `CheckCircle2` in `--success`
- `@starting-style`: from `opacity: 0; transform: translateY(8px)`, 200ms cubic-bezier(0.23, 1, 0.32, 1), auto-dismiss 3.5s

ANIMATIONS (complete list)
- Entrances: `beacon-rise` — flag rows 0.2s stagger 40ms (caps 200ms)
- Rollout bars: scaleX 0 → target, 300ms cubic-bezier(0.23, 1, 0.32, 1), transform-origin left, runs ONCE on table mount, never re-triggers on scroll
- Targeting panel slide: translateX 200ms cubic-bezier(0.23, 1, 0.32, 1)
- Env switcher / avatar dropdown: scale 0.96→1 + opacity, 150ms, transform-origin from the trigger (top left / top right respectively)
- Switch track/thumb: 140ms · press `active:scale-[0.97]` on buttons, `active:scale-[0.95]` on switch thumb · toast 200ms `@starting-style`
- Everything else (nav hover, env pill glances): color-only or fully static

RESPONSIVE
- Below md: flags table becomes stacked cards (flag name + key on top, env pills + rollout bar below, switch top-right); targeting panel becomes full-width (`w-full` instead of `sm:w-[420px]`); environment switcher collapses to icon-only trigger

KEY DEPENDENCIES
`react@^18` `react-dom@^18` `typescript@^5` `vite@^5` `tailwindcss@^3` `lucide-react@latest` `@radix-ui/react-dropdown-menu@^2`

CONSTRAINTS: product-ui restraint — every interaction ≤ 250ms, entrances 0.15–0.35s; easing only from {cubic-bezier(0.23,1,0.32,1) · cubic-bezier(0.4,0,0.2,1) · cubic-bezier(0.34,1.56,0.64,1)}; never an ease-in start. Animate only transform/opacity — documented paint-only exception: background-color on row/pill hover (never width/height/top/left/margin; rollout bars and the targeting panel move via `transform`, never `width`/`right`). Popovers/dropdowns scale from their trigger via explicit `transform-origin`. Press feedback on every pressable. No decorative gradients, no video. Light + dark via `.dark`. Respect `prefers-reduced-motion` (block above). ARIA: `aria-label` on icon-only buttons, `role="switch" aria-checked` on toggles, `role="status"` on the toast. All percentages are `tabular-nums`. Never apply `overflow-x: hidden` to `html`/`body` or a root wrapper — it creates a scroll container and silently breaks `position: sticky`; contain any horizontal bleed with `overflow-x: clip` on the overflowing section instead.
