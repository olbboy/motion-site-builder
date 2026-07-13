# Contributing

Thanks for helping make AI-generated websites less generic. Three ways to contribute, in order of impact:

## 1. Add a Prompt

The library grows one great prompt at a time.

**Requirements** (see [docs/prompt-guidelines.md](docs/prompt-guidelines.md) for the full spec):

- One `.md` file in `prompts/` (or `prompts/apps/` for mobile showcases), kebab-case name: `brand-or-concept-type.md` (e.g. `nebula-fintech-hero.md`).
- Opens with ONE imperative sentence stating what to build + exact stack.
- **Absolute values only** — full Tailwind class strings, hex colors, px, seconds, easing curves, copy verbatim. Adjectives without values ("elegant", "smooth") are spec bugs.
- Includes `prefers-reduced-motion` handling and ARIA on interactive elements (we hold a higher bar than the original corpus).
- Media URLs must be assets you have rights to (or clearly marked placeholders like `{YOUR_VIDEO_URL}`).
- No recreations of existing brands' trade dress.

**Then:**

```bash
# re-index the corpus (your prompt becomes retrievable by the skill)
python3 skills/motion-site-builder/scripts/build_index.py

# lint any embedded CSS/JSX blocks
python3 skills/motion-site-builder/scripts/lint_motion.py path/to/snippet.css
```

Add a row to the table in `prompts/README.md`, then open a PR using the prompt-submission template.

## 2. Improve the Engine

The skill lives in `skills/motion-site-builder/`. Ground rules:

- **Taste never goes in code.** Numbers, whitelists, and severities belong in `config/motion-tokens.json`. Engine scripts read config.
- **New lint rule** = one function in `scripts/lint_motion.py` with the `@rule("M13", WARNING)` decorator + a case in the self-test fixtures. Rules must be disable-able via config.
- **New technique tag** for the index = one regex line in `TECHNIQUE_SIGNALS` (`scripts/build_index.py`).
- Zero runtime dependencies is a feature — the linter and MCP server must run on stock Python 3.9+.

**Before pushing:**

```bash
python3 skills/motion-site-builder/scripts/lint_motion.py --self-test   # must pass
python3 skills/motion-site-builder/scripts/build_index.py               # must succeed
python3 -c "import json; json.load(open('skills/motion-site-builder/config/motion-tokens.json'))"
```

CI runs exactly these checks.

## 3. Improve the Docs

Docs live in `docs/` and `skills/motion-site-builder/references/`. Corrections, clearer examples, and translations are welcome. Keep reference docs normative ("do X") rather than narrative.

## Pull Request Conventions

- Conventional commits: `feat(prompts): add nebula fintech hero`, `fix(lint): M05 hue clustering`, `docs: clarify MCP setup`.
- One concern per PR. A prompt + an engine change = two PRs.
- PRs must pass CI and include the checklist in the PR template.

## Questions / Ideas

Open a [discussion or issue](.github/ISSUE_TEMPLATE) — especially before large engine changes, so we can agree on the config-vs-code boundary first.
