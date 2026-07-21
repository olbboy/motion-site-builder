# Motion Audit Playbook

The eight audit categories, what to hunt for in each, and where the exact target values live. **Values are delegated, not duplicated** — pull curves/durations/spring configs from `motion_get_tokens` and `../motion-site-builder/references/interaction-standards.md` (micro) / `../motion-site-builder/references/motion-design-dna.md` (macro). Never approximate a value that appears there — copy it.

The linter (`motion_validate_file`, rules M01–M20) covers the mechanical subset; run it first. This playbook is for the judgment the linter can't make.

## 1. Purpose & frequency

Every animation must answer "why does this animate?" — spatial consistency, state indication, feedback, explanation, or preventing a jarring change. "It looks cool" on a frequently-seen element is not a purpose.

| Frequency | Example | Decision |
| --- | --- | --- |
| 100+/day | keyboard shortcut, command-palette toggle | No animation. Ever. |
| Tens/day | nav link, list item hover | Remove or drastically reduce |
| Occasional | dropdown, toast, modal, CTA | Standard interaction animation |
| Rare / first-time | **hero entrance**, onboarding, success | Cinematic budget — delight allowed |

Hunt for: animation on keyboard-initiated actions, decorative motion on constantly-seen list/hover states. **Do not flag hero entrances for length or stagger** — that is the deliberate DNA. Strongest fix is often **delete the animation**.

## 2. Easing & duration

Easing decision order: enter/exit → `ease-out`; move/morph → `ease-in-out`; hover/color → `ease`; constant → `linear`. **`ease-in` on interactive UI is always a finding** (M13) — built-in CSS easings are too weak for deliberate motion. Values: interaction-standards.md §2.

Duration: **interaction elements < 300ms** (per-element budgets in interaction-standards.md §3). **Hero entrances 0.5–1.2s are exempt** — flagging them is the naive-port trap.

Hunt for: `ease-in` on buttons/dropdowns/toasts, interaction durations > 300ms, tooltip delay + animation on every tooltip in a toolbar (after the first, instant).

## 3. Physicality & origin

- **Never `scale(0)`** (M14) → `scale(0.9–0.97)` + `opacity: 0`.
- **Popovers/dropdowns/tooltips scale from their trigger** (M15), not center (`transform-origin: var(--radix-...-transform-origin)` / `var(--transform-origin)`). **Modals exempt** — centered is correct.
- **Press feedback** (M16): `active:scale-[0.97]` / `whileTap`, ~160ms ease-out, on every button/CTA link.

Hunt for: `scale(0)`, pure-fade entrances with no initial transform, `transform-origin: center` on trigger-anchored elements, CTAs/buttons with hover motion but no press feedback.

## 4. Interruptibility

CSS **transitions** retarget from the current state; **`@keyframes`** restart from zero. Anything triggered rapidly or reversible (toasts stacking, toggles, drags, expand/collapse) must use transitions/`@starting-style` or springs.

Hunt for: `@keyframes` on toasts/toggles/rapidly-triggered UI, gesture handlers that tween with fixed-duration keyframes, drags without velocity-based dismissal (`Math.abs(distance)/elapsedMs > ~0.11`), hard stops at drag boundaries instead of rising friction. Values: interaction-standards.md §5, §11.

## 5. Performance

- Animate **`transform`/`opacity`/`filter` only** — no `width`/`height`/`margin`/`padding`/`top`/`left` (M02).
- **`transition: all`** animates unintended props off-GPU (M10).
- **Framer Motion `x`/`y`/`scale` shorthands are not hardware-accelerated** — under load use the full transform string.
- Don't drive child transforms via a CSS variable on the parent (recalcs all children).
- **Macro hygiene:** background `<video>` needs `autoplay muted loop playsInline` + `poster` (M03); explicit z-layering (M09); no decorative blob/radial-gradient over video (M08).

Hunt for: `transition: all`, animated layout props, Framer shorthand on busy pages, `setProperty('--x', …)` driving child transforms, `<video>` missing attrs/poster, missing z-index on a video stack.

**If the codebase uses WebGL/Three.js** (`<canvas>`, `THREE.*`, `@react-three/fiber`) — the suite never *introduces* WebGL, but audits it where it exists: check `dispose()` on geometries/materials/textures + `renderer.dispose()` when the component/route unmounts (memory leaks), `setPixelRatio(Math.min(devicePixelRatio, 2))`, the render loop pausing when the tab is hidden and under `prefers-reduced-motion` (stop camera parallax/particles — most Three.js code ships without this), and a static-image fallback on WebGL context loss.

**If the codebase uses GSAP** — audit with the checklist in `../motion-site-builder/references/gsap-interop.md`: missing `useGSAP`/`ctx.revert()` cleanup, ScrollTrigger on nested tweens, `scrub`+`toggleActions` together, non-`none` ease on `containerAnimation`, `markers: true` in production, no `gsap.matchMedia()` reduced-motion branch.

## 6. Accessibility

Reduced motion = fewer and gentler, **not zero** — keep opacity/color that aids comprehension, drop movement (M01). Gate raw-CSS `:hover` motion behind `@media (hover: hover) and (pointer: fine)` (M17) — touch fires false hovers.

Hunt for: movement with no `prefers-reduced-motion` handling, ungated `:hover` motion, reduced-motion implementations that nuke all feedback, `<video>` without `aria-hidden`, icon-only buttons/nav without `aria-label`.

## 7. Cohesion & tokens

- Motion matches the product's personality — a cinematic marketing site is quiet and premium; a playful app can be bouncier. Mismatched personality across components is a finding.
- Curves/durations should live as shared tokens. Five hand-typed cubic-beziers that almost match is a consolidation finding (M07 flags non-token curves).
- One saturated accent max (M05); hierarchy via white opacity tiers.
- Everything-at-once group entrances where a **30–80ms stagger** belongs. A crossfade that double-exposes can be masked with `filter: blur(2px)`.

Hunt for: duplicated near-identical easings/durations, one bouncy component in a quiet site, > 1 accent hue, list/grid entrances with no stagger, crossfades that visibly double-expose.

**Drift inventory (cross-file, what a per-file lint can't see):** run `python3 skills/motion-site-builder/scripts/audit_consistency.py <src-dir>` from this repository, or resolve the script from the installed builder skill root. It inventories literal durations, easing/cubic-bezier values, and spring configs across the codebase with counts and locations. More than ~8 distinct duration values or ~5 distinct off-token easing curves is a consolidation lead; entrances that pop out with no exit (conditional renders without `AnimatePresence`/`@starting-style`) surface here too. Name findings with the troubleshooting vocabulary (`../motion-site-builder/references/troubleshooting.md`): "looks robotic", "feels cheap", "too distracting", "no personality".

## 8. Missed opportunities

The additive category — places that don't animate but should (report at most a handful, grounded in real UX seams):

- State changes that teleport (content swaps, layout jumps) where a brief transition would prevent a jarring change.
- Spatially-connected UI (a panel from a trigger) with no motion explaining where it came from.
- Rare, high-emotion moments (first-run, success, celebration) rendered with none of their delight budget.
- `translateY(100%)` (element's own height) and `clip-path: inset()` reveals as the tools for these — no hardcoded pixel offsets.
