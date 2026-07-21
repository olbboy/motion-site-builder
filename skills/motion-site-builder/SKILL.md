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

**Step 0a — derive a custom profile (when references replace a profile pick).** If the user brings reference screenshots/URLs ("make it feel like this") rather than a brief that maps to a shipped profile, don't force the nearest preset: follow `references/profile-schema.md` — analyze the references against the profile schema (color by area dominance, accent by CTA usage, radius vs element height, motion tempo class, elevation, imagery treatment, voice), write `config/profiles/<derived-name>.json`, verify with `lint_motion.py --self-test`, then run the normal workflow under that profile. If the reference is ~90% one shipped profile, use the preset and adjust tokens instead.

The default (no profile) is cinematic — the sections below describe it in full. For other profiles, the workflow is the same but you follow that profile's tokens; see `references/design-profiles.md` for each one's DNA and what relaxes. **Note:** the corpus is majority-cinematic, but each non-cinematic profile ships two exemplar prompts — retrieve them by including the profile name in the `motion_find_reference` query (e.g. `"editorial article"`), and pull that profile's primitives from the component catalog via `motion_get_template`. Never adapt a cinematic prompt into another profile; build from the exemplar + profile tokens + `interaction-standards.md`.

## Step 0.5 — Pre-flight scan & project memory (existing projects)

If the target project already has code (`package.json`, a Tailwind config, any CSS), **read it before asking the user anything**: fonts (deps / Google Fonts links), existing tokens (`--ease-*`, `--duration-*`, `:root` palettes), motion stance (`framer-motion`/`motion`/`gsap`/`lenis` in deps = motion-on; none = motion-cut), framework. Emit one short block with `file:line` citations before building — *"Pre-flight: … · Preserving: fonts, tokens · Introducing: entrance discipline, press feedback."* Extend the project's own tokens; never invent a parallel set. Greenfield → one line: *"No pre-flight signals — full motion-site stack."*

**Project memory & diversification.** Read `.motion-site/log.json` at the project root (and any `/* motion-site · … */` stamp atop existing entry CSS) before picking an archetype. If prior builds exist, this build's **archetype and pattern set must differ from the last entry** — two consecutive builds must not share the same hero pattern + section rhythm. State the rotation in plain text: *"Last build: Minimal Hero + staggered fade-rise. This build: Full Landing + sticky-stack, because …"*. Picking on the page, not in your head, is what stops repeat briefs from converging on one template.

## Core Workflow — 15 Steps

### Phase A: Plan (Steps 1–6) — No code yet

1. **Understand the brief + context gate** — Brand name, industry, one-line vibe. Then ask ONCE, in one message: **Audience** (who is this for?) · **Job** (the single action the page should drive) · **Tone** (pick an extreme — launch-cinematic, utilitarian, luxury, playful; "clean and modern" is not a tone). The user may say *"go ahead"* — then infer all three and **disclose the inference in one line** (*"Going with: audience = X · job = Y · tone = Z — redirect me if wrong."*). Never build on silent guesses; in non-interactive runs, skip the question but keep the disclosure.
2. **Pick archetype** — Use the archetype matrix below. Must differ from the previous build per the diversification rule (Step 0.5).
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

**Phase A gate — preview before code.** Output a five-line preview the user can redirect in five seconds, *before* any code: **Profile** · **Archetype** · **Palette family** · **Patterns** (per section, ` · `-separated) · **Deliverable mode**. If `.motion-site/log.json` has prior entries, add one line: *Differs from last build on: <archetype / patterns>.*

### Phase B: Build (Steps 7–12)

7. **Find a reference** — Call `motion_find_reference` with vibe + archetype; adapt the closest corpus prompt instead of generating from scratch.
8. **Scaffold** — Vite + React 18 + TS + Tailwind (default config, no extensions) + lucide-react. Framer Motion only if scroll-linked transforms are needed. App showcases: plain HTML/CSS/JS.
9. **Paste primitives verbatim** — `motion_get_template` for liquid-glass, text-glow, keyframes, etc. Do not paraphrase CSS.
10. **Layer explicitly** — video `z-0` → overlay `z-[1]` → content `z-10` → nav `z-20`. No decorative blobs or radial gradients when a video provides depth.
11. **Typography** — Display serif (huge, `leading-[0.9..1.15]`, negative tracking, optional `text-glow`), body grotesk in white opacity tiers. Emphasize one phrase via `<em>` color/italic swap.
12. **Motion** — Entrance: fade + rise 16–32px, 0.5–1.2s, staggered 0.08–0.2s, token easing (expo-out). Scroll: pick ONE school per page — Framer `useScroll`/`whileInView`, hand-rolled rAF + lerp, OR `@supports`-gated CSS scroll-driven animations (`modern-css-motion.md`); a project that already runs GSAP keeps GSAP (`gsap-interop.md`). Animate only `transform`/`opacity`/`filter`. Multi-element scenes follow `references/choreography.md` (attention budget, staging, follow-through, paired exits).

### Phase C: Validate (Steps 13–15)

13. **Lint each component** — Call `motion_validate` on every file's code; fix ERRORs (mandatory), WARNINGs (recommended), INFOs (nice-to-have). Rules M01–M12 cover macro composition; **M13–M18 cover interaction craft** (ease-in, `scale(0)`, popover origin, press feedback, hover gating, instant focus ring); **M19–M20 cover layout safety** (`overflow-x: hidden` on root, z-index escape hatches). If M16 flags a CTA, add `active:scale-[0.97]` rather than suppressing it.
14. **Runtime smoke (code mode)** — Run dev server in the browser pane: console clean, video plays muted+looped, entrance stagger visible, emulate `prefers-reduced-motion` and verify animations collapse.
15. **Critique, stamp, register / emit** —
    - **Pre-emit self-critique**: score the build 1–5 on six axes — **P**urpose (every animation has a reason) · **T**empo (budgets match the frequency filter) · **C**ohesion (one easing family, token values) · **R**estraint (nothing animates that shouldn't) · **A**ccessibility (reduced-motion, focus, ARIA) · **V**ariety (differs from the previous build). Any axis < 3 → revise before emitting.
    - **Stamp** the entry file's first comment: `/* motion-site · profile: <name> · archetype: <name> · patterns: <a·b·c> · critique: P5 T4 C5 R5 A5 V4 */`. The stamp is the durable record the next build (and `review-motion`/`improve-motion`) reads.
    - **Log**: append `{ "date", "profile", "archetype", "patterns", "brief" }` to the front of `.motion-site/log.json` (create it if missing; trim to the last 20 entries). Committing `.motion-site/` is the host project's choice — respect an existing `.gitignore` entry, and don't add one unasked.
    - Code mode: final `motion_validate_file` pass on the entry page. Prompt mode: assemble the portable prompt per the guide, then lint any embedded CSS/JSX blocks (stamp goes at the top of the prompt's CSS block; skip the log).

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
- ❌ Animating the focus ring's appearance — `:focus-visible` ring shows instantly (M18)
- ❌ `overflow-x: hidden` on `html`/`body` to mask a bleed — use `overflow-x: clip` and fix the overflowing element; `hidden` breaks `position: sticky` (M19)
- ❌ Invented metrics, testimonials, or logo walls (*"+47% conversion"*, *"trusted by 50,000 teams"*) — use the user's real numbers, a clearly-labeled placeholder, or drop the section
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
- [ ] Focus ring appears instantly; no `overflow-x: hidden` on html/body (use `clip`); z-index stays on the layering scale
- [ ] Anything auto-playing > 5s (marquee, ambient loop) pauses off-viewport; no spinning elements > 100px, parallax ≤ 2–3 layers (vestibular safety — `choreography.md` §7)
- [ ] Every animated conditional mount has a paired exit (`AnimatePresence` / `@starting-style`); exits 30–50% shorter than entrances
- [ ] Stamp comment written; `.motion-site/log.json` entry appended (code mode)

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

- `references/design-profiles.md` — the five design profiles (cinematic/product-ui/editorial/playful/ecommerce): DNA, motion voices, when-to-use, how to select & customize
- `references/profile-schema.md` — the profile JSON schema + deriving a custom profile from user references (Step 0a)
- `references/motion-design-dna.md` — full design-language guidelines (cinematic profile, macro composition)
- `references/interaction-standards.md` — micro-interaction craft: press/popover/toast/hover, easing rationale, springs & overshoot budgets, frequency filter (rules M13–M18)
- `references/choreography.md` — composing multi-element motion: attention budget, staging, follow-through, direction semantics, context adaptation
- `references/component-catalog.md` — verbatim primitives and snippets
- `references/animation-vocabulary.md` — precise motion terms (name an effect; write specs that don't guess)
- `references/modern-css-motion.md` — zero-dependency CSS techniques: scroll-driven animations, view transitions, `linear()` springs, `@property`, anchor positioning
- `references/gsap-interop.md` — behavior contract + idioms when the host project already uses GSAP
- `references/troubleshooting.md` — symptom → cause → fix when motion runs right but feels wrong
- `references/prompt-writing-guide.md` — portable prompt formula (prompt mode)
- `data/prompt-index.json` — tagged corpus index (generated)
