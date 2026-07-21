# Design Profiles

Motion Site Builder ships **five design languages**. Cinematic is the default; the other four extend the reach beyond marketing/hero sites. A profile is a complete token set (`config/motion-tokens.json` = cinematic; `config/profiles/*.json` for the rest) — the linter, MCP tools, and skill all read the *active* profile, so the same engine enforces a different taste per profile.

**Pick a profile FIRST** (`motion_list_profiles`), then pass its name as the `profile` arg to every tool (`motion_get_tokens`, `motion_validate`, `motion_suggest_pattern`, `motion_easing_rationale`) or set `MOTION_PROFILE` for the CLI. Default (no profile) = cinematic — nothing about existing behavior changes.

## What's universal vs. per-profile

**Universal** (every profile, non-negotiable): `prefers-reduced-motion` (M01), GPU-only `transform`/`opacity`/`filter` (M02), no `transition: all` (M10), ARIA (M11), no `scale(0)` (M14), press feedback on pressables (M16), and the whole interaction-craft layer — `ease-in` ban (M13), origin-aware popovers (M15), hover gating (M17). Good motion feel is the same everywhere.

**Per-profile** (the taste that varies): entrance tempo, easing curves, palette strategy & accent count, typography, radius, video/decor expectations, and which cinematic-only rules relax.

## The five profiles

### cinematic *(default)*
Video-first canvas, glassmorphism, editorial serif, single saturated accent, dark. Apple-keynote energy. **Entrances 0.5–1.2s, expo-out.** Use for: hero sections, product launches, brand landing pages, app showcases. Constraints: no decorative blobs/gradients over video, no WebGL, one accent.

### product-ui
Crisp SaaS/dashboard/app UI — motion serves function, not spectacle. **Entrances 0.15–0.35s** (fast — the UI appears, it doesn't perform); interaction under 250ms. Multi-accent *semantic* palette (brand + success/warn/error), light+dark, Inter/system type, neutral tracking, `rounded-md`. Radix + recharts welcomed. Use for: dashboards, settings, tables, admin, SaaS apps.

### editorial
Typography-first content/blog/docs/magazine. Reading-optimized, generous whitespace, **restrained** scroll-reveal motion (0.4–0.8s). Serif display + prose body (`@tailwindcss/typography`), single accent, paper/ink palettes, no video/glass requirement. Use for: articles, documentation, marketing-content, changelogs, long-form.

### playful
Bold, colorful, maximalist. Vibrant **multi-accent** (up to 4), **springs with bounce** (pop-in / back-out), expressive scale (hover up to ~1.08), high-contrast. Decorative gradients/shapes are the identity here — **M08 is disabled**. Display grotesk, `rounded-full`/`rounded-3xl`. Use for: consumer apps, creative studios, events, bold campaigns.

### ecommerce
Product-grid commerce — imagery-first, conversion-focused. **Entrances 0.25–0.5s** (snappy browsing), brand + neutral (2 accents), quick-view/add-to-cart with crisp press feedback, card hover-lift gated for touch, embla carousels, tabular-number prices. Use for: storefronts, product pages, catalogs, checkout.

## Motion voice — the three archetypes behind the profiles

Each profile's motion tokens encode a recognizable *voice* (three archetypes widely practiced by contemporary design engineers — the interaction layer of this project is distilled from Emil Kowalski's published philosophy; see interaction-standards.md):

| Voice | Character | Signature |
|:---|:---|:---|
| **Invisible** | motion you feel but never notice | opacity + tiny translate (2–6px), 100–200ms, stiff springs, no blur/rotation |
| **Storytelling** | motion as cinematography | fade + rise + blur-to-sharp, 0.5–1.2s, layered timing, clip-path reveals, parallax depth |
| **Joyful** | motion as personality | scale + rotation pops, springs with visible bounce, decorative flourishes |

Profile → voice weighting: **cinematic** = storytelling-primary (macro) over an invisible interaction layer · **product-ui** = invisible-primary · **editorial** = invisible with storytelling accents at section boundaries · **playful** = joyful-primary · **ecommerce** = invisible with storytelling product moments. Two rules: never mix voices *within one animation*, and the more frequently an element is used, the more invisible its motion must be (frequency filter). Every profile's interaction layer stays invisible-voice — bounce never lands on a dropdown.

## Selecting & customizing

- **Switch**: `motion_get_tokens(profile="editorial")`, `motion_validate(code, profile="product-ui")`, or `MOTION_PROFILE=playful python3 scripts/lint_motion.py <file>`.
- **New profile**: drop `config/profiles/<name>.json` (same schema — copy the closest existing one, edit values). `motion_list_profiles` and `--self-test` pick it up automatically; the required keys are validated. The full schema — including the qualitative `aesthetic` / `imagery` / `elevation` / `voice` blocks every shipped profile now carries — is documented in `profile-schema.md`.
- **Derive from references**: when the user brings reference screenshots/URLs instead of picking a shipped profile, follow the extraction workflow in `profile-schema.md` (Step 0a) to generate a custom profile JSON that plugs into the same engine.
- **Re-skin a profile**: edit its JSON — easings, durations, palette, `max_accent_hues`, `typography.display.tracking` (drives M12), `lint.disabled_rules`. No engine code changes.

## Profile-aware build resources

- **Patterns**: `motion_suggest_pattern(intent, profile=…)` returns that profile's macro patterns (e.g. product-ui `list_stagger`/`panel_slide`, editorial `sticky_toc`, ecommerce `product_grid`) plus the universal interaction patterns (press/hover/popover/toast).
- **Primitives**: each non-cinematic profile ships signature primitives via `motion_get_template` — `product-ui-stat-card`, `product-ui-data-row`, `editorial-prose`, `editorial-sticky-toc`, `playful-pop-cta`, `playful-sticker-badge`, `ecommerce-product-card`, `ecommerce-add-to-cart`. The cinematic primitives (liquid-glass, video-*) stay cinematic — don't reach for them in another profile.
- **Easing**: `motion_easing_rationale(intent, profile=…)` resolves the right curve from the active profile's tokens.

## Corpus coverage

- The **54-prompt library** (`motion_find_reference`) contains 14 cinematic prompts and 10 prompts for each of the other four profiles, including the Vietnam landscape collection. Each non-cinematic profile also ships **two starred exemplars** (see `prompts/README.md`) that make especially strong structural references. Query by profile plus intent (for example, `motion_find_reference("product-ui dashboard")`), then pair the result with active-profile tokens, patterns, and primitives; do not transplant cinematic glass/video conventions into another language.
