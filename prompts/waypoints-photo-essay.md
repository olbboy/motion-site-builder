# Waypoints — Overland from Hà Giang to Cao Bằng

- **ID:** `waypoints-photo-essay`
- **Category:** Travel / Photo Essay
- **Type:** longread photo essay
- **Profile:** `editorial`

---

Build a single-page photo essay for "Waypoints" — a travel journal — titled "Overland from Hà Giang to Cao Bằng". Photography carries the page; motion stays out of its way. Use React + Vite + Tailwind CSS + TypeScript + lucide-react. Default Tailwind config, no other UI libraries.

FONTS (Google Fonts, load via `<link>` in index.html)
- Display: Spectral (500/600, italic) — masthead, chapter titles, pull quotes, drop cap
- Body: Lora (400/500, italic) — standfirst, opening paragraphs, captions
- UI: Inter (400/500) — byline, meta, journal number

COLORS (CSS variables on :root — paper family, light only)
- --paper: #FBF9F4 · --ink: #221D18 · --accent: #BB5B34 (terracotta — the ONLY accent hue)
- Text tiers: ink at 100% / 75% / 60%. Rules and borders: `#221D18` at 10%

GLOBAL CSS (paste verbatim)
```css
@keyframes ed-reveal { from { opacity: 0; transform: translateY(16px); } to { opacity: 1; transform: none; } }
.reveal { animation: ed-reveal 0.65s cubic-bezier(0.22, 1, 0.36, 1) backwards; }

@keyframes ed-image-in { from { opacity: 0; transform: scale(1.02); } to { opacity: 1; transform: none; } }
.img-reveal { animation: ed-image-in 0.7s cubic-bezier(0.16, 1, 0.3, 1) backwards; }

.route-progress { transform-origin: left; transform: scaleX(var(--p, 0)); }

@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { animation-duration: 0.01ms !important; animation-iteration-count: 1 !important; transition-duration: 0.01ms !important; }
}
```

ROUTE PROGRESS BAR (fixed top-0, z-30)
- `h-[2px] w-full bg-[var(--accent)] route-progress` — set `--p` (0→1) from a passive scroll listener tracking position through the whole essay; pure `transform: scaleX`, no width animation, no easing (directly bound to scroll)
- 4 waypoint markers: small dots (`w-1.5 h-1.5 rounded-full absolute top-1/2 -translate-y-1/2`) positioned at each chapter's scroll offset along the bar; each fills from `bg-[var(--ink)]/20` to `bg-[var(--accent)]` (color-only transition, 200ms `cubic-bezier(0.16, 1, 0.3, 1)`) once that chapter's own IntersectionObserver fires — the bar's scaleX itself never eases

MASTHEAD (sticky top-[2px], z-20, bg-[var(--paper)]/95 backdrop-blur-sm, border-b border-[#221D18]/10 — persistent, no reveal)
- Left: "Waypoints" — Spectral italic text-xl
- Right: "Journal 04 — Northern Loop" — Inter text-xs ink 60%

TITLE BLOCK (`<main>` starts here; max-w-[70ch] mx-auto px-6 pt-20 pb-10, staggered `.reveal`: kicker 0ms → H1 100ms → standfirst 220ms → byline 340ms)
- Kicker: "FIELD JOURNAL · VIETNAM" — Inter text-xs font-medium tracking-[0.16em] uppercase text-[var(--accent)]
- H1: "Overland from Hà Giang to Cao Bằng" — Spectral font-semibold text-5xl md:text-7xl leading-[1.05], ink 100%
- Standfirst: "Three hundred kilometers of switchbacks, one motorbike with a failing clutch, and the parts of the Đồng Văn Karst Plateau that don't show up on a map." — Lora italic text-xl md:text-2xl leading-relaxed, ink 75%
- Byline row (border-t border-[#221D18]/10 pt-4): "Words & photographs by Minh Tran · 14 min read" — Inter text-sm ink 60%

OPENING (max-w-[65ch] mx-auto px-6 pb-16)
- First paragraph carries a drop cap: `p:first-of-type::first-letter { font-family: 'Spectral', serif; float: left; font-size: 3.6em; line-height: 0.85; padding-right: 0.08em; color: var(--accent); }`
- Paragraph 1 (Lora text-lg leading-relaxed, ink 90%): "The road out of Hà Giang climbs before it does anything else. It doesn't ease you into the mountains — it takes the switchbacks in the first ten minutes, past the last petrol station with a roof, past the last flat stretch of anything, and then it just keeps going up. By the time the valley opens out below Quản Bạ, the town is a rumor behind you and the karst towers are close enough to touch the cloud line."
- Paragraph 2 (Lora text-lg leading-relaxed, ink 75%): "Nobody warns you how loud silence is up here. No traffic, no construction, just wind moving through corn planted in rock. We stopped counting switchbacks after the ninetieth one and started counting the times the road disappeared into a bank of cloud and came back somewhere else entirely."

CHAPTER 1 — full-bleed figure (`relative left-1/2 right-1/2 -mx-[50vw] w-screen`)
- `<img src="{YOUR_IMAGE_URL_1}" alt="A single-lane road cut into a sheer limestone cliff face along the Mã Pí Lèng Pass, motorbike parked at the edge, valley floor 800 meters below" className="w-full h-[70vh] md:h-[85vh] object-cover img-reveal">` (IntersectionObserver threshold 0.2, animate once)
- `<figcaption>` (max-w-[65ch] mx-auto px-6 pt-3, Lora italic text-sm ink 60%): "The pass cuts along the cliff face for 20 kilometers — locals call this stretch 'the pathway to heaven.'"
- Below (max-w-[65ch] mx-auto px-6 pt-10, `.reveal` on scroll, threshold 0.2): H2 "The Pass That Doesn't Warn You" — Spectral text-3xl leading-snug ink 100%; paragraph (Lora leading-relaxed ink 90%): "There's no sign before Mã Pí Lèng, no overlook to prepare you. The road just narrows, the guardrail disappears, and the valley opens on your left like the floor fell out of the world."

PULL QUOTE 1 (max-w-[65ch] mx-auto px-6 my-4, border-l-2 border-[var(--accent)] pl-6): "The pass doesn't reveal itself gradually. It arrives all at once, the valley falling away on both sides of a road cut straight into the rock." — Spectral italic text-3xl leading-snug ink 100%

CHAPTER 2 — full-bleed figure
- `<img src="{YOUR_IMAGE_URL_2}" alt="Hmong and Tày vendors laying out indigo-dyed fabric, dried corn, and silver jewelry on tarpaulins at the Sunday market in Đồng Văn's old quarter" className="w-full h-[70vh] md:h-[85vh] object-cover img-reveal">`
- `<figcaption>`: "Đồng Văn's Sunday market draws traders down from villages a full day's walk away."
- H2 "A Market That Runs on One Day a Week" — Spectral text-3xl ink 100%; paragraph: "Everything here happens on Sunday. The rest of the week the square is just a square — by seven in the morning it's a market that took generations to schedule and will be gone again by two."

CHAPTER 3 — full-bleed figure
- `<img src="{YOUR_IMAGE_URL_3}" alt="A river valley near Cao Bằng at golden hour, terraced rice fields following the contour of the water, low mist over the far ridgeline" className="w-full h-[70vh] md:h-[85vh] object-cover img-reveal">`
- `<figcaption>`: "The descent toward Cao Bằng trades limestone for water — the Quây Sơn river shows up before the road does."
- H2 "Where the Karst Gives Way to Water" — Spectral text-3xl ink 100%; paragraph: "Cao Bằng announces itself with rice terraces instead of cliffs. After four days of rock, the sound of the river feels almost too soft to be real."

PULL QUOTE 2 (border-l-2 border-[var(--accent)] pl-6, max-w-[65ch] mx-auto px-6 my-4): "You don't arrive in Cao Bằng so much as you notice, slowly, that the mountains have stopped trying to kill you." — Spectral italic text-3xl leading-snug ink 100%

END MATTER (max-w-[65ch] mx-auto px-6 pb-12)
- "Next in the series" — teaser link: "Journal 05 — The Bạch Mã Cloud Road" (Spectral text-2xl) + dek (Lora italic ink 75%) — hover = gated scaleX underline on the title, press `active:scale-[0.98]`

FOOTER (border-t border-[#221D18]/10, py-12, max-w-[65ch] mx-auto px-6, Inter text-sm ink 60%)
- "Waypoints — dispatches from the road, twice a season." + links Archive / About / `Rss` icon "RSS feed" (`aria-label="RSS feed"`)

ANIMATIONS (complete list — restraint is the brief)
- Load: title block 4-element stagger, 0.65s each, delays 0/100/220/340ms
- Scroll: each full-bleed image gets `.img-reveal` once (opacity + scale 1.02→1, no translate — deliberately not parallax), 0.7s; each H2 section gets `.reveal` once, 0.65s; both `cubic-bezier(0.16, 1, 0.3, 1)` or `cubic-bezier(0.22, 1, 0.36, 1)`
- Route progress bar scaleX is bound directly to scroll position — no duration, no easing; waypoint dots fill color-only, 200ms, on chapter entry
- Hover: teaser-link underline scaleX 200ms (gated) · Press: `active:scale-[0.98]` on links
- Nothing loops, nothing bounces, no parallax — images arrive once and stay still

RESPONSIVE
- Mobile: full-bleed images stay full-bleed (100vw) at `h-[55vh]`; title block px-6, H1 text-4xl; drop cap scales to 2.8em; route progress bar and its markers remain visible at all breakpoints
- The reading column (title, opening, chapter text, captions) is ALWAYS ≤ 65–70ch; only figures break the column

KEY DEPENDENCIES
`react@^18` `react-dom@^18` `typescript@^5` `vite@^5` `tailwindcss@^3` `lucide-react@latest`

CONSTRAINTS: editorial restraint — reveals 0.4–0.8s, easing from {cubic-bezier(0.16,1,0.3,1) · cubic-bezier(0.22,1,0.36,1) · cubic-bezier(0.65,0,0.35,1)}, never ease-in; animate only transform/opacity (image reveals use scale + opacity, never translate tied to scroll position — that's parallax, and it's excluded here). ONE accent hue (#BB5B34). No video, no glassmorphism, no decorative gradients, no carousel. Replace `{YOUR_IMAGE_URL_*}` with media you have rights to — every image ships with the real `alt` text specified above. Respect `prefers-reduced-motion` (block above). Semantic HTML: `<main>`, `<figure>` + `<figcaption>` per chapter, `<nav aria-label>` where applicable, one `<h1>`.
