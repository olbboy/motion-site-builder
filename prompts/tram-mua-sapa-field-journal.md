# Trạm Mùa — Sa Pa Field Journal

- **ID:** `tram-mua-sapa-field-journal`
- **Category:** Seasonal field journal
- **Type:** longread
- **Profile:** `editorial`

---

Build a single-page editorial field journal for "Trạm Mùa" — one agricultural year read through a Sa Pa hillside, from flooded mirror to harvested gold. Use React + Vite + Tailwind CSS + TypeScript + `@tailwindcss/typography` + lucide-react. Default Tailwind config, no other UI libraries.

SELECTED PEXELS MEDIA
- Source: [Sa Pa rice terraces and village](https://www.pexels.com/photo/scenic-view-of-sapa-rice-terraces-in-vietnam-34782073/) by sephylmism.
- Download to `/media/vietnam/pexels-34782073.jpg`; use `<img src="/media/vietnam/pexels-34782073.jpg" alt="A village nested among green rice terraces in Sa Pa under a bright summer sky">`.
- Lead crop 3:2 `object-cover object-[50%_48%]`; keep both the village cluster and three terrace bands visible.

FONTS
- Display and prose: Newsreader 400/500/600 with Vietnamese subset; UI: Inter 400/500/600; metadata: IBM Plex Mono 400.

COLORS
- `--paper:#F7F4EC` · `--ink:#1B1B17` · `--muted:#6F6C62` · single accent `--soil:#A34F2B`.

GLOBAL CSS
```css
@keyframes journal-in { from { opacity:0; transform:translateY(14px); } to { opacity:1; transform:none; } }
.journal-in { animation:journal-in .6s cubic-bezier(0.16, 1, 0.3, 1) backwards; }
.pressable { transition:transform 140ms cubic-bezier(0.16, 1, 0.3, 1); }
.pressable:active { transform:scale(.98); }
@media (hover:hover) and (pointer:fine) { .text-link:hover { text-decoration-thickness:2px; } }
@media (prefers-reduced-motion:reduce) { *,*::before,*::after { animation-duration:.01ms!important; animation-iteration-count:1!important; transition-duration:.01ms!important; } }
```

DOCUMENT HEADER
- Sticky `top-0 z-20 h-14 bg-[var(--paper)]/92 backdrop-blur border-b border-black/10`; left "TRẠM MÙA / JOURNAL 01", center reading progress as `transform:scaleX(progress)` on a 2px line, right "VI / EN" button with press feedback.

LEAD
- `max-w-7xl px-6 pt-20`; metadata "LÀO CAI · 1,520 M · 08 MIN READ"; H1 `max-w-5xl text-6xl md:text-[104px] leading-[.94]` "A hillside keeps / its own calendar.".
- Dek `max-w-2xl text-xl md:text-2xl leading-relaxed`: "Four visits to one terrace reveal a year made of water levels, shared labor, and decisions taken uphill.".
- Full-width figure below with selected image `aspect-[3/2] md:aspect-[16/9]`; figcaption includes Pexels source, photographer, place, and selected alt text.

ARTICLE GRID
- Desktop `grid grid-cols-[220px_minmax(0,680px)_220px] gap-12`; sticky left table of contents with Flood / Transplant / Green / Harvest; prose in center; right margin hosts quiet field data.
- Four chapters, each `min-h-[72vh] py-16 border-t border-black/12`:
  1. "I · The mirror month" — flooded terraces, 12 cm water depth, May.
  2. "II · Lines by hand" — transplanting, 24 households, June.
  3. "III · A green that changes hourly" — canopy temperature, August.
  4. "IV · Gold is a deadline" — harvest window, 11 days, September.
- Begin chapter I with a 4-line drop cap. Include one pull quote: "The terrace is not a picture. It is a promise renewed uphill." Label it as editorial copy, not a real interview quote.

FIELD DATA
- Right-margin modules: 1,520 m elevation; 18–26°C field range; 11-day harvest window; 24 households. Use tabular nums, thin rules, no count-up.
- One accessible inline SVG terrace profile with static axes and `aria-label="Schematic elevation profile of four rice-terrace bands"`; no chart library.

ENDNOTE
- Full-bleed `bg-[#1B1B17] text-[#F7F4EC] py-24`; H2 "Next station: the flooded mirror." Newsletter field + button "Receive Journal 02". Footer links Method / Sources / License and repeats photo provenance.

ANIMATIONS
- Initial lead reveal .6s with 80ms stagger; figures and chapters fade + rise 14px over .6s once; reading progress scaleX tied to scroll; no parallax, typewriter, or animated numbers.

RESPONSIVE
- Below lg: hide right margin and convert its data to an inline 2×2 grid; TOC becomes horizontal scroll with current chapter; H1 `text-6xl`; lead image 3:2; body `prose-lg`. No horizontal page overflow.

KEY DEPENDENCIES
`react@^18` `react-dom@^18` `typescript@^5` `vite@^5` `tailwindcss@^3` `@tailwindcss/typography@^0.5` `lucide-react@latest`

CONSTRAINTS: editorial restraint, one soil accent, paper/ink palette, no video, glassmorphism, decorative gradients, carousel, or fabricated documentary attribution. Only transform/opacity animate. Semantic `<article>`, `<figure>`, `<figcaption>`, `<nav aria-label>`, one H1; preserve Pexels source credit; respect reduced motion. Never apply `overflow-x: hidden` to `html`/`body` or a root wrapper — it creates a scroll container and silently breaks `position: sticky`; contain any horizontal bleed with `overflow-x: clip` on the overflowing section instead.
