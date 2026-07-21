# Troubleshooting Feel — Symptom → Cause → Fix

When motion runs correctly but *feels* wrong, diagnose by symptom. This is the named-failure vocabulary `review-motion` cites in verdicts and `improve-motion` uses to title findings. Values reference the active profile's tokens (`motion_get_tokens`); fixes reuse the remedial hierarchy in review-motion's SKILL.md.

## "It looks robotic / mechanical"

| Likely cause | Fix |
| --- | --- |
| Linear easing on spatial movement | Token ease-out (expo-out) for enter/exit; ease-in-out for on-screen moves. Linear is for marquee/progress/spinners only. |
| Everything starts and stops on the same frame | Stagger siblings (profile stagger token); offset stop times 100–200ms (choreography §3). |
| Uniform duration on every element | Vary by weight/role: hero slower, secondaries 30–50% lighter. |
| Perfectly straight diagonal paths | Add a slight arc (a few px perpendicular offset) or sequence x-then-y. |
| No settle | Stronger ease-out tail; let the last 30–40% of the duration be deceleration (choreography §5). |

## "It feels cheap / flat"

| Likely cause | Fix |
| --- | --- |
| Opacity-only entrances | Pair fade with rise (profile `entrance.translate_y_px`) and optional blur-to-sharp. |
| Built-in `ease`/`ease-out` keywords on deliberate moments | Strong custom curves — the token set exists for this. |
| No follow-through or secondary action | Child settles 50–150ms after parent; add one 30–50%-amplitude secondary (glow, icon nudge). |
| Zero overshoot anywhere (over-damped everything) | Give *rare, positive* moments 5–10% overshoot (spring-pop token). Keep UI controls critically damped. |
| Same easing curve on every property | Transform and opacity may run slightly different durations/curves; identical everything reads as a fade preset. |

## "It's too distracting / exhausting"

| Likely cause | Fix |
| --- | --- |
| High-frequency elements animate (nav hover, list items, shortcuts) | Frequency filter (interaction-standards §1): delete or reduce to press/hover feedback. |
| More than ⅓ of elements moving at once | Attention budget (choreography §1) — regroup, stagger, or cut. |
| Motion loops with no pause | Stop off-viewport; pause affordance for >5s loops (choreography §7). |
| Overshoot on everything, including errors | Overshoot budget (interaction-standards §6): errors 0%, feedback 2–5%, celebration only 15–25%. |
| Durations past their budget (400ms dropdowns, 2s reveals) | Interaction < 300ms; entrances within the profile's entrance range. |

## "It has no personality / feels generic"

| Likely cause | Fix |
| --- | --- |
| Default library curves and durations everywhere | Adopt the profile's signature (cinematic: expo-out 0.5–1.2s; playful: springs with bounce; product-ui: crisp <250ms). |
| Motion contradicts the profile | A playful site easing like a bank, or a dashboard bouncing like a toy — re-read design-profiles.md §lineage and pick one voice. |
| Every element uses the same pattern | Vary by role: hero gets the featured move, sections get one pattern each (pattern matrix, SKILL.md). |
| No emphasized moment anywhere | Choose ONE rare moment (hero entrance, success) and spend the cinematic budget there. |

## Per-profile failure modes (the profile's own way of going wrong)

- **cinematic** — too *slow*: 1.5s+ entrances, scroll-jacking, every section performing. The DNA budget is 0.5–1.2s for the *hero*, not for everything.
- **product-ui** — too *invisible*: so conservative that state changes snap jarringly. Sub-250ms is still animation; keep the feedback layer.
- **editorial** — motion competing with reading: reveals firing mid-paragraph, parallax under text. Motion belongs at section boundaries only.
- **playful** — broken, not bouncy: overshoot past ~25%, springs that never settle, chaos with no stillness beats. Playful still needs choreography.
- **ecommerce** — friction on the money path: animated add-to-cart confirmations that delay the next action, quick-view transitions over 300ms. Conversion paths get the *fastest* motion on the site.

## Quick diagnostic (run before deep-diving)

1. Does anything animate that's hit tens+ times a day? → delete/reduce first.
2. Slow it down 4× (DevTools Animations panel): does the easing stop abruptly? wrong `transform-origin`? double-exposure mid-crossfade?
3. Is there exactly one hero motion per moment?
4. Do exits mirror entrances at ~60–70% duration?
5. Does the same interaction animate identically everywhere?
6. `prefers-reduced-motion`: gentler, not broken?
7. Fresh eyes the next day — the feel bugs you can't see today.
