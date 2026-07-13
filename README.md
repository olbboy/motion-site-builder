<div align="center">

<img src="docs/assets/logo.svg" alt="Motion Site Builder logo — the cubic-bezier(0.16, 1, 0.3, 1) curve" width="96" height="96">

# Motion Site Builder

**Build cinematic, motion-driven websites with AI — from a single prompt.**

A library of 54 original, production-grade website prompts + a suite of agent skills that **build**, **review**, and **audit** motion UI so the result actually looks premium.

[![CI](https://github.com/olbboy/motion-site-builder/actions/workflows/ci.yml/badge.svg)](https://github.com/olbboy/motion-site-builder/actions/workflows/ci.yml)
[![Release](https://img.shields.io/github/v/release/olbboy/motion-site-builder?color=7342e2)](https://github.com/olbboy/motion-site-builder/releases/latest)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Prompts](https://img.shields.io/badge/prompts-54%20original-8A2BE2)](prompts/README.md)
[![Lint Rules](https://img.shields.io/badge/motion%20lint%20rules-17-success)](skills/motion-site-builder/scripts/lint_motion.py)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

[**Live demo**](https://olbboy.github.io/motion-site-builder/) · [Quick Start](#-quick-start) · [How It Works](#-how-it-works) · [The Design DNA](#-the-design-dna) · [Docs](#-documentation) · [Contributing](#-contributing)

[![Motion Site Builder landing page — built and linted by its own skill](docs/assets/demo.gif)](https://olbboy.github.io/motion-site-builder/)

*This [landing page](https://olbboy.github.io/motion-site-builder/) ([`site/`](site)) was built from [its own prompt](prompts/motion-site-builder-landing.md) — a cinematic shell whose hero embeds a live five-language stage — and scores 100/A+ on every file with the bundled motion linter.*

</div>

---

## ✨ What's Inside

| | |
|---|---|
| 🎬 **[Prompt Library](prompts/README.md)** | 54 original prompts (cinematic heroes, dashboards, docs, storefronts, campaigns) ready to paste into Bolt, Lovable, v0, or Cursor — including [our own landing page](prompts/motion-site-builder-landing.md), two 100/A+ exemplars per non-cinematic profile, and a 20-concept Vietnam landscape collection with locally downloaded Pexels media targets. Every prompt is authored from the project's own design DNA — no brand replicas and no hotlinked third-party assets. |
| 🤖 **Agent Skills (×3)** | A suite for Claude Code and compatible agents: **[motion-site-builder](skills/motion-site-builder/SKILL.md)** (15-step Plan → Build → Validate → working code *or* portable prompt), **[review-motion](skills/review-motion/SKILL.md)** (strict diff review → Before/After table + Block/Approve), **[improve-motion](skills/improve-motion/SKILL.md)** (audit a whole codebase → self-contained plans for cheaper models) |
| ✅ **[Motion Linter](skills/motion-site-builder/scripts/lint_motion.py)** | 17 rules that catch what makes AI-generated sites look cheap: missing reduced-motion, layout-property animation, easing chaos, accent-color soup — plus interaction craft (`ease-in` on UI, `scale(0)`, popover origin, missing press feedback) |
| 🔌 **[MCP Server](skills/motion-site-builder/scripts/server.py)** | Zero-dependency tools: validate code, fetch design tokens, suggest motion patterns, explain the right easing per intent, retrieve the nearest reference prompt |

## 🚀 Quick Start

### Path 1 — I just want a beautiful site (30 seconds)

1. Browse the [prompt catalog](prompts/README.md) and open a prompt close to your idea.
2. Copy the whole file into **Bolt / Lovable / v0 / Cursor**.
3. Change only: brand name, headline copy, accent color, and the background video URL (use your own — see [licensing](#-license--provenance)).

### Path 2 — I use Claude Code (the full experience)

```bash
git clone https://github.com/olbboy/motion-site-builder
cd motion-site-builder
for s in motion-site-builder review-motion improve-motion; do
  ln -s "$(pwd)/skills/$s" ~/.claude/skills/$s
done
```

Then just ask: *"Build a cinematic hero for my AI startup"* — the builder picks an archetype, adapts the closest reference prompt, and lints the result before showing you. Later, *"review the motion in this component"* runs `review-motion`; *"improve the animations in this app"* runs `improve-motion`. All three share one engine (linter, tokens, standards).

### Path 3 — Enable the MCP tools (optional, zero deps)

```json
{
  "mcpServers": {
    "motion-site-tools": {
      "command": "python3",
      "args": ["<repo>/skills/motion-site-builder/scripts/server.py"]
    }
  }
}
```

You get `motion_list_profiles`, `motion_validate`, `motion_get_tokens`, `motion_get_template`, `motion_suggest_pattern`, `motion_easing_rationale`, `motion_find_reference`, `motion_validate_file`. Every taste-bearing tool takes an optional `profile` arg.

## 🧠 How It Works

Most AI-generated sites look generic because taste is left to chance. This repo turns taste into a **system**:

```
 Plan                    Build                      Validate
┌─────────────────┐    ┌──────────────────────┐    ┌────────────────────┐
│ pick archetype  │ →  │ adapt nearest of 92  │ →  │ 17-rule motion     │
│ palette, story  │    │ reference prompts +  │    │ linter → score,    │
│ motion patterns │    │ verbatim primitives  │    │ grade, fix loop    │
└─────────────────┘    └──────────────────────┘    └────────────────────┘
```

- **Retrieval over generation** — the skill finds the closest existing prompt and adapts values instead of hallucinating structure.
- **Verbatim primitives** — signature CSS (`liquid-glass`, `text-glow`, seamless video crossfade, rAF+lerp parallax) is pasted exactly, never paraphrased.
- **Deterministic quality gate** — the linter scores every file 0–100; errors block, warnings advise.

## 🎨 The Design DNA — five profiles

The engine ships **five design languages** — pick one, and the linter + tools enforce *that* taste (`motion_list_profiles`, then a `profile` arg). Full guide: [design-profiles.md](skills/motion-site-builder/references/design-profiles.md).

| Profile | For | Signature |
|---|---|---|
| **cinematic** *(default)* | hero, landing, launch | video-first, glass, serif, 1 accent, entrances 0.5–1.2s |
| **product-ui** | dashboard, SaaS, admin | crisp, fast (<250ms), light+dark, semantic multi-accent |
| **editorial** | blog, docs, articles | typography-first, prose, restrained motion |
| **playful** | consumer, creative, events | vibrant multi-accent, bouncy springs, decorative color |
| **ecommerce** | storefront, product page | imagery-first, snappy, quick-view, brand+neutral |

Good motion *feel* (reduced-motion, GPU-only, press feedback, no `ease-in` on UI) is universal across all five; the tempo, palette, and typography vary per profile.

### Cinematic (the default) — the signature elements the linter and tokens enforce:

| Signature | What it means |
|---|---|
| Fullscreen video background | media is the canvas; UI stays quiet on top |
| Explicit z-index layering | depth via layering (video 0 → overlay 1 → content 10 → nav 20), never WebGL |
| `rounded-full` pill UI | glass pills for nav and buttons |
| Negative tracking on display type | tight, editorial headlines |
| Glassmorphism (`backdrop-blur`) | the `liquid-glass` surface primitive |
| Instrument Serif + Inter pairing | serif display over a clean sans body |
| Signature easing `cubic-bezier(0.16, 1, 0.3, 1)` | expo-out on entrances |

Full guidelines: [motion-design-dna.md](skills/motion-site-builder/references/motion-design-dna.md). **Everything is customizable** — all taste lives in one JSON file: [customization guide](skills/motion-site-builder/README.md#customize-the-whole-point).

## 📁 Repository Structure

```
prompts/                      # the library — one .md per prompt (all original)
skills/motion-site-builder/   # the engine (build)
  SKILL.md                    #   agent workflow (entry point)
  references/                 #   design profiles, DNA, interaction standards, catalog
  config/motion-tokens.json   #   cinematic taste (default profile)
  config/profiles/*.json      #   product-ui · editorial · playful · ecommerce
  data/prompt-index.json      #   generated corpus index
  scripts/                    #   linter · index builder · MCP server (all zero-dep Python)
skills/review-motion/         # strict diff review (Before/After table + Block/Approve)
skills/improve-motion/        # codebase audit → self-contained plans (SKILL + AUDIT + PLAN-TEMPLATE)
site/                         # cinematic landing page — dogfooded from its own prompt
examples/                     # profile dogfoods (e.g. product-ui-dashboard — 100/A+ under product-ui)
docs/                         # getting started, prompt guidelines, architecture
```

`review-motion` and `improve-motion` are *method* skills — they reuse the builder's linter, tokens, and standards rather than duplicating them.

## 📚 Documentation

- [Getting Started](docs/getting-started.md) — all three usage paths in detail
- [Prompt Guidelines](docs/prompt-guidelines.md) — how to write and submit a prompt
- [Architecture](docs/architecture.md) — how the skill, linter, index, and MCP server fit together
- [Skill README](skills/motion-site-builder/README.md) — customize & extend the engine

## 🤝 Contributing

Prompts, lint rules, and primitives are all welcome — see [CONTRIBUTING.md](CONTRIBUTING.md). The short version:

1. Add your prompt to `prompts/` following the [guidelines](docs/prompt-guidelines.md).
2. Run `python3 skills/motion-site-builder/scripts/build_index.py` to re-index.
3. Run `python3 skills/motion-site-builder/scripts/lint_motion.py --self-test` if you touched the engine.
4. Open a PR — CI runs the same checks.

## ⚖️ License & Provenance

- **Everything in this repo — code, skill, linter, docs, landing page, and all 54 prompts**: [MIT](LICENSE).
- **Original prompts**: every prompt is authored from this project's own design profiles and motion DNA. No brand replicas, no copied copy, and no hardcoded third-party assets — media is referenced as placeholders you fill in.
- **Bring your own media**: supply footage/images you have rights to (your own, or royalty-free sources such as Pexels, Coverr, or Unsplash under their licenses). All fonts are open-licensed (Google Fonts / OFL).

---

<div align="center">
Made with an unhealthy obsession for <code>cubic-bezier(0.16, 1, 0.3, 1)</code>
</div>
