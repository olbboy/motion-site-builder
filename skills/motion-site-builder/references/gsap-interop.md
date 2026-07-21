# GSAP Interop — When the Host Project Already Uses It

GSAP stays on the default `dependencies.forbidden` list — the builder never *introduces* it. But two suite skills legitimately meet GSAP in the wild: the builder's pre-flight scan (SKILL.md Step 0.5 detects `gsap`/`lenis` in deps) and `improve-motion`/`review-motion` auditing an existing codebase. This reference is the behavior contract for those encounters, plus the idioms needed to judge (or extend) GSAP code correctly instead of flagging it blindly.

## Behavior contract

- **Builder, pre-flight finds `gsap` in deps** → GSAP is that project's established scroll school. Respect it: extend the project's existing GSAP conventions for scroll work instead of introducing Framer as a *second* scroll library (the "one school per page" rule generalizes to "one scroll library per project"). All taste rules (tokens, easing values, durations, M-rules) still apply — GSAP is an engine, not an exemption.
- **improve-motion / review-motion meet GSAP code** → audit it with the checklist below; don't file "uses GSAP" itself as a finding when it predates the audit. Do file a finding if GSAP was added for something CSS/Framer already on the page does (duplicate motion stacks).
- **User explicitly asks for GSAP on a greenfield build** → surface the conflict with the profile's forbidden list once; if they confirm, they own the config change (`dependencies.allowed` in their profile JSON — the documented extension point). Then follow the idioms below.

## React lifecycle (the #1 leak source)

```jsx
import { useGSAP } from "@gsap/react";
gsap.registerPlugin(useGSAP);

function Section() {
  const container = useRef(null);
  const { contextSafe } = useGSAP(() => {
    gsap.from(".card", { y: 24, opacity: 0, stagger: 0.08 });  // selector scoped below
  }, { scope: container });                                     // ← always scope
  const onHover = contextSafe(() => gsap.to(".icon", { rotate: 8 })); // handler-created tweens
  return <div ref={container}>…</div>;
}
```

- **`useGSAP` + `scope`** replaces `useEffect` — auto-reverts every tween/ScrollTrigger on unmount, and scopes string selectors to the component subtree (unscoped `".card"` animates strangers).
- Tweens created inside event handlers must be wrapped in **`contextSafe`** or they escape the context and never get cleaned up.
- Without `@gsap/react`: `const ctx = gsap.context(() => {…}, ref); return () => ctx.revert();`.
- **SSR**: no `gsap.*`/`ScrollTrigger.*` at module top level or during render — client-only effects.

## ScrollTrigger correctness checklist

- **`scrub` XOR `toggleActions`** — scroll-linked progress or discrete play/reverse, never both on one trigger.
- **ScrollTrigger goes on the timeline or a top-level tween** — never on a tween nested inside a timeline (it silently misbehaves).
- Horizontal-scroll sections (`containerAnimation`): the parent tween driving the scroll **must use `ease: "none"`** — any other ease desyncs child triggers.
- Create triggers in top-to-bottom page order, or set `refreshPriority`; call `ScrollTrigger.refresh()` after layout-affecting DOM changes.
- **Route change/unmount**: `ScrollTrigger.getAll().forEach(t => t.kill())` (or rely on `useGSAP` revert). Stale triggers on dead elements are the classic SPA bug.
- `ScrollTrigger.batch()` replaces per-item IntersectionObserver for grid reveals (stagger the batch, not 50 separate triggers).
- Sequenced `gsap.from()` tweens hitting the same property need `immediateRender: false` on the later ones.
- No `markers: true` or `GSDevTools` in production code — audit finding.

## Performance & a11y idioms

- `gsap.quickTo(el, "x", { duration: 0.3 })` for high-frequency updates (mouse followers) — reuses one tween instead of allocating per event. The GSAP equivalent of this project's rAF+lerp primitive.
- Prefer GSAP transform props (`x`, `y`, `scale`, `rotation`) and `autoAlpha` (opacity + `visibility: hidden` at 0, so faded-out elements don't eat clicks) — same GPU discipline as M02.
- **Reduced motion**: `gsap.matchMedia()` with a `(prefers-reduced-motion: reduce)` condition is the canonical pattern — it reverts automatically when the setting flips. A GSAP codebase with no `matchMedia`/reduced-motion branch is an M01-equivalent finding.

## Audit greps (add to the improve-motion recon sweep when GSAP is detected)

```
grep -rn "gsap.from\|fromTo" --include="*.tsx" src/ | grep -v immediateRender   # sequenced-from overwrite risk (manual check)
grep -rn "scrollTrigger" src/ | grep -c ""                                      # trigger count — dozens ⇒ check for batch()
grep -rln "gsap" src/ | xargs grep -L "revert\|useGSAP\|context"                # files animating without cleanup
grep -rn "markers: *true\|GSDevTools" src/                                      # dev tooling left in
```
