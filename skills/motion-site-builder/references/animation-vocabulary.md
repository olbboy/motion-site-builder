# Animation Vocabulary

The precise word for a motion effect — so a prompt (or a review finding) says exactly what it means instead of "make it move nicely." Use it two ways: **name** an effect a user describes loosely, and **write** specs/prompts in terms the builder can execute without guessing.

Structure adapted from Emil Kowalski's animation vocabulary ([animations.dev](https://animations.dev/), MIT); definitions rewritten and tuned for cinematic web motion.

> When a user describes a feel ("springy", "draws itself in", "the iOS rubber-band"), map the sensation to the term below — lead with the term, then one line on what it is. If two terms compete, contrast them.

## Entrances & exits
- **Fade in / out** — appear or disappear by animating opacity.
- **Slide in** — enter by translating in from off-screen (the signature entrance rises 16–32px).
- **Scale in** — grow from `scale(0.9–0.97)` to full size, usually with a fade. Never from `scale(0)`.
- **Pop in** — appear with a slight overshoot (spring curve), like it bounces into place.
- **Reveal** — uncover gradually by animating a `clip-path` or mask.
- **Stagger** — animate siblings one after another with a small delay (0.08–0.2s here), creating a cascade in narrative order.

## Sequencing & timing
- **Keyframes** — fixed points (0/50/100%) the browser tweens between; restart from zero, so avoid for interruptible UI.
- **Orchestration** — timing several animations so they read as one coordinated motion.
- **Delay / Duration** — time before an animation starts / how long it runs.
- **Fill mode** — whether an element holds its first/last frame before/after running (`backwards`/`forwards`).

## Movement & transforms
- **Translate / Scale / Rotate / Skew** — move / resize / spin / shear via `transform` (GPU-friendly).
- **translateY(100%)** — move by the element's *own height*, any size (how toasts/drawers hide themselves).
- **Transform origin** — the anchor a scale/rotation grows from; set it to the trigger for origin-aware popovers.
- **Parallax** — foreground and background move at different speeds while scrolling, creating depth.
- **3D tilt / Flip** — `rotateX/Y` + `preserve-3d` for depth without WebGL.

## Transitions between states
- **Crossfade** — one element fades out as another fades in, same spot. Mask a double-exposure with `blur(2px)`.
- **Morph** — one shape smoothly becomes another (e.g. Dynamic Island).
- **Shared element transition** — an element travels and transforms from one position into another (thumbnail → card).
- **Layout animation** — a size/position change animates to the new spot instead of snapping.
- **Direction-aware** — content slides one way going forward, the opposite going back.

## Scroll
- **Scroll reveal** — elements fade/slide in as they enter the viewport (fire once).
- **Scroll-driven** — animation progress tied directly to scroll position.
- **Sticky-stack** — cards pin and scale down as later ones scroll over them (`scale = 1 − (n−1−i)·0.03`).
- **Marquee** — content scrolling continuously in a loop (linear easing).

## Feedback & interaction
- **Press / Tap feedback** — a subtle scale-down (`scale(0.97)`) on `:active`, so a press feels physical.
- **Hover effect** — visual change on cursor-over; gate motion behind `@media (hover: hover)`.
- **Hold to confirm** — a fill (clip-path) that grows while a button is held; slow to press, fast to release.
- **Swipe to dismiss** — drag an element off-screen to close it (toast, drawer), dismissed by velocity, not distance.
- **Rubber-banding** — resistance and snap-back when dragging past a boundary (the iOS overscroll feel).
- **Ripple** — a circle expanding from the tap point.

## Easing & springs
- **Ease-out** — starts fast, ends slow. The default for entering/exiting and anything responding to the user.
- **Ease-in** — starts slow. Avoid on UI — it delays the moment the user watches most.
- **Ease-in-out** — slow-fast-slow; for elements already on screen moving A→B.
- **Cubic-bezier** — a custom curve; the signature curve is expo-out `cubic-bezier(0.16, 1, 0.3, 1)`.
- **Spring** — physics-based motion (no fixed duration); keeps velocity when interrupted. Keep bounce subtle (0.1–0.3).
- **Interruptible** — an animation that can be redirected mid-flight (CSS transitions, springs) instead of finishing first.

## Polish & effects
- **Clip-path (`inset`)** — clip from a side; the tool for reveals, hold-to-delete, seamless tab color, comparison sliders.
- **Text glow** — soft layered `text-shadow` on display type.
- **Blur-to-sharp** — enter with `blur(6px)` → `blur(0)` alongside the fade-rise.
- **Char-by-char reveal** — per-character opacity `0.2 → 1` mapped to scroll progress.
- **Number ticker** — digits rolling to a value (use tabular numbers so they don't shift).

## Principles
- **Purposeful animation** — motion serves a function (orient, feedback, explain), never decorates a frequently-seen element.
- **Frequency of use** — the more often an element is seen, the shorter/subtler its motion (keyboard actions: none).
- **Spatial consistency** — an element keeps its identity/position across states, so users never lose track of it.
- **Asymmetric timing** — slow where the user decides (a hold), fast where the system responds.
- **Reduced motion** — honor `prefers-reduced-motion`: fewer and gentler, not zero (keep opacity/color, drop movement).
