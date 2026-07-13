# Prompt Catalog

One markdown file per prompt, engineered for one-shot generation in AI builders (Bolt, Lovable, v0, Cursor). Every prompt in this library is **original**, authored from the project's own [design profiles](../skills/motion-site-builder/references/design-profiles.md) and motion DNA — no brand replicas, and no hardcoded third-party media.

> **Bring your own media.** Prompts reference media as placeholders (`{YOUR_VIDEO_URL}`, `{YOUR_POSTER_URL}`). Supply footage/images you have rights to (your own, or royalty-free sources such as Pexels/Coverr/Unsplash under their licenses). Fonts are all open-licensed (Google Fonts / OFL). Contributing? Read [docs/prompt-guidelines.md](../docs/prompt-guidelines.md).

## Cinematic (6)

Video-first, glassmorphism, editorial serif, single-accent, dark — the flagship profile.

| # | Name | Vertical | File |
|---|------|----------|------|
| 1 | Halcyon | AI compute infrastructure | [halcyon-hero.md](halcyon-hero.md) |
| 2 | Aphelion | Private orbital travel | [aphelion-hero.md](aphelion-hero.md) |
| 3 | Monolith | Architecture / design studio | [monolith-hero.md](monolith-hero.md) |
| 4 | Verdant | Regenerative agriculture | [verdant-hero.md](verdant-hero.md) |
| 5 | SkyElite | Private-jet landing | [skyelite-hero.md](skyelite-hero.md) |
| 6 | Motion Site Builder (official dogfood) | Product landing | [motion-site-builder-landing.md](motion-site-builder-landing.md) |

## Profile exemplars (8)

Reference prompts for the four non-cinematic profiles. Each is built from that profile's tokens and signature primitives, and scores 100/A+ under `MOTION_PROFILE=<profile>`.

| # | Name | Type · Profile | File |
|---|------|----------------|------|
| 1 | PulseGrid Analytics | Dashboard · product-ui | [pulsegrid-analytics-dashboard.md](pulsegrid-analytics-dashboard.md) |
| 2 | Aperture Team Settings | SaaS Settings · product-ui | [aperture-team-settings.md](aperture-team-settings.md) |
| 3 | Meridian Longread | Magazine Article · editorial | [meridian-longread-article.md](meridian-longread-article.md) |
| 4 | Ledgerline Changelog | Docs / Changelog · editorial | [ledgerline-changelog.md](ledgerline-changelog.md) |
| 5 | FizzPop Soda | Consumer Brand · playful | [fizzpop-soda-landing.md](fizzpop-soda-landing.md) |
| 6 | PixelJam Arcade Fest | Event / Campaign · playful | [pixeljam-arcade-fest.md](pixeljam-arcade-fest.md) |
| 7 | Arcadia Goods Storefront | Storefront · ecommerce | [arcadia-goods-storefront.md](arcadia-goods-storefront.md) |
| 8 | Maison Ondes Product Page | Product Page · ecommerce | [maison-ondes-product-page.md](maison-ondes-product-page.md) |

## Usage

Copy an entire file into your builder, then change only: brand name, headline copy, accent color, and the media placeholders. The design *patterns* (glass surfaces, signature easing `cubic-bezier(0.16, 1, 0.3, 1)`, staggered entrances) are enforced by the [motion linter](../skills/motion-site-builder/scripts/lint_motion.py).
