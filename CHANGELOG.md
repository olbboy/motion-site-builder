# Changelog

All notable changes to this project are documented here. Format follows [Keep a Changelog](https://keepachangelog.com/); versioning follows [SemVer](https://semver.org/).

## [Unreleased]

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
