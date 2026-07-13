# Bloop Synth Plugin

- **ID:** `bloop-synth-plugin`
- **Category:** Developer Tool / Music Software
- **Type:** landing
- **Profile:** `playful`

---

Build a single-page landing page for "Bloop" — a chunky analog-style synth VST/AU plugin, playful profile applied to a producer's tool: deep-purple dark canvas, neon accents, springy pop-ins instead of restrained SaaS motion. Use React + Vite + Tailwind CSS + TypeScript + lucide-react. Default Tailwind config, no other UI libraries.

FONTS (Google Fonts, load via `<link>` in index.html)
- Display: Archivo Black (400) — headlines, section titles
- Body: Space Grotesk (400/500/700) — everything else
- Mono accent: JetBrains Mono (500) — preset tags, version numbers, OS badges

COLORS (CSS variables on :root — neon-on-deep-purple family; dark-friendly playful, decorative color IS the identity here)
- --void: #1B1033 (background) · --panel: #22163B · --glow-white: #F4F0FF (foreground)
- Accents (all four earn their keep): --neon-pink: #FF3EA5 (primary CTA, price) · --neon-cyan: #2FF3E0 (waveform, links) · --neon-lime: #C6FF3E (preset highlights, success) · --neon-orange: #FF9F1C (OS badges, secondary highlights)
- Hard-shadow trick: solid offset shadows in `--neon-pink` at 40% opacity (`shadow-[0_6px_0_rgba(255,62,165,0.4)]`) on the primary CTA only — every other surface uses soft `--neon-cyan`/`--neon-lime` glows via `box-shadow`, never mixed with the shadow trick

GLOBAL CSS (paste verbatim)
```css
@keyframes pop-in { from { opacity: 0; transform: scale(0.9) translateY(12px); } to { opacity: 1; transform: none; } }
.pop { animation: pop-in 0.5s cubic-bezier(0.18, 0.89, 0.32, 1.28) backwards;   /* back-out overshoot */
       transition: transform 160ms cubic-bezier(0.34, 1.56, 0.64, 1); }
.pop:active { transform: scale(0.94); }
@media (hover: hover) { .pop:hover { transform: scale(1.06) rotate(-1.5deg); } }

@keyframes float-y { 0%,100% { transform: translateY(0) rotate(-3deg); } 50% { transform: translateY(-6px) rotate(-3deg); } }
.sticker { animation: float-y 3s cubic-bezier(0.65, 0, 0.35, 1) infinite;
           transition: transform 200ms cubic-bezier(0.34, 1.56, 0.64, 1); }
@media (hover: hover) { .sticker:hover { transform: scale(1.08) rotate(3deg); } }

@media (prefers-reduced-motion: reduce) {
  .sticker { animation: none; }
  *, *::before, *::after { animation-duration: 0.01ms !important; animation-iteration-count: 1 !important; transition-duration: 0.01ms !important; }
}
```

DECOR LAYER (z-[5], `aria-hidden="true"`, pointer-events-none — neon wallpaper, static)
- Hero: two glows — `w-[480px] h-[480px] rounded-full bg-[var(--neon-pink)] opacity-15 blur-3xl` top-left; same in `--neon-cyan` bottom-right
- Scattered dot/plus-sign SVGs, stroke `--neon-lime`, opacity-25
- Decor is static — entrances and stickers move, wallpaper doesn't

CHUNKY KNOB ILLUSTRATION (reusable CSS-shape component, purely decorative, `aria-hidden="true"`, static — no independent animation)
```tsx
<div className="relative w-20 h-20 rounded-full bg-[var(--panel)] border-4 border-[var(--neon-cyan)]/60 shadow-[0_4px_0_rgba(0,0,0,0.4)]">
  <div className="absolute left-1/2 top-2 w-1.5 h-7 -translate-x-1/2 rounded-full bg-[var(--neon-cyan)]"
       style={{ transformOrigin: '50% 34px', transform: 'rotate(-35deg)' }} />
</div>
```
Vary the `rotate(…deg)` value per instance (e.g. −35deg, 10deg, 60deg) to imply different knob positions across the mockup — always a static inline style, never animated.

NAVBAR (z-20, max-w-6xl mx-auto px-6 py-5, flex justify-between, text-[var(--glow-white)])
- Left: "BLOOP" — Archivo Black text-2xl, with the middle "O"s rendered as two tiny knob illustrations (w-5 h-5 each) instead of letterforms
- Links (hidden md:flex, Space Grotesk 500 text-sm): Presets · Specs · Pricing — hover = `scaleX` underline h-0.5 bg-[var(--neon-cyan)], `transform-origin: left`, 200ms cubic-bezier(0.23, 1, 0.32, 1), gated `@media (hover: hover) and (pointer: fine)`
- Right: "Buy — $89" `rounded-full bg-[var(--neon-pink)] text-[var(--void)] px-5 py-2 text-sm font-bold`, hover scale 1.06 spring 160ms, `active:scale-[0.94]`

HERO (z-10, max-w-6xl mx-auto px-6 pt-16 pb-20, grid md:grid-cols-2 gap-10 items-center)
- Left column (staggered `.pop` — badges 0ms, H1 90ms, sub 180ms, CTA row 270ms, OS badges 360ms):
  - Sticker (paste verbatim): `<span className="sticker inline-block rounded-2xl bg-[var(--neon-lime)] px-3 py-1 text-sm font-black text-[var(--void)]">v2.1 — NOW WITH DRIFT</span>`
  - H1 — Archivo Black, text-5xl md:text-7xl leading-[0.95] uppercase: "Knobs you can" on line 1, "actually feel." on line 2 with "feel." wrapped in `rounded-2xl bg-[var(--neon-pink)] text-[var(--void)] px-3 inline-block -rotate-1`
  - Sub (Space Grotesk text-lg, glow-white 85%, max-w-md): "Bloop is a hand-modeled analog synth plugin — three oscillators, one filter that misbehaves in all the right ways, and presets that sound like a mood board."
  - CTA row (mt-8, flex gap-4): `<button className="pop rounded-full bg-[var(--neon-pink)] px-8 py-4 text-lg font-bold text-[var(--void)] shadow-[0_6px_0_rgba(255,62,165,0.4)]">Buy Bloop — $89</button>` + secondary `<button className="pop rounded-full border-2 border-[var(--neon-cyan)] px-8 py-4 text-lg font-bold text-[var(--neon-cyan)]">Try the free demo</button>`
  - OS badges row (mt-6, flex gap-3, JetBrains Mono text-xs): "macOS 12+" · "Windows 10+" · "VST3" · "AU" · "AAX" — each `rounded-full border border-[var(--neon-orange)]/50 text-[var(--neon-orange)] px-3 py-1`
- Right column: 3 chunky knob illustrations + one slider illustration arranged in a `rounded-3xl bg-[var(--panel)] p-10 grid grid-cols-2 gap-8` panel, `.pop` at 200ms; behind it a `rounded-full bg-[var(--neon-lime)]/20 blur-2xl` glow (decor layer)

WAVEFORM DIVIDER (inline SVG, `aria-hidden="true"`, static, full-bleed `w-full h-16`)
```tsx
<svg viewBox="0 0 800 60" className="w-full h-16" preserveAspectRatio="none" aria-hidden="true">
  <path d="M0 30 Q 40 5 80 30 T 160 30 T 240 30 T 320 30 T 400 30 T 480 30 T 560 30 T 640 30 T 720 30 T 800 30"
        fill="none" stroke="var(--neon-cyan)" strokeWidth="3" />
</svg>
```

PRESET FEATURE GRID (max-w-6xl mx-auto px-6 py-24)
- H2 `.pop` when in view: "Presets that do the work" — Archivo Black text-4xl md:text-5xl, "work" in `--neon-cyan`
- 4 cards, grid sm:grid-cols-2 lg:grid-cols-4 gap-6, entering `.pop` via IntersectionObserver once, stagger 90ms, each `rounded-2xl bg-[var(--panel)] border-2 border-transparent p-6`:
  1. "Fat Bass" — "Warm analog low-end modeled from three vintage oscillators stacked and detuned."
  2. "Laser Choir" — "Granular vocal synthesis morphed through comb filters for otherworldly pads."
  3. "Analog Dust" — "Built-in tape saturation and drift for that not-quite-perfect vintage wobble."
  4. "Cloud Pad" — "128-voice unison engine so one key press fills the whole mix."
- Preset name Archivo Black text-xl, JetBrains Mono text-xs tag underneath ("PRESET 01" … "PRESET 04") in `--neon-lime`
- Card hover (gated `@media (hover: hover) and (pointer: fine)`): `scale(1.06) rotate(1deg)` spring 200ms cubic-bezier(0.34, 1.56, 0.64, 1) + border-color to `--neon-pink` (160ms); press `active:scale-[0.94]`; alternate cards pre-rotated ±1deg

UNDER THE HOOD (bg-[var(--panel)] py-24, rounded-t-[3rem])
- H2: "Under the hood" — Archivo Black text-4xl text-[var(--glow-white)], "hood" in `--neon-orange`
- 4 spec tiles, grid sm:grid-cols-2 lg:grid-cols-4 gap-6, `.pop` stagger 90ms, each pairs one chunky-knob illustration with a label: "3 Oscillators" · "1 Self-Oscillating Filter" · "128-Voice Unison" · "12 Macro Knobs" — label Space Grotesk 700 text-sm text-[var(--glow-white)]/85 mt-3

PRICING (max-w-4xl mx-auto px-6 py-24 text-center)
- Panel `rounded-3xl bg-[var(--neon-cyan)] text-[var(--void)] p-12 relative overflow-hidden` with `--neon-pink`/`--neon-lime` glow shapes inside (decor)
- Price Archivo Black text-6xl tabular-nums: "$89" · sub "One-time. No subscription, ever."
- CTA row: `.pop` primary "Buy Bloop" (bg-[var(--void)] text-[var(--neon-cyan)] shadow-[0_6px_0_rgba(27,16,51,0.5)]) + secondary text link "Download the free demo"

TESTIMONIALS (max-w-5xl mx-auto px-6 pb-24)
- H2: "Producers are talking" — Archivo Black text-3xl text-[var(--glow-white)]
- 3 quote cards `rounded-2xl bg-[var(--panel)] p-6 border-2 border-[var(--neon-lime)]/30`, `.pop` in view stagger 90ms:
  - "Bloop's filter growls like it's mad at you. 10/10." — Wax Moth, producer
  - "I replaced four of my go-to plugins with one Bloop preset." — DJ Ferro
  - "The demo alone got me through a deadline." — Suki Tanaka

FOOTER (border-t border-[var(--glow-white)]/10, py-10, max-w-6xl mx-auto px-6, flex justify-between, Space Grotesk text-sm text-[var(--glow-white)]/70)
- "© Bloop Audio" + links Manual / Support / Changelog (`aria-label` on icon-only links)

ANIMATIONS (complete list)
- Entrances: `.pop` 0.5s back-out cubic-bezier(0.18, 0.89, 0.32, 1.28), stagger 90ms, once (load in hero, IntersectionObserver below)
- Idle: `.sticker` float-y 3s loop — dies under reduced-motion
- Hover: spring scale ≤1.08, 160–200ms cubic-bezier(0.34, 1.56, 0.64, 1), gated; border-color swaps ≤160ms
- Press: `active:scale-[0.94]` on buttons/cards, `active:scale-[0.98]` on text links
- Knob/slider illustrations and the waveform divider: no animation, ever (static decor)

RESPONSIVE
- Mobile: hero stacks (copy first, knob panel second), OS badges wrap, preset grid 1→2→4, under-the-hood tiles 2×2, pricing panel p-8; glows clipped by section `overflow-hidden`; no horizontal scroll

KEY DEPENDENCIES
`react@^18` `react-dom@^18` `typescript@^5` `vite@^5` `tailwindcss@^3` `lucide-react@latest`

CONSTRAINTS: playful maximalism on a neon-dark canvas — decorative glows/gradients and the knob/slider illustrations are the identity here (allowed in this profile; M08 disabled), but motion still animates only transform/opacity (border-color swaps ≤160ms are the documented paint exception), easing only from {cubic-bezier(0.34,1.56,0.64,1) · cubic-bezier(0.18,0.89,0.32,1.28) · cubic-bezier(0.23,1,0.32,1) · cubic-bezier(0.65,0,0.35,1)}, never ease-in, no `transition: all`, and every entrance starts at scale 0.9 or above — nothing pops in from zero. Bounce belongs to deliberate moments (entrances, CTAs, the logo's knob "O"s do not spin). Respect `prefers-reduced-motion`. No hotlinked commercial fonts or plugin-name trademarks — "Bloop" is an original fictional product. ARIA labels on icon-only links and OS badge list; knob illustrations, waveform divider, and decor `aria-hidden`.
