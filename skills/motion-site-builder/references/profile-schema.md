# Profile Schema & Deriving a Custom Profile

A profile is one JSON file: `config/motion-tokens.json` (cinematic, the default) or `config/profiles/<name>.json`. The engine — linter, MCP tools, skills — reads whichever profile is active, so **a new profile is a full design language with zero engine changes**. This document is the authoritative schema (today it's otherwise only implicit in the five shipped files) and the workflow for deriving a profile from user-provided references instead of picking a shipped one.

## Schema

### Required blocks (validated by `lint_motion.py --self-test`)

| Block | Contents | Read by |
| --- | --- | --- |
| `easings` | name → `cubic-bezier(…)` / keyword | M07, `motion_easing_rationale`, `motion_get_tokens` |
| `durations` | `micro` / `entrance` / `scroll_reveal` / `video_crossfade` `[min,max]` seconds | M06, pattern suggestions |
| `stagger` | `min` / `max` / `default` seconds | entrance guidance |
| `typography` | `display` (fonts, `tracking`: negative\|neutral, `leading`, emphasis) + `body` (fonts, `opacity_tiers`) | M12 (tracking), build steps |
| `palette` | `strategy`, `max_accent_hues`, `families` (background[] / foreground / accent_examples[]) | M05 |
| `layering` | named z-index scale | M09, M20 |
| `dependencies` | `allowed[]` / `forbidden[]` (forbidden wins) | pre-flight, scaffold |
| `interaction` | `press_scale`, `press_duration_ms`, `ui_max_duration_ms`, `ban_ease_in`, `popover_origin_aware`, `gate_hover_pointer_fine` | M13–M17 |
| `lint` | `weights`, `z_index_escape_threshold`, `disabled_rules[]`, `severity_overrides{}` | scoring and M09/M20 escape-hatch detection |

Plus `meta` (name/version/note), `entrance` (translate/blur ranges), `radius`, `video` (required attrs, `poster_required`).

### Qualitative blocks (recommended — the perceptual layer)

These make a profile's *taste* queryable instead of living only in prose. All five shipped profiles carry them; a derived profile should too:

```jsonc
"aesthetic": {
  "mood": ["cinematic", "premium", "quiet"],        // 3–5 words
  "genre": "launch-cinematic marketing",             // e.g. "corporate SaaS", "luxury editorial"
  "personality": ["confident", "restrained"],
  "density": "spacious",                             // compact | comfortable | spacious
  "ornamentation": "none"                            // none | subtle-accents | decorative | maximalist
},
"imagery": {
  "photo_treatment": "fullscreen video/photo canvas, darkened overlay for text contrast",
  "illustration_style": "none",                      // or "flat spot illustrations", "3d-render", …
  "image_shape": "full-bleed",                       // full-bleed | rounded-card | circle | organic
  "pattern_usage": "none"
},
"elevation": {
  "shadow_style": "none",                            // none | soft-diffused | hard-drop | layered
  "levels": {}                                        // e.g. { "low": "0 1px 2px rgb(0 0 0 / 0.05)", … }
},
"voice": {
  "tone": "declarative, sensory",
  "formality": "confident-casual",
  "cta_style": "direct imperative",                  // direct imperative | friendly invitation | subtle suggestion
  "error_tone": "calm, plain"
}
```

The builder reads `aesthetic`/`imagery`/`voice` during Phase A (palette, storyboard, copy voice); `elevation` matters most for product-ui/ecommerce (real card shadows) and stays `"none"` for cinematic (depth via layering is the philosophy, not an omission).

## Deriving a profile from references (Step 0a)

When the user supplies reference screenshots/URLs/an existing site instead of naming a shipped profile ("make it feel like this"), derive one:

1. **Confirm intent** — a derived profile is for *a distinct design language*, not a palette tweak. If the reference is ~90% one shipped profile, use that profile and adjust tokens conversationally instead.
2. **Analyze against this schema, top down.** Fill every block; no empty strings. With multiple references, record the dominant pattern and note variants in the relevant `note` fields. Extraction heuristics:
   - **Color**: primary by area dominance, accent by CTA usage; count distinct saturated hues → `max_accent_hues`; light/dark → `families`.
   - **Type**: display vs body pairing; measure tracking direction (tight display = `negative`) and leading from headline blocks.
   - **Radius**: compare corner radius to element height (≥50% = pill → `rounded-full`).
   - **Motion**: watch/inspect entrances — distance, duration class (crisp <350ms vs cinematic 0.5s+), bounce or none → `durations`, `easings`, `entrance`.
   - **Elevation**: shadows present? style and layer count → `elevation`.
   - **Imagery**: photography treatment, illustration presence, image shapes → `imagery`.
   - **Voice**: read their buttons and headlines → `voice`.
   - **Effects**: note glass/gradients → `ornamentation`; if the reference leans on WebGL/canvas, capture the *feel* (depth, palette, tempo) — this engine reproduces it with video/layering/parallax, not WebGL.
3. **Priority order when references conflict or time is short**: color & typography → density/layout feel → shape & elevation → aesthetic/imagery/voice → motion tokens. (Get the material right before the movement.)
4. **Write `config/profiles/<derived-name>.json`** — copy the nearest shipped profile as the base, override every analyzed value, keep every required block. Name it after the language, not the client (`warm-editorial`, not `acme`).
5. **Validate**: `python3 scripts/lint_motion.py --self-test` must pass (schema keys + fixtures under the new profile), and `--list-profiles` must show it. Then proceed with the normal workflow using the derived profile name everywhere a `profile` arg is accepted.
6. **Iterate like the shipped profiles**: after the first build, re-compare against the references (hierarchy, ornamentation, typographic rhythm, motion) and fold corrections back into the JSON — the profile is the durable artifact, the build is disposable.

**Universal rules never derive away**: reduced-motion (M01), GPU-only animation (M02), no `transition: all` (M10), the interaction-craft layer (M13–M18), layout safety (M19–M20). A reference that violates these is a reference to *improve on*, not to copy.
