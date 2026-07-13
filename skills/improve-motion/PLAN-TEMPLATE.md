# Plan Template

Every plan written by `improve-motion` follows this structure. The executor may be a less capable model with zero context and zero taste — the plan must contain everything, exactly. No references to "the audit above" or "the easing we discussed."

````markdown
# NNN — <Short imperative title>

- **Status**: TODO
- **Commit**: <output of `git rev-parse --short HEAD` when this plan was written>
- **Severity**: HIGH | MEDIUM | LOW
- **Category**: <audit category>
- **Layer**: macro (composition) | micro (interaction)
- **Estimated scope**: <n files, rough size>

## Problem

What is wrong, where, and why it matters to how the product feels. Cite every
location as `path/to/file.tsx:123` and include the current code verbatim:

```css
/* src/components/dropdown.css:14 — current */
.dropdown { transition: all 400ms ease-in; transform-origin: center; }
```

## Target

The exact end state. Every value spelled out — curves, durations, spring configs,
media queries. Pull from `motion_get_tokens` / interaction-standards.md. Never
"use a nicer easing":

```css
/* target */
.dropdown {
  transition: transform 200ms var(--ease-out), opacity 200ms var(--ease-out);
  transform-origin: var(--radix-dropdown-menu-content-transform-origin);
}
```

## Scope guard (cinematic macro DNA)

State explicitly whether this touches interaction or the hero/cinematic layer.
Interaction elements target < 300ms + ease-out + press feedback; hero entrances
KEEP the 0.5–1.2s expo-out budget — do not shorten them. If the target would
shorten a hero entrance, STOP: it is out of scope.

## Repo conventions to follow

How this codebase already does it, with one exemplar to imitate (token names,
file placement, prop patterns):

- Easing tokens live in `<file>`; add new curves there.
- <exemplar file:line that already does this correctly>

## Steps

1. <One concrete edit per step: file, what changes, resulting code.>
2. …

## Boundaries

- Do NOT touch <files/components out of scope>.
- Do NOT change markup/structure — motion properties only (unless a step says otherwise).
- Do NOT add new dependencies (achieve springs with the whitelisted `framer-motion`/`motion`).
- If a step doesn't match the code you find (drift since the commit stamp), STOP and report instead of improvising.

## Verification

- **Mechanical**: run `motion_validate` (or `python3 skills/motion-site-builder/scripts/lint_motion.py <file>`) on each changed file — the targeted rule(s) must clear and the file must not drop below its prior score.
- **Feel check**: run the UI, trigger <interaction>, and confirm:
  - <observable check, e.g. "the dropdown scales from its trigger, not from center">
  - <e.g. "spamming the toggle never restarts the animation from zero">
  - In DevTools, set playback to 10% (Animations panel) and confirm <detail>.
  - Toggle `prefers-reduced-motion` (Rendering panel) and confirm movement is dropped but opacity feedback remains.
- **Done when**: <machine- or eye-checkable completion criteria>.
````

## Notes for the plan author

- One plan per finding. Two findings that share every file and the same fix pattern (e.g. the same easing-token swap across components) may merge into one plan.
- Pull every value from `motion_get_tokens` / [AUDIT.md](AUDIT.md) → interaction-standards.md — never approximate from memory.
- The feel check is not optional. Motion can be mechanically correct and still feel wrong; give the executor concrete things to watch for in slow motion.
- After writing plans, create or update `plans/README.md` with: a table of plans (number, title, severity, layer, status), the recommended execution order, and any dependencies.
