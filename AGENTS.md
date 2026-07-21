# Guidance for AI Agents Working in This Repo

This repository contains the **Motion Site Builder** suite: a prompt library (`prompts/`), three agent skills (`skills/`), a dogfooded landing page (`site/`), and profile dogfoods (`examples/`). When editing or extending it, follow these rules.

## Repo structure

- **skills/** — three skills, discovered by scanning for directories containing `SKILL.md`: `motion-site-builder` (build), `review-motion` (judge a diff), `improve-motion` (audit → plans). `skills/llms.txt` is the quick index.
- **Skill directory name** must exactly match the `name` in that skill's frontmatter.
- **All taste lives in config, never in engine code**: `skills/motion-site-builder/config/motion-tokens.json` (cinematic default) + `config/profiles/*.json`. Scripts (`lint_motion.py`, `server.py`, `build_index.py`, `audit_consistency.py`) are zero-dependency Python and read the active profile; they must keep working with any profile JSON that carries the required schema keys (see `references/profile-schema.md`).

## SKILL.md requirements

- Frontmatter: `name` (lowercase, hyphens, matches directory) and `description` (what + when + trigger terms, third person).
- Keep SKILL.md focused on workflow; long value catalogs go in `references/` and are linked, not inlined. Exact values (curves, durations, budgets) live in the references/config — SKILL.md cites, never approximates.

## Making changes

- **Add a prompt**: follow `docs/prompt-guidelines.md`, then re-run `python3 skills/motion-site-builder/scripts/build_index.py`.
- **Add or change a lint rule**: edit `scripts/lint_motion.py` (`@rule("MNN", …)` convention), document it in the matching reference file, and extend the built-in fixtures so `--self-test` covers it.
- **Change a profile / add a profile**: edit or add the JSON only (`config/profiles/<name>.json`); update `references/design-profiles.md`. Never hardcode taste in scripts.
- **After any engine/config change**: `python3 skills/motion-site-builder/scripts/lint_motion.py --self-test` must pass. CI runs the same checks.
- **Verify claims in docs**: counts (prompts, rules, tools) appear in README badges and prose — update them together.
- Conventional commits, no AI references. Plans go in `plans/`, docs in `docs/`.

## References

- [Agent Skills specification](https://agentskills.io/specification.md)
- [skills CLI (discovery, install)](https://github.com/vercel-labs/skills)
- `docs/architecture.md` — how skill, linter, index, and MCP server fit together
