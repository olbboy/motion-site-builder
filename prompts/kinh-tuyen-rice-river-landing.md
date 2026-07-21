# Kinh Tuyến — Rice & River Landing

- **ID:** `kinh-tuyen-rice-river-landing`
- **Category:** Regenerative landscape studio
- **Type:** landing
- **Profile:** `cinematic`

---

Build a single-page landing page for "Kinh Tuyến" — a Vietnamese regenerative-landscape studio whose identity follows the geometry of water and rice fields. Use React + Vite + Tailwind CSS + TypeScript + Framer Motion + lucide-react. Default Tailwind config, no other UI libraries.

SELECTED PEXELS MEDIA
- Source: [Aerial agricultural landscape in Cam Lâm](https://www.pexels.com/photo/aerial-view-of-agricultural-landscape-in-vietnam-35995797/) by Hữu Thịnh 79.
- Download to `/media/vietnam/pexels-35995797.jpg`; never hotlink the Pexels CDN.
- Hero asset: `<img src="/media/vietnam/pexels-35995797.jpg" alt="Aerial view of a river bending through geometric green rice fields in Cam Lâm, Vietnam">`.
- Crop: 16:9, `object-cover object-[52%_48%]`; keep the river bend inside the central 45% on desktop and the field/river intersection inside the center third on mobile.

FONTS
- Display: Cormorant Garamond 500/600; body: Be Vietnam Pro 400/500/600; data labels: IBM Plex Mono 500.

COLORS
- `--ink:#F6F2E9` · `--night:#07110D` · `--night-2:#0D1A13` · `--muted:rgba(246,242,233,.64)` · single accent `--rice:#D9F06A`.

GLOBAL CSS
```css
@keyframes field-rise { from { opacity:0; transform:translateY(28px); filter:blur(6px); } to { opacity:1; transform:none; filter:blur(0); } }
.field-rise { animation:field-rise .8s cubic-bezier(0.16, 1, 0.3, 1) backwards; }
.pressable { transition:transform 150ms cubic-bezier(0.16, 1, 0.3, 1); }
.pressable:active { transform:scale(.97); }
@media (hover:hover) and (pointer:fine) { .lift:hover { transform:translateY(-5px); } }
@media (prefers-reduced-motion:reduce) { *,*::before,*::after { animation-duration:.01ms!important; animation-iteration-count:1!important; transition-duration:.01ms!important; } }
```

SECTION ORDER
1. Water draws the first line. 2. Land answers in seasons. 3. Evidence becomes a living map. 4. Start with one watershed.

NAV (z-20)
- Fixed top-5, centered `w-[calc(100%-32px)] max-w-6xl`; `rounded-full border border-white/15 bg-[#07110D]/55 backdrop-blur-xl px-5 py-3`.
- Wordmark "KINH TUYẾN"; links Work / Method / Field notes; CTA "Map a site" with `bg-[var(--rice)] text-[#07110D] rounded-full px-5 py-2 pressable`.

HERO — "Water draws the first line" (media z-0, scrim z-[1], content z-10)
- `min-h-[100svh] relative overflow-hidden`; image absolute inset-0; scrim `bg-gradient-to-t from-[#07110D] via-[#07110D]/35 to-black/10`.
- Bottom-left copy `max-w-6xl mx-auto px-6 pb-14 md:pb-20`: mono eyebrow "CAM LÂM · 12.079° N"; H1 `text-6xl md:text-[108px] leading-[.84] tracking-[-.055em]` text "We design with the / intelligence of water." with "water" italic in `--rice`.
- Paragraph: "Watersheds, field edges, and village paths become one resilient system—measured in harvests, shade, and time." CTA "Trace the watershed" + circular ArrowDown button, both pressable.
- Entrance sequence 0/120/240/360ms. Add a static SVG contour line over the lower-right field, `stroke:var(--rice); opacity:.6`; no looping motion.

FIELD INDEX — "Land answers in seasons"
- `bg-[var(--night)] py-28`; 3 sticky rows: "01 / WATER" 18.4 km restored, "02 / SHADE" 3,800 trees, "03 / SOIL" +21% retention. Each row `border-t border-white/12 py-8 grid md:grid-cols-[100px_1fr_1fr]`.
- Numbers use `text-5xl md:text-7xl tabular-nums`; reveal once with fade + translateY(18px), .7s, 100ms stagger.

LIVING MAP — "Evidence becomes a living map"
- Two-column `max-w-6xl`; left sticky 44vh image crop in `rounded-2xl overflow-hidden`; right has 4 field-note cards with date, intervention, and result. The photo scales 1.04→1 as the section enters using `useScroll`; disable via `useReducedMotion()`.

FINAL CTA — "Start with one watershed"
- `min-h-[70vh] bg-[var(--night-2)]` centered; H2 "Bring us the contour lines."; CTA "Begin a field study"; footer carries selected-photo credit and source link.

ANIMATIONS
- Hero `field-rise` .8s, stagger 120ms; section reveals .7s cubic-bezier(0.16, 1, 0.3, 1), once; one scroll-linked image scale only; press .97/150ms. Only transform/opacity/filter.

RESPONSIVE
- Below md: H1 `text-6xl`, hero focal point 48% center, nav links hidden, index rows stack, living-map image becomes non-sticky and 56vh. No horizontal scroll.

KEY DEPENDENCIES
`react@^18` `react-dom@^18` `typescript@^5` `vite@^5` `tailwindcss@^3` `framer-motion@^11` `lucide-react@latest`

CONSTRAINTS: one saturated accent only; photograph supplies all depth—no decorative blobs or radial gradients. Explicit media z-0 → scrim z-[1] → content z-10 → nav z-20. Preserve the source credit in the footer. Respect `prefers-reduced-motion`; ARIA label on nav and icon-only buttons; only transform/opacity/filter animate. Never apply `overflow-x: hidden` to `html`/`body` or a root wrapper — it creates a scroll container and silently breaks `position: sticky`; contain any horizontal bleed with `overflow-x: clip` on the overflowing section instead.
