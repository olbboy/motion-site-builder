# Aperture Team Settings

- **ID:** `aperture-team-settings`
- **Category:** SaaS Settings
- **Type:** settings
- **Profile:** `product-ui`

---

Build a single-page workspace-settings console for "Aperture" — a collaborative photo-pipeline SaaS. Crisp product UI: motion is confirmation, never decoration. Use React + Vite + Tailwind CSS + TypeScript + lucide-react + @radix-ui/react-dropdown-menu + @radix-ui/react-dialog. Default Tailwind config, no other UI libraries.

FONTS
- Everything: Inter (Google Fonts, 400/500/600) — `font-family: 'Inter', system-ui, sans-serif` on html/body

COLORS (CSS variables on :root; `.dark` on `<html>` overrides)
- Light: --background: #FFFFFF · --wash: #F8FAFC · --border: #E2E8F0 · --foreground: #0F172A · --muted-foreground: #64748B
- Accents: --brand: #2563EB · --success: #16A34A · --danger: #DC2626
- Dark: --background: #0F172A · --wash: #1E293B · --border: #334155 · --foreground: #E2E8F0 · --brand: #3B82F6 · --success: #22C55E · --danger: #EF4444

GLOBAL CSS (paste verbatim)
```css
@keyframes ui-rise { from { opacity: 0; transform: translateY(6px); } to { opacity: 1; transform: none; } }
.section-enter { animation: ui-rise 0.24s cubic-bezier(0.23, 1, 0.32, 1) backwards; }

.row { animation: ui-rise 0.2s cubic-bezier(0.23, 1, 0.32, 1) backwards;
       transition: background-color 120ms cubic-bezier(0.23, 1, 0.32, 1); }
.row:nth-child(1){animation-delay:0ms} .row:nth-child(2){animation-delay:40ms} .row:nth-child(3){animation-delay:80ms}
.row:nth-child(4){animation-delay:120ms} .row:nth-child(5){animation-delay:160ms}
@media (hover: hover) { .row:hover { background: var(--wash); } }

@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { animation-duration: 0.01ms !important; animation-iteration-count: 1 !important; transition-duration: 0.01ms !important; }
}
```

PAGE FRAME (max-w-5xl mx-auto px-6 py-10; header z-20, content z-10)
- Page header: "Workspace settings" text-2xl font-semibold + subtext "Manage how Aperture works for Studio North." text-sm text-[var(--muted-foreground)]

TAB BAR (`<nav aria-label="Settings sections">`, border-b border-[var(--border)], mt-6)
- Tabs: General · Members · Notifications · Billing · Danger zone — `px-1 pb-3 mr-6 text-sm font-medium`, inactive text 56%, active text 100%
- ONE shared underline element (absolute, h-0.5, bg-[var(--brand)]) that translates + scales to the active tab: `transform: translateX(<tab.offsetLeft>px) scaleX(<tab.width/100>)`, transition transform 200ms cubic-bezier(0.23, 1, 0.32, 1), `transform-origin: left` — GPU-only, never animate `left`/`width`
- Tab press: `active:scale-[0.98]`; switching tabs swaps the panel with `.section-enter` (0.24s rise) — no exit animation
- Frequency filter: tabs are hit constantly — hover is color-only (no transform)

GENERAL PANEL (`.section-enter`)
- Card `rounded-lg border border-[var(--border)] p-6` with rows: Workspace name (text input `rounded-md border bg-[var(--background)] px-3 py-2 text-sm w-80`), Workspace URL (`aperture.app/` prefix + input), Default timezone (native select)
- Save bar: right-aligned "Save changes" `rounded-md bg-[var(--brand)] px-4 py-2 text-sm font-medium text-white`, hover bg −8% lightness 120ms, `active:scale-[0.98]` → triggers toast

MEMBERS PANEL — table of 5 `.row` entries (verbatim class, mount stagger 40ms)
- Columns: Member (avatar circle 32px + name + email 56%) / Role / Last active / ⋯
- Data: Mai Tran · Owner · now — Jonas Weber · Admin · 2h ago — Priya Shah · Editor · 1d ago — Leo Costa · Editor · 3d ago — Ana Fuentes · Viewer · 2w ago
- Role cell: Radix DropdownMenu — trigger `rounded-md border px-2.5 py-1 text-xs font-medium` with `ChevronDown`; menu enters scale 0.96→1 + opacity, 150ms cubic-bezier(0.23, 1, 0.32, 1), `transform-origin: top left` (from the trigger); items Owner/Admin/Editor/Viewer with check mark on current
- "Invite member" button top-right of panel (`UserPlus` icon, brand bg, `active:scale-[0.98]`)

NOTIFICATIONS PANEL — 4 toggle rows inside a bordered card, divided by border-b
- Rows: "Weekly digest" (on) · "Render completed" (on) · "Storage at 90%" (on) · "New device sign-in" (off)
- Each row: label text-sm font-medium + description text-xs 56% + a switch on the right
- Switch spec: track `w-9 h-5 rounded-full`, off = `--border`, on = `--brand`, transition background-color 140ms cubic-bezier(0.23, 1, 0.32, 1); thumb `w-4 h-4 rounded-full bg-white shadow-sm`, translates `translateX(16px)` when on, transition transform 140ms cubic-bezier(0.23, 1, 0.32, 1); `role="switch" aria-checked`, press `active:scale-[0.95]` on the thumb
- Toggling fires the toast ("Preferences updated")

BILLING PANEL — plan card: "Scale — $49/user/month" font-semibold + `9,412 renders used / 15,000` with a progress bar (h-1.5 rounded-full track `--wash`; fill = `--brand`, width set once via inline style on mount — scaleX from 0 → target over 300ms cubic-bezier(0.23, 1, 0.32, 1), `transform-origin: left`, run ONCE on panel enter) + "Manage billing" secondary button

DANGER ZONE PANEL — card with `border-[var(--danger)]/30`
- Row: "Delete workspace" font-medium + warning text-xs 56% + "Delete…" button `rounded-md border border-[var(--danger)] text-[var(--danger)] px-3 py-1.5 text-sm`, hover = danger bg at 8% 120ms, `active:scale-[0.98]`
- Opens a Radix Dialog: overlay `bg-black/40`, opacity 0→1 150ms; panel `rounded-lg bg-[var(--background)] p-6 max-w-md shadow-xl`, enters scale 0.96→1 + translateY(8px)→0 + opacity, 180ms cubic-bezier(0.23, 1, 0.32, 1), `transform-origin: center` (modals are the exception — they own the screen, center origin is correct)
- Dialog: title "Delete Studio North?", body text-sm 72%, confirm input ("type studio-north"), buttons Cancel (secondary) / "Delete forever" (danger bg, disabled until match, `active:scale-[0.98]`)

TOAST (fixed bottom-6 right-6, z-30, `role="status"`)
- `rounded-lg border bg-[var(--background)] px-4 py-3 text-sm shadow-lg` + `Check` icon in `--success`
- `@starting-style` transition: from `opacity: 0; transform: translateY(8px)`, 200ms cubic-bezier(0.23, 1, 0.32, 1), interruptible; auto-dismiss 3.5s

ANIMATIONS (complete list)
- Panel swap `.section-enter` 0.24s · rows 0.2s stagger 40ms · tab underline 200ms translate/scale · switches 140ms · dropdown/dialog 150–180ms origin-aware · toast 200ms `@starting-style` · progress fill 300ms scaleX once
- Everything else (nav hovers, inputs): color-only, 120ms

RESPONSIVE
- Below md: tab bar scrolls horizontally (`overflow-x-auto`, no scrollbar); members table becomes stacked cards (avatar + name on top, role dropdown right); page padding px-4

KEY DEPENDENCIES
`react@^18` `react-dom@^18` `typescript@^5` `vite@^5` `tailwindcss@^3` `lucide-react@latest` `@radix-ui/react-dropdown-menu@^2` `@radix-ui/react-dialog@^1`

CONSTRAINTS: product-ui restraint — every interaction ≤ 250ms; easing only from {cubic-bezier(0.23,1,0.32,1) · cubic-bezier(0.4,0,0.2,1) · cubic-bezier(0.34,1.56,0.64,1)}; never an ease-in start. Animate only transform/opacity — documented paint-only exceptions: background-color on hover/switch tracks (never width/height/top/left/margin; the tab underline and progress bar move via transform, not width). Popovers/dropdowns scale from their trigger via explicit `transform-origin`; only the centered modal is exempt. Press feedback on every pressable. No decorative gradients, no video. Light + dark via `.dark`. Respect `prefers-reduced-motion` (block above). ARIA: `aria-label` on icon-only buttons, `role="switch" aria-checked` on toggles, `role="status"` on the toast, focus trap + `aria-modal` on the dialog.
