# Velvet Static

- **ID:** `velvet-static-hero`
- **Category:** Hero Section
- **Type:** hero
- **Profile:** `cinematic`

---

Build a single-page cinematic hero section for "Velvet Static" — a 24-seat hi-fi vinyl listening bar in Saigon built around one hand-matched horn system. Use React + Vite + Tailwind CSS + TypeScript + lucide-react. Default Tailwind config, no other UI libraries.

FONTS
- Display (headline, logo mark): DM Serif Display (Google Fonts, regular + italic) — applied via inline `fontFamily: 'DM Serif Display'`
- Body (nav, description, labels): Inter (400/500)
- Import both in `index.css` via a Google Fonts `@import`

COLORS
- --background: #0D0906 (warm near-black bar interior, `bg-[#0D0906]`)
- --foreground: #F5EFE4
- --muted-foreground: rgba(245,239,228,0.6)
- --accent: #E0A458 (single warm-amber accent — used only on the text-glow, chip dots, focus ring, and the active nav state)

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
.text-glow { text-shadow: 0 0 40px rgba(245,239,228,0.28), 0 0 90px rgba(224,164,88,0.24); }

/* headline entrance — subtext, CTA, and the opening-hours chip */
@keyframes warm-rise {
  from { opacity: 0; transform: translateY(24px); filter: blur(6px); }
  to   { opacity: 1; transform: translateY(0);    filter: blur(0); }
}
.animate-warm-rise         { animation: warm-rise 0.9s cubic-bezier(0.16, 1, 0.3, 1) both; }
.animate-warm-rise-delay-1 { animation: warm-rise 0.9s cubic-bezier(0.16, 1, 0.3, 1) 0.7s both; }
.animate-warm-rise-delay-2 { animation: warm-rise 0.9s cubic-bezier(0.16, 1, 0.3, 1) 0.88s both; }

/* headline char-level reveal — a load-time variation on scroll-char-reveal (catalog #10),
   used here because a single hero has no scroll progress to bind to */
@keyframes glow-in {
  from { opacity: 0; transform: translateY(16px); filter: blur(4px); }
  to   { opacity: 1; transform: translateY(0);    filter: blur(0); }
}
.char {
  display: inline-block;
  animation: glow-in 0.6s cubic-bezier(0.16, 1, 0.3, 1) backwards;
  animation-delay: calc(150ms + var(--char-i) * 20ms);
}

@media (prefers-reduced-motion: reduce) {
  .animate-warm-rise, .animate-warm-rise-delay-1, .animate-warm-rise-delay-2, .char {
    animation: none; opacity: 1; transform: none; filter: none;
  }
}
```

VIDEO BACKGROUND (z-0)
- `<video autoPlay muted loop playsInline poster="{YOUR_POSTER_URL}" aria-hidden="true">` — `absolute inset-0 h-full w-full object-cover`
- src: `{YOUR_VIDEO_URL}` — supply your own licensed footage: a slow dolly across a glowing tube amp and a spinning record in low amber light, no visible seam at the loop point. Do not hotlink third-party media.
- Gradient overlay above video (z-[1]): `absolute inset-0 bg-gradient-to-r from-[#0D0906]/80 via-[#0D0906]/25 to-[#0D0906]/60`

NAVBAR (z-20, glass pill, fixed)
- Wrapper: `<nav aria-label="Primary" className="fixed top-6 inset-x-6 z-20">`
- Pill: `.liquid-glass rounded-full max-w-5xl mx-auto px-6 py-3 flex items-center justify-between`
- Left: lucide `Disc3` icon (16px, `text-[#E0A458]`) + "Velvet Static" (text-lg font-semibold tracking-tight text-[#F5EFE4], font-sans)
- Center (hidden md:flex, gap-8, ml-8): Sessions · The Room · Records · Reserve — `text-sm text-[#F5EFE4]/70 hover:text-[#F5EFE4] transition-colors`
- Right: "Reserve a seat" — `.liquid-glass rounded-full px-6 py-2 text-sm font-medium text-[#F5EFE4] transition-transform hover:scale-[1.03] active:scale-[0.97]`

HERO (z-10, anchored top-left — differs from a bottom/centered hero so the video's lower two-thirds, where the amp and turntable sit, stays uncovered)
- Container: `absolute top-24 left-6 md:top-32 md:left-12 lg:left-16 max-w-xl flex flex-col items-start text-left`
- Eyebrow (`.animate-warm-rise`): "HI-FI · VINYL ONLY · SAIGON" — text-xs tracking-[0.22em] text-[#F5EFE4]/60 mb-5
- H1 (`.text-glow`, text-5xl sm:text-7xl md:text-8xl, DM Serif Display, leading-[0.95], tracking-tight, text-[#F5EFE4]) — char-level reveal: split "Vinyl, after midnight." into individual characters, each `<span className="char" style={{ '--char-i': i }}>` (space rendered as ` `); the characters spanning "midnight" additionally get `italic` on their `className` (`"char italic"`) so the phrase reads emphasized once fully revealed — indices run continuously 0…21 across the whole string so the stagger never resets
- Subtext (`.animate-warm-rise-delay-1`): "Velvet Static is a 24-seat listening bar built around a single system — hand-matched horns, first-pressing vinyl, and a no-phones policy after 22:00." — text-sm sm:text-base text-[#F5EFE4]/65 max-w-md mt-5 leading-relaxed
- CTA row (`.animate-warm-rise-delay-2`, mt-8 flex flex-col sm:flex-row gap-3):
  - "Reserve a seat" — `bg-white text-black rounded-full px-8 py-3.5 text-base font-medium transition-transform hover:scale-[1.03] active:scale-[0.97]`
  - "See tonight's records" — `.liquid-glass rounded-full px-6 py-3.5 text-base text-[#F5EFE4] transition-transform hover:scale-[1.03] active:scale-[0.97]`
- Opening-hours chip (`.animate-warm-rise-delay-2`, mt-6): `.liquid-glass rounded-full px-4 py-2 inline-flex items-center gap-2 text-xs text-[#F5EFE4]/70` — lucide `Clock` icon (12px, `text-[#E0A458]`) + "OPEN THU–SUN · 19:00–01:00"

LAYOUT
- Root: `relative min-h-screen w-full overflow-hidden bg-[#0D0906]`
- Layer order: video z-0 → gradient overlay z-[1] → hero content z-10 → navbar z-20

ANIMATIONS
- Headline: `glow-in` 0.6s cubic-bezier(0.16, 1, 0.3, 1), per-character delay `150ms + i * 20ms` (char-level reveal, see GLOBAL CSS)
- Rest of hero: `warm-rise` 0.9s cubic-bezier(0.16, 1, 0.3, 1) — eyebrow 0s · subtext 0.7s · CTA row + hours chip 0.88s
- Hover: buttons scale 1.03; Press: `active:scale-[0.97]` (~160ms); `transition-transform`
- Animate only transform / opacity / filter

RESPONSIVE: mobile-first; nav center links hidden below `md`; H1 scales text-5xl → sm:text-7xl → md:text-8xl (characters reflow, per-char delays unchanged); CTA row stacks vertically below `sm`; hero copy caps at `max-w-xl`; no horizontal scroll.

CONSTRAINTS: cinematic minimalism — warm near-black background, ONE amber accent used sparingly (glow, chip dot/icon, focus, active nav state), no decorative blobs or radial gradients beyond the video + single gradient overlay (the video provides all depth). Default Tailwind config, no extra UI libraries beyond `lucide-react`. Only animate transform/opacity/filter. Respect `prefers-reduced-motion` (char-level reveal collapses to the final state instantly). ARIA label on nav; `aria-hidden` on the decorative video; `poster` fallback required. Press feedback (`active:scale-[0.97]`) on every button.
