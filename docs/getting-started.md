# Getting Started

Three ways to use this repo, from zero-setup to full agent workflow.

## Path 1 — Copy a Prompt (no setup)

Best if you use an AI website builder (Bolt, Lovable, v0) or an AI editor (Cursor, Windsurf).

1. **Pick a prompt.** Browse the [catalog](../prompts/README.md), grouped by design profile:
   - *Cinematic* — video-first, glassmorphism, editorial serif (the flagship; 6 prompts)
   - *Profile exemplars* — two 100/A+ references each for product-ui, editorial, playful, ecommerce
2. **Paste the entire file** into your builder's prompt box. These prompts are engineered for one-shot generation — don't trim sections.
3. **Personalize only these values** (everything else is load-bearing):
   - Brand name and all copy (headline / subtext / CTA labels)
   - Accent color (keep it to ONE saturated hue)
   - Media placeholders (`{YOUR_VIDEO_URL}`, `{YOUR_POSTER_URL}`) — **supply your own licensed or royalty-free media** (e.g. Pexels/Coverr under their licenses)
4. If the output drifts (extra gradients, wrong fonts), re-paste the prompt's `CONSTRAINTS` block as a follow-up message.

## Path 2 — Claude Code Skill (recommended)

The skill turns "build me a hero" into a planned, linted result.

```bash
git clone <this-repo>
ln -s "$(pwd)/<repo>/skills/motion-site-builder" ~/.claude/skills/motion-site-builder
```

Ask naturally: *"Build a cinematic landing page for my coffee subscription brand."* The skill will:

1. Pick an archetype and palette family, storyboard the sections (Plan)
2. Retrieve the nearest of the 92 reference prompts and adapt it with verbatim primitives (Build)
3. Lint every file with 12 motion rules and fix findings before showing you (Validate)

You can also ask for **prompt mode**: *"...and give me a portable prompt for Lovable instead of code."*

## Path 3 — MCP Tools (optional power-up)

Registers 8 tools any MCP client can call. Zero dependencies — stock Python 3.9+.

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
| `motion_find_reference` | "closest prompt to *dark SaaS glass hero*" |
| `motion_suggest_pattern` | "how should this section move?" |
| `motion_get_template` | verbatim CSS/JSX primitive by name |
| `motion_get_tokens` | the full design-token JSON |
| `motion_validate` / `motion_validate_file` | lint code, get score + grade |

## CLI Cheatsheet (no MCP needed)

```bash
# lint a file (exit 1 on errors)
python3 skills/motion-site-builder/scripts/lint_motion.py src/App.tsx

# verify the engine
python3 skills/motion-site-builder/scripts/lint_motion.py --self-test

# re-index after adding prompts
python3 skills/motion-site-builder/scripts/build_index.py
```

## Make It Yours

Every taste decision (easings, durations, palette, dependency whitelist, rule severities) lives in [`config/motion-tokens.json`](../skills/motion-site-builder/config/motion-tokens.json). See the [customization recipes](../skills/motion-site-builder/README.md#customize-the-whole-point).
