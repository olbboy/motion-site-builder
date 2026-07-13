# Watershed One — River Monitor

- **ID:** `watershed-one-river-monitor`
- **Category:** Watershed monitoring dashboard
- **Type:** app
- **Profile:** `product-ui`

---

Build a responsive monitoring dashboard for "Watershed One" — a clear, field-first interface for river reach, irrigation, rainfall, and inspection status across a Vietnamese agricultural valley. Use React + Vite + Tailwind CSS + TypeScript + lucide-react + Recharts + Radix Popover. Default Tailwind config, no other UI libraries.

SELECTED PEXELS MEDIA
- Source: [River and agricultural fields in Vietnam](https://www.pexels.com/photo/river-and-agricultural-fields-in-vietnam-6872866/) by Quang Nguyen Vinh.
- Download to `/media/vietnam/pexels-6872866.jpg`; use `<img src="/media/vietnam/pexels-6872866.jpg" alt="A broad river crossing agricultural fields with green mountains beneath a cloudy sky in Vietnam">`.
- Context-panel crop 16:9 `object-cover object-[50%_55%]`; photo is a field context image, not a live camera feed.

FONTS
- Geist 400/500/600; IBM Plex Mono 400/500 for station IDs, times, and units; tabular nums everywhere numerical.

COLORS
- Light `--bg:#F8FAFC --surface:#FFFFFF --wash:#F1F5F9 --border:#DCE3EA --text:#102033 --muted:#607184`.
- Semantic `--brand:#1769AA --ok:#16845B --warn:#C27614 --danger:#C43D3D`; corresponding dark theme `#0B1420/#152235/#2A3A4D/#E6EDF5`.

GLOBAL CSS
```css
@keyframes monitor-in { from { opacity:0; transform:translateY(5px); } to { opacity:1; transform:none; } }
.monitor-in { animation:monitor-in .18s cubic-bezier(0.23, 1, 0.32, 1) backwards; }
.pressable { transition:transform 120ms cubic-bezier(0.23, 1, 0.32, 1); }
.pressable:active { transform:scale(.97); }
.popover { transform:scale(.97); opacity:0; transform-origin:var(--radix-popover-content-transform-origin); transition:transform 150ms cubic-bezier(0.23, 1, 0.32, 1),opacity 150ms cubic-bezier(0.23, 1, 0.32, 1); }
.popover[data-state="open"] { transform:scale(1); opacity:1; }
@media (prefers-reduced-motion:reduce) { *,*::before,*::after { animation-duration:.01ms!important; animation-iteration-count:1!important; transition-duration:.01ms!important; } }
```

SHELL
- Collapsible sidebar with River overview / Stations / Inspections / Thresholds / Data health. Topbar: search, period selector "Last 24 hours", connection badge "Demo · 11/12 stations", theme toggle.

STATUS SUMMARY
- Header "Upper Valley / Reach 04" with helper "Mock telemetry for interface demonstration".
- Four cards `.monitor-in`, 40ms stagger: River level 2.14 m +0.08; Flow 36.2 m³/s; Rainfall 18 mm/24h; Data health 98.6%. Trends are static SVG sparklines with accessible text equivalents.

HYDROGRAPH + THRESHOLDS
- Recharts ComposedChart, 24 hourly points, two lines: level and rainfall. Thresholds: Advisory 2.40 m, Action 2.70 m. Provide demo-data badge and table fallback.
- Radix popover on threshold info icon, `.popover`, explains thresholds are illustrative and must be configured by the operator.

FIELD CONTEXT
- Split card: selected photo left 58%, right inspection summary. Overlay on photo only a small label "FIELD CONTEXT · 10 JUL · NOT LIVE"; no simulated camera UI.
- Inspector right: bank condition Stable; debris Minor; access Open; next visit 15 Jul; button "Open inspection".

STATION TABLE
- 8 stations R04-01…R04-08; columns Level / 1h change / Battery / Last packet / State. Include one warning battery 18%, one offline packet 47m, everything else normal. Sortable headers with `aria-sort`; state never communicated by color alone.

ALERT RULE DRAWER
- Button "Edit alerts" opens right drawer via translateX, 200ms. Inputs for advisory/action threshold with units, notification channel checkboxes, Save. Inline validation, no animated height.

ANIMATIONS
- Entrance .18s/40ms stagger; popover 150ms scale-from-trigger; drawer 200ms; press .97/120ms. Recharts animation disabled. No continuous pulses on connection or alert states.

RESPONSIVE
- Stats 2×2; context photo 4:3 above inspector; station table becomes cards below md; drawer full width; bottom nav replaces sidebar below sm.

KEY DEPENDENCIES
`react@^18` `react-dom@^18` `typescript@^5` `vite@^5` `tailwindcss@^3` `lucide-react@latest` `recharts@^2` `@radix-ui/react-popover@^1`

CONSTRAINTS: every metric and threshold labeled mock/demo; no false live claim, video, gradient, blur-heavy glass, or decorative map. Interactions ≤250ms; only transform/opacity animate, semantic paint swaps ≤150ms. Reduced motion, ARIA sort/popover/form labels, chart table fallback, Pexels provenance in About.
