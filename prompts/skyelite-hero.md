# SkyElite Private Jets

- **ID:** `skyelite-hero`
- **Category:** Landing Page
- **Type:** hero

---

Build a single-page hero section for "SkyElite" — a premium private jet landing page. Use React + Vite + Tailwind CSS + TypeScript + lucide-react. Default Tailwind config, no other UI libraries.

FONTS
- Body & UI (headings, nav, all text): Inter (Google Fonts, weights 400/500/600/700) — `font-family: 'Inter', sans-serif` on body

COLORS
- --background: #F9FAFB (bg-gray-50)
- --foreground: #111827 (text-gray-900)
- --muted-foreground: #4B5563 (text-gray-600)
- --muted-foreground-hover: #6B7280 (text-gray-700, nav hover)
- --heading-secondary: #6B7280 (text-gray-500, "Premium.")
- --heading-primary: #202A36 ("Accessible.", primary CTA)
- --heading-primary-hover: #1A2229
- --button-secondary-bg: #D1D5DB (bg-gray-300)
- --button-secondary-bg-hover: #9CA3AF (bg-gray-400)
- --button-secondary-text: #1F2937 (text-gray-800)

GLOBAL CSS (paste verbatim)
```css
@keyframes fade-rise {
  from { opacity: 0; transform: translateY(20px); }
  to   { opacity: 1; transform: translateY(0); }
}
.animate-fade-rise         { animation: fade-rise 0.7s cubic-bezier(0.16, 1, 0.3, 1) both; }
.animate-fade-rise-delay   { animation: fade-rise 0.7s cubic-bezier(0.16, 1, 0.3, 1) 0.15s both; }
.animate-fade-rise-delay-2 { animation: fade-rise 0.7s cubic-bezier(0.16, 1, 0.3, 1) 0.3s both; }

@media (prefers-reduced-motion: reduce) {
  .animate-fade-rise,
  .animate-fade-rise-delay,
  .animate-fade-rise-delay-2 { animation: none; opacity: 1; transform: none; }
  * { transition-duration: 0.01ms !important; }
}
```

VIDEO BACKGROUND (z-0)
- `<video autoPlay muted loop playsInline poster="{YOUR_POSTER_URL}" aria-hidden="true">` — `absolute inset-0 w-full h-full object-cover`
- src: `{YOUR_VIDEO_URL}` — supply your own licensed or royalty-free footage (e.g. Pexels/Coverr under their license); do not hotlink third-party media
- Container: h-screen, overflow-hidden

NAVBAR (relative z-10)
- Wrapper `<nav aria-label="Primary">` — max-w-7xl mx-auto px-8 py-6, flex items-center justify-between
- Logo: "SkyElite" — text-2xl font-semibold text-gray-900
- Desktop links (hidden md:flex, gap-8, text-sm): Start · Story · Rates · Benefits · FAQ — text-gray-900, hover:text-gray-700, transition-colors
- Mobile menu button: lucide `Menu`/`X` icon (24px), `aria-label="Toggle menu"`, toggled via `useState`
- Mobile dropdown (on open): absolute inset-x-0 top-full, bg-white/95, backdrop-blur-md, rounded-2xl, shadow-xl, mx-4 mt-2 p-6, flex flex-col gap-4 — same 5 links stacked, text-base

HERO (centered, z-10)
- Content wrapper: relative h-full flex flex-col; main content area flex-1 flex items-center justify-center flex-col text-center px-6, style `marginTop: '-20rem'` (-mt-80 pull up)
- Label (`.animate-fade-rise`): "PRIVATE JETS" — uppercase, text-sm font-semibold text-gray-600 tracking-wider mb-4
- Heading (`.animate-fade-rise-delay`), two overlapping lines:
  - Line 1: "Premium." — text-6xl md:text-7xl lg:text-8xl, font-normal, text-gray-500, leading-none, tracking-tighter
  - Line 2: "Accessible." — same size, color #202A36, `margin-top: -12px` for overlap
- Subtitle (`.animate-fade-rise-delay-2`): "Your dedication deserves recognition." — text-lg md:text-xl text-gray-600 mb-6 max-w-2xl mx-auto
- CTA row (`.animate-fade-rise-delay-2`, flex gap-4, justify-center):
  - "Discover" — px-4 py-2, rounded-full, bg-gray-300 text-gray-800 font-medium, hover:bg-gray-400, transition-colors, active:scale-[0.97]
  - "Book Now" — px-4 py-2, rounded-full, white text, bg-[#202A36], hover:bg-[#1A2229], transition-colors, active:scale-[0.97]

LAYOUT
- Outer container: min-h-screen, bg-gray-50
- Hero section: relative, h-screen, overflow-hidden
- Layer order: video z-0 → nav + hero content z-10

ANIMATIONS
- Entrance: fade-rise 0.7s cubic-bezier(0.16, 1, 0.3, 1), staggered — label 0s · heading 0.15s · subtitle/CTAs 0.3s
- Hover: "Discover" bg-gray-400; "Book Now" bg-[#1A2229]; transition-colors ~200ms
- Press: `active:scale-[0.97]` on both CTA buttons
- Mobile menu: dropdown fade + scale-in ~200ms ease-out
- Animate only transform / opacity / filter

RESPONSIVE: mobile-first; desktop nav links + mobile menu button toggle at `md`; heading scales text-6xl → md:text-7xl → lg:text-8xl; no horizontal scroll.

CONSTRAINTS: clean premium minimalism — bg-gray-50 base, no decorative blobs or radial gradients over the video. Default Tailwind config, no extra UI libraries beyond lucide-react. Only animate transform/opacity/filter (never width/height/top/left/margin). Respect `prefers-reduced-motion`. `aria-label` on nav and the mobile menu toggle; `aria-hidden` on the decorative video; `poster` fallback required.
