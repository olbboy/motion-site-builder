# Halcyon

- **ID:** `halcyon-hero`
- **Category:** Hero Section
- **Type:** hero

---

Build a single-page cinematic hero section for "Halcyon" — an AI compute-infrastructure brand whose promise is *calm* intelligence at scale. Use React + Vite + Tailwind CSS + TypeScript + lucide-react. Default Tailwind config, no other UI libraries.

FONTS
- Display (headline, logo): Instrument Serif (Google Fonts) — applied via inline `fontFamily: 'Instrument Serif'`
- Body (nav, description, labels): Inter (400/500)
- Import both in `index.css` via a Google Fonts `@import`

COLORS
- --background: #0B0B0F (near-black, `bg-[#0B0B0F]`)
- --foreground: #FFFFFF
- --muted-foreground: rgba(255,255,255,0.62)
- --accent: #7342E2 (single violet accent — used only on the text-glow, focus ring, and the active nav dot)

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
.text-glow { text-shadow: 0 0 40px rgba(255,255,255,0.30), 0 0 90px rgba(115,66,226,0.18); }

@keyframes rise {
  from { opacity: 0; transform: translateY(22px); filter: blur(6px); }
  to   { opacity: 1; transform: translateY(0);    filter: blur(0); }
}
.animate-rise         { animation: rise 0.9s cubic-bezier(0.16, 1, 0.3, 1) both; }
.animate-rise-delay-1 { animation: rise 0.9s cubic-bezier(0.16, 1, 0.3, 1) 0.15s both; }
.animate-rise-delay-2 { animation: rise 0.9s cubic-bezier(0.16, 1, 0.3, 1) 0.30s both; }
.animate-rise-delay-3 { animation: rise 0.9s cubic-bezier(0.16, 1, 0.3, 1) 0.45s both; }

@media (prefers-reduced-motion: reduce) {
  .animate-rise, .animate-rise-delay-1, .animate-rise-delay-2, .animate-rise-delay-3 {
    animation: none; opacity: 1; transform: none; filter: none;
  }
}
```

VIDEO BACKGROUND (z-0)
- `<video autoPlay muted loop playsInline poster="{YOUR_POSTER_URL}" aria-hidden="true">` — `absolute inset-0 h-full w-full object-cover`
- src: `{YOUR_VIDEO_URL}` — supply your own licensed or royalty-free footage (e.g. Pexels/Coverr under their license); a slow drifting particle-field or data-flow loop suits the brand. Do not hotlink third-party media.
- Gradient overlay above video (z-[1]): `absolute inset-0 bg-gradient-to-t from-[#0B0B0F] via-[#0B0B0F]/20 to-[#0B0B0F]/60`

NAVBAR (z-20, glass pill, fixed)
- Wrapper: `<nav aria-label="Primary" className="fixed top-6 inset-x-6 z-20">`
- Pill: `.liquid-glass rounded-full max-w-5xl mx-auto px-6 py-3 flex items-center justify-between`
- Left: a 6px violet dot (`bg-[#7342E2] rounded-full`) + "Halcyon" (text-lg font-semibold tracking-tight text-white, font-sans)
- Center (hidden md:flex, gap-8, ml-8): Platform · Compute · Research · Company — `text-sm text-white/70 hover:text-white transition-colors`
- Right: "Request access" — `.liquid-glass rounded-full px-6 py-2 text-sm font-medium text-white transition-transform hover:scale-[1.03] active:scale-[0.97]`

HERO (z-10, anchored bottom-left)
- Container: `absolute bottom-12 left-6 md:bottom-16 md:left-12 lg:left-16 max-w-2xl flex flex-col items-start text-left`
- Eyebrow (`.animate-rise`): "AI COMPUTE, WITHOUT THE NOISE" — text-xs tracking-[0.22em] text-white/60 mb-5
- H1 (`.animate-rise-delay-1 .text-glow`): "Compute, <em class=\"italic\">quieted</em>." — text-5xl sm:text-7xl md:text-8xl, Instrument Serif, leading-[0.95], tracking-tight, text-white
- Subtext (`.animate-rise-delay-2`): "Halcyon runs your largest models on calm, dedicated silicon — predictable latency, transparent cost, zero drama." — text-sm sm:text-base text-white/62 max-w-md mt-5 leading-relaxed
- CTA row (`.animate-rise-delay-3`, mt-8 flex gap-3):
  - "Start building" — bg-white text-black rounded-full px-8 py-3.5 text-base font-medium transition-transform hover:scale-[1.03] active:scale-[0.97]
  - "Read the docs" — `.liquid-glass rounded-full px-6 py-3.5 text-base text-white transition-transform hover:scale-[1.03] active:scale-[0.97]`

LAYOUT
- Root: `relative min-h-screen w-full overflow-hidden bg-[#0B0B0F]`
- Layer order: video z-0 → gradient overlay z-[1] → hero content z-10 → navbar z-20

ANIMATIONS
- Entrance: `rise` 0.9s cubic-bezier(0.16, 1, 0.3, 1), staggered — eyebrow 0s · H1 0.15s · subtext 0.30s · CTA 0.45s
- Hover: buttons scale 1.03; Press: `active:scale-[0.97]` (~160ms); `transition-transform`
- Animate only transform / opacity / filter

RESPONSIVE: mobile-first; nav center links hidden below `md`; H1 scales text-5xl → sm:text-7xl → md:text-8xl; hero block caps at `max-w-2xl`; no horizontal scroll.

CONSTRAINTS: cinematic minimalism — near-black background, ONE violet accent used sparingly (glow, dot, focus), no decorative blobs or radial gradients beyond the video + single overlay (the video provides all depth). Default Tailwind config, no extra UI libraries beyond `lucide-react`. Only animate transform/opacity/filter. Respect `prefers-reduced-motion`. ARIA label on nav; `aria-hidden` on the decorative video; `poster` fallback required. Press feedback (`active:scale-[0.97]`) on every button.
