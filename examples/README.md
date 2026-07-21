# Examples — profile dogfoods

Self-contained pages that prove a **design profile** end-to-end: real UI, hand-written CSS using that profile's tokens, and a clean pass under that profile's lint bar.

| Example | Profile | Proof |
|---|---|---|
| [product-ui-dashboard](product-ui-dashboard/index.html) | `product-ui` | **100/A+** under `product-ui` · **75/C** under `cinematic` |
| [aurelia-landing](aurelia-landing/src/App.tsx) | `cinematic` | **100/A+** on every source file · built from [its own prompt](../prompts/aurelia-landing.md), code mode |

The cross-profile score gap is the point: the *same* file is excellent under the profile it targets and "wrong" under another — because each profile enforces its own tempo, palette, and easing. The cinematic site lives at [`site/`](../site).

Verify:

```bash
python3 skills/motion-site-builder/scripts/lint_motion.py --profile product-ui examples/product-ui-dashboard/index.html
# open it: any static server, e.g.
python3 -m http.server 8099 --directory examples   # then http://localhost:8099/product-ui-dashboard/

# aurelia-landing (React + Vite — the builder's code-mode output):
python3 skills/motion-site-builder/scripts/lint_motion.py examples/aurelia-landing/src/index.css examples/aurelia-landing/src/App.tsx
cd examples/aurelia-landing && npm install && npm run dev   # then replace the {YOUR_*_URL} media placeholders
```

`product-ui-dashboard` is one HTML file with an inline `<style>` — no build, no dependencies. `aurelia-landing` is the other deliverable proven end-to-end: the full React + Vite + framer-motion project that code mode ships for a cinematic prompt (staggered `unveil` hero, `whileInView` reveals, a `useScroll` sticky-stack, all gated behind `useReducedMotion()`), stamped with its `/* motion-site · … */` receipt and carrying bring-your-own-media placeholders. They embody the profiles rather than exhaust them.
