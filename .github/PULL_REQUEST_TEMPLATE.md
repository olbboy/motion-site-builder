# Pull Request

## What

<!-- One sentence. Conventional-commit style title, e.g. "feat(prompts): add nebula fintech hero" -->

## Type

- [ ] New prompt
- [ ] Engine change (linter / index / MCP server / config)
- [ ] Docs

## Checklist

**All PRs**
- [ ] CI passes locally (see commands in [CONTRIBUTING.md](../CONTRIBUTING.md))
- [ ] One concern per PR

**New prompt**
- [ ] Absolute values only (no adjective-without-value specs)
- [ ] `prefers-reduced-motion` + ARIA included
- [ ] Media URLs are owned/licensed or `{PLACEHOLDER}` marked
- [ ] `build_index.py` re-run, `data/prompt-index.json` committed
- [ ] Row added to `prompts/README.md`

**Engine change**
- [ ] Taste values live in `config/motion-tokens.json`, not in code
- [ ] `lint_motion.py --self-test` passes (fixtures updated if rules changed)
- [ ] Still zero runtime dependencies (stock Python 3.9+)
