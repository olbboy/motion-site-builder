# Mochi Club Snack Box

- **ID:** `mochi-club-snackbox`
- **Category:** Consumer Brand / Subscription
- **Type:** landing
- **Profile:** `playful`

---

Build a single-page DTC landing page for "Mochi Club" — a monthly Asian-snack subscription box that treats "I've never heard of this" as a selling point. Pastel candy color, bouncy springs, sticker energy. Use React + Vite + Tailwind CSS + TypeScript + lucide-react. Default Tailwind config, no other UI libraries.

FONTS (Google Fonts, load via `<link>` in index.html)
- Display: Fredoka (500/600/700) — headlines, box names, prices
- Body: Nunito (400/600/700) — everything else

COLORS (CSS variables on :root — pastel candy family, distinct from any bright-primary palette; decorative color IS the identity here)
- --cream: #FFF9F5 (background) · --ink: #2E1F3B (foreground, deep plum)
- Accents (all four earn their keep): --blossom: #F472B6 (primary CTA, price highlights) · --taro: #A78BFA (badges, links) · --matcha: #86EFAC (flavor tags, success states) · --peach: #FDBA74 (secondary highlights, dividers)
- Hard-shadow trick: solid offset shadows in ink (`shadow-[0_6px_0_#2E1F3B]`), never soft blurs — shadows stay neutral so the four accents stay exactly four

GLOBAL CSS (paste verbatim)
```css
@keyframes pop-in { from { opacity: 0; transform: scale(0.9) translateY(12px); } to { opacity: 1; transform: none; } }
.pop { animation: pop-in 0.5s cubic-bezier(0.18, 0.89, 0.32, 1.28) backwards;   /* back-out overshoot */
       transition: transform 160ms cubic-bezier(0.34, 1.56, 0.64, 1); }
.pop:active { transform: scale(0.94); }
@media (hover: hover) { .pop:hover { transform: scale(1.06) rotate(-1.5deg); } }

@keyframes float-y { 0%,100% { transform: translateY(0) rotate(-5deg); } 50% { transform: translateY(-6px) rotate(-5deg); } }
.sticker { animation: float-y 3s cubic-bezier(0.65, 0, 0.35, 1) infinite;
           transition: transform 200ms cubic-bezier(0.34, 1.56, 0.64, 1); }
@media (hover: hover) { .sticker:hover { transform: scale(1.08) rotate(3deg); } }

@keyframes marquee-x { from { transform: translateX(0); } to { transform: translateX(-50%); } }
.marquee-track { animation: marquee-x 22s linear infinite; }

@media (prefers-reduced-motion: reduce) {
  .sticker, .marquee-track { animation: none; }
  *, *::before, *::after { animation-duration: 0.01ms !important; animation-iteration-count: 1 !important; transition-duration: 0.01ms !important; }
}
```

DECOR LAYER (z-[5], `aria-hidden="true"`, pointer-events-none — wallpaper, static)
- Top-left: blob `w-[420px] h-[420px] rounded-full bg-gradient-to-br from-[var(--blossom)] to-[var(--taro)] opacity-20 blur-3xl`
- Bottom-right: `w-60 h-60 rounded-full border-[6px] border-dashed border-[var(--matcha)] opacity-30` rotated −10deg
- Scattered dot-and-ring confetti as inline SVGs, stroke/fill `var(--peach)`, opacity-30
- Decor is static — entrances and stickers move, wallpaper doesn't

NAVBAR (z-20, max-w-6xl mx-auto px-6 py-5, flex justify-between)
- Left: "Mochi Club" — Fredoka 700 text-2xl, "Club" in `--blossom`
- Links (hidden md:flex, Nunito 700 text-sm): This Month · How it Works · Reviews — hover = marker underline: `scaleX` pseudo-element h-1 bg-[var(--taro)] rounded-full, `transform-origin: left`, 0→1 in 200ms cubic-bezier(0.23, 1, 0.32, 1), gated `@media (hover: hover) and (pointer: fine)`
- Right: "Join" `rounded-full bg-[var(--ink)] text-[var(--cream)] px-5 py-2 text-sm font-bold`, hover scale 1.06 (spring 160ms), `active:scale-[0.94]`

HERO (z-10, max-w-6xl mx-auto px-6 pt-14 pb-20, grid md:grid-cols-2 gap-10 items-center)
- Left column (staggered `.pop` entrance — sticker 0ms, H1 90ms, sub 180ms, CTA 270ms via `animation-delay`):
  - Sticker badge (paste verbatim): `<span className="sticker inline-block rounded-2xl bg-[var(--taro)] px-3 py-1 text-sm font-black text-white">NEW MEMBER: 20% OFF</span>`
  - H1 — Fredoka 700, text-5xl md:text-7xl leading-[0.95]: "Open it." on line 1, "Regret nothing." on line 2 with "Regret" wrapped in a `rounded-2xl bg-[var(--blossom)] text-white px-3 inline-block -rotate-1`
  - Sub (Nunito text-lg, ink 85%, max-w-md): "12 hand-picked snacks from Tokyo to Taipei, delivered monthly. Some are sweet. Some are a dare."
  - CTA row (mt-8, flex gap-4): `<button className="pop rounded-full bg-[var(--blossom)] px-8 py-4 text-lg font-bold text-white shadow-[0_6px_0_#2E1F3B]">Get my first box — $28</button>` + secondary text link "See March's box" (ink, marker underline on hover)
- Right column: box render `<img src="{YOUR_IMAGE_URL_HERO}" alt="Mochi Club snack box opened, showing twelve wrapped snacks">` rounded-3xl, entering `.pop` at 200ms; behind it a `rounded-full bg-[var(--matcha)]/30 blur-2xl` glow (decor layer)

UNBOXING MARQUEE (border-y-4 border-[var(--ink)], bg-[var(--peach)], py-3, overflow-hidden)
- `.marquee-track` = two identical inline flex halves (total 200% width) so `translateX(-50%)` loops seamlessly, 22s linear infinite
- Content: "RIP ✺ TASTE ✺ SCREAM ✺ REPEAT ✺ " ×8 — Fredoka 600 text-xl uppercase text-[var(--ink)], `aria-hidden="true"` (pure decoration)

WHAT'S IN THE BOX (max-w-6xl mx-auto px-6 py-24)
- H2 `.pop` when in view: "March's lineup" — Fredoka 700 text-4xl md:text-5xl, "lineup" in `--taro`
- 6 cards, grid sm:grid-cols-2 lg:grid-cols-3 gap-6, entering `.pop` via IntersectionObserver once, stagger 90ms (`animation-delay: 0/90/…/450ms`), each `rounded-2xl bg-[var(--taro)]/15 border-4 border-[var(--ink)] p-5`:
  1. "Yuzu Kit Kat" — flavor tag "Sweet" (bg-[var(--matcha)]/40)
  2. "Ube Pocky" — flavor tag "Sweet"
  3. "Salted Egg Chips" — flavor tag "Weird" (bg-[var(--peach)]/40)
  4. "Taro Mochi" — flavor tag "Sweet"
  5. "Wasabi Peas" — flavor tag "Dare" (bg-[var(--blossom)]/30)
  6. "Milk Tea Gummies" — flavor tag "Sweet"
- Each card: snack shot `<img src="{YOUR_IMAGE_URL_N}" alt="…">` rounded-xl, name Fredoka 600 text-lg, flavor tag `rounded-full px-3 py-1 text-xs font-bold text-[var(--ink)]`
- Card hover (gated `@media (hover: hover) and (pointer: fine)`): `scale(1.06) rotate(1.5deg)` spring 200ms cubic-bezier(0.34, 1.56, 0.64, 1); press `active:scale-[0.94]`; alternate cards rotate −1.5deg

BOX TIERS (bg-[var(--ink)] text-[var(--cream)] py-24, rounded-t-[3rem])
- H2: "Pick your box" — Fredoka 700 text-4xl, "box" in `--peach`
- 3 tier cards, grid md:grid-cols-3 gap-6, `.pop` stagger 90ms, `rounded-3xl p-8 bg-[var(--cream)]/10`:
  1. "Curious" — "$22/mo" tabular-nums · 8 snacks · border-2 border-[var(--matcha)]/50
  2. "Classic" — "$28/mo" · 12 snacks · border-2 border-[var(--blossom)], sticker "MOST POPPED" (`--blossom` bg, white text) pinned top-right at rotate 6deg
  3. "Family" — "$45/mo" · 20 snacks + 2 drinks · border-2 border-[var(--taro)]
- Each: perks list with lucide `Sparkles` bullets in tier color + full-width `.pop` CTA "Start my box" (tier-colored bg, `--ink` text, hard shadow `shadow-[0_6px_0_#2E1F3B]`)

TESTIMONIAL STICKERS (max-w-5xl mx-auto px-6 py-24)
- H2: "People are yelling about us" — Fredoka 700 text-4xl, "yelling" in `--blossom`
- 3 quote cards `rounded-2xl bg-[var(--taro)]/15 border-4 border-[var(--ink)] p-6`, each rotated (−2deg / 1deg / −1deg), `.pop` in view stagger 90ms:
  - "My roommate ate my whole box in one sitting. We are no longer roommates." — Tam N.
  - "I now know what yuzu is. My life has changed accordingly." — Brooke L.
  - "Worth it for the ube mochi alone." — Kenji T.
- Stars row: 5× lucide `Star` filled `--peach`, w-4 h-4

FINAL CTA (max-w-4xl mx-auto px-6 py-24 text-center)
- Panel `rounded-3xl bg-[var(--matcha)] text-[var(--ink)] p-12 relative overflow-hidden` with two `--blossom`/`--taro` glow shapes inside (decor)
- H2 Fredoka 700 text-4xl md:text-6xl: "Hungry for weird yet?" · sub "Free shipping on your first box. Cancel anytime, no guilt."
- CTA `.pop` verbatim styling but bg-[var(--blossom)] text-white shadow-[0_6px_0_#2E1F3B]: "Build my box"

FOOTER (py-10, max-w-6xl mx-auto px-6, flex justify-between, Nunito text-sm ink 85%)
- "© Mochi Club Snacks Co." + links Instagram / TikTok / Wholesale (`aria-label` on icon links); sticker "★ curated with chopsticks" rotated −3deg

ANIMATIONS (complete list)
- Entrances: `.pop` 0.5s back-out cubic-bezier(0.18, 0.89, 0.32, 1.28), stagger 90ms, once per element (load for hero, IntersectionObserver for below-fold)
- Idle: `.sticker` float-y 3s loop (reduced-motion: none) · marquee 22s linear loop
- Hover: spring scale ≤1.08 + rotate ≤3deg, 160–200ms cubic-bezier(0.34, 1.56, 0.64, 1), always gated behind `@media (hover: hover)`
- Press: `active:scale-[0.94]` on every button/card; text links `active:scale-[0.98]`

RESPONSIVE
- Mobile: single-column hero (image first), reveal grid 1→2→3, tiers stack, marquee text-base, final CTA p-8; no horizontal scroll (blobs are `overflow-hidden` inside their sections)

KEY DEPENDENCIES
`react@^18` `react-dom@^18` `typescript@^5` `vite@^5` `tailwindcss@^3` `lucide-react@latest`

CONSTRAINTS: playful maximalism, engineered — all four accents and the decorative gradients/shapes are intentional (this profile inverts the cinematic no-decor rule), but motion still only animates transform/opacity, easing only from {cubic-bezier(0.34,1.56,0.64,1) · cubic-bezier(0.18,0.89,0.32,1.28) · cubic-bezier(0.23,1,0.32,1) · cubic-bezier(0.65,0,0.35,1)}, never ease-in, no `transition: all`, and every entrance starts at scale 0.9 or above — nothing pops in from zero. Bounce is for deliberate moments (entrances, CTA, stickers) — nav links don't wobble. Respect `prefers-reduced-motion` (stickers and marquee stop dead). Replace `{YOUR_IMAGE_URL_*}` with media you have rights to. ARIA labels on icon-only links; decorative shapes and the marquee are `aria-hidden`.
