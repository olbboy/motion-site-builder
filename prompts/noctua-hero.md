# Noctua

- **ID:** `noctua-hero`
- **Category:** Hero Section
- **Type:** hero
- **Profile:** `cinematic`

---

Build a single-page cinematic hero section for "Noctua" — a dark-sky observatory retreat brand operating three off-grid domes under certified Bortle-1 skies. Use React + Vite + Tailwind CSS + TypeScript + lucide-react. Default Tailwind config, no other UI libraries.

FONTS
- Display (headline, logo mark): Cormorant Garamond (Google Fonts, 500/600 + italic) — applied via inline `fontFamily: 'Cormorant Garamond'`
- Body (nav, description, labels): Inter (400/500)
- Import both in `index.css` via a Google Fonts `@import`

COLORS
- --background: #05070C (near-black indigo, `bg-[#05070C]`)
- --foreground: #FFFFFF
- --muted-foreground: rgba(255,255,255,0.6)
- --accent: #6EA8FF (single ice-blue accent — used only on the text-glow, forecast-chip dot, focus ring, and the active nav state)

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
.text-glow { text-shadow: 0 0 40px rgba(255,255,255,0.28), 0 0 90px rgba(110,168,255,0.22); }

@keyframes drift-in {
  from { opacity: 0; transform: translateY(28px); filter: blur(7px); }
  to   { opacity: 1; transform: translateY(0);    filter: blur(0); }
}
.animate-drift-in         { animation: drift-in 1s cubic-bezier(0.16, 1, 0.3, 1) both; }
.animate-drift-in-delay-1 { animation: drift-in 1s cubic-bezier(0.16, 1, 0.3, 1) 0.18s both; }
.animate-drift-in-delay-2 { animation: drift-in 1s cubic-bezier(0.16, 1, 0.3, 1) 0.36s both; }
.animate-drift-in-delay-3 { animation: drift-in 1s cubic-bezier(0.16, 1, 0.3, 1) 0.54s both; }

@media (prefers-reduced-motion: reduce) {
  .animate-drift-in, .animate-drift-in-delay-1, .animate-drift-in-delay-2, .animate-drift-in-delay-3 {
    animation: none; opacity: 1; transform: none; filter: none;
  }
}
```

VIDEO BACKGROUND (z-0)
- `<video autoPlay muted loop playsInline poster="{YOUR_POSTER_URL}" aria-hidden="true">` — `absolute inset-0 h-full w-full object-cover`
- src: `{YOUR_VIDEO_URL}` — supply your own licensed footage: a slow, static-tripod star-field timelapse with no visible seam at the loop point (e.g. a locked-off astro timelapse under a release-cleared license). Do not hotlink third-party media.
- Gradient overlay above video (z-[1]): `absolute inset-0 bg-gradient-to-b from-[#05070C]/70 via-[#05070C]/10 to-[#05070C]/80` (darkens the nav strip and footer strip, keeps the mid-sky visible)

NAVBAR (z-20, glass pill, fixed)
- Wrapper: `<nav aria-label="Primary" className="fixed top-6 inset-x-6 z-20">`
- Pill: `.liquid-glass rounded-full max-w-5xl mx-auto px-6 py-3 flex items-center justify-between`
- Left: lucide `Moon` icon (16px, `text-[#6EA8FF]`) + "Noctua" (text-lg font-semibold tracking-tight text-white, font-sans)
- Center (hidden md:flex, gap-8, ml-8): Retreats · Sky Almanac · Field Notes · Access — `text-sm text-white/70 hover:text-white transition-colors`
- Right: "Check availability" — `.liquid-glass rounded-full px-6 py-2 text-sm font-medium text-white transition-transform hover:scale-[1.03] active:scale-[0.97]`

HERO (z-10, centered — vertically centered rather than corner-anchored)
- Container: `absolute inset-0 z-10 flex flex-col items-center justify-center text-center px-6 -translate-y-[4%]`
- Eyebrow (`.animate-drift-in`): "BORTLE ONE · ZERO LIGHT POLLUTION" — text-xs tracking-[0.22em] text-white/60 mb-5
- H1 (`.animate-drift-in-delay-1 .text-glow`): "The dark, <em class=\"italic\">unbroken</em>." — text-5xl sm:text-7xl md:text-8xl, Cormorant Garamond, leading-[0.95], tracking-tight, text-white
- Subtext (`.animate-drift-in-delay-2`): "Noctua operates three off-grid domes beneath certified Bortle-1 skies — a private telescope, a research-grade mount, and forty miles of silence between you and the nearest bulb." — text-sm sm:text-base text-white/62 max-w-md mx-auto mt-5 leading-relaxed
- CTA row (`.animate-drift-in-delay-3`, mt-8 flex flex-col sm:flex-row gap-3 items-center justify-center):
  - "Reserve a night" — `bg-white text-black rounded-full px-8 py-3.5 text-base font-medium transition-transform hover:scale-[1.03] active:scale-[0.97]`
  - "Read the sky report" — `.liquid-glass rounded-full px-6 py-3.5 text-base text-white transition-transform hover:scale-[1.03] active:scale-[0.97]`
- Forecast chip (`.animate-drift-in-delay-3`, mt-6): `.liquid-glass rounded-full px-4 py-2 inline-flex items-center gap-2 text-xs text-white/70` — a 4px accent dot (`bg-[#6EA8FF] rounded-full`) + "Tonight's seeing: 9.8/10 · New moon in 3 days"

LAYOUT
- Root: `relative min-h-screen w-full overflow-hidden bg-[#05070C]`
- Layer order: video z-0 → gradient overlay z-[1] → hero content z-10 → navbar z-20

ANIMATIONS
- Entrance: `drift-in` 1s cubic-bezier(0.16, 1, 0.3, 1), staggered — eyebrow 0s · H1 0.18s · subtext 0.36s · CTA row + chip 0.54s
- Hover: buttons scale 1.03; Press: `active:scale-[0.97]` (~160ms); `transition-transform`
- Animate only transform / opacity / filter

RESPONSIVE: mobile-first; nav center links hidden below `md`; H1 scales text-5xl → sm:text-7xl → md:text-8xl; CTA row stacks vertically below `sm`; hero copy caps at `max-w-md`; no horizontal scroll.

CONSTRAINTS: cinematic minimalism — near-black background, ONE ice-blue accent used sparingly (glow, dot, focus, active nav state), no decorative blobs or radial gradients beyond the video + single gradient overlay (the video provides all depth). Default Tailwind config, no extra UI libraries beyond `lucide-react`. Only animate transform/opacity/filter. Respect `prefers-reduced-motion`. ARIA label on nav; `aria-hidden` on the decorative video; `poster` fallback required. Press feedback (`active:scale-[0.97]`) on every button.
