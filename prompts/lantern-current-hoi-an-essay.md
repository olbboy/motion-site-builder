# Lantern Current — Hội An River Essay

- **ID:** `lantern-current-hoi-an-essay`
- **Category:** Urban river photo essay
- **Type:** longread
- **Profile:** `editorial`

---

Build a single-page visual essay for "Lantern Current" — an overhead reading of Hội An where bridges, roofs, boats, and foot traffic orbit one river spine. Use React + Vite + Tailwind CSS + TypeScript + `@tailwindcss/typography` + lucide-react. Default Tailwind config, no other UI libraries.

SELECTED PEXELS MEDIA
- Source: [Aerial Hội An river and old town](https://www.pexels.com/photo/river-between-residential-areas-of-hoi-an-city-in-vietnam-23857948/) by VANNGO Ng.
- Download to `/media/vietnam/pexels-23857948.jpg`; use `<img src="/media/vietnam/pexels-23857948.jpg" alt="Bird's-eye view of Hội An's river, bridges, boats, and tiled old-town roofs">`.
- Lead crop 16:10 `object-cover object-[50%_50%]`; the river must run vertically through the middle 30%.

FONTS
- Display: Fraunces 500/600; reading: Source Serif 4 400/600; interface: Be Vietnam Pro 400/500.

COLORS
- `--paper:#FBF7ED` · `--ink:#222019` · `--quiet:#716C5F` · single accent `--lantern:#B4531F`.

GLOBAL CSS
```css
@keyframes current-in { from { opacity:0; transform:translateY(12px); } to { opacity:1; transform:none; } }
.current-in { animation:current-in .55s cubic-bezier(0.22, 1, 0.36, 1) backwards; }
.pressable { transition:transform 140ms cubic-bezier(0.16, 1, 0.3, 1); }
.pressable:active { transform:scale(.98); }
@media (prefers-reduced-motion:reduce) { *,*::before,*::after { animation-duration:.01ms!important; animation-iteration-count:1!important; transition-duration:.01ms!important; } }
```

OPENING SPREAD
- Minimal header `max-w-7xl px-6 py-5 flex justify-between border-b`; title "LANTERN CURRENT" and issue metadata "FIELD NOTE 04 · HỘI AN".
- Asymmetric grid `md:grid-cols-[5fr_7fr] min-h-[82vh]`: left title and dek, right selected photo edge-to-edge. H1 `text-6xl md:text-[96px] leading-[.98]` "The city / leans toward / the water."; dek "Read one afternoon from roofline to riverline, without turning the old town into a postcard.".
- On the image, place only four numbered coordinate pins, 28px circles, `bg-[var(--paper)] text-[var(--ink)]`; they are buttons opening captions, with `aria-expanded` and press feedback. Captions fade 160ms and originate beside their pin; no center-scale popover.

FOUR OBSERVATIONS
- `max-w-5xl mx-auto py-24`; alternating text/image-detail crops all from the same source file using `object-position` and `scale(1.35)` inside clipped containers:
  1. "01 / The bridge is a clock" — pedestrian density changes by hour.
  2. "02 / Roofs make shade public" — covered edges as civic infrastructure.
  3. "03 / Boats redraw the street" — water as a parallel lane.
  4. "04 / Light returns the facades" — dusk color without invented lantern imagery.
- Each observation has 140–180 words of original editorial copy, a 2-line caption, and one static typographic fact; never claim measurements as verified research.

RIVER INDEX
- A single horizontal sequence at `border-y border-black/15 py-10`: 15:40 delivery boats / 16:25 bridge shade / 17:10 market spill / 18:05 reflected light. Use no animation beyond one .55s group reveal.

SOURCE NOTE
- `max-w-3xl prose-xl`; explain that the essay is a speculative design narrative grounded in one selected photograph, not a reported ethnography. Link the Pexels page, photographer, and license.

END CARD
- Full-width burnt-orange `bg-[var(--lantern)] text-white`; H2 "Look down. Read slowly."; links "Next essay" and "Photo source" with visible underlines and press .98.

ANIMATIONS
- Opening .55s/80ms stagger; observation reveal .6s once; pin caption opacity 160ms; no parallax, scroll-jacking, image zoom on scroll, or perpetual animation.

RESPONSIVE
- Opening stacks copy before image; image `aspect-[4/5]` with river central; pins remain at least 44×44 touch targets; cropped observations become 3:2; H1 `text-6xl`.

KEY DEPENDENCIES
`react@^18` `react-dom@^18` `typescript@^5` `vite@^5` `tailwindcss@^3` `@tailwindcss/typography@^0.5` `lucide-react@latest`

CONSTRAINTS: one burnt-orange accent, typography-first, no glass, video, gradients, decorative blobs, carousel, or romanticized factual claims. Every caption is keyboard accessible; one H1; semantic figure/caption structure; only transform/opacity animate; preserve Pexels provenance and reduced-motion behavior.
