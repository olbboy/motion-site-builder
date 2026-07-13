# Architecture

How the pieces fit, and the design contracts that keep the project extensible.

## System Overview

```
                        ┌──────────────────────────────────────┐
                        │  config/motion-tokens.json           │
                        │  ALL taste: easings, durations,      │
                        │  palette, whitelists, severities     │
                        └───────┬───────────────┬──────────────┘
                                │ read           │ read
        ┌───────────────────────▼──┐      ┌──────▼──────────────────┐
 prompts/*.md ──► build_index.py   │      │  lint_motion.py         │
 (92 files)      └► data/          │      │  @rule registry M01–M17 │
                    prompt-index   │      │  score · grade · CLI    │
                    .json          │      └──────▲──────────────────┘
                        ▲          │             │ import
                        │ query    │             │
                  ┌─────┴──────────┴─────────────┴───┐
                  │  server.py — MCP stdio (0 deps)  │
                  │  validate · tokens · template ·  │
                  │  suggest_pattern · find_reference│
                  └─────────────▲────────────────────┘
                                │ tools
                  ┌─────────────┴────────────────────┐
                  │  SKILL.md — agent workflow       │
                  │  Plan → Build → Validate         │
                  │  references/ = knowledge layer   │
                  └──────────────────────────────────┘
```

## The Three Contracts

### 1. Taste lives in config, never in code

`config/motion-tokens.json` is the single source of truth for every aesthetic decision. The linter reads ranges and whitelists from it; the MCP pattern matrix interpolates its values; the skill cites it. **Re-skinning the entire system for a different design language = editing one JSON file.** Engine code changes are only needed for new *kinds* of checks, never new *values*.

This is realized as **design profiles**: `config/motion-tokens.json` is the cinematic default; `config/profiles/*.json` are alternate design languages (product-ui, editorial, playful, ecommerce), same schema, different values. `load_config(profile=…)` resolves the active one (also via `--profile` / `MOTION_PROFILE`); the MCP tools take an optional `profile` arg. Universal rules (reduced-motion, GPU-only, `ease-in` ban, press feedback) hold across profiles; per-profile values (entrance tempo, `max_accent_hues`, tracking, `lint.disabled_rules`) select the taste. Adding a profile is a JSON drop-in — `--self-test` validates each profile's schema and that it lints without crashing.

### 2. The corpus is data, the index is derived

Prompts are plain markdown — no frontmatter, no build step for authors. `build_index.py` derives everything (archetype, techniques, fonts, palette, stack) via regex signals at index time. Consequences:

- Adding a prompt = drop a file + re-run one script.
- Tags are lower bounds (a prompt not *mentioning* React may still assume it). Retrieval treats them as hints, not truth.
- New technique? Add one regex to `TECHNIQUE_SIGNALS`. The whole corpus re-tags on the next run.

### 3. Zero runtime dependencies

The linter, index builder, and MCP server run on stock Python 3.9+. The MCP server implements its own minimal JSON-RPC 2.0 stdio loop rather than importing an SDK. This keeps installation to a `git clone` and makes the skill portable to any agent runtime.

## Component Notes

**Linter (`lint_motion.py`)** — Rules are functions registered via `@rule(id, default_severity)`. Each receives a pre-parsed `Source` (raw text + cheap derived properties) and the config; each returns finding dicts. Config can disable rules or override severities without code changes. `Score = 100 − 15·errors − 5·warnings − 1·infos` (weights configurable). `--self-test` runs two built-in fixtures: a bad one that must fire 16 rules (M01–M17 except the package.json-only M04), a good one that must score ≥ 90. Rules M01–M12 cover macro composition; M13–M17 cover interaction craft (see `references/interaction-standards.md`).

**Index builder (`build_index.py`)** — Walks the prompts dir, merges metadata parsed from `prompts/README.md` tables with regex-derived signals. Archetype classification is heuristic (path, keywords, size) and can be corrected by editing `classify_archetype`.

**MCP server (`server.py`)** — Thin adapter: every tool is a small function over the linter, config, catalog, or index. `motion_get_template` extracts `## N. name` sections from `references/component-catalog.md` — keep those headers stable. `motion_find_reference` scores query terms against name/category/techniques/fonts/stack (weighted 3/2/1). `motion_easing_rationale` maps a motion intent (entrance/press/popover/toast/…) to the right easing + duration + why, reading curves and budgets from config so it stays re-skinnable.

**Skill (`SKILL.md` + `references/`)** — The compressed operational layer (workflow, matrices, forbidden list) lives in SKILL.md; deep knowledge (design DNA, catalog, prompt formula) loads on demand from references. The skill degrades gracefully without MCP: it reads the config directly and shells out to the linter CLI.

**Skill suite (build · review · improve)** — Three skills share the one engine, each doing ONE thing: `motion-site-builder` (build), `review-motion` (review a diff → Before/After table + Block/Approve), `improve-motion` (audit a codebase → self-contained plans for cheaper executors). `review-motion` and `improve-motion` are *method* skills — they call `motion_validate*` for the mechanical layer and delegate every precise value to `references/interaction-standards.md` / `motion-design-dna.md` and `motion_get_tokens`, never duplicating tables. This keeps the "taste lives in config" contract intact across the suite. All carry the macro/micro scoping rule: hero entrances keep the cinematic budget (0.5–1.2s); interaction elements are held to the sub-300ms bar.

## Validation Layers

| Layer | Catches | Mechanism |
|---|---|---|
| Static lint | Structure: missing reduced-motion, layout-prop animation, easing drift, video hygiene, accent soup | regex/heuristics, deterministic |
| Runtime smoke | Behavior: jank, broken loops, console errors, reduced-motion actually collapsing | agent drives a browser (dev server + screenshot + console) |
| CI | Regression: engine self-test, config validity, index freshness, MCP handshake | `.github/workflows/ci.yml` |

Static linting is necessary but not sufficient for motion — the skill's workflow makes the runtime smoke test an explicit step (14) rather than pretending regex can see animation.
