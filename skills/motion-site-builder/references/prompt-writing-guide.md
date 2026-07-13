# Prompt Writing Guide — Portable One-Shot Prompts

For `prompt` deliverable mode: produce a single markdown prompt the user pastes into an AI builder (Bolt, Lovable, v0, Cursor). The prompt is a *spec of absolute values* — the same values code mode would ship.

## The 6 Laws

1. **Open with ONE imperative sentence**: what to build + exact stack.
   > "Build a single-page hero section for 'Brand' — a cinematic AI startup landing. Use React, TypeScript, Tailwind CSS, and Lucide React."
2. **Labeled spec sections in fixed order**: `FONTS` → `COLORS` → `GLOBAL CSS` → per-section layout (top to bottom) → `REUSABLE COMPONENTS` (landing only) → `ANIMATIONS` → `DEPENDENCIES` (pin versions, landing only) → `RESPONSIVE` → closing constraints.
3. **Absolute values only** — full Tailwind class strings, hex/HSL, px, seconds, easing curves, real asset URLs, and copy VERBATIM (headline, subtext, CTA labels). Never "a nice serif" or "smooth animation".
4. **Paste primitive CSS verbatim** — `.liquid-glass`, `.text-glow`, keyframes from the component catalog go in as-is, not described.
5. **Close with constraints**: "Default Tailwind config, no other UI libraries. No decorative blobs or radial gradients — the video provides all depth. Respect prefers-reduced-motion."
6. **Engineer's voice** — lists, terse, no rationale. What + which value, never why.

Name effects with precise terms (see `references/animation-vocabulary.md`) — "staggered scale-in", "clip-path reveal", "press feedback" — not "a nice animation". For the right easing + duration per intent, query `motion_easing_rationale`.

## Fill-in Template

```
Build a single-page {hero|landing page} for "{Brand}" — {one-line vibe}.
Use React + Vite + Tailwind CSS + TypeScript + lucide-react. Default Tailwind config, no other UI libraries.

FONTS
- Display: {Instrument Serif} (Google Fonts) — headings, inline fontFamily
- Body: {Inter} (400/500/600)

COLORS (CSS variables)
- --background: {#0C0C0C}   --foreground: #FFFFFF
- --muted-foreground: {rgba(255,255,255,0.6)}   --accent: {single saturated hue}

GLOBAL CSS (paste verbatim)
{.liquid-glass block}
{.text-glow block}
{@keyframes fade-up block + .delay-* classes}
{prefers-reduced-motion block}

VIDEO BACKGROUND
- <video autoplay muted playsinline poster="{poster.jpg}"> absolute inset-0 z-0 object-cover
- src: {your video URL}
- {optional: JS crossfade seamless loop — describe timeupdate/ended handlers with exact ms values}

NAVBAR (z-20)
- liquid-glass rounded-full pill, max-w-5xl mx-auto px-6 py-3, flex justify-between
- Left: "{Brand}" (text-white font-semibold text-lg) + links {…} (hidden md:flex, text-white/80 hover:text-white text-sm)
- Right: CTA pill "{label}" (liquid-glass rounded-full px-6 py-2 text-sm)

HERO (z-10, centered, -translate-y-[10%])
- H1: text-5xl md:text-8xl, tracking-tight, leading-[0.95], text-glow, Instrument Serif.
  Text: "{Headline}" — wrap "{phrase}" in <em class="italic">
- Subtext (text-white/70 max-w-xl mt-6): "{Subtext}"
- CTA (bg-white text-black rounded-full px-8 py-3.5 font-medium transition-transform hover:scale-[1.03] active:scale-[0.97]): "{CTA label}"

ANIMATIONS
- Entrance: fade-up 0.8s cubic-bezier(0.16,1,0.3,1), stagger — H1 0s · subtext 0.25s · CTA 0.4s
- Hover: buttons scale 1.03; Press: active:scale-[0.97] (~160ms ease-out); transition-transform

RESPONSIVE: mobile-first; nav links hidden below md; H1 scales text-5xl → md:text-8xl.

CONSTRAINTS: cinematic minimalism — no decorative blobs, radial gradients, or overlays
(the video provides all depth). Only animate transform/opacity. Respect prefers-reduced-motion.
ARIA labels on nav and icon-only buttons.
```

## Landing-Page Extras

For the Full Landing archetype, add:

- `SECTION ORDER` — numbered list; titles must read as a narrative (Hook → Proof → Detail → CTA).
- `REUSABLE COMPONENTS` — each with full prop/class spec.
- `KEY DEPENDENCIES` — pinned versions (e.g. `framer-motion@^11`).
- Per-section motion spec: which pattern (sticky-stack, marquee, char reveal), with exact numbers.

## Quality Gate

Before delivering, lint every embedded CSS/JSX block with `motion_validate`, and self-check the 6 laws: any adjective without a value attached ("elegant", "modern") is a spec bug — replace it with numbers.
