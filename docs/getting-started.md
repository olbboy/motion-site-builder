# Getting Started

Use Motion Site Builder to create new UI, review a motion change, improve an existing codebase, or validate/tune motion directly. The repository currently ships **54 prompts**, **5 design profiles**, **3 agent skills**, **17 lint rules**, **24 reusable primitives**, and **8 MCP tools**.

## Choose the job first

| You want to… | Use | Result |
|---|---|---|
| Generate a new page or component | `motion-site-builder` | Working code or a portable one-shot prompt |
| Judge a changed component or diff | `review-motion` | Before/After findings plus Block/Approve |
| Improve motion across an existing app | `improve-motion` | Prioritized audit and executable plans |
| Check/tune existing code without a workflow | CLI or `motion_validate*` | Rule findings, score, grade, exact profile tokens |

## Path 1 — Copy a Prompt (no setup)

Best for AI website builders (Bolt, Lovable, v0) and AI editors (Cursor, Windsurf).

1. Browse the [54-prompt catalog](../prompts/README.md). It covers cinematic, product-ui, editorial, playful, and ecommerce work, plus a 20-concept Vietnam landscape collection.
2. Paste the entire prompt into the builder. The labeled sections and closing constraints are load-bearing; do not trim them.
3. Personalize only the values the prompt marks for replacement:
   - Brand and all copy (headline, subtext, CTA labels)
   - Palette within the chosen profile's accent budget
   - Licensed media placeholders or the documented local-download targets
4. If the output drifts, re-paste the prompt's `CONSTRAINTS` block and the affected section verbatim.

Most prompts use `{YOUR_VIDEO_URL}`, `{YOUR_POSTER_URL}`, or `{YOUR_IMAGE_URL_*}`. The Vietnam collection instead keeps Pexels **source-page** links and local asset targets; download the image locally and never hotlink the CDN. See the [media manifest](vietnam-landscape-pexels-selection.md).

## Path 2 — Install the Agent Suite

The three skills share one profile system, linter, token set, and motion standard. From the repository root, this is the Claude Code symlink setup:

```bash
git clone <this-repo>
cd motion-site-builder
for s in motion-site-builder review-motion improve-motion; do
  ln -s "$(pwd)/skills/$s" ~/.claude/skills/$s
done
```

Any agent runtime that reads `SKILL.md` can use the same skill directories. Runtime-specific discovery/install behavior varies; follow that runtime's skill-loading convention.

### Build new UI

```text
Build a product-ui subscription dashboard. Return working React code.
```

`motion-site-builder` will choose one of the five profiles, plan the narrative and patterns, retrieve the closest of 54 references, build with exact primitives, lint every file, and perform a runtime smoke check in code mode. Ask for **prompt mode** when you want Markdown for Bolt/Lovable/v0 instead of code.

### Review a diff or component

```text
Use review-motion to review the animation changes in this diff.
```

`review-motion` runs the mechanical M01–M17 checks, then applies judgment the linter cannot provide: frequency, interruptibility, timing asymmetry, origin, physicality, cohesion, and whether motion should be deleted. Output is an exact Before/After table followed by a **Block** or **Approve** verdict. It reviews motion only; it does not implement unrelated features.

### Improve an existing codebase

```text
Use improve-motion deep to audit this application.
```

The default workflow is deliberately read-only on source:

```text
Recon → 8-category audit → vetted findings → prioritized plans
```

Plans contain exact file paths, current excerpts, target curves/durations, scope guards, ordered edits, and mechanical plus feel-check verification. Then use an explicit execution path:

```text
improve-motion execute plans/001-fix-dropdown-origin.md
improve-motion reconcile
```

`execute <plan>` dispatches an executor and reviews its diff with the `review-motion` standard. `reconcile` marks completed plans, refreshes stale locations, and retires findings already fixed. Other variants include `quick`, `deep`, a category focus (`performance`, `accessibility`, `easing`, `frequency`), and `plan <description>`.

## Path 3 — Enable the MCP Tools

The zero-dependency Python server registers eight tools. This repo includes a generic [`.mcp.json`](../.mcp.json) example; use the equivalent MCP-server fields in clients with a different config format. Client runtimes may require approval, reload, or a new session before newly configured tools appear.

```json
{
  "mcpServers": {
    "motion-site-tools": {
      "command": "python3",
      "args": ["<absolute-repo-path>/skills/motion-site-builder/scripts/server.py"]
    }
  }
}
```

| Tool | Use |
|---|---|
| `motion_list_profiles` | List the five languages and choose the active taste first |
| `motion_get_tokens` | Get easing, duration, palette, typography, layering, dependency, and lint config |
| `motion_get_template` | Return one of 24 verbatim CSS/JSX primitives |
| `motion_suggest_pattern` | Suggest the right profile-specific pattern for an intent |
| `motion_easing_rationale` | Return which curve, how long, why, and what to avoid |
| `motion_find_reference` | Retrieve the nearest prompt by name/category/technique/font/stack/archetype |
| `motion_validate` | Lint an inline code string and return findings/score/grade |
| `motion_validate_file` | Lint a file on disk under the selected profile |

Taste-bearing tools accept `profile=cinematic|product-ui|editorial|playful|ecommerce`. Pattern and easing tools fuzzy-match free text, including common Vietnamese intent keywords.

## Path 4 — Validate Existing Code with the CLI

No MCP or agent skill is required.

```bash
# List profiles
python3 skills/motion-site-builder/scripts/lint_motion.py --list-profiles

# Lint an existing file under the right design language
python3 skills/motion-site-builder/scripts/lint_motion.py \
  --profile product-ui src/components/Dropdown.tsx

# Verify the rule engine and every profile schema
python3 skills/motion-site-builder/scripts/lint_motion.py --self-test

# Re-index after adding or editing prompts
python3 skills/motion-site-builder/scripts/build_index.py
```

Static lint catches deterministic problems; it cannot judge every spring, crossfade, or gesture. For changed UI, follow lint with `review-motion` and a runtime feel check at slow playback plus `prefers-reduced-motion`.

## Make It Yours

Cinematic defaults live in [`config/motion-tokens.json`](../skills/motion-site-builder/config/motion-tokens.json). Product UI, editorial, playful, and ecommerce live in [`config/profiles/`](../skills/motion-site-builder/config/profiles/). Every profile uses the same schema, so you can change easing/duration/stagger, palette and accent budget, typography, allowed dependencies, and lint severity without forking the engine.

See the [customization and extension guide](../skills/motion-site-builder/README.md#customize-the-whole-point).
