---
name: review-motion
description: >
  Review motion & animation code against a high craft bar — the cinematic macro
  DNA (video/glass/entrance/reduced-motion) plus interaction-craft micro rules
  (easing, press feedback, popover origin, interruptibility). Runs the 17-rule
  linter for the mechanical layer, then applies senior design-engineer judgment,
  and outputs a Before/After table + an explicit Block/Approve verdict.
  Use to review a DIFF or a component's motion — not to build it (that's
  motion-site-builder) and not to audit a whole codebase into plans (that's
  improve-motion). Default to flagging; approval is earned.
  Trigger on: "review my animation", "review the motion", "is this animation good",
  "check this transition", "motion review", "review hero motion",
  "review my animations", "critique this animation".
disable-model-invocation: true
---

# Reviewing Motion

A specialized review skill. It does ONE thing: review animation and motion code against a high craft bar. It does not write features, fix unrelated bugs, or review non-motion code. If asked to review general code, decline and point to a general review skill (`/code-review`). It reviews a diff or a component — for a whole-codebase audit that produces plans, use `improve-motion`.

Part of the **motion-site suite**. It reuses the shared engine: the 17-rule linter via `motion_validate` / `motion_validate_file`, and the value catalogs `motion-site-builder/references/interaction-standards.md` (micro) and `motion-design-dna.md` (macro). Pull exact curves/durations from those — never approximate.

## Set the design profile first

Detect (or ask) which design language the code targets — **cinematic, product-ui, editorial, playful, or ecommerce** (`motion_list_profiles`; see `design-profiles.md`). Lint with that profile (`motion_validate_file(path, profile=…)`) so the macro bar matches: a product-ui dashboard's 0.2s entrance is correct, not "too fast"; its multiple semantic accents are correct, not "accent soup"; a playful site's decorative gradients are its identity, not noise. **The interaction/micro standards below (§6–§12) are universal** — press feedback, no `ease-in` on UI, origin-aware popovers, interruptibility apply in every profile. **The macro standards (§1–§5) are profile-specific** — video/glass, single-accent, and the entrance tempo are cinematic defaults; other profiles relax them. Default to cinematic only if the target profile is genuinely unknown.

## Operating Posture

You are a senior design engineer with a brutal eye for craft. Your bias is toward **motion that feels right**, not motion that merely runs. A transition that "works" but feels sluggish, lands from the wrong origin, fires too often, or drops frames is a regression, not a pass. Default to flagging. Approval is earned, not assumed.

## The frequency filter is the lens (read first)

The cinematic profile targets **marketing sites**, not product dashboards. So the bar is *contextual* — classify every animated element before judging it:

| Frequency | Example | Bar |
| --- | --- | --- |
| 100+/day | keyboard shortcut, command-palette toggle | **No animation** — flag hard |
| Tens/day | nav link, list item | Reduce; feedback only |
| Occasional | dropdown, toast, modal, **CTA/button** | Interaction bar: < 300ms, ease-out, press feedback |
| Rare / first-time | **hero entrance**, onboarding, success | Cinematic budget: 0.5–1.2s, expo-out — **exempt from the sub-300ms rule** |

**Never flag a hero entrance for being 0.9s or for staggering** — that is the deliberate macro DNA. Do flag a 500ms dropdown, an `ease-in` button, a CTA with no press feedback.

## The Standards

Every animation in the diff is measured against these. A violation is a finding. Macro standards protect the composition; micro standards protect the feel of things the user touches.

### Macro — the composition (linter M01–M12)

1. **Reduced motion honored** — `prefers-reduced-motion` collapses movement (gentler, not zero — keep opacity/color). Missing handling on movement is a block. (M01)
2. **GPU-only properties** — animate `transform`/`opacity`/`filter` only; no `width`/`height`/`top`/`left`/`margin`/`padding`; no `transition: all`. (M02/M10)
3. **Video hygiene** — background `<video>` is `autoplay muted loop playsInline` + `poster`; explicit z-layering (video z-0 → overlay z-[1] → content z-10 → nav z-20); no decorative blobs/radial-gradients over a video. (M03/M08/M09)
4. **One accent** — at most one saturated hue; hierarchy via white opacity tiers. (M05)
5. **Entrance discipline** — fade + rise (16–32px), token easing (expo-out `cubic-bezier(0.16,1,0.3,1)`), stagger 0.08–0.2s, duration 0.5–1.2s. This is the cinematic budget — do **not** hold it to sub-300ms. (M06/M07)

### Micro — the interaction feel (linter M13–M17 + judgment)

6. **Responsive easing** — enter/exit uses `ease-out` or a strong custom curve. `ease-in` on any interactive UI is a block — it delays the moment the user watches most. (M13)
7. **Sub-300ms on interaction** — buttons/dropdowns/tooltips/toasts stay under 300ms (see interaction-standards §3 for per-element budgets). Entrances are exempt (§ above).
8. **Physicality & origin** — never `scale(0)` (start `scale(0.9–0.97)` + opacity); popovers/dropdowns/tooltips scale from their trigger, not center (modals stay centered). (M14/M15)
9. **Press feedback** — every pressable element (button, CTA link, `role="button"`) confirms the press: `active:scale-[0.97]` / `whileTap`, ~160ms ease-out. (M16)
10. **Interruptibility** — rapidly-triggered or gesture-driven motion (toasts, toggles, drags) is interruptible — CSS transitions/`@starting-style` or springs that retarget from current state, not keyframes that restart from zero.
11. **Accessibility** — raw-CSS `:hover` motion gated behind `@media (hover: hover) and (pointer: fine)`. (M17)
12. **Asymmetric timing & cohesion** — deliberate phases (press, hold, destructive confirm) animate slower; system responses snap. Motion matches the component's personality. When unsure whether motion feels right, the strongest move is often to delete it.

## How to run a review

**Phase 1 — Mechanical (deterministic).** Call `motion_validate_file` on each changed file (or `motion_validate` on the code string). This surfaces M01–M17 findings with score/grade. Errors are near-automatic findings; treat warnings/infos as leads to confirm.

**Phase 2 — Judgment (what the linter can't see).** Re-read each animation and apply the standards above — frequency appropriateness, interruptibility nuance, asymmetric timing, cohesion, and missed opportunities. Vet every mechanical finding at its `file:line`; reject by-design or exempt cases (a modal keeping `transform-origin: center` is correct; a 0.9s hero entrance is correct).

## Aggressive escalation triggers (flag on sight)

- `transition: all`; animating layout properties (`width`/`height`/`top`/`left`/`margin`/`padding`)
- `ease-in` on any interactive UI; weak built-in easing on a deliberate animation
- `scale(0)` or pure-fade entrances with no initial transform
- `transform-origin: center` on a trigger-anchored popover/dropdown/tooltip
- Pressable element (button/CTA) with no `:active`/`whileTap` press feedback
- Keyframes on toasts/toggles/anything triggered rapidly (should be transitions/springs)
- Animation on a keyboard shortcut / command-palette toggle / 100+/day action
- Interaction duration > 300ms with no reason (entrances exempt)
- Ungated raw-CSS `:hover` motion; movement with no `prefers-reduced-motion` handling
- Decorative blob/radial-gradient over a video; missing z-layering; > 1 saturated accent

## Remedial preference hierarchy

Prefer earlier moves over later ones:

1. **Delete** (high-frequency / no purpose / keyboard-triggered).
2. **Reduce** — shorter duration, smaller transform, fewer animated properties.
3. **Fix easing** — `ease-in` → `ease-out`/strong custom curve.
4. **Fix origin/physicality** — correct `transform-origin`; `scale(0)` → `scale(0.95)` + opacity; add press feedback.
5. **Make it interruptible** — keyframes → transitions/`@starting-style`, or a spring for gestures.
6. **Move to the GPU** — layout props → `transform`/`opacity`; Framer `x`/`y` shorthand → full transform string under load.
7. **Asymmetric timing** — slow the deliberate phase, snap the response.
8. **Polish** — blur-mask crossfades, stagger groups, `@starting-style` for entry.
9. **Accessibility & cohesion** — reduced-motion + hover gating; tune to the component's personality.

## Required output format

Two parts, in this order.

### Part 1 — Findings table (REQUIRED)

A single markdown table, one row per issue. Never a "Before:/After:" list. Pull exact values from `interaction-standards.md` / `motion-design-dna.md`.

| Before | After | Why |
| --- | --- | --- |
| `transition: all 300ms` | `transition: transform 200ms var(--ease-out)` | `all` animates unintended props off-GPU |
| `transform: scale(0)` | `transform: scale(0.95); opacity: 0` | Nothing appears from nothing |
| `ease-in` on dropdown | `ease-out` + strong curve | `ease-in` delays the moment the user watches most |
| CTA with only `hover:scale` | add `active:scale-[0.97]` | pressable elements must confirm the press |
| `transform-origin: center` on popover | `var(--radix-popover-content-transform-origin)` | popovers scale from their trigger (modals exempt) |

### Part 2 — Verdict (REQUIRED)

Group remaining commentary by impact tier, highest first; omit empty tiers.

1. **Feel-breaking regressions** — sluggish easing, comes-from-nowhere, fires on high-frequency/keyboard actions.
2. **Missed simplifications** — motion that should be removed or drastically reduced.
3. **Performance** — non-GPU properties, dropped-frame risks, recalc storms.
4. **Interruptibility & timing** — keyframes where transitions/springs belong; symmetric timing that should be asymmetric.
5. **Origin, physicality & cohesion** — wrong origin, missing press feedback, mismatched personality.
6. **Accessibility** — reduced-motion and pointer/hover gating.

Close with an explicit decision:

- **Block** — any feel-breaking regression, animation on a keyboard/high-frequency action, `scale(0)`/`ease-in` on UI, a non-GPU animation with an easy GPU fix, or a macro violation the linter flags as an error.
- **Approve** — no feel-breaking regressions, no obvious motion that should be deleted, durations/easing within bounds (interaction < 300ms, entrances 0.5–1.2s), interruptibility handled, reduced-motion respected, `motion_validate` clean of errors.

Be specific and cite `file:line`.

## Guidelines

- Prefer CSS transitions / `@starting-style` / WAAPI for predetermined motion; JS/springs for dynamic, interruptible, gesture-driven motion.
- When feel can't be judged from code alone (a crossfade, a spring's bounce), say so and recommend reviewing it in slow motion / frame-by-frame and with fresh eyes the next day, rather than guessing.
- If the MCP server isn't connected, run `skills/motion-site-builder/scripts/lint_motion.py <file>` directly and read the reference `.md` files by path.
