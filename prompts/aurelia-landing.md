# Aurelia

- **ID:** `aurelia-landing`
- **Category:** Landing Page
- **Type:** landing
- **Profile:** `cinematic`

---

Build a single-page marketing landing page for "Aurelia" — an independent haute-horlogerie atelier that designs and hand-finishes exactly one wristwatch movement per year. Use React + Vite + Tailwind CSS + TypeScript + framer-motion + lucide-react. Default Tailwind config, no other UI libraries.

SECTION ORDER (narrative Hook → Proof → Detail → CTA)
1. Hero — Hook: a single caliber, once a year
2. Craft Philosophy — Proof: why the atelier refuses to scale
3. Movement Detail (sticky-stack) — Detail: the four hand-finished parts of Caliber AUR-01
4. Specifications — Detail: the numbers behind the caliber
5. Waitlist — CTA: reserve the 2027 allocation

FONTS
- Display (headline, section titles, movement numerals): Playfair Display (Google Fonts, 400/600 + italic) — applied via inline `fontFamily: 'Playfair Display'`
- Body (nav, copy, specs): Inter (400/500/600); specs and prices `tabular-nums`
- Import both in `index.css` via a Google Fonts `@import`

COLORS
- --background: #0B0906 (near-black warm bronze, `bg-[#0B0906]`)
- --foreground: #F7F2E7
- --muted-foreground: rgba(247,242,231,0.6)
- --accent: #C9A227 (single champagne-gold accent — glow, movement numerals, hairline hovers, CTAs, focus ring)

GLOBAL CSS (paste verbatim into `index.css`)
```css
.liquid-glass {
  background: rgba(255, 255, 255, 0.01);
  background-blend-mode: luminosity;
  backdrop-filter: blur(4px);
  -webkit-backdrop-filter: blur(4px);
  border: none;
  box-shadow: inset 0 1px 1px rgba(255, 255, 255, 0.1);
  position: relative;
  overflow: hidden;
}
.liquid-glass::before {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: inherit;
  padding: 1.4px;
  background: linear-gradient(180deg,
    rgba(255,255,255,0.45) 0%, rgba(255,255,255,0.15) 20%,
    rgba(255,255,255,0) 40%, rgba(255,255,255,0) 60%,
    rgba(255,255,255,0.15) 80%, rgba(255,255,255,0.45) 100%);
  -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  -webkit-mask-composite: xor;
  mask-composite: exclude;
  pointer-events: none;
}

/* large surfaces (movement cards, spec table) get a real hairline; liquid-glass stays for small pills */
.panel { background: rgba(247,242,231,0.03); border: 1px solid rgba(247,242,231,0.08); }

.text-glow { text-shadow: 0 0 40px rgba(247,242,231,0.26), 0 0 90px rgba(201,162,39,0.24); }

@keyframes unveil {
  from { opacity: 0; transform: translateY(26px); filter: blur(6px); }
  to   { opacity: 1; transform: translateY(0);    filter: blur(0); }
}
.animate-unveil         { animation: unveil 1s cubic-bezier(0.16, 1, 0.3, 1) both; }
.animate-unveil-delay-1 { animation: unveil 1s cubic-bezier(0.16, 1, 0.3, 1) 0.18s both; }
.animate-unveil-delay-2 { animation: unveil 1s cubic-bezier(0.16, 1, 0.3, 1) 0.36s both; }
.animate-unveil-delay-3 { animation: unveil 1s cubic-bezier(0.16, 1, 0.3, 1) 0.54s both; }

@media (prefers-reduced-motion: reduce) {
  .animate-unveil, .animate-unveil-delay-1, .animate-unveil-delay-2, .animate-unveil-delay-3 {
    animation: none; opacity: 1; transform: none; filter: none;
  }
  *, *::before, *::after {
    animation-duration: 0.01ms !important; animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important; scroll-behavior: auto !important;
  }
}
```

SCROLL REVEAL (Framer Motion — every section heading/body/card beyond the hero)
- Base props: `initial={{ opacity: 0, y: 28, filter: 'blur(6px)' }} whileInView={{ opacity: 1, y: 0, filter: 'blur(0px)' }} viewport={{ once: true, amount: 0.3 }} transition={{ duration: 0.9, ease: [0.16, 1, 0.3, 1] }}`
- Grouped children (spec rows, movement-card copy) add `transition={{ ...base, delay: i * 0.1 }}` on top of the base transition
- Gate everything behind `useReducedMotion()`: when true, skip the `initial`/`whileInView` props entirely so content renders at its final state with no scroll-jacking

VIDEO BACKGROUND (hero only, z-0)
- `<video autoPlay muted loop playsInline poster="{YOUR_POSTER_URL}" aria-hidden="true">` — `absolute inset-0 h-full w-full object-cover`
- src: `{YOUR_VIDEO_URL}` — supply your own licensed footage: a static macro close-up of a balance wheel ticking, shallow depth of field, slow rack focus, no visible seam at the loop point
- Gradient overlay (z-[1]): `absolute inset-0 bg-gradient-to-t from-[#0B0906] via-[#0B0906]/20 to-[#0B0906]/70`

NAVBAR (z-20, sticky, glass pill)
- Wrapper: `<nav aria-label="Primary" className="sticky top-0 z-20 px-6 py-5">`
- Pill: `.liquid-glass rounded-full max-w-5xl mx-auto px-6 py-3 flex items-center justify-between`
- Left: lucide `Watch` icon (16px, `text-[#C9A227]`) + "Aurelia" (text-lg font-semibold tracking-tight text-[#F7F2E7])
- Center (hidden md:flex, gap-8, ml-8): Philosophy · The Movement · Specifications — `text-sm text-[#F7F2E7]/70 hover:text-[#F7F2E7] transition-colors`, each linking to its section `id`
- Right: "Join the waitlist" — `bg-[#C9A227] text-[#0B0906] rounded-full px-6 py-2 text-sm font-medium transition-transform hover:scale-[1.03] active:scale-[0.97]`

1 · HERO (`id="hero"`, z-10, h-screen, flex flex-col items-center justify-center text-center px-6)
- Eyebrow (`.animate-unveil`): "ONE MOVEMENT. ONE YEAR. NO EXCEPTIONS." — text-xs tracking-[0.22em] text-[#C9A227] mb-5
- H1 (`.animate-unveil-delay-1 .text-glow`): "Time, <em class=\"italic\">unhurried</em>." — text-5xl sm:text-7xl md:text-8xl, Playfair Display, leading-[0.95], tracking-tight, text-[#F7F2E7]
- Subtext (`.animate-unveil-delay-2`): "Aurelia designs a single wristwatch movement each year — hand-finished, individually numbered, and never repeated." — text-sm sm:text-base text-[#F7F2E7]/65 max-w-md mx-auto mt-5 leading-relaxed
- CTA row (`.animate-unveil-delay-3`, mt-8 flex flex-col sm:flex-row gap-3 items-center justify-center):
  - "Join the 2027 waitlist" — `bg-[#C9A227] text-[#0B0906] rounded-full px-8 py-3.5 text-base font-medium transition-transform hover:scale-[1.03] active:scale-[0.97]`
  - "See the movement →" — `.liquid-glass rounded-full px-6 py-3.5 text-base text-[#F7F2E7] transition-transform hover:scale-[1.03] active:scale-[0.97]`

2 · CRAFT PHILOSOPHY (`id="philosophy"`, py-28, max-w-6xl mx-auto px-6, grid md:grid-cols-2 gap-16 items-center — text left, image right)
- Eyebrow: "01 · Why scarcity is the point" — text-xs tracking-[0.22em] text-[#C9A227] mb-4
- H2 (Playfair Display, text-4xl md:text-5xl leading-[1.05]): "We build <em class=\"italic\">one</em> thing, once."
- Body 1 (mt-6, max-w-lg, text-base text-[#F7F2E7]/70 leading-relaxed): "Every Aurelia atelier ships a single caliber a year — no variants, no reissues, no second batch. The watchmaker who starts a movement in January is the one who cases it in December."
- Body 2 (mt-4, max-w-lg, text-base text-[#F7F2E7]/70 leading-relaxed): "We turned down three retailers this year. An atelier that says yes to everyone eventually says yes to nothing in particular."
- Image: `{YOUR_IMAGE_URL_1}` — `rounded-2xl aspect-[4/5] object-cover w-full` (the watchmaker's bench, replace with media you have rights to)

3 · MOVEMENT DETAIL — STICKY STACK (`id="movement"`, py-28, text-center)
- Eyebrow: "02 · Inside Caliber AUR-01" — text-xs tracking-[0.22em] text-[#C9A227] mb-4
- H2 (Playfair Display, text-4xl md:text-5xl mb-16): "Four parts. <em class=\"italic\">One</em> year."
- Scroll container: `relative h-[400vh]` wrapping a `ref={containerRef}`; `useScroll({ target: containerRef, offset: ['start start', 'end end'] })`
- 4 sticky cards (n = 4), each `.panel rounded-2xl grid md:grid-cols-2 gap-10 p-10 md:p-14 max-w-5xl mx-auto items-center sticky`, `style={{ top: `calc(8vh + ${i * 24}px)` }}`
- Per-card scale: `targetScale = 1 - (n - 1 - i) * 0.03`; `scale: useTransform(scrollYProgress, [i / n, 1], [1, targetScale])` — card content itself does NOT fade, only scale changes, so each stays fully legible while stacked
- Card layout: left — ghost numeral (Playfair Display, text-8xl md:text-9xl, `text-[#C9A227]/20`, leading-none, "01"–"04"); right — title (text-2xl md:text-3xl, Playfair Display, text-[#F7F2E7]) + description (text-sm text-[#F7F2E7]/65 mt-3 max-w-sm)
- Card content (index → numeral / title / description):
  1. "01" — Mainplate & Bridges — "Hand-beveled German silver, black-polished by hand under a loupe — eighteen hours per bridge." (targetScale 0.91)
  2. "02" — Escapement — "A free-sprung balance beating at 21,600 vph, regulated over six weeks before it ever sees a case." (targetScale 0.94)
  3. "03" — Micro-Rotor — "A 950-platinum rotor, half the thickness of a standard automatic, so the caliber stays 4.1mm thin." (targetScale 0.97)
  4. "04" — Case & Crystal — "38mm of 950 platinum, box-domed sapphire front and back — the movement is meant to be seen, not hidden." (targetScale 1.00)

4 · SPECIFICATIONS (`id="specifications"`, py-28, max-w-3xl mx-auto px-6)
- Eyebrow: "03 · Caliber AUR-01 — specifications" — text-xs tracking-[0.22em] text-[#C9A227] mb-4
- H2 (Playfair Display, text-4xl md:text-5xl mb-10): "Every number, <em class=\"italic\">accounted for</em>."
- Table: `.panel rounded-2xl divide-y divide-[#F7F2E7]/10`; each row (`SpecRow`) `px-8 py-5 flex items-center justify-between text-sm hover:bg-white/[0.02] transition-colors`; label `text-[#F7F2E7]/60`; value `text-[#F7F2E7] font-medium tabular-nums`
- Rows: Movement — "Manual-wind, in-house" · Power reserve — "72 hours" · Frequency — "21,600 vph (3 Hz)" · Jewels — "31" · Case — "38mm · 950 platinum" · Crystal — "Sapphire, box-domed front & back" · Water resistance — "30m" · Production — "1 per year, individually numbered"

5 · WAITLIST CTA + FOOTER (`id="waitlist"`, py-32, text-center, max-w-xl mx-auto px-6)
- Eyebrow: "04 · Reserve your allocation" — text-xs tracking-[0.22em] text-[#C9A227] mb-4
- H2 (Playfair Display, text-4xl md:text-6xl leading-[1.05]): "The 2027 movement. <em class=\"italic\">One</em> collector."
- Form (mt-8, flex flex-col sm:flex-row gap-3): email input `.liquid-glass rounded-full px-6 py-3.5 text-sm text-[#F7F2E7] placeholder-[#F7F2E7]/40 flex-1` placeholder "you@domain.com" + submit "Request an allocation" `bg-[#C9A227] text-[#0B0906] rounded-full px-8 py-3.5 text-sm font-medium transition-transform hover:scale-[1.03] active:scale-[0.97]`
- Fine print (mt-4, text-xs text-[#F7F2E7]/50): "No deposit today. Confirmed collectors are contacted in production order, one email, once a year."
- Footer (`border-t border-[#F7F2E7]/10 pt-8 pb-10 mt-20 flex flex-col sm:flex-row justify-between gap-4 text-xs text-[#F7F2E7]/50`): "© Aurelia — one movement, one year." + links "Philosophy" / "Instagram" / "Press" (`hover:text-[#F7F2E7] transition-colors`)

REUSABLE COMPONENTS
- `MovementCard` — props `{ index: number; total: number; numeral: string; title: string; description: string }`; renders the sticky `.panel` card described in §3; scale bound via `useTransform(scrollYProgress, [index / total, 1], [1, 1 - (total - 1 - index) * 0.03])`; sticky offset `top: calc(8vh + ${index * 24}px)`.
- `SpecRow` — props `{ label: string; value: string }`; `px-8 py-5 flex items-center justify-between text-sm border-b border-[#F7F2E7]/10 last:border-b-0 hover:bg-white/[0.02] transition-colors`.
- `WaitlistForm` — controlled email input + submit button per the markup in §5; submit button `disabled` state drops to `opacity-50 cursor-not-allowed` while `status === 'loading'`; on success the label swaps to "You're on the list" for 3000ms (`setTimeout`) then reverts to "Request an allocation".

ANIMATIONS (complete inventory)
- Hero entrance: `unveil` 1s cubic-bezier(0.16, 1, 0.3, 1), staggered — eyebrow 0s · H1 0.18s · subtext 0.36s · CTA 0.54s
- Section entrance (Philosophy, Specifications, Waitlist): Framer `whileInView`, 0.9s cubic-bezier(0.16, 1, 0.3, 1), rise 28px, blur 6px → 0, `once: true`, `amount: 0.3`; grouped children stagger 0.1s
- Movement sticky-stack: scroll-linked `scale` only (1 → 0.91 / 0.94 / 0.97 / 1.00 per card) — no opacity change, cards stay fully legible while stacked
- Hover: buttons and nav links scale 1.03 or color-only (150ms); spec rows `background-color` 150ms
- Press: `active:scale-[0.97]` on every button
- Animate only transform / opacity / filter

KEY DEPENDENCIES
`react@^18` `react-dom@^18` `typescript@^5` `vite@^5` `tailwindcss@^3` `framer-motion@^11` `lucide-react@latest`

RESPONSIVE
- Mobile: H1 text-5xl; philosophy grid stacks to a single column (image below text); movement cards drop to single-column `p-6`, numeral shrinks to text-6xl; specifications table stays full-width with `px-5`; waitlist form stacks the input above the button; nav center links hidden below `md`; no horizontal scroll anywhere.

CONSTRAINTS: cinematic minimalism — warm near-black background, ONE champagne-gold accent used sparingly (glow, numerals, hairline hovers, CTAs), no decorative blobs or radial gradients (the hero video and hairline `.panel` surfaces provide all depth). Default Tailwind config, no UI libraries beyond `framer-motion` and `lucide-react`. Only animate transform/opacity/filter; the movement-stack cards scale only, never a layout-shifting property. Respect `prefers-reduced-motion` and gate every `whileInView`/`useScroll` effect behind `useReducedMotion()` — the stack freezes at its resting scale and sections render fully visible with no scroll-jacking. ARIA label on nav; `aria-hidden` on the decorative hero video; `poster` fallback required. Press feedback (`active:scale-[0.97]`) on every button. Replace `{YOUR_VIDEO_URL}` / `{YOUR_POSTER_URL}` / `{YOUR_IMAGE_URL_1}` with media you have rights to.
