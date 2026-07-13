# Verdant

- **ID:** `verdant-hero`
- **Category:** Hero Section
- **Type:** hero

---

Build a single-page cinematic hero section for "Verdant" — a regenerative-agriculture brand that funds and tracks living farmland. Warm, patient, alive. Use React + Vite + Tailwind CSS + TypeScript + lucide-react. Default Tailwind config, no other UI libraries.

FONTS
- Display (headline, logo): Playfair Display (Google Fonts, 500/500-italic) — class `.font-display`
- Body (nav, description): DM Sans (400/500)
- Import both in `index.css` via Google Fonts `@import`; body uses DM Sans

COLORS
- --background: #1F2A1D (deep forest)
- --foreground: #F4F1E8 (cream)
- --muted-foreground: rgba(244,241,232,0.64)
- --accent: #E1E0CC (single warm-cream accent — used only on the italic emphasis word and the CTA hover)

GLOBAL CSS (paste verbatim into `index.css`)
```css
.font-display { font-family: 'Playfair Display', Georgia, serif; }

@keyframes grow-in {
  from { opacity: 0; transform: translateY(20px) scale(0.98); }
  to   { opacity: 1; transform: translateY(0) scale(1); }
}
.animate-grow         { animation: grow-in 0.9s cubic-bezier(0.16, 1, 0.3, 1) both; }
.animate-grow-delay-1 { animation: grow-in 0.9s cubic-bezier(0.16, 1, 0.3, 1) 0.18s both; }
.animate-grow-delay-2 { animation: grow-in 0.9s cubic-bezier(0.16, 1, 0.3, 1) 0.36s both; }

@media (prefers-reduced-motion: reduce) {
  .animate-grow, .animate-grow-delay-1, .animate-grow-delay-2 {
    animation: none; opacity: 1; transform: none;
  }
}
```

VIDEO BACKGROUND (z-0)
- `<video autoPlay muted loop playsInline poster="{YOUR_POSTER_URL}" aria-hidden="true">` — `absolute inset-0 h-full w-full object-cover`
- src: `{YOUR_VIDEO_URL}` — supply your own licensed or royalty-free footage (wind moving across a field, or morning light through leaves, suits the brand); do not hotlink third-party media
- Gradient overlay above video (z-[1]): `absolute inset-0 bg-gradient-to-t from-[#1F2A1D] via-[#1F2A1D]/25 to-[#1F2A1D]/55`

NAVBAR (z-20)
- Wrapper: `<nav aria-label="Primary">` — flex justify-between items-center, max-w-6xl mx-auto, px-8 py-6
- Logo: "Verdant" — `.font-display text-2xl tracking-tight text-[#F4F1E8]`
- Links (hidden md:flex, gap-8, text-sm): Farmland · Impact · Science · Journal — text-[#F4F1E8]/64 hover:text-[#F4F1E8] transition-colors
- CTA: "Invest in soil" — rounded-full px-6 py-2.5 text-sm bg-[#F4F1E8] text-[#1F2A1D], transition-transform hover:scale-[1.03] active:scale-[0.97]

HERO (z-10, bottom-left)
- Container: `min-h-screen flex flex-col justify-end max-w-6xl mx-auto w-full px-8 pb-16 md:pb-24`
- Eyebrow (`.animate-grow`): "REGENERATIVE FARMLAND, MEASURED" — text-xs tracking-[0.2em] text-[#F4F1E8]/60 mb-5
- H1 (`.animate-grow` `.font-display`): "Grown <em class=\"italic text-[#E1E0CC]\">slow</em>, on purpose." — text-5xl sm:text-7xl md:text-8xl, max-w-3xl, leading-[1.0], tracking-tight, text-[#F4F1E8]
- Description (`.animate-grow-delay-1`): "We put capital into land that heals — then show you the carbon, the water, and the yield, season by season, in numbers you can trust." — text-base sm:text-lg text-[#F4F1E8]/64 max-w-xl mt-6 leading-relaxed
- CTA row (`.animate-grow-delay-2`, mt-8 flex gap-3):
  - "Explore the fund" — rounded-full px-8 py-3.5 text-base bg-[#F4F1E8] text-[#1F2A1D] transition-transform hover:scale-[1.03] active:scale-[0.97]
  - "How it works" — rounded-full px-6 py-3.5 text-base border border-[#F4F1E8]/30 text-[#F4F1E8] transition-transform hover:scale-[1.03] active:scale-[0.97]

LAYOUT
- Root: relative min-h-screen w-full overflow-hidden bg-[#1F2A1D]
- Layer order: video z-0 → gradient overlay z-[1] → hero content z-10 → navbar z-20

ANIMATIONS
- Entrance: grow-in 0.9s cubic-bezier(0.16, 1, 0.3, 1), staggered — eyebrow/H1 0s · description 0.18s · CTA 0.36s
- Hover: buttons scale 1.03; Press: `active:scale-[0.97]` (~160ms); `transition-transform`
- Animate only transform / opacity (the grow-in scale is a transform)

RESPONSIVE: mobile-first; nav links hidden below `md`; H1 scales text-5xl → sm:text-7xl → md:text-8xl; no horizontal scroll.

CONSTRAINTS: cinematic organic minimalism — deep-forest background, ONE warm-cream accent used sparingly, no decorative blobs or radial gradients beyond the video + single overlay (the video provides all depth). Default Tailwind config, no extra UI libraries beyond `lucide-react`. Only animate transform/opacity. Respect `prefers-reduced-motion`. ARIA label on nav; `aria-hidden` on the decorative video; `poster` fallback required. Press feedback (`active:scale-[0.97]`) on every button.
