# Aphelion

- **ID:** `aphelion-hero`
- **Category:** Hero Section
- **Type:** hero

---

Build a single-page cinematic hero section for "Aphelion" — a private orbital-travel brand that sells the quiet awe of leaving the planet. Use React + Vite + Tailwind CSS + TypeScript + lucide-react. Default Tailwind config, no other UI libraries.

FONTS
- Display (headline, logo): Instrument Serif (Google Fonts) — inline `fontFamily: 'Instrument Serif'`
- Body (nav, description): Inter (400/500)
- Import both in `/src/styles/fonts.css`

COLORS (CSS variables in `/src/styles/theme.css`)
- --background: #051A24 (deep space-teal)
- --foreground: #D7E2EA
- --muted-foreground: rgba(215,226,234,0.62)
- --accent: #00D2FF (single cyan accent — used only on the italic emphasis word and the active nav underline)

GLOBAL CSS (paste verbatim into `/src/styles/theme.css`)
```css
@keyframes fade-rise {
  from { opacity: 0; transform: translateY(24px); }
  to   { opacity: 1; transform: translateY(0); }
}
.animate-fade-rise         { animation: fade-rise 1s cubic-bezier(0.16, 1, 0.3, 1) both; }
.animate-fade-rise-delay   { animation: fade-rise 1s cubic-bezier(0.16, 1, 0.3, 1) 0.2s both; }
.animate-fade-rise-delay-2 { animation: fade-rise 1s cubic-bezier(0.16, 1, 0.3, 1) 0.4s both; }

@media (prefers-reduced-motion: reduce) {
  .animate-fade-rise, .animate-fade-rise-delay, .animate-fade-rise-delay-2 {
    animation: none; opacity: 1; transform: none;
  }
}
```

VIDEO BACKGROUND (z-0, seamless fade loop)
- `<video autoPlay muted playsInline poster="{YOUR_POSTER_URL}" aria-hidden="true">` — className `absolute inset-0 h-full w-full object-cover`
- src: `{YOUR_VIDEO_URL}` — supply your own licensed or royalty-free footage (a slow orbital / cloud-layer / starfield drift suits the brand); do not hotlink third-party media
- Seamless fade loop via React `useEffect` + `useRef`: `requestAnimationFrame` monitors `currentTime`/`duration`; fade opacity 0→1 over 0.5s at start, 1→0 over 0.5s before end; on `ended` set opacity 0, wait 100ms, reset `currentTime = 0`, then `play()`. (No `loop` attribute — the handler drives the loop.)
- Gradient overlay above video (z-[1]): `absolute inset-0 bg-gradient-to-b from-[#051A24]/70 via-transparent to-[#051A24]`

NAVBAR (z-20)
- Wrapper: `<nav aria-label="Primary">` — flex justify-between items-center, max-w-7xl mx-auto, px-8 py-6
- Logo: "Aphelion" — text-2xl tracking-tight, Instrument Serif, color #D7E2EA
- Links (hidden md:flex, gap-8, text-sm, transition-colors): Missions · Vehicle · Crew · Journal — text-[#D7E2EA]/70 hover:text-[#D7E2EA]
- CTA: "Reserve a seat" — rounded-full, px-6 py-2.5, text-sm, bg-[#D7E2EA] text-[#051A24], transition-transform hover:scale-[1.03] active:scale-[0.97]

HERO (z-10, centered)
- Container: flex flex-col items-center justify-center text-center min-h-screen px-6
- Eyebrow (`.animate-fade-rise`): "PRIVATE ORBITAL FLIGHT" — text-xs tracking-[0.24em] text-[#D7E2EA]/60 mb-6
- H1 (`.animate-fade-rise`): "Farther than <em class=\"italic text-[#00D2FF]\">far</em>." — text-5xl sm:text-7xl md:text-8xl, max-w-4xl, font-normal, Instrument Serif, leading-[0.95], tracking-[-0.02em], color #D7E2EA
- Description (`.animate-fade-rise-delay`): "Eleven minutes of weightlessness. A window seat above the terminator line. Aphelion makes the edge of space a place you can actually go." — text-base sm:text-lg, max-w-2xl, mt-8, leading-relaxed, color #D7E2EA/62
- CTA (`.animate-fade-rise-delay-2`): "Begin pre-flight" — rounded-full, px-12 py-4, text-base, mt-10, bg-[#D7E2EA] text-[#051A24], transition-transform hover:scale-[1.03] active:scale-[0.97]

LAYOUT
- Root: relative min-h-screen w-full overflow-hidden bg-[#051A24]
- Layer order: video z-0 → gradient overlay z-[1] → nav + hero z-10..z-20

ANIMATIONS
- Entrance: fade-rise 1s cubic-bezier(0.16, 1, 0.3, 1), staggered — eyebrow/H1 0s · description 0.2s · CTA 0.4s
- Hover: buttons scale 1.03; Press: `active:scale-[0.97]` (~160ms); `transition-transform`
- Animate only transform / opacity

RESPONSIVE: mobile-first; nav links hidden below `md`; H1 scales text-5xl → sm:text-7xl → md:text-8xl; no horizontal scroll.

CONSTRAINTS: cinematic minimalism — deep space-teal background, ONE cyan accent used sparingly, no decorative blobs or radial gradients over the video (the video + gradient overlay provide all depth). Default Tailwind config, no extra UI libraries beyond `lucide-react`. Only animate transform/opacity. Respect `prefers-reduced-motion`. ARIA label on nav; `aria-hidden` on the decorative video; `poster` fallback required.
