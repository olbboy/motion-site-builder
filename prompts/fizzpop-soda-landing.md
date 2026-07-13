# FizzPop Soda

- **ID:** `fizzpop-soda-landing`
- **Category:** Consumer Brand
- **Type:** landing
- **Profile:** `playful`

---

Build a single-page DTC landing page for "FizzPop" — a craft soda brand that refuses to be quiet. Loud color, bouncy springs, sticker energy; the maximalist counterpart to cinematic's hush. Use React + Vite + Tailwind CSS + TypeScript + lucide-react. Default Tailwind config, no other UI libraries.

FONTS (Google Fonts, load via `<link>` in index.html)
- Display: Bricolage Grotesque (700/800) — headlines, flavor names
- Body: Space Grotesk (400/500/700) — everything else

COLORS (CSS variables on :root — candy family; decorative color IS the identity here)
- --cream: #FFF8F0 (background) · --ink: #1A1A2E (foreground)
- Accents (all four earn their keep): --pink: #FF5C8A · --violet: #7C3AED · --cyan: #22D3EE · --lemon: #FACC15
- Hard-shadow trick: solid offset shadows in ink (`shadow-[0_6px_0_#1A1A2E]`), never soft blurs — shadows stay neutral so the four accents stay exactly four

GLOBAL CSS (paste verbatim)
```css
@keyframes pop-in { from { opacity: 0; transform: scale(0.9) translateY(12px); } to { opacity: 1; transform: none; } }
.pop { animation: pop-in 0.5s cubic-bezier(0.18, 0.89, 0.32, 1.28) backwards;   /* back-out overshoot */
       transition: transform 160ms cubic-bezier(0.34, 1.56, 0.64, 1); }
.pop:active { transform: scale(0.94); }
@media (hover: hover) { .pop:hover { transform: scale(1.06) rotate(-1.5deg); } }

@keyframes float-y { 0%,100% { transform: translateY(0) rotate(-6deg); } 50% { transform: translateY(-6px) rotate(-6deg); } }
.sticker { animation: float-y 3s cubic-bezier(0.65, 0, 0.35, 1) infinite;
           transition: transform 200ms cubic-bezier(0.34, 1.56, 0.64, 1); }
@media (hover: hover) { .sticker:hover { transform: scale(1.08) rotate(3deg); } }

@keyframes marquee-x { from { transform: translateX(0); } to { transform: translateX(-50%); } }
.marquee-track { animation: marquee-x 24s linear infinite; }

@media (prefers-reduced-motion: reduce) {
  .sticker, .marquee-track { animation: none; }
  *, *::before, *::after { animation-duration: 0.01ms !important; animation-iteration-count: 1 !important; transition-duration: 0.01ms !important; }
}
```

DECOR LAYER (z-[5], `aria-hidden="true"`, pointer-events-none — shapes are the brand, not clutter)
- Top-right: blob `w-[480px] h-[480px] rounded-full bg-gradient-to-br from-[var(--pink)] to-[var(--violet)] opacity-20 blur-3xl`
- Mid-left: `w-64 h-64 rounded-full border-[6px] border-dashed border-[var(--cyan)] opacity-30` rotated 12deg
- Near the CTA: hand-drawn squiggle as inline SVG stroke `var(--lemon)` strokeWidth 6
- Decor is static — entrances and stickers move, wallpaper doesn't

NAVBAR (z-20, max-w-6xl mx-auto px-6 py-5, flex justify-between)
- Left: "FizzPop" — Bricolage 800 text-2xl, with the final "!" in `--pink` ("FizzPop!")
- Links (hidden md:flex, Space Grotesk 500 text-sm): Flavors · Story · Find us — hover = marker underline: `scaleX` pseudo-element h-1 bg-[var(--lemon)] rounded-full, `transform-origin: left`, 0→1 in 200ms cubic-bezier(0.23, 1, 0.32, 1), gated `@media (hover: hover) and (pointer: fine)`
- Right: cart button `rounded-full bg-[var(--ink)] text-[var(--cream)] px-5 py-2 text-sm font-bold` "Cart (0)", hover scale 1.06 (spring 160ms), `active:scale-[0.94]`

HERO (z-10, max-w-6xl mx-auto px-6 pt-12 pb-24, grid md:grid-cols-2 gap-10 items-center)
- Left column (staggered `.pop` entrance — badge 0ms, H1 90ms, sub 180ms, CTA 270ms via `animation-delay`):
  - Sticker badge (paste verbatim): `<span className="sticker inline-block rounded-2xl bg-[var(--lemon)] px-3 py-1 text-sm font-black text-[var(--ink)]">NEW! YUZU CRUSH</span>`
  - H1 — Bricolage 800, text-5xl md:text-7xl leading-[0.95]: "Fizz first." on line 1, "Questions later." on line 2 with "later." wrapped in a `rounded-2xl bg-[var(--pink)] text-[var(--cream)] px-3 inline-block -rotate-1`
  - Sub (Space Grotesk text-lg, ink 85%, max-w-md): "Small-batch soda with big-batch personality. Real fruit, real bubbles, zero apologies."
  - CTA (paste verbatim): `<button className="pop rounded-full bg-[var(--pink)] px-8 py-4 text-lg font-bold text-white shadow-[0_6px_0_#1A1A2E]">Grab a 6-pack →</button>` + secondary text link "Find a store" (ink, marker underline on hover)
- Right column: can lineup `<img src="{YOUR_IMAGE_URL_HERO}" alt="Three FizzPop cans">` rounded-3xl, entering `.pop` at 200ms; behind it a `rounded-full bg-[var(--cyan)]/30 blur-2xl` glow (decor layer)

MARQUEE (border-y-4 border-[var(--ink)], bg-[var(--lemon)], py-3, overflow-hidden)
- `.marquee-track` = two identical inline flex halves (total 200% width) so `translateX(-50%)` loops seamlessly, 24s linear infinite
- Content: "FIZZ ✺ POP ✺ CRUSH ✺ REPEAT ✺ " ×8 — Bricolage 700 text-xl uppercase text-[var(--ink)], `aria-hidden="true"` (pure decoration)

FLAVOR GRID (max-w-6xl mx-auto px-6 py-24)
- H2 `.pop` when in view: "Pick your poison. (It's soda.)" — Bricolage 800 text-4xl md:text-5xl
- 4 cards, grid sm:grid-cols-2 lg:grid-cols-4 gap-6, entering `.pop` via IntersectionObserver once, stagger 90ms (`animation-delay: 0/90/180/270ms`):
  1. "Yuzu Crush" — card `rounded-2xl bg-[var(--lemon)]/40 border-4 border-[var(--ink)] p-6`
  2. "Hibiscus Riot" — bg-[var(--pink)]/30
  3. "Cucumber Cool" — bg-[var(--cyan)]/30
  4. "Grape Static" — bg-[var(--violet)]/25
- Each card: can shot `<img src="{YOUR_IMAGE_URL_N}" alt="…">`, flavor name Bricolage 700 text-2xl, one-liner Space Grotesk text-sm ink 85% ("Tart enough to raise both eyebrows."), price "$3.50" font-bold tabular-nums
- Card hover (gated `@media (hover: hover) and (pointer: fine)`): `scale(1.06) rotate(1.5deg)` spring 200ms cubic-bezier(0.34, 1.56, 0.64, 1); press `active:scale-[0.94]`; alternate cards rotate −1.5deg

WALL OF LOVE (bg-[var(--ink)] text-[var(--cream)] py-24, rounded-t-[3rem])
- H2: "People are yelling about us" — Bricolage 800 text-4xl, with "yelling" in `--lemon`
- 3 quote cards `rounded-2xl bg-[var(--cream)]/10 p-6`, each rotated (−2deg / 1deg / −1deg), `.pop` in view stagger 90ms:
  - "I have a favorite carbonation now. That's where I'm at." — Dana R.
  - "The grape one tastes like a Saturday." — Mo K.
  - "Five stars, my fridge is 40% FizzPop." — Priya L.
- Stars row: 5× lucide `Star` filled `--lemon`, w-4 h-4

FINAL CTA (max-w-4xl mx-auto px-6 py-24 text-center)
- Panel `rounded-3xl bg-[var(--violet)] text-white p-12 relative overflow-hidden` with two `--pink`/`--cyan` blob glows inside (decor)
- H2 Bricolage 800 text-4xl md:text-6xl: "Thirsty yet?" · sub "Free shipping on 2+ packs. Cancel your seltzer."
- CTA `.pop` verbatim styling but bg-[var(--lemon)] text-[var(--ink)] shadow-[0_6px_0_#1A1A2E]: "Build your pack"

FOOTER (py-10, max-w-6xl mx-auto px-6, flex justify-between, Space Grotesk text-sm ink 85%)
- "© FizzPop Beverage Co." + links Instagram / TikTok / Wholesale (`aria-label` on icon links); sticker "★ made loud in Saigon" rotated −3deg

ANIMATIONS (complete list)
- Entrances: `.pop` 0.5s back-out cubic-bezier(0.18, 0.89, 0.32, 1.28), stagger 90ms, once per element (load for hero, IntersectionObserver for below-fold)
- Idle: `.sticker` float-y 3s loop (reduced-motion: none) · marquee 24s linear loop
- Hover: spring scale ≤1.08 + rotate ≤3deg, 160–200ms cubic-bezier(0.34, 1.56, 0.64, 1), always gated behind `@media (hover: hover)`
- Press: `active:scale-[0.94]` on every button; text links `active:scale-[0.98]`

RESPONSIVE
- Mobile: single column hero (image first), flavor grid 1→2→4, marquee text-base, final CTA p-8; no horizontal scroll (blobs are `overflow-hidden` inside their sections)

KEY DEPENDENCIES
`react@^18` `react-dom@^18` `typescript@^5` `vite@^5` `tailwindcss@^3` `lucide-react@latest`

CONSTRAINTS: playful maximalism, engineered — all four accents and the decorative gradients/shapes are intentional (this profile inverts the cinematic no-decor rule), but motion still only animates transform/opacity, easing only from {cubic-bezier(0.34,1.56,0.64,1) · cubic-bezier(0.18,0.89,0.32,1.28) · cubic-bezier(0.23,1,0.32,1) · cubic-bezier(0.65,0,0.35,1)}, never ease-in, no `transition: all`, and every entrance starts at scale 0.9 or above — nothing pops in from zero. Bounce is for deliberate moments (entrances, CTA, stickers) — nav links and the cart count don't wobble. Respect `prefers-reduced-motion` (stickers and marquee stop dead). Replace `{YOUR_IMAGE_URL_*}` with media you have rights to. ARIA labels on icon-only links; decorative shapes and the marquee are `aria-hidden`.
