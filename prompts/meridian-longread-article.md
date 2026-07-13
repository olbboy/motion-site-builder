# Meridian Longread

- **ID:** `meridian-longread-article`
- **Category:** Magazine Article
- **Type:** article
- **Profile:** `editorial`

---

Build a single-page magazine feature article for "Meridian" — a slow-journalism publication. Typography carries the page; motion stays out of the way. The piece: "The Slow Web". Use React + Vite + Tailwind CSS + TypeScript + @tailwindcss/typography + lucide-react. Default Tailwind config (plus the typography plugin), no other UI libraries.

FONTS (Google Fonts, load via `<link>` in index.html)
- Display: Fraunces (weights 400/600, optical size auto, italic) — masthead, headline, pull quote
- Body: Newsreader (400/500, italic) — article prose
- UI: Inter (400/500) — captions, byline, TOC, footer

COLORS (CSS variables on :root — paper family, light only)
- --paper: #FBFBF9 · --ink: #1A1A1A · --accent: #B4531F (burnt sienna — the ONLY accent hue)
- Text tiers: ink at 100% / 75% / 60%. Rules and borders: `#1A1A1A` at 12%

GLOBAL CSS (paste verbatim)
```css
@keyframes ed-reveal { from { opacity: 0; transform: translateY(12px); } to { opacity: 1; transform: none; } }
.reveal { animation: ed-reveal 0.6s cubic-bezier(0.22, 1, 0.36, 1) backwards; }

.progress { transform-origin: left; transform: scaleX(var(--p, 0)); }

article .prose p:first-of-type::first-letter {
  font-family: 'Fraunces', serif; float: left; font-size: 3.6em;
  line-height: 0.85; padding-right: 0.08em; color: var(--accent);
}

@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { animation-duration: 0.01ms !important; animation-iteration-count: 1 !important; transition-duration: 0.01ms !important; }
}
```

READING PROGRESS BAR (fixed top-0, z-20)
- `h-[2px] w-full bg-[var(--accent)] progress` — set `--p` (0→1) from scroll position via a passive scroll listener writing to the CSS variable; pure `transform: scaleX`, no width animation, no easing (directly bound to scroll)

MASTHEAD (sticky top-0, z-10, bg-[var(--paper)]/95 backdrop-blur-sm, border-b border-[#1A1A1A]/12)
- Center: "Meridian" — Fraunces, text-xl, tracking-normal
- Left: "Issue 14 — Attention" (Inter text-xs, ink 60%) · Right: "Subscribe" text link — underline via a `scaleX` pseudo-element (h-px, `transform-origin: left`, scaleX 0→1 on hover, 200ms cubic-bezier(0.16, 1, 0.3, 1), gated `@media (hover: hover) and (pointer: fine)`), press `active:scale-[0.98]`
- Frequency filter: the masthead is persistent chrome — nothing in it animates on load

TITLE BLOCK (max-w-[65ch] mx-auto px-6 pt-20 pb-12, staggered `.reveal` on load: kicker 0ms → H1 120ms → standfirst 240ms → byline 360ms, i.e. `animation-delay`)
- Kicker: "FIELD NOTES · TECHNOLOGY" — Inter text-xs font-medium tracking-[0.18em] uppercase text-[var(--accent)]
- H1: "The Slow Web" — Fraunces text-5xl md:text-7xl leading-[1.05], ink 100%
- Standfirst: "What happens to reading — and to readers — when the feed stops refreshing? A month inside the movement that wants the internet to load a little less." — Newsreader italic text-xl md:text-2xl leading-relaxed, ink 75%
- Byline row: "By Iris Kowalczyk · Photographs by D. Anand" + "22 min read" — Inter text-sm, ink 60%, separated by a thin rule above (border-t border-[#1A1A1A]/12 pt-4)

BODY GRID (max-w-6xl mx-auto, lg:grid lg:grid-cols-[1fr_65ch_1fr] gap-8)
- Center column — the article (paste verbatim):
```tsx
<article className="prose prose-neutral mx-auto max-w-[65ch] prose-headings:font-serif
                    prose-headings:tracking-tight prose-p:leading-relaxed">
  {/* prose body */}
</article>
```
  - Prose body: 6+ paragraphs of the piece in Newsreader; H2s ("The refresh reflex", "Rooms with one door", "What the loaf knows") in Fraunces with anchor `id`s; links = ink with `underline decoration-[var(--accent)] decoration-1 underline-offset-4`
  - Pull quote after paragraph 3: "We didn't lose our attention. We rented it out, one refresh at a time." — Fraunces italic text-3xl leading-snug, border-l-2 border-[var(--accent)] pl-6, ink 100%
  - Two figures: `<figure>` with `<img src="{YOUR_IMAGE_URL_1}" alt="…">` (rounded-lg) + `<figcaption>` Inter text-sm ink 60%; second figure breaks the column (`lg:-mx-24`)
  - Footnote markers: `<sup>` buttons (accent color, `aria-label="Footnote 1"`) opening a small popover card (`rounded-lg border bg-[var(--paper)] shadow-md p-4 text-sm max-w-xs`) — enters scale 0.96→1 + opacity, 160ms cubic-bezier(0.16, 1, 0.3, 1), `transform-origin: bottom left` (from the marker, it sits above); dismiss on outside click
- Right rail (lg+ only) — sticky TOC (paste verbatim):
```tsx
<nav className="sticky top-24 hidden lg:block" aria-label="On this page">
  {headings.map(h => (
    <a key={h.id} href={`#${h.id}`}
       className="block border-l-2 border-transparent py-1 pl-3 text-sm text-neutral-500
                  transition-colors duration-150 data-[active=true]:border-neutral-900
                  data-[active=true]:text-neutral-900">
      {h.title}
    </a>
  ))}
</nav>
```
  - IntersectionObserver sets `data-active` on the current section's link; smooth-scroll on click; never scroll-jack

SCROLL REVEAL
- Each H2 section and each figure gets `.reveal` when it first enters the viewport (IntersectionObserver adds the class once, threshold 0.2) — 0.6s cubic-bezier(0.22, 1, 0.36, 1), reading pace, one element at a time; paragraphs themselves do NOT animate (prose just reads)

END MATTER (max-w-[65ch] mx-auto)
- Footnotes list under a thin rule (Inter text-sm, ink 60%)
- "Next in Issue 14" — 2 teaser links: title (Fraunces text-2xl) + dek (Newsreader ink 75%); hover = the same scaleX underline on the title, gated; press `active:scale-[0.98]`

FOOTER (border-t border-[#1A1A1A]/12, py-12, Inter text-sm ink 60%)
- "Meridian — published quarterly, read slowly." + links About / Archive / RSS

ANIMATIONS (complete list — restraint is the brief)
- Load: title block 4-element stagger, 0.6s each, delays 0/120/240/360ms
- Scroll: `.reveal` once per section/figure, 0.6s cubic-bezier(0.22, 1, 0.36, 1); progress bar scaleX bound to scroll
- Hover: underline scaleX 200ms; TOC = color only 150ms · Popover: 160ms origin-aware · Press: `active:scale-[0.98]` on links/buttons
- Nothing loops, nothing bounces, nothing moves while you read

RESPONSIVE
- Mobile: single column, px-6; TOC hidden; figures full-bleed (`-mx-6`); H1 text-5xl; pull quote text-2xl
- The reading column is ALWAYS ≤ 65ch

KEY DEPENDENCIES
`react@^18` `react-dom@^18` `typescript@^5` `vite@^5` `tailwindcss@^3` `@tailwindcss/typography@^0.5` `lucide-react@latest`

CONSTRAINTS: editorial restraint — motion 0.4–0.8s reveals only, easing from {cubic-bezier(0.16,1,0.3,1) · cubic-bezier(0.22,1,0.36,1) · cubic-bezier(0.65,0,0.35,1)}, never ease-in; animate only transform/opacity (the TOC color transition is the sole paint exception). ONE accent hue (#B4531F) — emphasis comes from italic serif, the drop cap, and thin rules, not color. No video, no glassmorphism, no decorative gradients, no parallax. Replace `{YOUR_IMAGE_URL_*}` with media you have rights to, with real `alt` text. Respect `prefers-reduced-motion` (block above). Semantic HTML: `<article>`, `<figure>`, `<nav aria-label>`, one `<h1>`.
