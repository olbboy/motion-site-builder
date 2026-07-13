# Motion Design DNA — Full Guidelines

Normative design language distilled from a corpus of 83 production prompts. Statistics cited as (n%) are corpus frequencies — they justify each rule empirically.

## 1. Philosophy — Cinematic Minimalism

> A fullscreen AI/licensed video is the canvas. The UI is a thin sheet of glass laid over it: monochrome, quiet, premium — Apple-keynote energy. Color and movement come from the video; the interface stays silent.

Consequences:
- **Video-first** (72% of corpus has a fullscreen `<video>` background). The video IS the visual identity.
- **Anti-clutter is explicit**: "No decorative blobs, radial gradients, or overlays. The video provides all visual depth."
- **Depth via layering, not 3D** (71% declare explicit z-index; 0% use WebGL). "3D" looks are achieved with imagery + parallax.

## 2. Layout & Layering

Canonical stack (declare every layer):

```
z-0   <video> background (absolute inset-0, object-cover)
z-[1] optional darkening overlay (bg-black/30..50) — only if text contrast requires it
z-10  content (hero block, sections)
z-20  navigation (glass pill)
z-30  edge fades (pointer-events-none)
```

- Full-viewport hero: `min-h-screen flex flex-col`.
- Full-bleed inside constrained parents: `w-screen` + `marginLeft: calc(-50vw + 50%)`.
- Preserve generous whitespace; hero content usually centered, `-translate-y-[10..20%]` optical lift.

## 3. Color System

- **Near-black grounds**: `#0C0C0C`, `#0a0a0c`, `#000` (mono-dark family); deep teal/navy for fintech (`#051a24`, `#192837`); green/cream for wellness (`#1f2a1d`, `#f4f1e8`).
- **Text hierarchy by opacity, not hue**: `text-white`, `/80`, `/70`, `/60`, `/40`.
- **ONE saturated accent maximum** — electric violet `#7342e2`, cyan `#00d2ff`, orange `#ef4d23`, yellow `#ffda00` are corpus examples. The accent marks ONE thing (CTA or key phrase).
- Colors declared as CSS variables (`--background`, `--foreground`, `--accent`) or absolute hex — never vague ("a nice blue").

## 4. Glassmorphism (61% of corpus)

The `.liquid-glass` primitive (31% of files copy it verbatim — see component catalog):
near-zero white fill + `backdrop-blur(4px)` + inset top highlight + gradient border via `mask-composite: exclude`. Used for: nav pill, CTA buttons, input pills, icon buttons, tag pills.

Rules:
- Blur budget: 4–12px. More blur = cheaper look + GPU cost.
- Glass elements are `rounded-full` (pills) or `rounded-2xl`+ (panels). 70% of corpus uses `rounded-full` for interactive elements.

## 5. Typography

- **Signature pair**: display serif + neutral grotesk body. Corpus: Instrument Serif (40%) + Inter (81%). Alternatives: Playfair/Kanit/Anton display; Geist/DM Sans body.
- **Display**: huge (`clamp()`/vw or `text-5xl md:text-8xl`), `leading-[0.9..1.15]`, negative tracking (65% use `tracking-tight`/`tracking-[-Npx]`), often inline `fontFamily`. Optional `.text-glow`.
- **Emphasis technique**: wrap one phrase in `<em className="italic">` (serif italic swap) or `<em className="not-italic text-muted-foreground">` (color swap).
- **Body**: relaxed leading, white opacity tiers, `max-w-xl` measure.
- Optical tweaks allowed: `-webkit-text-stroke` for weight correction.

## 6. Motion Language

### Entrances
- Pattern: fade + rise (`translateY(16–32px)` → 0), optionally blur(6px) → 0.
- Duration 0.5–1.2s (sweet spot 0.6–0.9s).
- **Stagger 0.08–0.2s** between siblings, in narrative order: badge → headline → subtext → CTA → footer.
- Signature easings: expo-out `cubic-bezier(0.16,1,0.3,1)`, quint-out `cubic-bezier(0.22,1,0.36,1)` (22% of corpus); spring `cubic-bezier(0.34,1.56,0.64,1)` for pops/hover only.

### Scroll — two schools, pick ONE per page
1. **Framer Motion** (31%): `useScroll` + `useTransform` for parallax; `whileInView` with `once: true` for reveals.
2. **Hand-rolled rAF + lerp** (24%): `current += (target − current) * 0.08..0.12`, applied via `translate3d`, `will-change: transform`. Buttery for parallax/marquee.

### Recurring patterns
- Sticky-stack cards: `targetScale = 1 − (total − 1 − index) * 0.03`.
- Char-by-char reveal: chars at opacity 0.2 → 1 mapped to scroll progress.
- Scroll-bound marquee, magnetic cursor, hover `scale-[1.03]`.
- Seamless video loop: JS crossfade (rAF; start fading ~0.55s before clip end, 500ms fade, guard flag against re-trigger). Never CSS transitions on `<video>`.
- App gating: wait for `loadeddata` + `document.fonts.ready` + 5s safety timeout before enabling entrance class.

### Performance rules (hard)
- Animate ONLY `transform`, `opacity`, `filter`.
- Never `transition: all`; list properties.
- `will-change` only on actively animated elements.

## 7. Accessibility — exceed the source

The corpus is weak here (8/83 reduced-motion, 4/83 ARIA). This skill treats both as mandatory:

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

- In React, gate parallax/rAF loops behind `useReducedMotion()` (Framer) or a `matchMedia` check.
- `aria-label` on icon-only buttons and nav; `<nav>` landmark; focus-visible styles on CTAs.
- Videos are decorative: `aria-hidden="true"`, always `muted`.

## 8. Stack Contract

| Tech | Rule |
|:---|:---|
| React 18 + Vite + TS | Default scaffold (90% of corpus is React) |
| Tailwind CSS | **Default config, no extensions** — custom utilities as plain CSS in `index.css` (84%) |
| lucide-react | The only icon set (72%) |
| Framer Motion | Only when scroll-linked transforms/inview needed (~30%) |
| shadcn/ui tokens | Optional, only `--background/--foreground` style vars |
| Three.js/WebGL | Never (0%) |
| App Showcase archetype | Plain HTML/CSS/JS, no framework |

## 9. Copy Voice

- Headlines: short, declarative, sensory ("Know it then *all*.").
- Provide copy VERBATIM in specs — headline, subtext, CTA label. Never "add a nice headline".
- CTA labels: 2–4 words, action verbs ("Get Started for Free", "Join the Waitlist").

## 10. Customizing this DNA

Every numeric/enumerable rule above is mirrored in `config/motion-tokens.json`. To adapt the skill to another design language (e.g. light-mode editorial, brutalist), change the JSON first, then update this file's prose to match. The lint engine follows the JSON, not this document.
