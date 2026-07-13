# Chào Nhà — Weekend Routes

- **ID:** `chao-nha-weekend-routes`
- **Category:** Micro-adventure campaign
- **Type:** landing
- **Profile:** `playful`

---

Build a single-page campaign site for "Chào Nhà" — a bright Vietnamese micro-adventure club that turns one free weekend into a coast, a hill, and a story home by Sunday night. Use React + Vite + Tailwind CSS + TypeScript + lucide-react. Default Tailwind config, no other UI libraries.

SELECTED PEXELS MEDIA
- Source: [Green coastal hills and clear sea in Vietnam](https://www.pexels.com/photo/scenic-coastal-landscape-in-vietnam-35268948/) by Hugo Guillemard.
- Download to `/media/vietnam/pexels-35268948.jpg`; use `<img src="/media/vietnam/pexels-35268948.jpg" alt="Green coastal hills meeting clear blue sea beneath a bright Vietnamese sky">`.
- Hero crop 4:3 `object-cover object-[56%_48%]`; place inside a tilted paper frame, not as a background.

FONTS
- Display: Bricolage Grotesque 700/800; body: Be Vietnam Pro 400/500/700; stickers: Space Mono 700.

COLORS
- `--cream:#FFF8EA --ink:#1B1A35 --coral:#FF5C7A --violet:#7347D8 --cyan:#21C7D9 --yellow:#F6C945`; all four accents have distinct roles: CTA / route / water / badges.

GLOBAL CSS
```css
@keyframes pop-trip { from { opacity:0; transform:scale(.92) translateY(22px) rotate(-2deg); } to { opacity:1; transform:none; } }
.pop-trip { animation:pop-trip .55s cubic-bezier(0.18, 0.89, 0.32, 1.28) backwards; }
.pressable { transition:transform 170ms cubic-bezier(0.34, 1.56, 0.64, 1); }
.pressable:active { transform:scale(.94); }
@media (hover:hover) and (pointer:fine) { .wiggle:hover { transform:scale(1.05) rotate(1.5deg); } }
@media (prefers-reduced-motion:reduce) { *,*::before,*::after { animation-duration:.01ms!important; animation-iteration-count:1!important; transition-duration:.01ms!important; } }
```

DECOR LAYER (z-5, aria-hidden)
- Static marker squiggles, sunburst circles, ticket-edge dividers, and tiny route arrows. No moving wallpaper and no more than the four declared accents.

NAV (z-20)
- Wordmark "CHÀO NHÀ!" inside a wobbly cyan outline; links This weekend / Route cards / Club rules; coral pill CTA "Pick a route".

HERO (content z-10)
- `min-h-[88svh] grid md:grid-cols-[1.05fr_.95fr] gap-12 items-center max-w-7xl px-6`.
- Left: yellow sticker "48 HOURS · ZERO FLIGHTS"; H1 `text-6xl md:text-[104px] leading-[.9]` "Go far enough / to miss home." with "home" on coral highlight; sub "Leave after work. Swim before breakfast. Be back with sand in the laundry."; CTA "Show me Saturday" and secondary "How the club works".
- Right: selected photo inside `rounded-[32px] border-[10px] border-white shadow-[12px_14px_0_#7347D8] rotate-2`; caption tape "COAST ROUTE 03"; 3 static pin stickers.
- Pop sequence sticker 0ms, H1 90ms, sub 180ms, CTA 270ms, photo 180ms.

ROUTE DECK
- Four chunky cards: Coast & Camp / Hill & Hammock / River & Rice / Market & Miles. Each `rounded-3xl border-2 border-[var(--ink)] p-6` with exact badges: 36h, 2–4 friends, under 1.5M ₫, moderate.
- Use CSS illustrations only; selected photo appears only on Coast & Camp. Gated hover scale 1.05 rotate ±1.5°, press .94.

WEEKEND BUILDER
- Three-step interactive picker: Start city (Đà Nẵng/Huế/Quy Nhơn), energy (Soft/Steady/Send it), sleep (Tent/Homestay/Small hotel). Native buttons with `aria-pressed`; result card updates instantly with 180ms opacity, no carousel.

CLUB RULES
- Oversized numbered strip: 01 Leave no trace / 02 Pay local / 03 Ask before portraits / 04 Come home together. Each rule on a different declared accent background with WCAG contrast.

FINAL CTA
- Violet block, huge text "Saturday is closer than it looks."; coral CTA "Pick my route"; footer source/photographer credit.

ANIMATIONS
- Pop entrances .55s/90ms; gated card hover scale ≤1.05; press .94/170ms; picker result fade 180ms. No infinite stickers, marquee, cursor follower, or parallax.

RESPONSIVE
- Hero stacks with copy first; photo frame max 88vw; route deck one column; picker buttons wrap; H1 text-6xl. Decorative shapes clipped; no horizontal scroll.

KEY DEPENDENCIES
`react@^18` `react-dom@^18` `typescript@^5` `vite@^5` `tailwindcss@^3` `lucide-react@latest`

CONSTRAINTS: playful maximalism with exactly four assigned accents; no video, fake prices presented as live, auto-carousel, infinite animation, or commercial brand references. Only transform/opacity animate; reduced motion; button/pressed semantics; photo source and credit remain visible.
