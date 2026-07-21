# motion-site-builder

An agent skill for building publication-quality motion UI across **five design profiles**:

- `cinematic` — video/image-first marketing, glass, serif, one accent
- `product-ui` — fast dashboards, SaaS, admin, settings
- `editorial` — typography-first articles, docs, and changelogs
- `playful` — expressive campaigns, events, and consumer UI
- `ecommerce` — imagery-first storefronts, catalogs, and product pages

It converts a brief into a profile-aware **Plan → Build → Validate** workflow and returns either working code or a portable one-shot prompt. It is the build member of the larger motion-site suite; [`review-motion`](../review-motion/SKILL.md) reviews a diff/component, while [`improve-motion`](../improve-motion/SKILL.md) audits existing codebases and writes executable improvement plans.

## What ships

- **54 original reference prompts** in [`../../prompts/`](../../prompts/)
- **A 15-step workflow** with runtime smoke validation in [SKILL.md](SKILL.md)
- **Two deliverable modes** — working React/Vite/Tailwind code or portable Markdown for Bolt/Lovable/v0/Cursor
- **20 profile-aware lint rules** (M01–M12 macro composition, M13–M18 interaction craft, M19–M20 layout safety) with findings, score, and grade
- **8 zero-dependency MCP tools** for profiles, tokens, primitives, patterns, easing rationale, retrieval, and validation
- **24 verbatim catalog primitives** shared by cinematic and non-cinematic profiles
- **A generated corpus index** for retrieval by archetype, technique, stack, font, category, and palette signals

## Layout

```text
SKILL.md                         workflow, matrices, forbidden list
README.md                        install, customize, extend
references/
  design-profiles.md             five languages, motion voices, selection rules
  profile-schema.md              profile JSON schema + deriving custom profiles
  motion-design-dna.md           cinematic macro composition
  interaction-standards.md       universal micro-motion values, springs, overshoot
  choreography.md                multi-element composition and context adaptation
  animation-vocabulary.md        precise effect terminology
  component-catalog.md           24 verbatim primitives
  modern-css-motion.md           scroll-driven CSS, view transitions, linear() springs
  gsap-interop.md                contract + idioms for GSAP-using host projects
  troubleshooting.md             symptom → cause → fix for motion feel
  prompt-writing-guide.md        portable-prompt formula
config/
  motion-tokens.json             cinematic defaults
  profiles/*.json                product-ui · editorial · playful · ecommerce
data/prompt-index.json           generated 54-prompt index
scripts/
  lint_motion.py                 CLI/library rule engine
  audit_consistency.py           cross-file duration/easing drift inventory
  build_index.py                 prompt scanner → index
  server.py                      minimal MCP stdio server
```

## How the builder works

1. Pick the profile first; profile controls tempo, easing, palette, typography, dependencies, and lint severity.
2. Plan the archetype, palette, scroll narrative, motion frequency budget, and assets before code.
3. Retrieve the nearest prompt and request exact primitives/tokens rather than inventing near-matches.
4. Build with explicit layers, GPU-safe properties, profile-correct interaction budgets, reduced-motion, and ARIA.
5. Lint every motion-bearing file, fix findings, then smoke-test runtime behavior and reduced motion.

Code mode defaults to React 18 + Vite + TypeScript + Tailwind + lucide-react. Profile configs allow Radix/Recharts for product UI, Embla for ecommerce, and Framer Motion only when the motion requires it. Prompt mode writes an absolute-value specification that another builder can implement without guessing.

## Install

With the [skills CLI](https://github.com/vercel-labs/skills) (Claude Code, Cursor, Codex, …):

```bash
npx skills add olbboy/motion-site-builder --skill motion-site-builder
```

Or, from a repository clone, install only the builder in Claude Code:

```bash
ln -s "$(pwd)/skills/motion-site-builder" ~/.claude/skills/motion-site-builder
```

Or install the full build/review/improve suite in Claude Code:

```bash
for s in motion-site-builder review-motion improve-motion; do
  ln -s "$(pwd)/skills/$s" ~/.claude/skills/$s
done
```

For another agent runtime, copy or link the skill directories using that runtime's `SKILL.md` discovery convention.

## Optional MCP server

The server runs on stock Python and exposes all eight `motion_*` tools:

```json
{
  "mcpServers": {
    "motion-site-tools": {
      "command": "python3",
      "args": ["<absolute-path>/skills/motion-site-builder/scripts/server.py"]
    }
  }
}
```

This repository includes a generic [`.mcp.json`](../../.mcp.json) example. Use the equivalent MCP-server fields in clients with a different config format; a client may require a reload or new session before newly configured tools appear.

Without MCP, the workflow still works: read the active profile JSON directly, search the prompt index/catalog, and run the CLI linter.

## Customize (the whole point)

**No brand lock-in.** Taste values live in the active profile JSON, not in engine code:

| Want to… | Edit |
|---|---|
| Change cinematic defaults | `config/motion-tokens.json` |
| Change product-ui/editorial/playful/ecommerce | `config/profiles/<profile>.json` |
| Tune easing, duration, stagger | `easings`, `durations`, `stagger` |
| Change palette families or accent budget | `palette` |
| Change typography or radii | `typography`, `radius` |
| Allow or forbid a dependency | `dependencies.allowed`, `dependencies.forbidden` |
| Relax or raise a lint rule | `lint.disabled_rules`, `lint.severity_overrides` |

Every profile uses the same schema. To add a sixth language, copy the closest profile JSON, change its values, and run `lint_motion.py --self-test`; profile discovery is automatic.

## Extend

- **Add a prompt**: add a `.md` file under `prompts/`, add its catalog row, then run `python3 scripts/build_index.py [prompts_dir]`.
- **Add a technique signal**: add one regex entry to `TECHNIQUE_SIGNALS` in `build_index.py` and rebuild the index.
- **Add a primitive**: add a numbered `## N. name` section to `component-catalog.md`; `motion_get_template` discovers it from the heading.
- **Add a lint rule**: register one function with `@rule("MNN", SEVERITY)`, add self-test coverage, and keep values in profile config.
- **Add a pattern intent**: extend the matching profile's pattern matrix and its fuzzy-keyword map in `server.py`.

## Verify

```bash
# Validate every profile schema and linter fixture
python3 scripts/lint_motion.py --self-test

# List profiles or lint existing code under one
python3 scripts/lint_motion.py --list-profiles
python3 scripts/lint_motion.py --profile editorial path/to/article.tsx

# Rebuild retrieval data after prompt changes
python3 scripts/build_index.py
```

## License and media

The prompt corpus is original and designed for adaptation, not brand replication. Supply media you own or can license. Most prompts use explicit placeholders; curated source-page links must resolve to local downloaded assets rather than third-party CDN hotlinks.
