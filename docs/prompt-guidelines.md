# Prompt Guidelines

How to write a prompt worthy of the library. The full formula lives in the skill's [prompt-writing guide](../skills/motion-site-builder/references/prompt-writing-guide.md) — this page is the contributor-facing contract.

## The Standard

A library prompt is a **spec, not a wish**. It must generate a near-identical result on any capable AI builder, one-shot. That means:

### 1. Structure (fixed order)

```
<ONE imperative sentence: what to build + exact stack>

FONTS → COLORS → GLOBAL CSS → <sections top-to-bottom> → ANIMATIONS → RESPONSIVE → CONSTRAINTS
```

Full Landing prompts add: `SECTION ORDER`, `REUSABLE COMPONENTS`, `KEY DEPENDENCIES` (pinned versions).

### 2. Absolute values only

| ❌ Reject | ✅ Accept |
|---|---|
| "a large elegant serif headline" | `text-5xl md:text-8xl, tracking-tight, leading-[0.95], fontFamily: 'Instrument Serif'` |
| "smooth entrance animation" | `fade-up 0.8s cubic-bezier(0.16,1,0.3,1), stagger: H1 0s · subtext 0.25s · CTA 0.4s` |
| "a nice dark background" | `--background: #0C0C0C` |
| "add a call to action" | `CTA (bg-white text-black rounded-full px-8 py-3.5): "Start Free Trial"` |

Copy is part of the spec — headline, subtext, and CTA labels appear verbatim.

### 3. Primitives are pasted, never described

If your prompt uses `liquid-glass`, `text-glow`, or entrance keyframes, include the CSS block verbatim from the [component catalog](../skills/motion-site-builder/references/component-catalog.md).

### 4. The quality bar (higher than the source corpus)

Every submission must include:

- `prefers-reduced-motion` handling (the catalog's boilerplate is fine)
- ARIA labels on nav and icon-only buttons; `aria-hidden` on decorative video
- A `poster` fallback on background videos
- Only `transform` / `opacity` / `filter` in animations
- A closing `CONSTRAINTS` block (no extra UI libraries, no decorative blobs over video, etc.)

### 5. Legal hygiene

- Media URLs: your own assets or `{YOUR_VIDEO_URL}` placeholders. No hotlinks to assets you don't control.
- No recreations of existing brands (names, logos, trade dress, mascots, or exact product UIs). Use original, fictional brands and original copy.
- Fonts must be open-licensed (Google Fonts / OFL). No hotlinking commercial fonts from font-piracy mirrors.

## File Conventions

- Location: `prompts/`
- Name: `brand-or-concept-type.md` — kebab-case, e.g. `lumen-wellness-hero.md`
- First line: `# <Display Name>` (used by the index builder)

## Submission Flow

```bash
# 1. add your file, then re-index
python3 skills/motion-site-builder/scripts/build_index.py

# 2. sanity-check any embedded CSS/JSX
python3 skills/motion-site-builder/scripts/lint_motion.py <snippet-file>

# 3. add a row to prompts/README.md, open a PR
```

Self-review with the [SKILL.md polish checklist](../skills/motion-site-builder/SKILL.md#polish-checklist-every-page) before submitting. If any adjective in your prompt has no number attached, fix it — that's the whole game.
