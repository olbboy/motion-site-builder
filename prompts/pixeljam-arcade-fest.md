# PixelJam Arcade Fest

- **ID:** `pixeljam-arcade-fest`
- **Category:** Event / Campaign
- **Type:** event
- **Profile:** `playful`

---

Build a single-page event site for "PixelJam Arcade Fest" — three neon nights of indie games, chiptune sets, and high-score grudges. Nov 14–16, Warehouse 22, Da Nang. Loud neon-dark, springy, poster-like. Use React + Vite + Tailwind CSS + TypeScript + lucide-react. Default Tailwind config, no other UI libraries.

FONTS (Google Fonts, load via `<link>` in index.html)
- Display: Anton (400) — headlines, ticket prices, day tabs
- Body: Space Grotesk (400/500/700) — everything else

COLORS (CSS variables on :root — neon-dark family)
- --night: #0D0221 (background) · --panel: #190A34 · --glow-white: #F5F3FF (foreground)
- Accents: --magenta: #F72585 · --cyan: #4CC9F0 · --gold: #FFD60A (three, loud, everywhere) · hard-shadow color #B5179E

GLOBAL CSS (paste verbatim)
```css
@keyframes pop-in { from { opacity: 0; transform: scale(0.9) translateY(12px); } to { opacity: 1; transform: none; } }
.pop { animation: pop-in 0.5s cubic-bezier(0.18, 0.89, 0.32, 1.28) backwards;
       transition: transform 160ms cubic-bezier(0.34, 1.56, 0.64, 1); }
.pop:active { transform: scale(0.94); }
@media (hover: hover) { .pop:hover { transform: scale(1.06) rotate(-1.5deg); } }

@keyframes float-y { 0%,100% { transform: translateY(0) rotate(-6deg); } 50% { transform: translateY(-6px) rotate(-6deg); } }
.sticker { animation: float-y 3s cubic-bezier(0.65, 0, 0.35, 1) infinite;
           transition: transform 200ms cubic-bezier(0.34, 1.56, 0.64, 1); }
@media (hover: hover) { .sticker:hover { transform: scale(1.08) rotate(3deg); } }

@keyframes marquee-x { from { transform: translateX(0); } to { transform: translateX(-50%); } }
.marquee-track { animation: marquee-x 20s linear infinite; }

@media (prefers-reduced-motion: reduce) {
  .sticker, .marquee-track { animation: none; }
  *, *::before, *::after { animation-duration: 0.01ms !important; animation-iteration-count: 1 !important; transition-duration: 0.01ms !important; }
}
```

DECOR LAYER (z-[5], `aria-hidden="true"`, pointer-events-none — neon wallpaper, static)
- Hero: two glows — `w-[520px] h-[520px] rounded-full bg-[var(--magenta)] opacity-15 blur-3xl` top-left; same in `--cyan` bottom-right
- Scattered 8-bit plus-signs and dots as inline SVGs, stroke `--gold`, opacity-30
- Subtle scanline feel via a repeating-linear-gradient overlay at 3% opacity (this profile allows decorative gradients)

NAVBAR (z-20, max-w-6xl mx-auto px-6 py-5, flex justify-between, text-[var(--glow-white)])
- Left: "PIXELJAM" — Anton text-2xl tracking-wide, "JAM" in `--magenta`
- Links (hidden md:flex, Space Grotesk 500 text-sm): Lineup · Schedule · Tickets — hover = `scaleX` underline h-0.5 bg-[var(--cyan)], `transform-origin: left`, 200ms cubic-bezier(0.23, 1, 0.32, 1), gated `@media (hover: hover) and (pointer: fine)`
- Right: "Get tickets" `rounded-full bg-[var(--gold)] text-[var(--night)] px-5 py-2 text-sm font-bold`, hover scale 1.06 spring 160ms, `active:scale-[0.94]`

HERO (z-10, max-w-6xl mx-auto px-6 pt-16 pb-24, text-center)
- Staggered `.pop` entrance via `animation-delay`: sticker 0ms → H1 90ms → date row 180ms → CTA 270ms → countdown 360ms
- Sticker: `<span className="sticker inline-block rounded-2xl bg-[var(--gold)] px-3 py-1 text-sm font-black text-[var(--night)]">3 NIGHTS ONLY</span>`
- H1 — Anton, text-6xl md:text-8xl leading-[0.95] uppercase, stacked: "INSERT" (glow-white) / "COIN" (`--magenta`, hard shadow `[text-shadow:4px_4px_0_#B5179E]`) / "TO PLAY" (outline style: transparent fill, 2px `--cyan` text-stroke via `[-webkit-text-stroke:2px_var(--cyan)]`)
- Date row: "NOV 14–16 · WAREHOUSE 22 · DA NANG" — Space Grotesk 700 text-lg tracking-[0.14em] text-[var(--cyan)]
- CTA: `<button className="pop rounded-full bg-[var(--magenta)] px-8 py-4 text-lg font-bold text-white shadow-[0_6px_0_#B5179E]">Get your pass →</button>`
- COUNTDOWN: 4 tiles (Days/Hours/Min/Sec) `rounded-2xl bg-[var(--panel)] border-2 border-[var(--cyan)]/40 px-5 py-4` — numbers Anton text-4xl tabular-nums `--gold`, labels text-xs uppercase glow-white 70%. Frequency filter: it ticks every second — digits update with NO animation; only the tile group pops in once on load

MARQUEE (border-y-2 border-[var(--magenta)]/40, py-3, overflow-hidden, `aria-hidden="true"`)
- `.marquee-track` = two identical halves (200% width) so `translateX(-50%)` loops seamlessly, 20s linear
- "HIGH SCORES ▲ CHIPTUNE ▲ FREEPLAY ▲ TOURNAMENTS ▲ " ×8 — Anton text-xl uppercase text-[var(--glow-white)]/80

LINEUP GRID (max-w-6xl mx-auto px-6 py-24)
- H2 `.pop` in view: "THE CABINET" — Anton text-5xl, "CABINET" in `--cyan`
- 6 game cards, grid sm:grid-cols-2 lg:grid-cols-3 gap-6, `.pop` via IntersectionObserver once, stagger 90ms:
  - Each: key art `<img src="{YOUR_IMAGE_URL_N}" alt="…">` rounded-2xl aspect-[4/3] object-cover, title Anton text-2xl ("NEON DRIFT 2", "GHOST BODEGA", "SODA CRISIS", "MECHA PICNIC", "LAST TRAIN LOOP", "BYTE CLUB"), studio line Space Grotesk text-sm glow-white 70%, genre chip `rounded-full border border-[var(--gold)]/50 text-[var(--gold)] px-2 py-0.5 text-xs`
  - Card `rounded-2xl bg-[var(--panel)] p-4 border-2 border-transparent`; hover (gated): `scale(1.06) rotate(1deg)` spring 200ms + border-color to `--magenta` (160ms); press `active:scale-[0.94]`; alternate cards pre-rotated ±1deg

SCHEDULE (max-w-4xl mx-auto px-6 pb-24)
- Day tabs: FRI 14 · SAT 15 · SUN 16 — Anton text-xl, `rounded-full px-6 py-2`, active = bg-[var(--cyan)] text-[var(--night)], inactive = border-2 border-[var(--cyan)]/40 text-glow-white; switch = background/color 160ms + `active:scale-[0.94]`; panel swaps with `.pop` 0.4s (no exit animation)
- 4 slots per day, each a `rounded-2xl bg-[var(--panel)] p-4 flex justify-between` row: time (Anton `--gold` tabular-nums) + set name + stage chip — rows `.pop` stagger 90ms on tab change
- Sample (FRI): 18:00 Doors + freeplay · 20:00 Chipbreaker (live set) · 22:00 NEON DRIFT 2 launch bracket · 00:00 Midnight high-score run

TICKETS (max-w-6xl mx-auto px-6 pb-24)
- H2: "PICK YOUR PASS" — Anton text-5xl, "PASS" in `--gold`
- 3 tier cards, grid md:grid-cols-3 gap-6, `.pop` stagger 90ms, `rounded-3xl p-8 bg-[var(--panel)]`:
  1. DAY PASS — Anton text-5xl "$29" tabular-nums · one night, all cabinets · border-2 border-[var(--cyan)]/40
  2. FULL FEST — "$69" · 3 nights + tournament entry · border-2 border-[var(--magenta)], sticker "CROWD PICK" (`--magenta` bg, white text) pinned top-right at rotate 6deg
  3. VIP CABINET — "$129" · skip lines, arcade bar, artist meetup · border-2 border-[var(--gold)]
- Each: perks list with lucide `Zap` bullets in tier color + full-width `.pop` CTA "Take my coins" (tier-colored bg, `--night` text, hard shadow)

FOOTER (border-t border-[var(--glow-white)]/10, py-10, max-w-6xl mx-auto px-6, flex justify-between, text-sm glow-white 70%)
- "© PixelJam Collective" + links Discord / Instagram / Code of conduct (`aria-label` on icon-only links) + sticker "★ bring quarters" rotate −3deg

ANIMATIONS (complete list)
- Entrances: `.pop` 0.5s cubic-bezier(0.18, 0.89, 0.32, 1.28), stagger 90ms, once (load in hero, IntersectionObserver below)
- Idle: `.sticker` float 3s · marquee 20s linear — both die under reduced-motion
- Hover: spring scale ≤1.08, 160–200ms cubic-bezier(0.34, 1.56, 0.64, 1), gated; borders/colors 160ms
- Press: `active:scale-[0.94]` on buttons/cards, `active:scale-[0.98]` on text links
- Countdown digits: no animation (every-second frequency)

RESPONSIVE
- Mobile: H1 text-6xl, countdown tiles 2×2 grid, lineup 1-col, schedule rows stack (time above set), tickets stack; blobs clipped by section `overflow-hidden`; no horizontal scroll

KEY DEPENDENCIES
`react@^18` `react-dom@^18` `typescript@^5` `vite@^5` `tailwindcss@^3` `lucide-react@latest`

CONSTRAINTS: playful maximalism on a neon-dark canvas — decorative glows/gradients/scanlines are the identity (allowed in this profile), but motion still animates only transform/opacity (border-color/background color swaps ≤160ms are the documented paint exceptions), easing only from {cubic-bezier(0.34,1.56,0.64,1) · cubic-bezier(0.18,0.89,0.32,1.28) · cubic-bezier(0.23,1,0.32,1) · cubic-bezier(0.65,0,0.35,1)}, never ease-in, no `transition: all`, and every entrance starts at scale 0.9 or above — nothing pops in from zero. Bounce belongs to deliberate moments — the countdown and nav stay still. Respect `prefers-reduced-motion`. Replace `{YOUR_IMAGE_URL_*}` with art you have rights to. ARIA labels on icon-only links; marquee and decor `aria-hidden`; day tabs are buttons with `aria-pressed`.
