# Lan Hạ Stillwater — Expedition Landing

- **ID:** `lan-ha-stillwater-expedition`
- **Category:** Small-boat expedition
- **Type:** landing
- **Profile:** `cinematic`

---

Build a single-page landing page for "Lan Hạ Stillwater" — a two-night, twelve-guest small-boat expedition through mist, limestone, and tidal silence. Use React + Vite + Tailwind CSS + TypeScript + Framer Motion + lucide-react. Default Tailwind config, no other UI libraries.

SELECTED PEXELS MEDIA
- Source: [Misty Hạ Long Bay landscape](https://www.pexels.com/photo/serene-landscape-of-ha-long-bay-vietnam-36164068/) by Yagyaansh Khaneja.
- Download to `/media/vietnam/pexels-36164068.jpg`; use `<img src="/media/vietnam/pexels-36164068.jpg" alt="Misty limestone formations reflected in the calm water of Hạ Long Bay, Vietnam">`.
- Hero crop 16:9 `object-cover object-[52%_46%]`; preserve the negative-space water surface for the lower-third route panel.

FONTS
- Display: Bodoni Moda 500; body: Geist 400/500/600; route data: IBM Plex Mono 400/500.

COLORS
- `--deep:#061014` · `--fog:#E8EFF0` · `--muted:rgba(232,239,240,.62)` · single accent `--tide:#7FE4DD`.

GLOBAL CSS
```css
@keyframes mist-in { from { opacity:0; transform:translateY(20px); filter:blur(8px); } to { opacity:1; transform:none; filter:blur(0); } }
.mist-in { animation:mist-in 1s cubic-bezier(0.16, 1, 0.3, 1) backwards; }
.pressable { transition:transform 150ms cubic-bezier(0.16, 1, 0.3, 1); }
.pressable:active { transform:scale(.97); }
@media (hover:hover) and (pointer:fine) { .route-stop:hover { transform:translateX(6px); } }
@media (prefers-reduced-motion:reduce) { *,*::before,*::after { animation-duration:.01ms!important; animation-iteration-count:1!important; transition-duration:.01ms!important; } }
```

SECTION ORDER
1. Enter quietly. 2. Follow the tide, not a timetable. 3. Twelve berths, no spectacle. 4. Reserve the still water.

HERO
- `min-h-[100svh]`; image z-0, `bg-gradient-to-b from-black/10 via-transparent to-[#061014]/90` z-[1], content z-10, nav z-20.
- Top nav: coordinate wordmark "20.74°N / STILLWATER", links Route / Vessel / Departures, CTA "View departures".
- Centered H1 `text-6xl md:text-[120px] leading-[.82] tracking-[-.06em] text-center`: "The bay / between sounds."; italicize "between" in `--tide`.
- Lower-third glass route panel `max-w-5xl rounded-2xl bg-[#061014]/50 backdrop-blur-xl border border-white/15 p-5 grid md:grid-cols-[1fr_auto_1fr_auto_1fr]`: Bến Bèo → Việt Hải → Ba Trái Đào. Arrows are static; panel enters last at 360ms.

TIDAL ITINERARY
- Dark split: left sticky large numerals "48 / HOURS"; right four `.route-stop` rows with tide time, place, and action: Paddle 05:50, Cycle 09:30, Swim 15:40, Anchor 18:20.
- A thin vertical line fills by `scaleY` as the section scrolls. Stops reveal once at .7s/100ms stagger; reduced motion renders full line immediately.

VESSEL MANIFEST
- Off-white `#E8EFF0` with dark type; specification sheet, no invented vessel photo. Grid: 12 guests / 6 cabins / 2 kayaks / 1 naturalist; CSS outline side elevation of a 23 m boat.
- Cabin selector is an accessible tablist with three tabs: Bow / Midship / Stern; transition opacity 180ms only; selected tab underlined in `--tide` darkened to `#167C77` for contrast.

DEPARTURES
- Three rows: 14–16 Sep / 02–04 Oct / 21–23 Nov, from 9,600,000 ₫, 6/4/8 berths left. CTA per row "Hold a berth" with press feedback; no urgency animation.

FINAL CTA
- Reuse image as a 60vh background, focal 52% 58%; H2 "Twelve seats. One quiet route." CTA "Reserve Stillwater". Footer includes selected Pexels source and credit.

ANIMATIONS
- Hero mist-in 1s, 120ms stagger; vertical route line scaleY; stop reveals .7s; tab fade 180ms; press .97/150ms. No perpetual motion or parallax.

RESPONSIVE
- H1 `text-6xl`; route panel stacks and arrows rotate 90°; vessel manifest stacks; departure rows become cards. Hide nav links below md; preserve water negative space.

KEY DEPENDENCIES
`react@^18` `react-dom@^18` `typescript@^5` `vite@^5` `tailwindcss@^3` `framer-motion@^11` `lucide-react@latest`

CONSTRAINTS: only one cyan-tide accent; no video, blobs, radial gradients, carousel, autoplay, or invented travel claims. Only transform/opacity/filter animate. Respect reduced motion; explicit z-layer contract; nav, tablist, and icon buttons carry ARIA; retain photographer credit and source link. Never apply `overflow-x: hidden` to `html`/`body` or a root wrapper — it creates a scroll container and silently breaks `position: sticky`; contain any horizontal bleed with `overflow-x: clip` on the overflowing section instead.
