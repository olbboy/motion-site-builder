# Sơn Trà Curve — Cycling Club

- **ID:** `son-tra-curve-cycling`
- **Category:** Road-cycling club
- **Type:** landing
- **Profile:** `cinematic`

---

Build a single-page launch site for "Sơn Trà Curve" — a dawn road-cycling club mapped around Đà Nẵng's coast and peninsula switchbacks. Use React + Vite + Tailwind CSS + TypeScript + Framer Motion + lucide-react. Default Tailwind config, no other UI libraries.

SELECTED PEXELS MEDIA
- Source: [Đà Nẵng coastline and winding road](https://www.pexels.com/photo/scenic-coastal-view-of-da-nang-s-lush-landscape-36947722/) by Cuong Nguyen Manh.
- Download to `/media/vietnam/pexels-36947722.jpg`; use `<img src="/media/vietnam/pexels-36947722.jpg" alt="A winding road crossing green Sơn Trà hills beside the blue Đà Nẵng coast">`.
- Hero crop 16:9 `object-cover object-[58%_50%]`; keep the strongest road curve visible behind the route trace.

FONTS
- Display: Kanit 600/700 italic; body: Inter 400/500/600; telemetry: JetBrains Mono 500.

COLORS
- `--asphalt:#080B0D` · `--white:#F4F7F7` · `--muted:rgba(244,247,247,.6)` · single accent `--signal:#D7FF3F`.

GLOBAL CSS
```css
@keyframes ride-in { from { opacity:0; transform:translateY(30px) skewY(1deg); } to { opacity:1; transform:none; } }
.ride-in { animation:ride-in .75s cubic-bezier(0.16, 1, 0.3, 1) backwards; }
.route-trace { stroke-dasharray:1; stroke-dashoffset:1; animation:draw-route 1.1s cubic-bezier(0.16, 1, 0.3, 1) .45s forwards; }
@keyframes draw-route { to { stroke-dashoffset:0; } }
.pressable { transition:transform 140ms cubic-bezier(0.16, 1, 0.3, 1); }
.pressable:active { transform:scale(.97); }
@media (hover:hover) and (pointer:fine) { .stage:hover { transform:translateY(-4px); } }
@media (prefers-reduced-motion:reduce) { .route-trace { stroke-dashoffset:0; } *,*::before,*::after { animation-duration:.01ms!important; animation-iteration-count:1!important; transition-duration:.01ms!important; } }
```

SECTION ORDER
1. Meet the road before the traffic. 2. Four climbs, one coastline. 3. Ride by effort, not ego. 4. Clip in Saturday.

HERO
- Full-screen selected photo z-0, scrim `bg-gradient-to-r from-[#080B0D]/90 via-[#080B0D]/30 to-transparent` z-[1], content z-10, nav z-20.
- Nav: compact mark "STC / 05:12", links Route / Pace / Club rules, CTA "Join next ride".
- Left copy max-w-xl: mono "SƠN TRÀ · 43.2 KM · +1,184 M"; H1 `text-6xl md:text-[104px] tracking-[-.05em] leading-[.82] uppercase italic` "Own the / first curve."; sub "A no-drop dawn loop from the river, over the peninsula, and back before the city heats up.".
- Overlay a single SVG path aligned over the road, `.route-trace`, `pathLength="1"`, stroke `--signal`, 3px, z-[2], pointer-events-none, aria-hidden. It draws once; it never loops.

STAGE CARDS
- Four `.stage` cards in a staggered 12-column grid: River Warm-up 7.4 km / Radar Climb 9.8 km / Sea Wall 16.2 km / Bridge Home 9.8 km. Use CSS elevation profiles as inline SVG polylines, no extra photography.
- Card `rounded-2xl border border-white/12 bg-white/[.035] p-6`; numeric metrics tabular; gated lift -4px and press .98.

PACE CHARTER
- Two-column: huge statement "Ride by effort, not ego." and 5 rules: regroup at summits, no headphones, two bottles, daylight rear light, nobody rides home alone. Each has a 2-digit index and thin progress rail that is static.

SATURDAY ROSTER
- Interactive roster form: name, experience select, emergency contact, consent checkbox; date card "SAT 18 JUL · 05:00 · 12/20 riders". Primary CTA "Request a wheel". Labels and error messages required; success message uses `role=status` and 180ms fade.

FINAL STRIP
- Reuse image at 21:9; H2 "See the coast before it wakes." CTA "Join the 05:12 roll-out"; Pexels source/photographer in footer.

ANIMATIONS
- Hero ride-in .75s/100ms stagger; route draw 1.1s once; cards .65s reveal; hover -4px; press .97; status fade 180ms. Only transform/opacity/filter and SVG stroke-dashoffset.

RESPONSIVE
- H1 text-6xl; SVG route hidden below sm if alignment cannot be preserved; cards stack; roster becomes one column; nav links hidden. No horizontal scroll.

KEY DEPENDENCIES
`react@^18` `react-dom@^18` `typescript@^5` `vite@^5` `tailwindcss@^3` `framer-motion@^11` `lucide-react@latest`

CONSTRAINTS: one acid-lime accent; no decorative blobs, radial gradients, video, WebGL, or fabricated live route data. Selected photo supplies depth. Only transform/opacity/filter animate, aside from the explicit one-shot SVG stroke reveal. Reduced motion shows the final route immediately. Full form labels, ARIA nav, and icon-button labels required.
