# Interaction Standards — Micro-Motion Craft

Precise values for **interaction-level** motion (buttons, popovers, toasts, hover, gestures) — the layer that makes a site feel *premium* once the macro composition (video, glass, typography, entrances) is right. Cite these exact values in reviews and specs; never approximate.

Distilled from Emil Kowalski's design-engineering philosophy ([emilkowal.ski](https://emilkowal.ski/), [animations.dev](https://animations.dev/)). This project is not affiliated with or endorsed by Emil Kowalski.

> **Scope discipline — read first.** These rules govern **interactive elements**: things the user presses, hovers, opens, drags. They do **NOT** govern the hero entrance or scroll storytelling. A marketing hero is a *first-time / rare* moment (see the frequency table) and may legitimately run 0.5–1.2 s with expo-out — that is motion-site's macro DNA, and it stays. Do not apply "UI < 300 ms" or "when unsure, delete it" to hero entrances.

The lint rules **M13–M17** enforce the mechanically-checkable subset of this document; the rest is judgment the builder/reviewer applies.

---

## 1. Should it animate? (frequency → decision)

Every animation must answer *"why does this animate?"* — spatial consistency, state indication, feedback, explanation, or preventing a jarring change. "It looks cool" on a frequently-seen element is not a purpose.

| Frequency | Example | Decision |
| --- | --- | --- |
| 100+ / day | keyboard shortcut, command-palette toggle | **No animation. Ever.** |
| Tens / day | hover effects, list/nav item | Remove or drastically reduce |
| Occasional | modal, drawer, toast, dropdown | Standard interaction animation (values below) |
| Rare / first-time | onboarding, **hero entrance**, success, celebration | Delight allowed — motion-site's cinematic budget lives here |

Map each animated element to a row before tuning it. The strongest fix for a high-frequency animation is often to **delete it**.

## 2. Easing (rationale, not just tokens)

Decision order:

- Entering / exiting → **`ease-out`** (starts fast, feels responsive)
- Moving / morphing on screen → **`ease-in-out`**
- Hover / color change → **`ease`**
- Constant (marquee, progress, spinner) → **`linear`**
- Default → **`ease-out`**

**`ease-in` on any interactive UI is a finding (M13).** It starts slow, delaying the exact moment the user is watching — a dropdown with `ease-in` *feels* slower than the same duration with `ease-out`. Built-in CSS easings are weak; use strong custom curves. motion-site's tokens already qualify:

```css
--ease-out: cubic-bezier(0.16, 1, 0.3, 1);      /* expo-out — motion-site signature */
--ease-out-strong: cubic-bezier(0.23, 1, 0.32, 1);
--ease-in-out: cubic-bezier(0.77, 0, 0.175, 1); /* on-screen movement */
--ease-drawer: cubic-bezier(0.32, 0.72, 0, 1);  /* iOS-like drawer */
```

## 3. Duration (interaction elements stay < 300 ms)

| Element | Duration |
| --- | --- |
| Button press feedback | 100–160 ms |
| Tooltips, small popovers | 125–200 ms |
| Dropdowns, selects | 150–250 ms |
| Modals, drawers | 200–500 ms |
| **Hero entrance / marketing** | 0.5–1.2 s (macro DNA — exempt) |

A 180 ms dropdown feels more responsive than a 400 ms one. Config: `interaction.ui_max_duration_ms`.

## 4. Physicality & origin

- **Never `scale(0)` (M14).** Nothing in the real world appears from nothing. Start from `scale(0.9–0.97)` + `opacity: 0`.
- **Popovers / dropdowns / tooltips scale from their trigger (M15)**, not center:
  ```css
  .popover { transform-origin: var(--radix-popover-content-transform-origin); } /* Radix   */
  .popover { transform-origin: var(--transform-origin); }                       /* Base UI */
  ```
  **Modals are exempt** — centered in the viewport, `transform-origin: center` is correct.
- **Press feedback (M16)** on every pressable element (button, styled-link CTA, `role="button"`):
  ```css
  .button        { transition: transform 160ms var(--ease-out); }
  .button:active { transform: scale(0.97); }   /* subtle: 0.95–0.98 */
  ```
  Tailwind: `transition-transform active:scale-[0.97]`. Framer: `whileTap={{ scale: 0.97 }}`.

## 5. Interruptibility

CSS **transitions** retarget from the current value mid-flight; **`@keyframes`** restart from zero. For anything triggered rapidly or reversible (toasts stacking, toggles, drags, expand/collapse), use transitions or springs.

- Entry without JS: `@starting-style` (legacy fallback: `data-mounted` set in `useEffect`).
- **`translateY(100%)`** moves an element by its own height regardless of size — how toasts/drawers hide themselves. Prefer over hardcoded px.

```css
.toast {
  opacity: 1; transform: translateY(0);
  transition: opacity 300ms var(--ease-out), transform 300ms var(--ease-out);
  @starting-style { opacity: 0; transform: translateY(100%); }
}
```

## 6. Springs (when a spring beats a duration)

Use for drag with momentum, "alive" elements, interruptible gestures, decorative mouse-tracking. Springs keep velocity when interrupted (keyframes restart from zero).

```js
// Apple-style (recommended — easier to reason about)
{ type: "spring", duration: 0.5, bounce: 0.2 }
```

Keep bounce subtle (0.1–0.3); default UI to no bounce (critically damped). Reserve visible bounce for drag-to-dismiss and playful moments. Requires `framer-motion`/`motion` (already whitelisted) — do **not** add GSAP or other libs for this.

## 7. Asymmetric timing

Slow where the user is deciding, fast where the system responds. Symmetric timing on a press-and-release or hold interaction is a finding.

```css
.overlay          { transition: clip-path 200ms var(--ease-out); } /* release: fast */
.button:active .overlay { transition: clip-path 2s linear; }       /* press: slow, deliberate */
```

## 8. Performance (beyond motion-site's transform/opacity rule)

- Animate **`transform` / `opacity` / `filter`** only. `width`/`height`/`margin`/`padding`/`top`/`left` trigger layout + paint.
- **Framer Motion `x`/`y`/`scale` shorthands are NOT hardware-accelerated** — they run on the main thread via rAF and drop frames *under load*. For motion that runs while the page is busy, use the full transform string: `animate={{ transform: "translateX(100px)" }}`. (Entrance-on-mount shorthand like `animate={{ y: 0 }}` is fine — this caveat is about motion competing with page work, which is why it's guidance here, not a blanket lint rule.)
- Don't drive child transforms via a CSS variable on the parent — it recalcs styles for all children. Set `transform` directly on the element.
- Keep transition-time `filter: blur()` < 20 px (heavy blur is expensive, especially Safari).

## 9. Accessibility (interaction layer)

- **Reduced motion = gentler, not zero.** Keep opacity/color that aids comprehension; drop movement. (motion-site's global boilerplate already collapses durations.)
- **Gate raw-CSS `:hover` motion (M17)** behind `@media (hover: hover) and (pointer: fine)` — touch fires a false hover on tap. (Tailwind `hover:` utilities are excluded from the lint rule; still prefer press feedback over hover motion on touch-first UIs.)

```css
@media (hover: hover) and (pointer: fine) {
  .card:hover { transform: scale(1.03); }
}
```

## 10. Polish techniques

- **Blur-masked crossfade**: when two states visibly double-expose during a swap, add `filter: blur(2px)` during the transition to blend them into one perceived change.
- **Stagger**: group entrances 30–80 ms apart, narrative order. Stagger is decorative — never block interaction while it plays. (motion-site stagger token: 0.08–0.2 s.)
- **`clip-path: inset(t r b l)`** — each value eats in from that side. Uses: scroll reveal (`inset(0 0 100% 0)` → `inset(0 0 0 0)`), hold-to-confirm overlay, seamless tab color (duplicate + clip active copy), comparison slider.

## 11. Gestures & drag (app-showcase / interactive)

- **Momentum dismissal**: don't require a distance threshold — dismiss if `Math.abs(distance)/elapsedMs > ~0.11`. A flick is enough.
- **Rubber-banding at boundaries**: resistance rises the further past the edge you drag (real things slow before stopping).
- **Pointer capture** once a drag starts; **ignore extra touch points** after it begins (`if (isDragging) return`).

## 12. Debugging feel (recommend when a review can't judge from code)

- **Slow motion**: bump duration 2–5× or use the DevTools Animations panel — check colors crossfade cleanly, easing doesn't stop abruptly, `transform-origin` is right.
- **Real devices** for gestures; **fresh eyes the next day** catch what's invisible during development.

---

### Lint coverage map

| Rule | Enforces | Section |
| --- | --- | --- |
| M13 | no `ease-in` on UI | §2 |
| M14 | no `scale(0)` entrance | §4 |
| M15 | popover/dropdown/tooltip origin-aware (modals exempt) | §4 |
| M16 | press feedback on pressable / hover-motion elements | §4 |
| M17 | raw-CSS `:hover` motion gated behind `@media (hover: hover)` | §9 |

Everything else here is builder/reviewer judgment. All flags/values live in `config/motion-tokens.json` → `interaction`.
