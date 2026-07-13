# Paddy Pattern — Field Planner

- **ID:** `paddy-pattern-field-planner`
- **Category:** Terrace crop planning tool
- **Type:** app
- **Profile:** `product-ui`

---

Build a responsive crop-block planning application for "Paddy Pattern" — a precise interface for sequencing terrace work, crews, and water windows without pretending a photograph is a survey map. Use React + Vite + Tailwind CSS + TypeScript + lucide-react + Radix Dialog + Radix Tooltip. Default Tailwind config, no other UI libraries.

SELECTED PEXELS MEDIA
- Source: [Golden rice terraces in Vietnam](https://www.pexels.com/photo/rice-terraces-in-the-mountains-of-vietnam-28000790/) by Blog Của Rọt.
- Download to `/media/vietnam/pexels-28000790.jpg`; use `<img src="/media/vietnam/pexels-28000790.jpg" alt="Golden rice terraces stepping across a mountain valley beneath blue sky in Vietnam">`.
- Inspiration panel crop 16:10 `object-cover object-[50%_55%]`; caption "visual reference only · not parcel geometry".

FONTS
- IBM Plex Sans 400/500/600; IBM Plex Mono 400/500 for block codes, dates, and area values.

COLORS
- Light `--bg:#F8FAFC --surface:#FFFFFF --wash:#F1F5F9 --border:#DDE4EC --text:#17202A --muted:#687482`.
- Semantic `--brand:#5A6E2F --ok:#2D7D4C --warn:#B66A16 --danger:#B63C3C`; dark `#0D1510/#18231B/#314036/#E7ECE8`.

GLOBAL CSS
```css
@keyframes planner-in { from { opacity:0; transform:translateY(5px); } to { opacity:1; transform:none; } }
.planner-in { animation:planner-in .2s cubic-bezier(0.23, 1, 0.32, 1) backwards; }
.pressable { transition:transform 120ms cubic-bezier(0.23, 1, 0.32, 1); }
.pressable:active { transform:scale(.97); }
.tooltip { transform:scale(.97); opacity:0; transform-origin:var(--radix-tooltip-content-transform-origin); transition:transform 120ms cubic-bezier(0.23, 1, 0.32, 1),opacity 120ms cubic-bezier(0.23, 1, 0.32, 1); }
.tooltip[data-state="delayed-open"] { transform:scale(1); opacity:1; }
@media (prefers-reduced-motion:reduce) { *,*::before,*::after { animation-duration:.01ms!important; animation-iteration-count:1!important; transition-duration:.01ms!important; } }
```

APP SHELL
- Sidebar: Plan / Blocks / Crews / Water windows / Materials; topbar search and season selector "Harvest 2026 · Demo".
- Header "Upper Terrace Plan"; subtitle "24 blocks · 18.6 ha · planning workspace"; actions Import CSV / New block.

WEEK BOARD
- Seven columns Mon 13 → Sun 19 Jul; 4 lanes Water / Prepare / Harvest / Move. Task chips: T-04 water 05:00, T-07 edge check, T-11 harvest crew A, T-12 harvest crew B, T-18 boat transfer.
- Drag-and-drop is out of scope; clicking a task opens its dialog. Keyboard navigation uses arrow keys between chips. Selected chip static 2px brand outline.

BLOCK LIST
- Left 62%: sortable table Block / Area / Stage / Water / Crew / Next work. Eight rows with demo data and explicit units. Right 38%: inspiration panel with selected image, caption, and source link; below photo show selected block detail.
- Do not place parcel overlays on the photograph.

RESOURCE STRIP
- Three compact cards: Crew capacity 32/40 shifts; Pumps 4/5 ready; Boat slots 6/8 open. Each has a static segmented bar built from 10 cells; never animate width.

TASK DIALOG
- Radix Dialog centered (modal exemption for centered origin), fade + scale .98→1 in 180ms. Fields Task / Block / Date / Window / Crew / Notes; footer Save task / Cancel. Full labels and errors.

CHANGE LOG
- 6-row activity feed; entries appear instantly after save with `@starting-style` opacity/translateY 6px over 180ms. No toast auto-dismiss for planning changes.

ANIMATIONS
- Page/card entrance .2s/40ms; task dialog 180ms; tooltip 120ms origin-aware; saved row 180ms; press .97. No animated bars, counters, or photograph.

RESPONSIVE
- Week board becomes day tabs; block table becomes cards; reference image moves after list; bottom nav below md; dialog full-screen below sm.

KEY DEPENDENCIES
`react@^18` `react-dom@^18` `typescript@^5` `vite@^5` `tailwindcss@^3` `lucide-react@latest` `@radix-ui/react-dialog@^1` `@radix-ui/react-tooltip@^1`

CONSTRAINTS: planning-demo data only; the selected photo is inspiration, never a geospatial source. No video, gradients, glass, decorative animation, drag-and-drop library, or false precision. Interactions ≤250ms; only transform/opacity animate; reduced motion; keyboard board, labeled forms, accessible dialog/tooltip, Pexels credit.
