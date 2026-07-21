# Motion Site Builder — Repository-wide instructions for GitHub Copilot

This repo ships a motion design system: a prompt library, three agent skills, five design-profile configs, and a 20-rule motion linter. When writing or suggesting UI/animation code here (or in projects using these skills), follow the motion DNA:

- **Animate only `transform`, `opacity`, `filter`.** Never `width`/`height`/`top`/`left`/`margin`/`padding` — they trigger layout. Never `transition: all`; list properties explicitly.
- **Always handle `prefers-reduced-motion`.** Movement collapses; keep opacity/color that aids comprehension. Gate rAF/parallax loops behind a `matchMedia` check or `useReducedMotion()`.
- **Easing:** enter/exit → strong `ease-out` (signature: `cubic-bezier(0.16, 1, 0.3, 1)`); on-screen movement → `ease-in-out`; constant motion → `linear`. **Never `ease-in` on interactive UI.**
- **Durations:** interaction elements (buttons, dropdowns, tooltips, toasts) stay **under 300ms**; hero/marketing entrances may run 0.5–1.2s with stagger 0.08–0.2s — that budget is deliberate, don't "fix" it.
- **Physicality:** never enter from `scale(0)` — start `scale(0.95)` + `opacity: 0`. Popovers/dropdowns/tooltips scale from their trigger (`transform-origin` from the trigger side); modals stay centered. Every pressable element gets press feedback (`active:scale-[0.97]` / `whileTap`).
- **Interruptibility:** rapidly-triggered UI (toasts, toggles) uses CSS transitions / `@starting-style` / springs — not `@keyframes` that restart from zero. Pair every entrance with an exit (`AnimatePresence` for conditional React mounts); exits run 30–50% shorter.
- **Accessibility:** gate raw-CSS `:hover` motion behind `@media (hover: hover) and (pointer: fine)`; the `:focus-visible` ring appears instantly (never transition it); `aria-label` on icon-only buttons; background `<video>` needs `autoplay muted loop playsinline` + `poster` and `aria-hidden="true"`.
- **Layout safety:** no `overflow-x: hidden` on `html`/`body` (breaks `position: sticky` — use `clip` and fix the overflow); z-index stays on the declared layering scale, no `z-index: 9999`.
- **Dependencies:** default stack is React + Vite + Tailwind (default config) + lucide-react, Framer Motion only when scroll-linked transforms are needed. Respect each profile's `dependencies.forbidden` list (no three.js/GSAP/UI kits by default).

**Validate:** run `python3 skills/motion-site-builder/scripts/lint_motion.py <file>` (profile-aware, rules M01–M20) on any motion-bearing file you touch; `--self-test` after engine/config changes.

**More detail:** `skills/llms.txt` indexes the three skills; full value catalogs live in `skills/motion-site-builder/references/` (motion-design-dna, interaction-standards, choreography, design-profiles, modern-css-motion, gsap-interop, troubleshooting). For agents supporting the Agent Skills format, install the skills directly for the complete workflow.
