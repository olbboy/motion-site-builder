# DeltaScope — Kon Tum Field Console

- **ID:** `deltascope-kon-tum-console`
- **Category:** Agricultural operations dashboard
- **Type:** app
- **Profile:** `product-ui`

---

Build a responsive field-operations dashboard for "DeltaScope" — a control surface for irrigation, access, and crop-block status across a Kon Tum river plain. Use React + Vite + Tailwind CSS + TypeScript + lucide-react + Recharts + Radix Dropdown Menu. Default Tailwind config, no other UI libraries.

SELECTED PEXELS MEDIA
- Source: [Aerial Kon Tum fields, river, and bridge](https://www.pexels.com/photo/aerial-view-of-lush-rice-fields-and-river-in-kon-tum-28897536/) by Duy Nguyen.
- Download to `/media/vietnam/pexels-28897536.jpg`; use `<img src="/media/vietnam/pexels-28897536.jpg" alt="Aerial view of green fields, a river, roads, and a bridge in Kon Tum, Vietnam">`.
- Map-context crop 16:10 `object-cover object-[52%_50%]`; this is contextual photography, not a georeferenced basemap. Show a visible "reference image" label.

FONTS
- Inter 400/500/600 throughout; JetBrains Mono 400/500 for block IDs, timestamps, and measurements; all measurements tabular nums.

COLORS
- Light: `--bg:#F8FAFC --surface:#FFFFFF --wash:#F1F5F9 --border:#E2E8F0 --text:#0F172A --muted:#64748B`.
- Semantic: `--brand:#2563EB --ok:#16A34A --warn:#D97706 --danger:#DC2626`; dark mode maps to `#0B1120/#1E293B/#334155/#E2E8F0` with `#3B82F6/#22C55E/#F59E0B/#EF4444`.

GLOBAL CSS
```css
@keyframes ui-rise { from { opacity:0; transform:translateY(6px); } to { opacity:1; transform:none; } }
.ui-rise { animation:ui-rise .2s cubic-bezier(0.23, 1, 0.32, 1) backwards; }
.pressable { transition:transform 120ms cubic-bezier(0.23, 1, 0.32, 1); }
.pressable:active { transform:scale(.97); }
.menu { transform:scale(.97); opacity:0; transform-origin:var(--radix-dropdown-menu-content-transform-origin); transition:transform 150ms cubic-bezier(0.23, 1, 0.32, 1),opacity 150ms cubic-bezier(0.23, 1, 0.32, 1); }
.menu[data-state="open"] { transform:scale(1); opacity:1; }
@media (prefers-reduced-motion:reduce) { *,*::before,*::after { animation-duration:.01ms!important; animation-iteration-count:1!important; transition-duration:.01ms!important; } }
```

APP SHELL
- Sidebar `w-16 lg:w-60 z-30`; topbar `h-14 sticky top-0 z-30`; content `p-5 lg:p-6 max-w-[1600px]`. Nav: Overview / Blocks / Irrigation / Access / Reports. Active item uses static 2px brand rail.
- Topbar: breadcrumb "DeltaScope / Kon Tum South"; season dropdown "Summer 2026" using Radix `.menu`; alert bell; avatar; theme toggle. All icon-only controls labeled.

OVERVIEW HEADER
- H1 "Kon Tum South" text-2xl font-semibold; sub "Last field sync 06:42 ICT · Reference image updated 12 Jul"; primary button "Log field check" and secondary "Export report" with press feedback.
- Four stat cards, `.ui-rise` stagger 40ms: Active blocks 28; Irrigation open 7/12; Access alerts 2; Estimated canopy 81%. Static trend badges; no count-up.

REFERENCE MAP + TASKS
- Desktop grid `grid-cols-[minmax(0,1.7fr)_minmax(320px,.8fr)]`.
- Left card: selected photo `aspect-[16/10]`, dimmed 8% with five numbered block overlays B-04/B-07/B-12/B-18/B-21 placed as accessible buttons. Header badge "REFERENCE IMAGE · NOT GEOREFERENCED". Selecting a marker updates the inspector; no fabricated GPS interaction.
- Right inspector: selected block ID, crop stage, last check, irrigation gate, access note. Default B-12: "Tillering · checked 05:55 · Gate G-3 open · East track soft". Button "Open block".

IRRIGATION SCHEDULE
- Table columns Gate / Serves / State / Opened / Next action. Six rows; state pills use semantic colors. Row hover is background-color only; row press .99. Toggle controls `role=switch aria-checked`; track/thumb transition 120ms.

7-DAY FIELD SIGNAL
- Recharts `AreaChart` for water level cm and rainfall mm using two semantic colors. Exact mock data labeled "demo data": Jul 7–13; water 18/21/19/24/22/20/23; rain 4/12/0/31/8/2/16. Accessible table fallback below chart.

ACTIVITY DRAWER
- Clicking a block opens right drawer `w-full sm:w-[420px]`, translateX 100→0 over 200ms, z-40; close button, last 5 events, text area, Save note. No animated width/right properties.

ANIMATIONS
- Cards/rows .2s stagger 40ms; drawer 200ms; dropdown 150ms origin-aware; button press .97/120ms; chart renders without draw animation. Everything else static or color-only.

RESPONSIVE
- Mobile sidebar becomes bottom nav; stats 2×2; map and inspector stack; table becomes block cards; drawer full width. Keep reference-image label visible.

KEY DEPENDENCIES
`react@^18` `react-dom@^18` `typescript@^5` `vite@^5` `tailwindcss@^3` `lucide-react@latest` `recharts@^2` `@radix-ui/react-dropdown-menu@^2`

CONSTRAINTS: product UI, interactions ≤250ms, no video, gradients, glassmorphism, decorative motion, or false geospatial accuracy. Demo data must be labeled. Only transform/opacity animate; paint-only color transitions ≤150ms allowed. Full keyboard access, chart table fallback, reduced motion, photo source and credit in an About panel. Never apply `overflow-x: hidden` to `html`/`body` or a root wrapper — it creates a scroll container and silently breaks `position: sticky`; contain any horizontal bleed with `overflow-x: clip` on the overflowing section instead.
