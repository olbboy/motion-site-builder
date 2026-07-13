# CoastSignal — Route Dashboard

- **ID:** `coastsignal-route-dashboard`
- **Category:** Coastal mobility operations
- **Type:** app
- **Profile:** `product-ui`

---

Build a responsive route-operations dashboard for "CoastSignal" — a planning interface for coastal shuttle frequency, stop readiness, and weather advisories where a Vietnamese city meets the sea. Use React + Vite + Tailwind CSS + TypeScript + lucide-react + Recharts + Radix Dropdown Menu. Default Tailwind config, no other UI libraries.

SELECTED PEXELS MEDIA
- Source: [Coastal landscape with city view](https://www.pexels.com/photo/coastal-landscape-with-city-view-33299005/) by Çiğdem Bilgin.
- Download to `/media/vietnam/pexels-33299005.jpg`; use `<img src="/media/vietnam/pexels-33299005.jpg" alt="A Vietnamese coastal city beside blue sea, green hills, and scattered islands">`.
- Network header crop 21:9 `object-cover object-[50%_48%]`; label the image "route context · not live".

FONTS
- Inter 400/500/600; JetBrains Mono 500 for trip IDs, headways, and timestamps.

COLORS
- Light `--bg:#F7F9FC --surface:#FFFFFF --wash:#EEF3F8 --border:#D9E2EC --text:#102A43 --muted:#627D98`.
- Semantic `--brand:#0B6E99 --ok:#14805E --warn:#C47A13 --danger:#C24141`; dark theme has `#0B1722/#132536/#294052/#E6F0F7`.

GLOBAL CSS
```css
@keyframes coast-in { from { opacity:0; transform:translateY(6px); } to { opacity:1; transform:none; } }
.coast-in { animation:coast-in .2s cubic-bezier(0.23, 1, 0.32, 1) backwards; }
.pressable { transition:transform 120ms cubic-bezier(0.23, 1, 0.32, 1); }
.pressable:active { transform:scale(.97); }
.dropdown { transform:scale(.97); opacity:0; transform-origin:var(--radix-dropdown-menu-content-transform-origin); transition:transform 150ms cubic-bezier(0.23, 1, 0.32, 1),opacity 150ms cubic-bezier(0.23, 1, 0.32, 1); }
.dropdown[data-state="open"] { transform:scale(1); opacity:1; }
@media (prefers-reduced-motion:reduce) { *,*::before,*::after { animation-duration:.01ms!important; animation-iteration-count:1!important; transition-duration:.01ms!important; } }
```

SHELL
- Sidebar: Network / Trips / Stops / Advisories / Reports; topbar with service-day selector, global search, notifications, operator profile.
- Page header "Coastal Loop A" with demo status badge, button "Publish draft" and overflow dropdown using `.dropdown`.

CONTEXT BANNER
- Selected photo `h-48 lg:h-56 rounded-xl` with dark 35% scrim and explicit z layers. Overlay left: "COASTAL LOOP A · 42.8 KM"; right: "REFERENCE IMAGE · 12 JUL". No route line drawn over non-georeferenced photo.

SERVICE HEALTH
- Four cards `.coast-in` 40ms stagger: Trips scheduled 96; On-time estimate 91%; Stops ready 18/20; Advisories 2. No count-up.

HEADWAY BOARD
- Timeline from 05:30 to 22:30 with three service bands: Peak 12 min, Day 18 min, Evening 24 min. Render with CSS grid, not an animated canvas. Current selected band gets static brand outline.
- Editing a band opens an inline panel: Start / End / Headway / Vehicle count, labeled fields, Save/Cancel.

STOP READINESS TABLE
- 8 sample stops with columns Stop / Shelter / Lighting / Access / Last check / Owner. Use icon + label for state; two warning rows: "Cliff Path" lighting review, "South Pier" access works. Row hover color only.

RIDERSHIP SHAPE
- Recharts AreaChart for demo hourly boardings: 12/35/88/72/49/61/84/103/77/43/21. Disable animation; provide data table fallback. Annotate peak at 17:30.

ADVISORY PANEL
- Two static alerts: Crosswind watch 14:00–18:00; South Pier access works all day. Severity uses icon, label, and color. Acknowledge buttons press .97; no pulse.

ANIMATIONS
- Card entrance .2s/40ms; dropdown 150ms origin-aware; inline editor opacity + translateY 160ms; press 120ms. Charts and status indicators static.

RESPONSIVE
- Bottom nav below md; photo banner 16:9; stats 2×2; headway board becomes stacked bands; readiness table becomes cards. No horizontal page overflow.

KEY DEPENDENCIES
`react@^18` `react-dom@^18` `typescript@^5` `vite@^5` `tailwindcss@^3` `lucide-react@latest` `recharts@^2` `@radix-ui/react-dropdown-menu@^2`

CONSTRAINTS: demo operations data only, no claim of a real network or live weather. No video, decorative gradients, glass, or fake map alignment. Interactions ≤250ms; only transform/opacity animate with brief semantic color swaps. Reduced motion, complete form labels and table headers, chart table fallback, photo provenance in About.
