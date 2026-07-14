# Motion Site Builder — Official Landing

Build a single-page marketing landing page for "Motion Site Builder" — an open-source suite that builds new motion UI, strictly reviews changes, and turns existing-app audits into executable improvement plans across **five design languages** (cinematic, product-ui, editorial, playful, ecommerce), backed by 54 curated prompts, a 17-rule motion linter, 8 MCP tools, and 3 agent skills. The page itself is **cinematic** profile; its hero embeds a live five-language stage as the product surface. Use React + Vite + Tailwind CSS + TypeScript + framer-motion + lucide-react. Default Tailwind config, no other UI libraries.

FONTS
- Display: Instrument Serif (Google Fonts, regular + italic) — all headings, via a `.font-display` utility
- Body: Inter (400/500/600) — everything else
- Eyebrows/terminal: `ui-monospace, 'SF Mono', monospace`

COLORS (CSS variables on :root)
- --background: #0C0C0C   --foreground: #FFFFFF
- --muted-foreground: rgba(255,255,255,0.6)
- --accent: #7342e2 (electric violet — the ONLY saturated hue on the cinematic shell; the stage vignettes use Tailwind palette utilities as demo colors)
- Text tiers: white at 100 / 70 / 60 / 50% — never below 50% for content

GLOBAL CSS (paste verbatim into index.css)

```css
.text-accent { color: var(--accent); }
.bg-accent { background: var(--accent); }
.font-display { font-family: 'Instrument Serif', serif; }

.eyebrow {
  font-family: ui-monospace, 'SF Mono', monospace;
  font-size: 11px; font-weight: 500; letter-spacing: 0.18em;
  text-transform: uppercase; color: var(--accent);
}

/* large surfaces get a real hairline; liquid-glass stays for small pills */
.panel { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); }

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
  position: absolute; inset: 0; border-radius: inherit; padding: 1.4px;
  background: linear-gradient(180deg,
    rgba(255,255,255,0.45) 0%, rgba(255,255,255,0.15) 20%,
    rgba(255,255,255,0) 40%, rgba(255,255,255,0) 60%,
    rgba(255,255,255,0.15) 80%, rgba(255,255,255,0.45) 100%);
  -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  -webkit-mask-composite: xor;
  mask-composite: exclude;
  pointer-events: none;
}

/* crisp edge + violet halo — never a fog of white blur */
.text-glow {
  text-shadow: 0 0 1px rgba(255,255,255,0.4),
               0 0 28px rgba(255,255,255,0.12),
               0 0 64px rgba(115,66,226,0.25);
}

@keyframes fade-up {
  from { opacity: 0; transform: translateY(24px); filter: blur(6px); }
  to   { opacity: 1; transform: translateY(0);   filter: blur(0); }
}
.animate-fade-up { animation: fade-up 0.8s cubic-bezier(0.16, 1, 0.3, 1) backwards; }
.delay-1 { animation-delay: 0.1s; } .delay-2 { animation-delay: 0.25s; } .delay-3 { animation-delay: 0.4s; }

/* scroll reveal — an interruptible transition, not a keyframe */
.reveal {
  opacity: 0; transform: translateY(24px); filter: blur(6px);
  transition: opacity 0.8s cubic-bezier(0.16,1,0.3,1),
              transform 0.8s cubic-bezier(0.16,1,0.3,1),
              filter 0.8s cubic-bezier(0.16,1,0.3,1);
}
.reveal.is-in { opacity: 1; transform: none; filter: none; }

@keyframes marquee { from { transform: translateX(0); } to { transform: translateX(-50%); } }
.animate-marquee { animation: marquee 40s linear infinite; }
.animate-marquee-reverse { animation: marquee 56s linear infinite reverse; }
.marquee-mask {
  mask-image: linear-gradient(90deg, transparent, #000 8%, #000 92%, transparent);
  -webkit-mask-image: linear-gradient(90deg, transparent, #000 8%, #000 92%, transparent);
}

@media (prefers-reduced-motion: reduce) {
  .animate-marquee, .animate-marquee-reverse { animation: none; }
  *, *::before, *::after {
    animation-duration: 0.01ms !important; animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important; transition-delay: 0ms !important;
    scroll-behavior: auto !important;
  }
}
```

BACKDROP — AURORA CURTAINS (fixed inset-0 z-0 `<canvas>`, `aria-hidden`, plus an `absolute inset-0 z-[1] bg-black/40` contrast overlay)
- Owned procedural media standing in for {YOUR_VIDEO_URL}: three horizontal aurora curtains drawn as thin filament polylines (anisotropic, directed light — never blurry orbs)
- Bands `{yc, amp, spread, lines, speed, rgb, alpha}`: (0.26, 0.09, 0.16, 44, 0.55, `139,92,246`, 0.10) · (0.52, 0.13, 0.22, 56, 0.38, `115,66,226`, 0.085) · (0.78, 0.07, 0.13, 36, 0.72, `88,46,178`, 0.10)
- Per filament i: `y = (yc + sin(x·0.0016 + t·speed·7 + i·0.17)·amp·0.55 + sin(x·0.0007 − t·speed·5 + i·0.045)·amp)·h + offset`, offset = `(i/(lines−1) − 0.5)·spread·h`; stroke alpha × `1 − |rel|·1.6` (core brighter than fringes); one white core line per band at alpha 0.09; composite `lighter`
- Before the curtains: an ambient violet bloom — radial gradient at (50%, 40%), `rgba(115,66,226,0.16) → 0.05 @55% → 0`; after: an edge vignette radial (50%,38%)→(50%,50%), transparent → `rgba(12,12,12,0.55)`
- Perf: ~30fps frame gate (33ms), DPR capped at 1.5, pause when `document.hidden`; `prefers-reduced-motion` draws ONE static frame and never starts the loop

REVEAL SYSTEM (one `Reveal` wrapper component)
- IntersectionObserver adds `.is-in` once (`rootMargin: '0px 0px -8% 0px'`); CRITICAL: on mount, if `el.getBoundingClientRect().top < innerHeight·0.92` set `.is-in` immediately — a deep link or fast scroll must never strand a section invisible
- Optional `delay` prop → `transition-delay` in ms; keep steps ≤ 160ms

NAVBAR (sticky top-0 z-30, px-6 pt-5)
- Pill `h-[52px] max-w-5xl mx-auto rounded-full border border-white/10 bg-white/[0.04] px-5 shadow-[0_8px_32px_rgba(0,0,0,0.4)] backdrop-blur-xl`
- Left: lucide `Clapperboard` in accent + "Motion Site Builder" text-[15px] font-semibold; links (hidden md:flex, gap-7): Profiles / How it works / Skills / Tools — `text-[13px] font-medium text-white/60 hover:text-white/90` (color only, 150ms)
- Right: "Star on GitHub" — `bg-accent rounded-full px-4 py-1.5 text-[13px] text-white shadow-[0_0_0_1px_rgba(115,66,226,0.4),0_8px_24px_rgba(115,66,226,0.3)]`, hover scale 1.03, `active:scale-[0.97]`

HERO + STAGE (z-10, flex-col items-center, pt-14 md:pt-20 pb-24, text-center — the stage IS the product surface, peeking above the fold)
- Badge (`.animate-fade-up`): liquid-glass pill — accent 6px dot + eyebrow-styled "Open source · MIT · 5 design languages" in white/60
- H1 (delay-1): "Motion UI that looks / *designed*, not generated." — font-display text-glow, text-5xl md:text-8xl, leading-[0.95], tracking-tight; "designed" = `<em class="italic text-accent">`
- Sub (delay-2, max-w-lg, white/70, `[text-wrap:balance]`): "Build new motion UI, review a change, or turn an existing app into executable improvement plans — all grounded by one 17-rule linter."
- CTAs (delay-3): primary "Explore the profiles" (bg-white text-black rounded-full px-8 py-3.5, hover scale 1.03, active 0.97) + quiet text link "View on GitHub →" (white/60 → white/90, color only) — ONE solid button in the hero
- STAGE (in a `Reveal delay={160}`, mt-16 md:mt-20, `id="profiles"` scroll-mt-28):
  - Eyebrow centered: "01 · The range — one engine, five design languages"
  - Tab row (`role="tablist"`, arrow-key navigation): cinematic / product-ui / editorial / playful / ecommerce — mono text-sm rounded-full px-5 py-2; active = liquid-glass + white, inactive white/55; active tab carries a 1px progress underline `scaleX 0→1` over 4s linear (only while autoplaying)
  - Stage panel: `.panel rounded-2xl h-[360px] md:h-[420px] overflow-hidden` (`role="tabpanel"`); all five vignettes stay mounted, absolutely stacked; active one animates `opacity 0→1 + scale 0.985→1`, 0.7s cubic-bezier(0.16,1,0.3,1); inactive: `aria-hidden`, `pointer-events: none`
  - Auto-advance every 4s; pause on pointerenter/focus-within; NO autoplay under reduced motion
  - Vignettes — each in its OWN language (all motion transform/opacity):
    1. cinematic: zinc-950, violet bloom blur-3xl, "A24 FILMS · PRESENTS" chip, serif "Ship *cinematic*" text-4xl md:text-6xl rising 14px with blur-to-sharp 0.9s expo-out, film scrubber (1px line + 7px playhead translating 224px over 3.6s linear), "00:07 / 00:24"
    2. product-ui: slate-50 dashboard — breadcrumb + toggle (thumb translateX 12px, 0.18s), 3 stat tiles ($48.2k +12% · 9,412 +312 · 2.1% −0.4pt, tabular-nums) rising 6px stagger 40ms, 8-bar chart `scaleY` origin-bottom stagger 30ms, all 0.2s quint-out
    3. editorial: stone-50 paper — kicker "Field notes · Issue 14" in amber-700, serif "The quiet craft of reading", amber rule `scaleX 0.25→1` 0.6s, drop-cap "W" + 6 prose skeleton lines stagger 70ms, sticky-TOC rail with active item
    4. playful: fuchsia-500 — amber "NEW!" sticker (spring 400/11, rotate −6°→4°, scale 1.08), "Make it **loud**" font-black text-4xl md:text-6xl (spring 300/13), 4 bouncing dots (spring 500/12, stagger 50ms), hard-shadow pill "Let's go →"
    5. ecommerce: white storefront — "ARCADIA" + cart badge (spring pop from scale 0.5 + fade, never from 0), 3 product cards rising stagger 50ms, first card lifts −4px and reveals "Add to cart" sliding up 26px, prices tabular-nums
  - Caption row under stage: `{key} — {signature}` + tempo chip (e.g. "cinematic — Video-first · glass · serif · one accent" / "0.5–1.2s · expo-out")

STATS STRIP (border-t border-white/5, py-16; grid 2→4 cols, md:divide-x divide-white/10)
- 5 design profiles · 17 motion lint rules · 54 curated prompts · 8 MCP tools
- Numbers: font-display text-6xl md:text-7xl tracking-tight, COUNT UP 0→target over 900ms quart-out once the strip enters view (`minWidth` in `ch` so nothing shifts; reduced-motion jumps straight to the value); labels text-xs uppercase tracking-[0.18em] white/50

HOW IT WORKS (`id="how"`, max-w-6xl, py-28 — LEFT-aligned editorial rail, not cards)
- Eyebrow "02 · The method" → serif H2 "Pick a profile. Plan. Build. Validate." (text-4xl md:text-5xl) → lede white/60 "Taste becomes a system — a deterministic pipeline, not a lucky prompt."
- 4 rows (max-w-3xl), each `grid-cols-[84px_1fr] md:grid-cols-[128px_1fr]`, border-t white/10 (last also border-b), py-9: ghost serif numeral 01–04 (text-6xl md:text-8xl, white/25, `group-hover:text-accent` 300ms color) + title (text-xl md:text-2xl font-medium) + body white/60
- Copy: Profile (pick 1 of 5 languages; linter and tools then enforce that taste) · Plan (archetype, palette, scroll story Hook → Proof → Detail → CTA) · Build (adapt the nearest of 54 reference prompts, measured profile-aware primitives) · Validate (17-rule linter; reduced-motion, GPU-only, ARIA are errors)
- Rows reveal with delay index·80ms

SKILLS SUITE (`id="skills"`, py-28, LEFT-aligned)
- Eyebrow "03 · The suite" → H2 "One engine. *Three* skills." → lede "Build, review, and improve — sharing one linter, one token set, one standard."
- ONE `.panel rounded-2xl` split `md:grid-cols-3 md:divide-x divide-white/10` (mobile: border-t between cells): each cell = `<a>` p-8, lucide icon (Hammer/ScanLine/Sparkles) in accent + tag chip (build/review/improve, mono uppercase), mono name (motion-site-builder / review-motion / improve-motion), body white/60, and an invoke line `› "Build a cinematic hero for my AI startup"` (mono text-xs white/50, accent ›). The improve cell must say that audit is read-only by default and selected plans can be explicitly executed and reconciled.
- Cell hover: background-color to white/[0.04] only; press `active:scale-[0.99]`

MCP TOOLS (`id="tools"`, max-w-5xl, py-28, centered)
- Eyebrow with Terminal icon: "04 · Zero-dependency MCP server" → H2 "*8* tools your agent can call" → lede "Taste, exposed as an API — every taste-bearing tool takes a `profile` argument."
- TERMINAL WINDOW: `.panel rounded-2xl font-mono text-sm` — chrome bar (three 12px white/15 dots + "motion-site-tools — stdio"), body `$ python3 skills/motion-site-builder/scripts/server.py · connected` (· connected in accent), then 8 tools in `sm:grid-cols-2` each on its own `Reveal delay={i·60}`: `▸ motion_list_profiles / motion_get_tokens / motion_suggest_pattern / motion_easing_rationale / motion_get_template / motion_find_reference / motion_validate / motion_validate_file` + one-line desc in white/45
- Footer line: `every taste-bearing tool takes profile=<cinematic·product-ui·editorial·playful·ecommerce>`

PROMPT MARQUEE (`aria-hidden`, border-y white/5, py-10, `.marquee-mask`, two counter-scrolling rows gap 20px)
- Names set in the display serif italic text-2xl md:text-3xl white/30, separated by `✦` in accent/60 with mx-6 — borderless type, no chips
- Row A (40s): 12 cinematic prompt names (Aethera Studio, Neuralyn, Stillmind, …); Row B (56s, reverse): 12 profile-exemplar names (PulseGrid Analytics, Meridian Longread, FizzPop Soda, Arcadia Goods, Maison Ondes, PixelJam Fest, …); each row duplicated 2× so `translateX(-50%)` wraps seamlessly

FINAL CTA + FOOTER (pt-32, centered, in one `Reveal`)
- Mono lint line: `$ motion_validate site/ → score 100 · grade A+` (white/40, result in accent)
- Serif H2 text-4xl md:text-6xl: "Five design languages. / *One* paste away."
- CTA — the page's accent climax: "Star on GitHub" `bg-accent rounded-full px-10 py-4 text-lg text-white shadow-[0_0_0_1px_rgba(115,66,226,0.4),0_16px_48px_rgba(115,66,226,0.35)]`, hover scale 1.03, active 0.97, Github icon
- Fine print white/50: "MIT licensed · Built with its own skill · 17-rule linter · cubic-bezier(0.16, 1, 0.3, 1)"
- Footer: border-t white/[0.06], pt-10 pb-12, flex justify-between text-[13px] — "© Motion Site Builder — dogfooded by its own linter" + links GitHub / Prompt library / Design profiles / MIT license (white/60 → white/90)

ANIMATIONS (complete inventory)
- Load: hero 4-beat fade-up stagger (0 / 0.1 / 0.25 / 0.4s) + stage reveal at 160ms — 0.8s cubic-bezier(0.16,1,0.3,1), rise 24px, blur 6px→0
- Scroll: `.reveal` once per block via the IO system above; stagger steps 60–160ms
- Stage: crossfade 0.7s expo-out; per-vignette motion at ITS profile's tempo (see vignettes)
- Idle: marquee 40s/56s linear loops (stopped under reduced motion); count-up 900ms once
- Hover: nav/links color-only 150ms; buttons scale 1.03; numerals color 300ms; skill cells background-color
- Press: `active:scale-[0.97]` on every solid button, `[0.98]`–`[0.99]` on quiet links/cells

KEY DEPENDENCIES
`react@^18` `react-dom@^18` `typescript@^5` `vite@^5` `tailwindcss@^3` `framer-motion@^11` `lucide-react@latest`

RESPONSIVE
- Mobile: H1 text-5xl; tab row wraps `grid-cols-2 sm:grid-cols-3`; stage h-[360px]; stats 2-col; method rail 84px numeral column; skills/tools stack; marquee text-2xl; no horizontal scroll anywhere
- The sticky pill nav persists at every width; hero stage peeks above the fold on ≥900px viewports

CONSTRAINTS: cinematic minimalism with ONE violet accent on the shell — the stage vignettes are quoted foreign languages (Tailwind palette utilities, no raw hex), everything else is white tiers + accent. Only animate transform/opacity/filter (paint-only exceptions: color/background-color on hovers ≤300ms, box-shadow on the two accent CTAs). Easing only from {cubic-bezier(0.16,1,0.3,1) · cubic-bezier(0.22,1,0.36,1) · springs in vignettes · linear for scrubber/marquee/progress}; never ease-in; no `transition: all`; no entrance below scale 0.5. The backdrop canvas is the only decorative layer — no DOM gradient washes or blobs over it. Respect `prefers-reduced-motion` everywhere (static canvas frame, no autoplay, no loops, instant reveals). ARIA: tablist/tab/tabpanel with arrow keys on the stage, `aria-hidden` on decor/marquee/inactive vignettes, labels on icon-only links, `role="status"` where async feedback appears. A deep link to any `#section` must land on fully visible content.
