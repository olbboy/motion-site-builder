# Changelog

All notable changes to this project are documented here. Format follows [Keep a Changelog](https://keepachangelog.com/); versioning follows [SemVer](https://semver.org/).

## [Unreleased]

### Added — motion-craft study: choreography, custom profiles, drift audit, multi-runtime packaging

Distilled from a study of five open motion/design skill repos ([lottiefiles/motion-design-skill](https://github.com/lottiefiles/motion-design-skill), [AThevon/genjutsu](https://github.com/AThevon/genjutsu), [zanwei/design-dna](https://github.com/zanwei/design-dna), [greensock/gsap-skills](https://github.com/greensock/gsap-skills), [cloudai-x/threejs-skills](https://github.com/cloudai-x/threejs-skills)) — concepts adapted to this project's profiles and values; nothing copied verbatim, and the no-WebGL / no-GSAP-by-default stance is deliberately preserved.

- **4 new reference docs** in `skills/motion-site-builder/references/`:
  - **`choreography.md`** — composing multi-element motion: attention budget (one hero motion per moment, ≤⅓ of elements active), 1/3 travel rule, staging & focus dimming, secondary action / follow-through offsets, parallax depth ratios, narrative act budgets, direction semantics (rise = arrival, sink = dismissal), context adaptation (platform tempo, vestibular safety, 100th-viewing test, pausable >5s loops), and six composed-moment recipes (page load, modal, list update, tabs, accordion, celebration).
  - **`troubleshooting.md`** — symptom → cause → fix vocabulary for review/audit verdicts ("looks robotic", "feels cheap/flat", "too distracting", "no personality") plus per-profile failure modes and a 7-point quick diagnostic.
  - **`modern-css-motion.md`** — zero-dependency techniques as progressive enhancement: CSS scroll-driven animations (`animation-timeline: view()/scroll()`, now the documented **third scroll school**), View Transitions API, `linear()` spring easing, `@property`, anchor positioning, container-query motion, and the rendering-cost table behind M02.
  - **`gsap-interop.md`** — behavior contract when a host project already uses GSAP (the builder still never introduces it): `useGSAP`/`scope`/`contextSafe` lifecycle, ScrollTrigger correctness (scrub XOR toggleActions, no nested triggers, `containerAnimation` needs `ease: "none"`), `quickTo`, `gsap.matchMedia()` reduced-motion, and audit greps.
- **Profile schema gains a perceptual layer** — every profile JSON now carries `aesthetic` (mood/genre/personality/density/ornamentation), `imagery` (photo treatment, illustration style, image shape), `elevation` (shadow style + levels; cinematic/editorial stay `"none"` by philosophy), and `voice` (tone, CTA style, error tone). Documented in the new **`references/profile-schema.md`** — which also adds **Step 0a: derive a custom profile from user references** (extraction heuristics + priority order), turning the five shipped profiles into presets of an open, reference-driven profile system. The engine needed zero changes — profiles were already name-parametric.
- **`scripts/audit_consistency.py`** — zero-dep cross-file drift audit (the layer a per-file linter can't see): inventories literal duration/easing/spring values across a source tree (including every item in comma-separated CSS declarations), marks token vs off-token curves per active profile, flags drift (>8 distinct durations / >5 off-token easings; `-delay` values and the mandatory reduced-motion `0.01ms` resets are excluded, and `ease: CONST` array constants are resolved to their curves), and lists exit-risk files (conditional `<motion.*>` mounts with no exit mechanism — `AnimatePresence`, `@starting-style`, or a mounted flag). Wired into `improve-motion` recon and AUDIT.md §7.
- **Interaction standards deepened** — spring preset table (snappy/gentle/bouncy/heavy stiffness-damping-mass), overshoot budget by context (errors 0%, feedback 2–5%, success 5–10%, celebration 15–25%), and the paired-exit rule (every entrance needs an exit; exits 30–50% shorter).
- **`design-profiles.md`** — the three motion-voice archetypes (invisible / storytelling / joyful) with per-profile weighting, plus the never-mix-within-one-animation rule.
- **Audit coverage for foreign stacks** — AUDIT.md now includes a WebGL checklist (`dispose()`, pixel-ratio cap ≤2, pause on hidden tab / reduced-motion, context-loss fallback) and the GSAP checklist, so `improve-motion` judges those surfaces by their own idioms instead of flagging them wholesale.
- **Multi-runtime packaging** — `.claude-plugin/` (plugin + marketplace manifests for `/plugin marketplace add olbboy/motion-site-builder`), `skills/llms.txt` (skill index with triggers for fast agent discovery), `.github/copilot-instructions.md` (condensed motion DNA for Copilot users), and root `AGENTS.md` (conventions for agents editing this repo).
- **SKILL/checklist updates** — builder Step 0a (derive profile), third scroll school in Step 12 and motion-design-dna §6, vestibular-safety + paired-exit items in the Polish Checklist; `review-motion` cites choreography/troubleshooting/gsap-interop.

### Fixed

- **M09** — the z-index detection regex is now word-bounded (`(?<![\w-])z-`), so unrelated utilities like `translate-z-12` no longer count as "explicit layering" on a video stack.
- **`--self-test` schema check** — `layering` added to the required profile keys, so a derived profile missing its z-scale fails validation up front instead of only surfacing later through M09/M20.
- `.claude/launch.json` — the aurelia dev-server entry now points at `examples/aurelia-landing` instead of a machine-local scratch path.
- **Dev toolchain: Vite 5 → 8** (+ `@vitejs/plugin-react` 4 → 6) in `site/` and `examples/aurelia-landing` — clears the remaining `npm audit` high/moderate advisories in the dev-server toolchain (full audit now 0 vulnerabilities in both projects). No config or runtime changes were needed; production builds, dev-server smoke, and the 100/A+ lint matrix all verified unchanged.

### Added — build accountability layer + 3 lint rules

Workflow disciplines adapted from studying [nutlope/hallmark](https://github.com/nutlope/hallmark)'s anti-slop methodology, translated to motion-site's motion-first scope:

- **3 new lint rules — total 20** (M01–M12 macro, M13–M18 interaction craft, M19–M20 layout safety):
  - **M18** — animated focus ring: a transition on `outline`/`box-shadow` in a `:focus`/`:focus-visible` block or its base selector delays the keyboard user's only location cue; Tailwind `transition[-shadow]` + `focus-visible:ring-*` is covered too.
  - **M19** — `overflow-x: hidden` on `html`/`body`: creates a scroll container that breaks `position: sticky` and masks the real overflow bug; use `overflow-x: clip` and fix the overflowing element.
  - **M20** — z-index escape hatches (`z-index: 9999`-style values ≥ 999) abandon the explicit layering scale. M09 (layering) no longer accepts an escape-hatch value as "explicit layering".
  - Self-test fixtures updated (bad fixture fires 19 rules; site + examples re-linted, all still 100/A+).
- **Builder accountability workflow** (`motion-site-builder/SKILL.md`):
  - **Step 0.5 pre-flight scan** — on existing projects, read fonts/tokens/motion stance/framework first and emit a cited "Preserving / Introducing" block; extend the project's tokens, never invent a parallel set.
  - **Context gate** — ask Audience · Job · Tone once (opt-out with `"go ahead"`); inferred picks must be disclosed in one line, never silent.
  - **Phase A preview gate** — a five-line Profile/Archetype/Palette/Patterns/Mode preview the user can redirect before any code is written.
  - **Pre-emit self-critique** — six axes (Purpose, Tempo, Cohesion, Restraint, Accessibility, Variety) scored 1–5; any axis < 3 forces a revision pass.
  - **Stamp + project memory + diversification** — every build stamps its entry file (`/* motion-site · profile · archetype · patterns · critique */`) and appends `.motion-site/log.json`; the next build's archetype and pattern set must differ from the last, with the rotation stated in plain text.
  - **Honest copy** — invented metrics/testimonials/logo walls added to the universal FORBIDDEN list.
- **`review-motion`**: verifies stamps against code ("stamp lies" are findings); escalation triggers for animated focus rings, root `overflow-x: hidden`, and z-index escape hatches.
- **`improve-motion`**: recon reads `.motion-site/log.json` + stamps as declared intent and audits stamp-vs-code drift.
- **`docs/project-roadmap.md`** — hallmark-inspired backlog (variant mode, briefs-as-fixtures eval suite, motion-DNA study verb, per-component duration multipliers, 8-state demo wrapper).
- **`examples/aurelia-landing/`** — cinematic code-mode dogfood: the full React + Vite + framer-motion project built from `prompts/aurelia-landing.md` (staggered hero, `whileInView` reveals, `useScroll` sticky-stack, `useReducedMotion()` gating), 100/A+ on every source file, stamped, bring-your-own-media placeholders. Born from a 3-way rebuild experiment (local skill build vs two Lovable runs) where the local build was the only one to pass the sticky-stack check first try.
- **Overflow guard in 25 sticky/scroll prompts + prompt-writing-guide** — appended to CONSTRAINTS: never `overflow-x: hidden` on html/body or a root wrapper (silently breaks `position: sticky`); use `overflow-x: clip`. Motivated by a live Lovable rebuild that spontaneously emitted the broken pattern (caught by the new M19 rule); index rebuilt.
- **`npx skills add` documented as the primary install path** — the repo's `skills/<name>/SKILL.md` layout is already discovered by the [skills CLI](https://github.com/vercel-labs/skills) (verified locally: all 3 skills found); README, getting-started, and the builder README now lead with it. No manifest needed — hallmark's `package.json "skill"` field is that repo's own convention, not part of the CLI spec.

### Changed — clean-room prompt rebuild and expansion

- **The prompt library is now 100% original.** Removed 82 prompts that were inherited from a third party and rebuilt from the project's own design profiles. The clean-room library first reached 14 prompts, then expanded with 20 general-purpose prompts and a 20-prompt Vietnam landscape collection. The current library contains **54 original prompts**, all MIT and linted under their intended profile.
- **Bring-your-own-media by default** — most prompts use `{YOUR_VIDEO_URL}` / `{YOUR_POSTER_URL}` placeholders. The Vietnam collection records Pexels source pages, photographer provenance, crop guidance, and stable local asset targets; no third-party CDN assets or image binaries are shipped. All fonts are open-licensed (Google Fonts / OFL). No brand replicas.
- **Documentation now covers the full suite** — generating new interfaces, strict change review, whole-codebase audit and planning, explicit plan execution/reconciliation, standalone linting, MCP guidance, and five-profile customization.
- Relicensed: removed the third-party provenance note from `LICENSE`; refreshed `README`, prompt/docs/community guidance, and landing copy to match the original library.

## [1.0.0] — 2026-07-13

First stable release. Five design languages, a live self-built demo, and a brand mark — everything the engine promises, dogfooded end to end.

### Added

- **Five-language landing redesign** (`site/`) — the demo leads with the product: the hero embeds a live, auto-advancing stage that plays each of the five profiles in its own art direction and tempo (cinematic serif-on-black, product-ui dashboard, editorial paper, playful springs, ecommerce grid). An aurora-curtain canvas backdrop with a violet bloom replaces the old orb wash; a robust `IntersectionObserver` reveal system (force-shows anything already scrolled past) fixes sections that could strand invisible on a deep link or fast scroll; numbered eyebrows, `.panel` hairline surfaces, a terminal-style MCP panel, count-up stats, a serif double marquee, and a violet climax CTA. Every source file stays **100/A+**.
- **Brand mark** (`site/public/logo.svg`, `docs/assets/logo.svg`) — the logo _is_ the signature easing curve `cubic-bezier(0.16, 1, 0.3, 1)` with its playhead at rest; hand-drawn SVG, crisp from the 16px favicon to the README header on either GitHub theme. Replaces the borrowed lucide icon and emoji favicon.
- **Profile exemplar prompts** — two 100/A+ reference prompts per non-cinematic profile (product-ui dashboard + settings, editorial article + changelog, playful landing + event, ecommerce storefront + product page), retrievable by `motion_find_reference` via the profile name (the catalog category carries the profile). Corpus grows 84 → **92 prompts**.
- **Live demo on GitHub Pages** — the landing page deploys on every push and the repo homepage points at it; Open Graph / Twitter card metadata and a generated `og.png` preview for rich link unfurls.
- **Per-profile build resources** — `motion_suggest_pattern` and the component catalog are now profile-aware, so non-cinematic profiles can actually be built (not just linted):
  - `motion_suggest_pattern(intent, profile=…)` returns that profile's macro patterns (product-ui `list_stagger`/`panel_slide`/`skeleton_load`, editorial `sticky_toc`/`reading_progress`/`image_reveal`, playful `pop_entrance`/`sticker_hover`/`marquee`, ecommerce `product_grid`/`quick_view`/`add_to_cart`) plus the universal interaction patterns; fuzzy-matches free-text incl. Vietnamese.
  - 8 signature catalog primitives via `motion_get_template`: `product-ui-stat-card`, `product-ui-data-row`, `editorial-prose`, `editorial-sticky-toc`, `playful-pop-cta`, `playful-sticker-badge`, `ecommerce-product-card`, `ecommerce-add-to-cart`.
  - The prompt corpus stays cinematic-only by design (retrieval-over-generation is a cinematic optimization; no fabricated prompts).
- **Profile dogfood** — `examples/product-ui-dashboard/` is a real, self-contained product-ui page (sidebar, semantic stat cards, data table, interruptible toast) that scores **100/A+ under `product-ui`** and **75/C under `cinematic`** — the cross-profile gap proving each profile enforces its own taste.
- **Design profiles** — the engine now ships **five design languages** beyond the single cinematic one, making the "re-skin via config" promise real:
  - New profiles `product-ui`, `editorial`, `playful`, `ecommerce` (`config/profiles/*.json`); cinematic stays the default (`config/motion-tokens.json`) so all existing behavior is unchanged.
  - Profile-aware loader: `load_config(profile=…)`, CLI `--profile` / `--list-profiles`, `MOTION_PROFILE` env; `--self-test` now validates every profile's schema and lints under it.
  - `motion_list_profiles` MCP tool + an optional `profile` arg on `motion_get_tokens` / `motion_validate` / `motion_validate_file` / `motion_suggest_pattern` / `motion_easing_rationale`. 8 MCP tools total. `motion_easing_rationale` resolves curves by *kind* from the active profile (no hardcoded cinematic names).
  - `references/design-profiles.md`; the builder gains a "Step 0 — pick profile" and a universal-vs-cinematic FORBIDDEN split; `review-motion`/`improve-motion` apply the profile's macro bar (interaction/micro standards stay universal).
  - Each profile differs in entrance tempo, easing, palette strategy (`max_accent_hues`), typography, and which cinematic-only rules relax (e.g. `playful` disables M08). Universal rules (reduced-motion, GPU-only, press feedback, `ease-in` ban) apply to all.
- **`motion_easing_rationale` MCP tool** — the easing decision framework made programmatic: a motion intent (entrance/exit/move/hover/press/popover/toast/constant/scroll_reveal) → the right easing + duration + why + what to avoid. Config-driven (re-skin safe); cinematic intents keep the long budget, interaction intents obey the sub-300ms bar; fuzzy-matches free-text incl. Vietnamese. Total MCP tools: 7.
- **`references/animation-vocabulary.md`** — a concise glossary of motion terms (entrances, transitions, scroll, feedback, easing/springs, polish, principles) so prompts and review findings name effects precisely instead of "make it move nicely". Wired into the prompt-writing guide. Structure adapted from Emil Kowalski's MIT-licensed vocabulary.
- **Skill suite** — the repo grows from one skill to three, all sharing one engine (linter, tokens, standards):
  - **`review-motion`**: strict review of a diff or component's motion — 17-rule linter + senior design-engineer judgment, Before/After table, explicit Block/Approve verdict. `disable-model-invocation` (explicit action).
  - **`improve-motion`**: whole-codebase audit → prioritized findings → self-contained plans for cheaper executor models (two-tier). Read-only on source. Companion `AUDIT.md` (8 categories) + `PLAN-TEMPLATE.md`. Invocation variants (quick/deep/category/plan/execute/reconcile).
  - Both carry the macro/micro scoping discipline: hero entrances keep the cinematic budget; interaction elements held to the sub-300ms bar.
- **Interaction-craft layer** (distilled from Emil Kowalski's design-engineering philosophy): a micro-motion tier alongside the existing macro composition DNA.
  - **5 new lint rules M13–M17**: `ease-in` on UI (M13), `scale(0)` entrance (M14), popover/dropdown/tooltip origin-awareness (M15), press feedback on pressable/hover-motion elements (M16), raw-CSS `:hover` gating (M17). Total 17 rules. All scoped to interactive elements — hero entrances keep the cinematic budget.
  - **`config/motion-tokens.json` → `interaction`** block (press scale/duration, ui-max-duration, ease-in ban, popover origin, hover gating flags).
  - **`references/interaction-standards.md`**: precise-value catalog (frequency filter, easing rationale, duration budgets, physicality, interruptibility, springs, asymmetric timing, gestures).
  - **4 catalog primitives**: `press-scale-button`, `origin-aware-popover`, `interruptible-toast`, `hold-to-confirm` (exposed via `motion_get_template`).
  - **3 pattern intents** in `motion_suggest_pattern`: `press`, `popover`, `toast`.

### Changed

- Dogfood landing page CTAs now carry press feedback (`active:scale-[0.97]`), exemplifying M16 — still 100/A+ on every source file.

## 0.1.0 — 2026-07-12

### Added

- **Prompt library**: 83 curated motion-website prompts (78 sites + 5 mobile app showcases) with a catalog README.
- **motion-site-builder skill**: 15-step Plan → Build → Validate workflow with dual deliverable modes (working code or portable prompt).
- **Motion linter**: 12 config-driven rules (M01–M12) with score/grade output, CLI, and `--self-test`.
- **Corpus index builder**: regex-signal scanner generating `data/prompt-index.json` (archetypes, techniques, fonts, palettes, stack).
- **MCP server** (stdio, zero dependencies): `motion_validate`, `motion_validate_file`, `motion_get_tokens`, `motion_get_template`, `motion_suggest_pattern`, `motion_find_reference`.
- **Design references**: motion design DNA guidelines, 12-primitive component catalog, portable prompt-writing guide.
- **Customization layer**: all taste centralized in `config/motion-tokens.json` (easings, durations, palette families, dependency whitelist, lint severities).
- Community files: README, CONTRIBUTING, CODE_OF_CONDUCT, issue/PR templates, CI workflow.
- **Official landing page** (`site/`): dogfooded from the repo's own prompt (code mode), 100/A+ on every source file, procedural canvas aurora instead of third-party video; demo GIF + hero screenshot in `docs/assets/`.

[Unreleased]: https://github.com/olbboy/motion-site-builder/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/olbboy/motion-site-builder/releases/tag/v1.0.0
