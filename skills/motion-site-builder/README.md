# motion-site-builder

An agent skill for building **cinematic, motion-driven websites** — heroes, landing pages, mobile-app showcases — with a validation loop that turns design taste into lintable rules.

Distilled from a corpus of 83 production prompts. Ships with:

- **A 15-step workflow** (Plan → Build → Validate) in [SKILL.md](SKILL.md)
- **A motion linter** — 12 config-driven rules (reduced-motion, layout-prop animation, accent budget, easing tokens, video hygiene…) with score + grade
- **An MCP server** (zero dependencies, stdio) exposing 6 tools: validate, tokens, templates, pattern suggestion, corpus retrieval
- **A tagged corpus index** — find the nearest reference prompt and adapt it instead of generating from scratch
- **Two deliverable modes** — working code (React + Vite + Tailwind) or a portable one-shot prompt for Bolt/Lovable/v0

## Layout

```
SKILL.md                     workflow, matrices, forbidden list (agent entry point)
references/
  motion-design-dna.md       full design-language guidelines
  component-catalog.md       verbatim primitives (liquid-glass, crossfade loop, …)
  prompt-writing-guide.md    portable-prompt formula
config/motion-tokens.json    ALL taste lives here — edit to re-skin
data/prompt-index.json       generated corpus index
scripts/
  lint_motion.py             rule engine (CLI + library)
  build_index.py             corpus scanner → index
  server.py                  MCP stdio server
```

## Install

The skill works from any of these locations — pick one:

```bash
# 1. Per-project (this repo already does this via symlink)
ln -s ../../skills/motion-site-builder .claude/skills/motion-site-builder

# 2. Global (all projects)
ln -s "$(pwd)/skills/motion-site-builder" ~/.claude/skills/motion-site-builder

# 3. Copy standalone into any agent runtime that reads SKILL.md
```

Optional MCP server (enables `motion_*` tools):

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

Without MCP, everything still works: the agent reads `config/motion-tokens.json` directly and runs `python3 scripts/lint_motion.py <file>`.

## Customize (the whole point)

**No brand lock-in.** The engine never hardcodes taste — it reads `config/motion-tokens.json`:

| Want to… | Edit |
|:---|:---|
| Change signature easings / durations / stagger | `easings`, `durations`, `stagger` |
| Use your own palette families / accent budget | `palette` |
| Allow another library (e.g. GSAP) | `dependencies.allowed` / remove from `forbidden` |
| Relax or mute a lint rule | `lint.disabled_rules`, `lint.severity_overrides` |
| Swap the whole design language | edit the JSON, then update `references/*.md` prose to match |

## Extend

- **Add prompts to the corpus**: drop `.md` files into your prompts dir, run `python3 scripts/build_index.py [prompts_dir]` — they become retrievable via `motion_find_reference`. Technique tags are regex signals in `build_index.py` (`TECHNIQUE_SIGNALS`) — add a line to tag a new technique.
- **Add a lint rule**: one function in `lint_motion.py` with the `@rule("M13", WARNING)` decorator. It automatically appears in both CLI and MCP output, and is config-disable-able.
- **Verify the engine**: `python3 scripts/lint_motion.py --self-test`.

## License note

The bundled prompt corpus is for learning/adaptation — replace video asset URLs with your own licensed media. Replica-style prompts (recreating existing brands) are for study only.
