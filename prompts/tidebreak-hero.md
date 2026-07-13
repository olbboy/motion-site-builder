# Tidebreak

- **ID:** `tidebreak-hero`
- **Category:** Hero Section
- **Type:** hero
- **Profile:** `cinematic`

---

Build a single-page cinematic hero section for "Tidebreak" — a deep-sea autonomous robotics company whose AUV fleets map the ocean floor without a crew. Use React + Vite + Tailwind CSS + TypeScript + lucide-react. Default Tailwind config, no other UI libraries.

FONTS
- Display (headline, logo mark): Fraunces (Google Fonts, 400/600 + italic) — applied via inline `fontFamily: 'Fraunces'`
- Body (nav, description, labels): Inter (400/500)
- Import both in `index.css` via a Google Fonts `@import`

COLORS
- --background: #051A24 (near-black abyssal navy, `bg-[#051A24]`)
- --foreground: #D7E2EA
- --muted-foreground: rgba(215,226,234,0.6)
- --accent: #2DD4BF (single abyssal-teal accent — used only on the text-glow, telemetry dots, focus ring, and the active nav state)

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
.text-glow { text-shadow: 0 0 40px rgba(215,226,234,0.26), 0 0 90px rgba(45,212,191,0.24); }

@keyframes surface-in {
  from { opacity: 0; transform: translateY(24px); filter: blur(6px); }
  to   { opacity: 1; transform: translateY(0);    filter: blur(0); }
}
.animate-surface-in         { animation: surface-in 0.9s cubic-bezier(0.16, 1, 0.3, 1) both; }
.animate-surface-in-delay-1 { animation: surface-in 0.9s cubic-bezier(0.16, 1, 0.3, 1) 0.15s both; }
.animate-surface-in-delay-2 { animation: surface-in 0.9s cubic-bezier(0.16, 1, 0.3, 1) 0.30s both; }
.animate-surface-in-delay-3 { animation: surface-in 0.9s cubic-bezier(0.16, 1, 0.3, 1) 0.45s both; }

@media (prefers-reduced-motion: reduce) {
  .animate-surface-in, .animate-surface-in-delay-1, .animate-surface-in-delay-2, .animate-surface-in-delay-3 {
    animation: none; opacity: 1; transform: none; filter: none;
  }
}
```

VIDEO BACKGROUND (z-0)
- `<video autoPlay muted loop playsInline poster="{YOUR_POSTER_URL}" aria-hidden="true">` — `absolute inset-0 h-full w-full object-cover`
- src: `{YOUR_VIDEO_URL}` — supply your own licensed footage: a slow AUV point-cloud scan or bioluminescent deep-water drift, no visible seam at the loop point. Do not hotlink third-party media.
- Gradient overlay above video (z-[1]): `absolute inset-0 bg-gradient-to-b from-[#051A24]/75 via-[#051A24]/15 to-[#051A24]/80`

NAVBAR (z-20, glass pill, fixed)
- Wrapper: `<nav aria-label="Primary" className="fixed top-6 inset-x-6 z-20">`
- Pill: `.liquid-glass rounded-full max-w-5xl mx-auto px-6 py-3 flex items-center justify-between`
- Left: lucide `Waves` icon (16px, `text-[#2DD4BF]`) + "Tidebreak" (text-lg font-semibold tracking-tight text-[#D7E2EA], font-sans)
- Center (hidden md:flex, gap-8, ml-8): Fleet · Missions · Telemetry · Company — `text-sm text-[#D7E2EA]/70 hover:text-[#D7E2EA] transition-colors`
- Right: "Request access" — `.liquid-glass rounded-full px-6 py-2 text-sm font-medium text-[#D7E2EA] transition-transform hover:scale-[1.03] active:scale-[0.97]`

HERO (z-10, anchored bottom-right — mirrors Halcyon's bottom-left, flipped, to read like a status readout in the corner of a sonar display)
- Container: `absolute bottom-12 right-6 md:bottom-16 md:right-12 lg:right-16 max-w-2xl flex flex-col items-end text-right`
- Eyebrow (`.animate-surface-in`): "AUTONOMOUS · NO CREW · NO DAYLIGHT" — text-xs tracking-[0.22em] text-[#D7E2EA]/60 mb-5
- H1 (`.animate-surface-in-delay-1 .text-glow`): "The deep, <em class=\"italic\">charted</em>." — text-5xl sm:text-7xl md:text-8xl, Fraunces, leading-[0.95], tracking-tight, text-[#D7E2EA]
- Subtext (`.animate-surface-in-delay-2`): "Tidebreak's autonomous fleets survey the ocean floor at depths no diver could reach, streaming bathymetric data back to the surface in real time." — text-sm sm:text-base text-[#D7E2EA]/62 max-w-md mt-5 leading-relaxed ml-auto
- CTA row (`.animate-surface-in-delay-3`, mt-8 flex gap-3 justify-end):
  - "Deploy a survey" — `bg-white text-black rounded-full px-8 py-3.5 text-base font-medium transition-transform hover:scale-[1.03] active:scale-[0.97]`
  - "View live telemetry" — `.liquid-glass rounded-full px-6 py-3.5 text-base text-[#D7E2EA] transition-transform hover:scale-[1.03] active:scale-[0.97]`
- Telemetry chip row (`.animate-surface-in-delay-3`, mt-6 flex flex-wrap gap-2 justify-end) — the depth/fleet micro-detail: three `.liquid-glass rounded-full px-4 py-2 inline-flex items-center gap-2 text-xs font-medium text-[#D7E2EA]/75 tabular-nums` chips, each prefixed with a 4px accent dot (`bg-[#2DD4BF] rounded-full`):
  1. "DEPTH 3,812 M"
  2. "FLEET 12 AUVs ACTIVE"
  3. "UPTIME 99.2%"

LAYOUT
- Root: `relative min-h-screen w-full overflow-hidden bg-[#051A24]`
- Layer order: video z-0 → gradient overlay z-[1] → hero content z-10 → navbar z-20

ANIMATIONS
- Entrance: `surface-in` 0.9s cubic-bezier(0.16, 1, 0.3, 1), staggered — eyebrow 0s · H1 0.15s · subtext 0.30s · CTA row + telemetry chips 0.45s
- Hover: buttons scale 1.03; Press: `active:scale-[0.97]` (~160ms); `transition-transform`
- Animate only transform / opacity / filter

RESPONSIVE: mobile-first; nav center links hidden below `md`; H1 scales text-5xl → sm:text-7xl → md:text-8xl; telemetry chip row wraps onto two lines below `sm` (still right-aligned); hero copy caps at `max-w-md`; no horizontal scroll.

CONSTRAINTS: cinematic minimalism — near-black abyssal background, ONE teal accent used sparingly (glow, telemetry dots, focus, active nav state), no decorative blobs or radial gradients beyond the video + single gradient overlay (the video provides all depth). Default Tailwind config, no extra UI libraries beyond `lucide-react`. Only animate transform/opacity/filter. Respect `prefers-reduced-motion`. ARIA label on nav; `aria-hidden` on the decorative video; `poster` fallback required. Press feedback (`active:scale-[0.97]`) on every button.
