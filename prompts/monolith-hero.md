# Monolith

- **ID:** `monolith-hero`
- **Category:** Hero Section
- **Type:** hero

---

Build a single-page cinematic hero section for "Monolith" — a brutalist architecture and industrial-design studio. Confident, heavy, quiet. Use React + Vite + Tailwind CSS + TypeScript + lucide-react. Default Tailwind config, no other UI libraries.

FONTS
- Display (logo, headline): Anton (Google Fonts, 400) — a tall condensed grotesque; class `.font-display`
- Body (nav, description): Inter (400/500)
- Import both in `index.css` via Google Fonts `@import`; body uses Inter

COLORS
- --background: #0A0A0C (ink)
- --foreground: #F2F0EC (warm bone-white)
- --muted-foreground: rgba(242,240,236,0.60)
- --accent: #EF4D23 (single ember accent — used only on the index numerals and the CTA underline)

GLOBAL CSS (paste verbatim into `index.css`)
```css
.font-display { font-family: 'Anton', system-ui, sans-serif; }

@keyframes reveal {
  from { opacity: 0; transform: translateY(28px); }
  to   { opacity: 1; transform: translateY(0); }
}
.animate-reveal    { animation: reveal 0.85s cubic-bezier(0.16, 1, 0.3, 1) both; }
.animate-reveal-1  { animation: reveal 0.85s cubic-bezier(0.16, 1, 0.3, 1) 0.12s both; }
.animate-reveal-2  { animation: reveal 0.85s cubic-bezier(0.16, 1, 0.3, 1) 0.24s both; }
.animate-reveal-3  { animation: reveal 0.85s cubic-bezier(0.16, 1, 0.3, 1) 0.36s both; }

@media (prefers-reduced-motion: reduce) {
  .animate-reveal, .animate-reveal-1, .animate-reveal-2, .animate-reveal-3 {
    animation: none; opacity: 1; transform: none;
  }
}
```

VIDEO BACKGROUND (z-0)
- `<video autoPlay muted loop playsInline poster="{YOUR_POSTER_URL}" aria-hidden="true">` — `absolute inset-0 h-full w-full object-cover object-center`
- src: `{YOUR_VIDEO_URL}` — supply your own licensed or royalty-free footage (a slow pan across raw concrete / a monolithic structure suits the brand); do not hotlink third-party media
- Overlay above video (z-[1]): `absolute inset-0 bg-[#0A0A0C]/45` (flat scrim, no gradient blobs)

NAVBAR (z-20, fixed top)
- `<nav aria-label="Primary">` — flex justify-between items-center, px-6 md:px-12 py-6
- Left: "MONOLITH" — `.font-display text-2xl tracking-wide text-[#F2F0EC]`
- Center (hidden md:flex, gap-10, text-sm): Work · Studio · Process · Contact — text-[#F2F0EC]/60 hover:text-[#F2F0EC] transition-colors
- Right: "Start a project" — border border-[#F2F0EC]/25 rounded-full px-6 py-2.5 text-sm text-[#F2F0EC] transition-transform hover:scale-[1.03] active:scale-[0.97]

HERO (z-10, bottom-aligned)
- Container: `min-h-screen flex flex-col justify-end px-6 md:px-12 pb-14 md:pb-20`
- Meta row (`.animate-reveal`, mb-6, flex gap-6 text-xs tracking-[0.18em] text-[#F2F0EC]/60): `<span class="text-[#EF4D23]">01</span>` "STRUCTURE" · `<span class="text-[#EF4D23]">02</span>` "MATERIAL" · `<span class="text-[#EF4D23]">03</span>` "LIGHT"
- H1 (`.animate-reveal-1`): two lines `.font-display uppercase` — "WE BUILD" / "WHAT LASTS." — text-6xl sm:text-8xl md:text-[9rem], leading-[0.88], tracking-tight, text-[#F2F0EC]
- Description (`.animate-reveal-2`): "A studio for permanent things — concrete, steel, and daylight, arranged so a place still feels inevitable fifty years on." — text-base md:text-lg text-[#F2F0EC]/60 max-w-xl mt-6
- CTA (`.animate-reveal-3`, mt-8, inline-flex items-center gap-2): "See the work" — text-base text-[#F2F0EC], border-b-2 border-[#EF4D23] pb-1, with a lucide `ArrowUpRight` (size 18), transition-transform hover:translate-x-1 active:scale-[0.97]

LAYOUT
- Root: relative min-h-screen w-full overflow-hidden bg-[#0A0A0C]
- Layer order: video z-0 → scrim z-[1] → hero content z-10 → nav z-20

ANIMATIONS
- Entrance: reveal 0.85s cubic-bezier(0.16, 1, 0.3, 1), staggered — meta 0s · H1 0.12s · description 0.24s · CTA 0.36s
- Hover: outline button scale 1.03; CTA arrow `translate-x-1`; Press: `active:scale-[0.97]`; `transition-transform`
- Animate only transform / opacity

RESPONSIVE: mobile-first; nav center links hidden below `md`; H1 scales text-6xl → sm:text-8xl → md:text-[9rem]; no horizontal scroll.

CONSTRAINTS: cinematic brutalist minimalism — ink background, bone-white type, ONE ember accent confined to the index numerals and CTA underline, a single flat scrim over the video (no gradient blobs or radial glows). Default Tailwind config, no extra UI libraries beyond `lucide-react`. Only animate transform/opacity. Respect `prefers-reduced-motion`. ARIA label on nav; `aria-hidden` on the decorative video; `poster` fallback required. Press feedback (`active:scale-[0.97]`) on interactive controls.
