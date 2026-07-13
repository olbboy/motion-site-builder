# Doodlecamp Kids Coding Camp

- **ID:** `doodlecamp-kids-coding`
- **Category:** Education / Family
- **Type:** landing
- **Profile:** `playful`

---

Build a single-page landing page for "Doodlecamp" — a summer coding camp for kids 8–12 that feels like a treehouse, not a classroom. Crayon-bright color, wobbly hand-drawn accents, sticker badges, zero corporate energy. Use React + Vite + Tailwind CSS + TypeScript + lucide-react. Default Tailwind config, no other UI libraries.

FONTS (Google Fonts, load via `<link>` in index.html)
- Display: Baloo 2 (700/800) — headlines, badges, prices
- Body: DM Sans (400/500/700) — everything else

COLORS (CSS variables on :root — crayon-box family; decorative color IS the identity here)
- --paper: #FFFDF6 (background) · --ink: #23262B (foreground)
- Accents (all four earn their keep): --sky: #38BDF8 (links, badges) · --coral: #FF6B6B (primary CTA) · --grass: #4ADE80 (enroll/success states) · --sun: #FDE047 (highlights, underlines)
- Hard-shadow trick: solid offset shadows in ink (`shadow-[0_6px_0_#23262B]`), never soft blurs — shadows stay neutral so the four accents stay exactly four

GLOBAL CSS (paste verbatim)
```css
@keyframes pop-in { from { opacity: 0; transform: scale(0.9) translateY(12px); } to { opacity: 1; transform: none; } }
.pop { animation: pop-in 0.5s cubic-bezier(0.18, 0.89, 0.32, 1.28) backwards;   /* back-out overshoot */
       transition: transform 160ms cubic-bezier(0.34, 1.56, 0.64, 1); }
.pop:active { transform: scale(0.94); }
@media (hover: hover) { .pop:hover { transform: scale(1.06) rotate(-1.5deg); } }

@keyframes float-y { 0%,100% { transform: translateY(0) rotate(-4deg); } 50% { transform: translateY(-6px) rotate(-4deg); } }
.sticker { animation: float-y 3s cubic-bezier(0.65, 0, 0.35, 1) infinite;
           transition: transform 200ms cubic-bezier(0.34, 1.56, 0.64, 1); }
@media (hover: hover) { .sticker:hover { transform: scale(1.08) rotate(3deg); } }

.faq-panel { transform-origin: top; }   /* scale-from-trigger: panel grows down from its question, not from center */

@media (prefers-reduced-motion: reduce) {
  .sticker { animation: none; }
  *, *::before, *::after { animation-duration: 0.01ms !important; animation-iteration-count: 1 !important; transition-duration: 0.01ms !important; }
}
```

DECOR LAYER (z-[5], `aria-hidden="true"`, pointer-events-none — crayon scribbles, static)
- Top-right: `w-72 h-72 rounded-full border-[6px] border-dashed border-[var(--sky)] opacity-25` rotated 8deg
- Bottom-left: `w-56 h-56 rounded-full bg-[var(--sun)]/20 blur-2xl`
- Scattered pencil-scribble inline SVGs (stroke `var(--coral)`, strokeWidth 4, opacity-30) near section edges
- Decor is static — entrances and stickers move, wallpaper doesn't

WOBBLY UNDERLINE (reusable inline SVG, decorative, `aria-hidden="true"`, static — no independent animation, only enters with its parent word's `.pop`)
```tsx
<svg className="absolute -bottom-2 left-0 w-full" viewBox="0 0 120 12" fill="none" aria-hidden="true">
  <path d="M2 8C20 2 40 10 60 6C80 2 100 10 118 4" stroke="var(--sun)" strokeWidth="5" strokeLinecap="round" />
</svg>
```

NAVBAR (z-20, max-w-6xl mx-auto px-6 py-5, flex justify-between)
- Left: "Doodlecamp" — Baloo 2 800 text-2xl, with the "o"s in "Doodle" alternating `--sky`/`--coral`
- Links (hidden md:flex, DM Sans 500 text-sm): Tracks · Schedule · FAQ — hover = marker underline: `scaleX` pseudo-element h-1 bg-[var(--sun)] rounded-full, `transform-origin: left`, 0→1 in 200ms cubic-bezier(0.23, 1, 0.32, 1), gated `@media (hover: hover) and (pointer: fine)`
- Right: "Enroll" `rounded-full bg-[var(--coral)] text-white px-5 py-2 text-sm font-bold`, hover scale 1.06 (spring 160ms), `active:scale-[0.94]`

HERO (z-10, max-w-5xl mx-auto px-6 pt-16 pb-24, text-center)
- Staggered `.pop` entrance via `animation-delay`: sticker 0ms → H1 90ms → sub 180ms → CTA row 270ms
- Sticker (paste verbatim): `<span className="sticker inline-block rounded-2xl bg-[var(--sky)] px-3 py-1 text-sm font-black text-[var(--ink)]">SUMMER 2026 · AGES 8–12</span>`
- H1 — Baloo 2 800, text-5xl md:text-7xl leading-[0.95]: "Screens are cool." on line 1, "Building is cooler." on line 2, with "Building" wrapped in `relative inline-block` carrying the wobbly underline SVG above
- Sub (DM Sans text-lg, ink 85%, max-w-xl mx-auto mt-6): "Four weeks. Real projects. Zero worksheets. Your kid ships a game, a website, and a story they'll brag about at dinner."
- CTA row (mt-8, flex justify-center gap-4): primary `<button className="pop rounded-full bg-[var(--coral)] px-8 py-4 text-lg font-bold text-white shadow-[0_6px_0_#23262B]">Save my kid's spot →</button>` + secondary text link "See this week's projects" (ink, marker underline on hover)

TRACKS GRID (max-w-6xl mx-auto px-6 py-24)
- H2 `.pop` when in view: "Pick your quest" — Baloo 2 800 text-4xl md:text-5xl
- 4 cards, grid sm:grid-cols-2 lg:grid-cols-4 gap-6, entering `.pop` via IntersectionObserver once, stagger 90ms (`animation-delay: 0/90/180/270ms`), each `rounded-2xl border-4 border-[var(--ink)] p-6`:
  1. "Scratch Sprites" — bg-[var(--sky)]/30, lucide `Gamepad2` icon w-8 h-8, "Make characters move, talk, and cause chaos — all with drag-and-drop blocks." · Ages 8–9
  2. "Web Wizards" — bg-[var(--coral)]/25, lucide `Globe` icon, "Build a real website with HTML, CSS, and way too many colors." · Ages 9–11
  3. "Game Jam Squad" — bg-[var(--grass)]/30, lucide `Trophy` icon, "Team up to build a playable game in five days flat." · Ages 10–12
  4. "AI Explorers" — bg-[var(--sun)]/35, lucide `Bot` icon, "Train a tiny AI to recognize doodles and guess what they drew." · Ages 11–12
- Card hover (gated `@media (hover: hover) and (pointer: fine)`): `scale(1.06) rotate(1.5deg)` spring 200ms cubic-bezier(0.34, 1.56, 0.64, 1); press `active:scale-[0.94]`; alternate cards pre-rotated ±1deg

SCHEDULE (bg-[var(--ink)] text-[var(--paper)] py-24, rounded-t-[3rem])
- H2: "Four weeks. Zero boring ones." — Baloo 2 800 text-4xl, with "boring" struck through and "ones" in `--sun`
- 4 week cards, grid sm:grid-cols-2 lg:grid-cols-4 gap-6, `.pop` in view stagger 90ms, `rounded-2xl bg-[var(--paper)]/10 p-6`:
  1. "Week 1 — Scratch & Sprites" · Mon–Fri, 9am–3pm · "Everyone leaves with a playable mini-game."
  2. "Week 2 — Web Wizards" · Mon–Fri, 9am–3pm · "Personal website goes live on Friday demo day."
  3. "Week 3 — Game Jam" · Mon–Fri, 9am–3pm · "Team-built arcade game, judged by actual campers."
  4. "Week 4 — Show & Tell" · Mon–Thu 9am–3pm, Fri 9am–12pm · "Portfolio polish + Family Showcase Friday."
- Week label Baloo 2 700 text-lg `--sun`; time row DM Sans text-sm 70%; one-liner DM Sans text-sm 85%

PARENT FAQ (max-w-3xl mx-auto px-6 py-24)
- H2 `.pop` in view: "Questions grown-ups ask" — Baloo 2 800 text-4xl, "grown-ups" in `--coral`
- 4 accordion rows (divide-y-4 divide-[var(--ink)]/10, first item open by default):
  1. "My kid has never coded. Is that a problem?" → "Nope — most campers start at zero. Counselors meet every kid where they are, not where the syllabus says they should be."
  2. "What if my kid gets frustrated?" → "We teach 'stuck is normal' on day one. Every cabin has a 'debug buddy' system so nobody struggles alone for long."
  3. "Do they need their own laptop?" → "Nope — we provide laptops. Bring a water bottle and a name you don't mind us mispronouncing."
  4. "Can I actually see what they built?" → "Every Friday is Showcase Friday. Parents welcome, popcorn provided, standing ovations mandatory."
- Header button: `flex justify-between w-full py-4 text-left font-bold text-lg`, chevron (lucide `ChevronDown`) rotates 0→180deg 200ms cubic-bezier(0.23, 1, 0.32, 1), `aria-expanded`
- Panel (mounts on open, class `pop faq-panel`, i.e. 0.5s back-out scaling from `transform-origin: top` — scale-from-trigger, springs like every other entrance here): DM Sans text-base ink 85%, pb-5

WALL OF LOVE (max-w-5xl mx-auto px-6 pb-24)
- H2: "Grown-ups are saying" — Baloo 2 800 text-3xl
- 3 quote cards `rounded-2xl border-4 border-[var(--ink)] p-6`, each rotated (−2deg / 1deg / −1deg), `.pop` in view stagger 90ms:
  - "My daughter used to say 'I'm bad at computers.' Now she corrects my Wi-Fi password." — Linh, mom of Mai (9)
  - "He built a game where the boss is his little sister. She's thrilled. I'm terrified." — Duc, dad of Nam (11)
  - "First camp he didn't beg to leave early." — Ha, mom of An (10)

FINAL CTA (max-w-4xl mx-auto px-6 py-24 text-center)
- Panel `rounded-3xl bg-[var(--grass)] text-[var(--ink)] p-12 relative overflow-hidden` with two `--sky`/`--sun` glow shapes inside (decor)
- H2 Baloo 2 800 text-4xl md:text-6xl: "Ready to build something loud?" · sub "Spots are first-come. Early Bird pricing ends July 31."
- CTA `.pop` verbatim styling but bg-[var(--coral)] text-white shadow-[0_6px_0_#23262B]: "Enroll now — from $349/week"

FOOTER (py-10, max-w-6xl mx-auto px-6, flex justify-between, DM Sans text-sm ink 85%)
- "© Doodlecamp Coding Studio" + links Curriculum / Counselors / Contact (`aria-label` on icon links); sticker "★ made for curious kids" rotated −3deg

ANIMATIONS (complete list)
- Entrances: `.pop` 0.5s back-out cubic-bezier(0.18, 0.89, 0.32, 1.28), stagger 90ms, once per element (load for hero, IntersectionObserver for below-fold, remount for FAQ panels on open)
- Idle: `.sticker` float-y 3s loop (reduced-motion: none)
- FAQ panel: `.pop.faq-panel` reuses the entrance timing with `transform-origin: top` so it visibly grows from its trigger question
- Hover: spring scale ≤1.08 + rotate ≤3deg, 160–200ms cubic-bezier(0.34, 1.56, 0.64, 1), always gated behind `@media (hover: hover)`
- Press: `active:scale-[0.94]` on every button/card; text links `active:scale-[0.98]`
- Chevron rotate: 200ms cubic-bezier(0.23, 1, 0.32, 1)

RESPONSIVE
- Mobile: single-column hero, tracks grid 1→2→4, schedule cards 1→2→4, FAQ full width, final CTA p-8; no horizontal scroll (decor shapes are `overflow-hidden` inside their sections)

KEY DEPENDENCIES
`react@^18` `react-dom@^18` `typescript@^5` `vite@^5` `tailwindcss@^3` `lucide-react@latest`

CONSTRAINTS: playful maximalism, engineered — all four accents and the decorative shapes are intentional (this profile inverts the cinematic no-decor rule), but motion still only animates transform/opacity, easing only from {cubic-bezier(0.34,1.56,0.64,1) · cubic-bezier(0.18,0.89,0.32,1.28) · cubic-bezier(0.23,1,0.32,1) · cubic-bezier(0.65,0,0.35,1)}, never ease-in, no `transition: all`, and every entrance starts at scale 0.9 or above — nothing pops in from zero. Bounce is for deliberate moments (entrances, CTA, stickers, FAQ panels) — nav links don't wobble. Respect `prefers-reduced-motion` (stickers stop dead). Replace `{YOUR_IMAGE_URL_*}` with media you have rights to. ARIA labels on icon-only links; decorative shapes and the wobbly underlines are `aria-hidden`; accordion headers carry `aria-expanded`.
