# The Slow Post

- **ID:** `slowpost-newsletter-issue`
- **Category:** Newsletter
- **Type:** newsletter issue
- **Profile:** `editorial`

---

Build a single-page newsletter issue for "The Slow Post" — a weekly slow-living newsletter — plus an archive strip of past issues. Typography reads like a letter; motion stays quiet. Use React + Vite + Tailwind CSS + TypeScript + lucide-react. Default Tailwind config, no other UI libraries.

FONTS (Google Fonts, load via `<link>` in index.html)
- Display: Source Serif 4 (500/600, italic) — masthead, salutation, section titles
- Body: Literata (400/500) — letter paragraphs, recommendation deks
- UI: Inter (400/500) — meta, archive labels, form

COLORS (CSS variables on :root — paper family, light only)
- --paper: #FDFBF6 · --wash: #F3EFE4 · --ink: #24231D · --accent: #5B6E4F (sage green — the ONLY accent hue)
- Text tiers: ink at 100% / 75% / 60%. Rules and borders: `#24231D` at 10%

GLOBAL CSS (paste verbatim)
```css
@keyframes ed-reveal { from { opacity: 0; transform: translateY(14px); } to { opacity: 1; transform: none; } }
.reveal { animation: ed-reveal 0.6s cubic-bezier(0.16, 1, 0.3, 1) backwards; }

.archive-strip { scroll-snap-type: x mandatory; }
.archive-card { scroll-snap-align: start; }

@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { animation-duration: 0.01ms !important; animation-iteration-count: 1 !important; transition-duration: 0.01ms !important; }
}
```

MASTHEAD (`<main>` starts here; max-w-[65ch] mx-auto px-6 pt-20 pb-8 text-center, `.reveal` delay 0ms)
- "The Slow Post" — Source Serif 4 italic text-3xl ink 100%
- "Issue №42 · July 13, 2026" — Inter text-sm tracking-[0.08em] ink 60%, mt-2
- Thin rule (border-t border-[#24231D]/10, mt-6, w-16 mx-auto)

LETTER BODY (max-w-[65ch] mx-auto px-6 pb-16, `.reveal` delay 120ms)
- Salutation: "Dear reader," — Source Serif 4 italic text-2xl ink 100%, mb-6
- Paragraph 1 (Literata text-lg leading-relaxed ink 90%): "There's a particular kind of relief in doing one thing at a time. Not because multitasking is a moral failure, but because the alternative — half-attention spread across six tabs — never actually feels like rest, even when it looks like it from the outside."
- Paragraph 2 (Literata text-lg leading-relaxed ink 75%, mt-5): "This week we made a pot of black beans that took four hours and required nothing from us for three of them. We're recommending three things below that ask for the same kind of patience — a book, a conversation, a way of cooking. None of them are fast. That's the point."
- Sign-off (mt-8, Source Serif 4 italic text-xl ink 100%): "Slowly yours," + "— The Editors" (Inter text-sm ink 60%, not italic, mt-1)

THREE RECOMMENDATIONS (`<ol>` max-w-[65ch] mx-auto px-6 pb-16, `.reveal` once per item on scroll, IntersectionObserver threshold 0.15, one at a time)
- Each `<li>` (flex gap-5 items-baseline py-6 border-b border-[#24231D]/10 last:border-none): a numeral ("01" / "02" / "03" — Source Serif 4 text-3xl text-[var(--accent)] shrink-0 w-10) + a linked block (title + dek)
  - Title (Source Serif 4 text-xl ink 100%) — underline via scaleX pseudo-element on hover, gated `@media (hover: hover) and (pointer: fine)`, 200ms `cubic-bezier(0.16, 1, 0.3, 1)`; press `active:scale-[0.98]`
  - Dek (Literata text-base ink 75%, mt-1, max-w-[52ch])
- Items:
  1. "A pot of black beans, cooked slowly" — "No pressure cooker, no shortcuts — just low heat, a bay leaf, and four hours you weren't planning to get back."
  2. "The Ministry for the Future, revisited" — "A second read changes which chapters feel like warning and which feel like instructions."
  3. "A conversation with a beekeeper in Vermont" — "On reading weather the way her grandmother did, one hive at a time."

ARCHIVE STRIP (full-bleed, `relative left-1/2 right-1/2 -mx-[50vw] w-screen bg-[var(--wash)] py-10`, `.reveal` once as a whole strip on scroll)
- Label: "Past issues" — Inter text-xs uppercase tracking-[0.14em] ink 60%, max-w-[65ch] mx-auto px-6, mb-4
- `<ul role="list" className="archive-strip flex gap-4 overflow-x-auto px-6 pb-2 [scrollbar-width:thin]">` — native horizontal scroll, `scroll-snap-type: x mandatory` (no carousel plugin, no autoplay, no JS-driven track)
- Each `<li className="archive-card shrink-0 w-64 rounded-lg border border-[#24231D]/10 bg-[var(--paper)] p-5">`: "Issue №41" (Inter text-xs ink 60%) + "July 06, 2026" (Inter text-xs ink 60%) + title (Source Serif 4 text-lg ink 100%, mt-2, e.g. "On Keeping a Single Houseplant Alive") + "Read issue →" link (Inter text-sm text-[var(--accent)], mt-3), press `active:scale-[0.98]`
- 6 cards total, issues №41 down to №36, each with a distinct one-line title in the same voice (e.g. "The Forty-Minute Walk," "What a Sourdough Starter Teaches You About Waiting," "Letters We Never Sent")

SUBSCRIBE FORM (max-w-[65ch] mx-auto px-6 py-16 text-center, `.reveal` once on scroll)
- H2: "Get the next issue" — Source Serif 4 italic text-2xl ink 100%
- Dek: "One letter a week, always free, unsubscribe any time." — Inter text-base ink 75%, mt-2
- `<form className="mt-6 flex flex-col sm:flex-row items-center justify-center gap-3">`:
  - Input: `type="email"` `aria-label="Email address"` `rounded-md border border-[#24231D]/15 bg-[var(--paper)] px-4 py-2.5 text-sm w-72` — focus ring: `focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[var(--accent)] focus-visible:ring-offset-2 focus-visible:ring-offset-[var(--paper)]`
  - Button: "Subscribe" `bg-[var(--ink)] text-[var(--paper)] rounded-md px-5 py-2.5 text-sm font-medium`, hover bg ink 85% (color only, 150ms), press `active:scale-[0.98]`

FOOTER (border-t border-[#24231D]/10, py-12, max-w-[65ch] mx-auto px-6, Inter text-sm ink 60%)
- "The Slow Post — one letter a week, nothing else." + links Archive / About / `Rss` icon "RSS feed" (`aria-label="RSS feed"`)

ANIMATIONS (complete list — restraint is the brief)
- Load: masthead 0ms → letter body 120ms, `.reveal` fade-rise, 0.6s `cubic-bezier(0.16, 1, 0.3, 1)`
- Scroll: recommendations reveal one at a time, 0.6s, threshold 0.15; archive strip reveals once as a whole block, 0.6s; subscribe form reveals once, 0.6s
- Hover: recommendation and archive-card titles use the gated scaleX underline, 200ms · Press: `active:scale-[0.98]` on every link/button
- Archive strip scrolling is native touch/drag scroll with CSS `scroll-snap` — no JS autoplay, no easing, no carousel library
- Nothing loops, nothing bounces — a letter doesn't perform

RESPONSIVE
- Mobile: letter column stays ≤ 65ch at px-6; recommendation numerals shrink to w-8 text-2xl; archive cards stay `w-64` and scroll natively with touch (snap points every card); subscribe form stacks input above button, both `w-full`

KEY DEPENDENCIES
`react@^18` `react-dom@^18` `typescript@^5` `vite@^5` `tailwindcss@^3` `lucide-react@latest`

CONSTRAINTS: editorial restraint — reveals 0.4–0.8s, easing from {cubic-bezier(0.16,1,0.3,1) · cubic-bezier(0.22,1,0.36,1) · cubic-bezier(0.65,0,0.35,1)}, never ease-in; animate only transform/opacity (link color-only hovers are the sole paint exception). ONE accent hue (#5B6E4F). No video, no glass, no decorative gradients, no carousel plugin — the archive strip is plain CSS `scroll-snap`. Respect `prefers-reduced-motion` (block above). Semantic HTML: `<main>`, `<ol>` for the numbered recommendations, `<ul role="list">` for the archive strip, `aria-label` on the email input and icon-only buttons, visible focus ring on all inputs/links.
