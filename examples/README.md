# Examples — profile dogfoods

Self-contained pages that prove a **design profile** end-to-end: real UI, hand-written CSS using that profile's tokens, and a clean pass under that profile's lint bar.

| Example | Profile | Proof |
|---|---|---|
| [product-ui-dashboard](product-ui-dashboard/index.html) | `product-ui` | **100/A+** under `product-ui` · **75/C** under `cinematic` |

The cross-profile score gap is the point: the *same* file is excellent under the profile it targets and "wrong" under another — because each profile enforces its own tempo, palette, and easing. The cinematic site lives at [`site/`](../site).

Verify:

```bash
python3 skills/motion-site-builder/scripts/lint_motion.py --profile product-ui examples/product-ui-dashboard/index.html
# open it: any static server, e.g.
python3 -m http.server 8099 --directory examples   # then http://localhost:8099/product-ui-dashboard/
```

Each page is one HTML file with an inline `<style>` — no build, no dependencies. They embody the profile rather than exhaust it.
