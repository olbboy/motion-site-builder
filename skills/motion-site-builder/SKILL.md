---
name: motion-site-builder
description: >
  Build polished, motion-driven web UI across FIVE design profiles — cinematic
  (video-first, glassmorphism, serif; the default), product-ui (SaaS/dashboard),
  editorial (blog/docs), playful (bold/maximalist), and ecommerce (product grid).
  Pick a profile, then plan → build → lint. Produces working code (React + Vite +
  Tailwind) or a portable one-shot prompt for AI builders (Bolt/Lovable/v0). Uses
  MCP tools for profile selection, pattern & easing suggestion, reference retrieval,
  and motion linting. Fully customizable via config profiles — no brand lock-in.
  Trigger on: "build hero", "hero section", "landing page", "motion UI",
  "cinematic site", "glassmorphism", "video background", "dashboard UI",
  "SaaS app", "blog/docs site", "editorial layout", "e-commerce store",
  "product grid", "playful site", "tạo hero", "tạo landing", "làm website động",
  "làm dashboard", "motion prompt", "lint motion", "validate motion",
  "suggest motion pattern".
---

# Motion Site Builder

Build publication-quality motion websites on a customizable design DNA distilled from a corpus of production prompts.

## Two Deliverable Modes

Decide with the user FIRST (default: **code**):

| Mode | Output | When |
|:---|:---|:---|
| `code` | Working React + Vite + TypeScript + Tailwind project (or plain HTML/CSS/JS for app showcases) | User wants a runnable site |
| `prompt` | One-shot portable prompt (markdown) for AI builders | User wants to paste into Bolt/Lovable/v0/Cursor |

Both modes share the same tokens, catalog, and lint rules — a prompt is a spec of the same absolute values the code would contain. For `prompt` mode, follow `references/prompt-writing-guide.md`.

## Step 0 — Pick the design profile (before anything else)

Motion Site Builder ships **five design languages**. The profile decides the tempo, palette, typography, and which constraints apply — everything downstream reads it. Call `motion_list_profiles`, choose with the user (infer from the brief when obvious), then pass that profile name to every tool (`motion_get_tokens`, `motion_validate`, `motion_suggest_pattern`, `motion_easing_rationale`).

| Profile | Use for | Signature |
|:---|:---|:---|
| **cinematic** *(default)* | hero, landing, launch, app showcase | video-first, glass, serif, 1 accent, entrances 0.5–1.2s |
| **product-ui** | dashboard, SaaS, admin, settings | crisp, fast (<250ms), light+dark, semantic multi-accent |
| **editorial** | blog, docs, articles, changelog | typography-first, prose, restrained motion, light |
| **playful** | consumer, creative, events, campaigns | vibrant multi-accent, bouncy springs, decorative color |
| **ecommerce** | storefront, product page, catalog | imagery-first, snappy, quick-view, brand+neutral |

The default (no profile) is cinematic — the sections below describe it in full. For other profiles, the workflow is the same but you follow that profile's tokens; see `references/design-profiles.md` for each one's DNA and what relaxes. **Note:** the corpus is majority-cinematic, but each non-cinematic profile ships two exemplar prompts — retrieve them by including the profile name in the `motion_find_reference` query (e.g. `"editorial article"`), and pull that profile's primitives from the component catalog via `motion_get_template`. Never adapt a cinematic prompt into another profile; build from the exemplar + profile tokens + `interaction-standards.md`.

## Core Workflow — 15 Steps

### Phase A: Plan (Steps 1–6) — No code yet

1. **Understand the brief** — Brand name, industry, one-line vibe, target audience.
2. **Pick archetype** — Use the archetype matrix below.
3. **Pick palette** — `motion_get_tokens(profile)` → `palette.families` / `palette.strategy`. Respect the profile's `max_accent_hues` (cinematic/editorial/ecommerce = 1–2; product-ui/playful allow multi-accent).
4. **Storyboard the scroll narrative** — Section order must tell a story: Hook → Proof → Detail → CTA. Read section titles in sequence; if they don't narrate, reorder.
5. **Choose motion patterns per section** — Call `motion_suggest_pattern` or use the pattern matrix below. First apply the **frequency filter**: classify each animated element and match the budget. This decides *whether* to animate before *how*.

   | Frequency | Example | Budget |
   |:---|:---|:---|
   | 100+/day | keyboard shortcut, command-palette toggle | **No animation** |
   | Tens/day | nav link, list item hover | Reduce; press/hover feedback only |
   | Occasional | dropdown, toast, modal, CTA | Interaction values (< 300ms, ease-out, press feedback) |
   | Rare/first-time | **hero entrance**, onboarding, success | Cinematic budget (0.5–1.2s, expo-out) — macro DNA |

   Interaction elements (buttons/popovers/hover) follow `references/interaction-standards.md`; hero entrances keep the cinematic DNA. Don't cross the two.
6. **Check assets** — Background video URL (user-supplied or licensed), poster image fallback. Never ship without a poster.

### Phase B: Build (Steps 7–12)

7. **Find a reference** — Call `motion_find_reference` with vibe + archetype; adapt the closest corpus prompt instead of generating from scratch.
8. **Scaffold** — Vite + React 18 + TS + Tailwind (default config, no extensions) + lucide-react. Framer Motion only if scroll-linked transforms are needed. App showcases: plain HTML/CSS/JS.
9. **Paste primitives verbatim** — `motion_get_template` for liquid-glass, text-glow, keyframes, etc. Do not paraphrase CSS.
10. **Layer explicitly** — video `z-0` → overlay `z-[1]` → content `z-10` → nav `z-20`. No decorative blobs or radial gradients when a video provides depth.
11. **Typography** — Display serif (huge, `leading-[0.9..1.15]`, negative tracking, optional `text-glow`), body grotesk in white opacity tiers. Emphasize one phrase via `<em>` color/italic swap.
12. **Motion** — Entrance: fade + rise 16–32px, 0.5–1.2s, staggered 0.08–0.2s, token easing (expo-out). Scroll: pick ONE school per page — Framer `useScroll`/`whileInView` OR hand-rolled rAF + lerp. Animate only `transform`/`opacity`/`filter`.

### Phase C: Validate (Steps 13–15)

13. **Lint each component** — Call `motion_validate` on every file's code; fix ERRORs (mandatory), WARNINGs (recommended), INFOs (nice-to-have). Rules M01–M12 cover macro composition; **M13–M17 cover interaction craft** (ease-in, `scale(0)`, popover origin, press feedback, hover gating). If M16 flags a CTA, add `active:scale-[0.97]` rather than suppressing it.
14. **Runtime smoke (code mode)** — Run dev server in the browser pane: console clean, video plays muted+looped, entrance stagger visible, emulate `prefers-reduced-motion` and verify animations collapse.
15. **Register / emit** — Code mode: final `motion_validate_file` pass on the entry page. Prompt mode: assemble the portable prompt per the guide, then lint any embedded CSS/JSX blocks.

## Archetype Matrix

| Archetype | Signals in brief | Shape | Spec size |
|:---|:---|:---|:---|
| **Minimal Hero** | "hero", single message, waitlist | 1 full-viewport section: video bg + glass nav pill + display headline + subtext + 1 CTA | 3–8 KB |
| **Full Landing** | multiple sections, features, pricing | `SECTION ORDER` + `REUSABLE COMPONENTS` + pinned `DEPENDENCIES`; marquee / sticky-stack / scroll-reveal | 8–19 KB |
| **Design Replica** | "match brand X", styleguide | Design tokens first: CSS vars, type scale, button variants with 3D `translateY` states, dark variant | 6–12 KB |
| **App Showcase** | mobile app, iPhone frames | Plain HTML/CSS/JS, 2 device frames (370×790, Dynamic Island) on auto-scaling stage, pixel-positioned | 10–19 KB |

## Motion Pattern Matrix

| Intent | Pattern | Avoid |
|:---|:---|:---|
| First impression | Staggered fade-rise entrance (headline → subtext → CTA) | Everything animating at once |
| Ambient depth | Fullscreen looping video + explicit z-layers | WebGL/Three.js, parallax blobs |
| Seamless bg loop | JS crossfade near clip end (rAF, ~500ms fade) | CSS transition on `<video>`, visible restart jump |
| Scroll storytelling | Framer `useScroll`+`useTransform`, or `whileInView` once | Scroll-jacking, >1 scroll library |
| Buttery parallax | Hand-rolled rAF + lerp (`current += (target−current)*k`) on `translate3d` | Animating `top/left`, layout thrash |
| Section stacking | Sticky-stack cards (`scale = 1 − (n−1−i)*0.03`) | Carousel plugins |
| Text drama | Char-by-char opacity reveal tied to scroll | Typewriter with cursor blink |
| Continuous strip | Marquee bound to `scrollY` or CSS loop | Auto-carousels with dots |
| Hover feedback | `scale(1.03)` + glow, spring easing for pops | Color-only hover, >1.1 scale |
| Press feedback | `active:scale-[0.97]` / `whileTap`, ~160ms ease-out | No `:active` state; `scale(0)` |
| Popover / menu open | Scale from trigger (`transform-origin` var), 150–250ms ease-out | `transform-origin: center`; `ease-in` |
| Toast / dynamic UI | CSS transition + `@starting-style` (interruptible) | `@keyframes` that restart from zero |

## FORBIDDEN

### Universal — never generate, any profile

- ❌ Animating layout properties (`width/height/top/left/margin`) — transform/opacity/filter only (M02)
- ❌ `transition: all` (M10)
- ❌ Shipping without `prefers-reduced-motion` handling (M01)
- ❌ `ease-in` on interactive UI (starts slow) — use the profile's ease-out (M13)
- ❌ Entrances from `scale(0)` — start from `scale(0.95)` + opacity (M14)
- ❌ `transform-origin: center` on popovers/dropdowns/tooltips — scale from the trigger; modals exempt (M15)
- ❌ Pressable elements (buttons, CTA links) with no press feedback (`active:scale-[0.97]`/`whileTap`) (M16)
- ❌ Applying interaction-tempo rules to a reveal/entrance — the entrance budget is deliberate, not a violation

### Cinematic profile only (other profiles relax these — see `design-profiles.md`)

- ❌ Decorative blobs, radial-gradient washes, grain overlays over a video background — video provides all depth *(playful profile inverts this — decorative color is its identity; M08 off there)*
- ❌ More than ONE saturated accent hue *(product-ui/playful allow multi-accent via `max_accent_hues`)*
- ❌ Three.js / WebGL — "3D" via imagery + parallax
- ❌ Extra UI libraries — default Tailwind only *(product-ui adds Radix/recharts; ecommerce adds embla; per profile `dependencies.allowed`)*
- ❌ Custom Tailwind config extensions — customize via plain CSS utilities in `index.css`

## Polish Checklist (every page)

- [ ] `<video>` has `autoplay muted loop playsInline` + `poster`
- [ ] Explicit z-index on every layer
- [ ] Entrance stagger 0.08–0.2s between siblings
- [ ] Easing from token set (see `motion_get_tokens` → `easings`)
- [ ] Display type: negative tracking, tight leading
- [ ] Text hierarchy via white opacity tiers, not extra colors
- [ ] `prefers-reduced-motion` collapses entrances + disables parallax
- [ ] ARIA labels on nav and icon-only buttons
- [ ] Mobile-first responsive (`sm/md/lg`), no horizontal scroll
- [ ] Press feedback (`active:scale-[0.97]`) on every button / CTA link
- [ ] Popovers/dropdowns/tooltips scale from their trigger; no `ease-in` on UI
- [ ] Raw-CSS `:hover` motion gated behind `@media (hover: hover) and (pointer: fine)`

## MCP Tools — When to Call

| Situation | Tool |
|:---|:---|
| Step 0 — choose the design profile | `motion_list_profiles` (then pass `profile` to the tools below) |
| Starting Phase B (cinematic) | `motion_find_reference` — nearest corpus prompts by vibe/archetype |
| Choosing a motion approach | `motion_suggest_pattern` |
| Which easing + how fast + why (per intent) | `motion_easing_rationale` |
| Need verbatim primitive/snippet | `motion_get_template` |
| Need tokens (easing, palette, deps) | `motion_get_tokens` |
| After writing each file | `motion_validate` (code string) |
| Final pass on a file | `motion_validate_file` |

If the MCP server isn't connected, read `config/motion-tokens.json` and run `scripts/lint_motion.py <file>` directly, and search `data/prompt-index.json` manually.

## Customization (open-source contract)

All taste lives in **`config/motion-tokens.json`** — easings, duration ranges, stagger, palette families, dependency whitelist, lint severities. The engine (`scripts/`) never hardcodes taste. To re-skin for another design language: edit the JSON, optionally swap `references/` content, re-run `scripts/build_index.py` if the prompt corpus changed. See `README.md` for extension recipes (add prompt, add lint rule, override tokens).

## References

- `references/design-profiles.md` — the five design profiles (cinematic/product-ui/editorial/playful/ecommerce): DNA, when-to-use, how to select & customize
- `references/motion-design-dna.md` — full design-language guidelines (cinematic profile, macro composition)
- `references/interaction-standards.md` — micro-interaction craft: press/popover/toast/hover, easing rationale, frequency filter (rules M13–M17)
- `references/component-catalog.md` — verbatim primitives and snippets
- `references/animation-vocabulary.md` — precise motion terms (name an effect; write specs that don't guess)
- `references/prompt-writing-guide.md` — portable prompt formula (prompt mode)
- `data/prompt-index.json` — tagged corpus index (generated)
