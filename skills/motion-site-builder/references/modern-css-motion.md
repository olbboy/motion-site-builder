# Modern CSS Motion — Zero-Dependency Techniques

Native CSS features that replace JS for common motion jobs. They fit this project's anti-bloat stance better than adding libraries — but each needs a `@supports` gate and a working fallback, because support is recent. Verify support before making one load-bearing; treat everything here as **progressive enhancement** over the two established scroll schools (motion-design-dna §6).

## 1. Scroll-driven animations (`animation-timeline`) — the third scroll school

Scroll-linked animation with zero JS, running off the main thread:

```css
/* Reading progress bar */
@supports (animation-timeline: scroll()) {
  .progress { animation: grow linear; animation-timeline: scroll(root block); transform-origin: left; }
  @keyframes grow { from { transform: scaleX(0); } to { transform: scaleX(1); } }
}

/* Reveal on viewport entry — replaces whileInView / IntersectionObserver for simple cases */
@supports (animation-timeline: view()) {
  .reveal {
    animation: fade-rise linear both;
    animation-timeline: view();
    animation-range: entry 0% entry 100%;   /* ranges: cover | contain | entry | exit */
  }
}
```

- Use `scroll()` for progress-linked, `view()` for enter-viewport effects. Named ranges (`entry`, `exit`, `cover`, `contain`) scope where along the scroll the keyframes map.
- **Fallback rule**: outside the `@supports` block the element must be fully visible and static — never hidden-by-default (a no-support browser would show nothing). Same discipline as the JS schools: only `transform`/`opacity`/`filter` in the keyframes. A scroll timeline is progress-driven, so the global `animation-duration: 0.01ms` boilerplate does **not** disable it; explicitly detach optional timelines under reduced motion:
  ```css
  @media (prefers-reduced-motion: reduce) {
    .progress, .reveal { animation: none; animation-timeline: none; }
  }
  ```
- **School discipline still holds — pick ONE scroll school per page.** This is now a three-way choice: Framer `useScroll`/`whileInView`, hand-rolled rAF+lerp, or CSS `animation-timeline`. CSS wins for simple reveals/progress on content pages (editorial especially); the JS schools win when scroll drives interdependent values (sticky-stack scale math, parallax layers).

## 2. View Transitions API (route/state swaps)

```js
// Same-document (SPA state/route change)
if (document.startViewTransition) {
  document.startViewTransition(() => updateDOM());
} else {
  updateDOM();
}
```

```css
::view-transition-old(root) { animation-duration: 150ms; }
::view-transition-new(root) { animation-duration: 250ms; }
.card { view-transition-name: card-3; }   /* shared-element morph between states */
```

- Feature-detect (`document.startViewTransition`) and always call the DOM update in the else branch — the transition is decoration, the update is the job.
- `view-transition-name` must be unique per element per state; it gives FLIP-style shared-element morphs without Framer `layoutId`.
- Scope: state/route swaps only. Entrances, hovers, popovers keep their existing patterns — don't route everything through view transitions.

## 3. `linear()` easing — springs in pure CSS

CSS transitions can't take spring physics, but `linear()` approximates a spring curve with sampled points:

```css
.pop {
  transition: transform 500ms linear(0, 0.009, 0.035 2.1%, 0.141 4.4%, 0.723 12.9%,
    0.938 16.7%, 1.017, 1.077 20.4%, 1.121, 1.149 24.3%, 1.159, 1.163 27%, 1.154,
    1.017 43.1%, 0.991, 0.977 51%, 0.974 53.8%, 0.975 57.1%, 0.997 69.8%, 1.003 76.9%, 1);
}
```

Generate the point list from a spring config (stiffness/damping) with a linear-easing generator tool; keep the generated comment noting the source config. Use only where a spring is genuinely wanted *and* Framer isn't already on the page — otherwise use the profile's cubic-bezier tokens (simpler, reviewable).

## 4. `@property` — animating custom properties

Registering a custom property gives it a type, making it interpolable (gradients, angles, numeric counters):

```css
@property --glow-angle { syntax: "<angle>"; inherits: false; initial-value: 0deg; }
.button { background: conic-gradient(from var(--glow-angle), …); transition: --glow-angle 600ms var(--ease-out); }
```

Use sparingly (decorative accents, rare moments). The interaction-standards §8 caveat still applies: don't drive many children off one animated parent variable — style recalc fans out.

## 5. Anchor positioning (popovers without a positioning library)

```css
.trigger { anchor-name: --menu-trigger; }
.menu {
  position: fixed;
  position-anchor: --menu-trigger;
  top: anchor(bottom); left: anchor(left);
  position-try-fallbacks: flip-block, flip-inline;
}
```

Positions a popover off its trigger natively (what Floating UI/Radix do in JS), with automatic flip fallbacks. The M15 origin rule still applies — the popover *scales from* the anchored edge. In React projects already using Radix, keep Radix; this is for the plain-HTML/CSS archetypes.

## 6. Container-query motion

`@container (min-width: 400px) { .card-art { animation: … } }` — gate a decorative animation on the *component's* size, not the viewport. Useful for cards that appear in both a sidebar and a full-width grid: small placements skip the motion.

## 7. Rendering-cost table (why the M02 rule is shaped the way it is)

| Property group | Cost | Pipeline |
| --- | --- | --- |
| `transform`, `opacity` | Low | composite only (GPU) |
| `filter`, `backdrop-filter` | Medium | GPU, but blur cost scales with radius — keep transition-time blur < 20px (Safari especially) |
| `clip-path` | Medium | GPU-composited in modern engines; fine for reveals |
| `background`, `box-shadow`, `color` | High | repaint — acceptable on small elements, avoid on large surfaces |
| `width`, `height`, `top/left`, `margin`, `padding` | Highest | reflow + repaint — **never animate** (M02) |

This is also the performance rationale for glassmorphism budgets: `backdrop-filter` is GPU-friendly but not free — the 4–12px blur budget (motion-design-dna §4) keeps it in the cheap zone.

---

**Adoption checklist** (any feature above): ① wrapped in `@supports`/feature-detect with a static-but-complete fallback · ② keyframes/transitions stay on the GPU property set · ③ reduced-motion explicitly disables optional scroll timelines (`animation-timeline: none`) · ④ still passes `motion_validate` — the linter's rules apply to CSS regardless of which API drives it.
