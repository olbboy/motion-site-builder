# Choreography — Composing Multi-Element Motion

Rules for how *several* animated elements share a scene — the layer between one element's easing (interaction-standards.md) and the page's macro DNA (motion-design-dna.md). Use when storyboarding (SKILL.md Step 4) and choosing patterns (Step 5), and when `review-motion`/`improve-motion` judge cohesion.

Inspired by classical animation principles (the Disney "12 principles" tradition) and modern motion-direction practice; all values below are this project's own, tuned to its profiles.

---

## 1. Attention budget

- **One hero motion per scene moment.** At any instant, at most one element performs the *featured* move; everything else supports or waits.
- **The 1/3 element rule**: with 3+ animated elements, no more than a third are in active motion simultaneously. Stagger or group the rest.
- **The 1/3 distance rule**: nothing travels more than ~1/3 of the viewport in one unbroken move. Longer journeys need an intermediate beat (scale/opacity handoff, or a scroll-linked mapping where the *user* provides the distance).
- **Stillness is a beat**: leave 100–200ms of rest before starting a new motion group. Back-to-back groups read as noise.

## 2. Staging & focus

- Dim supporting elements to 40–60% opacity (optionally `blur(2–4px)`) while the hero element performs — then restore. This is what the cinematic overlay layer already does for video; apply the same idea to in-page moments (spotlight a stat, a form, a card).
- Hero enters *after* its supporting context (100–200ms later), not before — the stage exists, then the actor walks on. This is why the canonical entrance order is badge → headline → subtext → CTA, not CTA-first.

## 3. Secondary action & follow-through

- **Secondary action** (a glow, an icon nudge, a shadow response) runs at 30–50% of the primary's amplitude, starts 50–100ms after it, and may use a *different* easing. Same-amplitude same-start secondaries read as two heroes fighting.
- **Follow-through**: children settle 50–150ms after their parent stops; trailing siblings offset their stop times 100–200ms. Everything freezing on the same frame is the #1 "feels robotic" cause (see troubleshooting.md).
- **Counter-motion** adds depth cheaply: when the hero moves/scales one way, let a background layer respond subtly the other way at 15–30% amplitude (hero rises → backdrop drifts down a few px). Keep it under the attention budget — counter-motion is felt, not seen.

## 4. Depth through speed (parallax ratios)

Layer speeds, not blur stacks, communicate depth:

| Layer | Scroll/pointer response |
| --- | --- |
| Foreground (content) | 1.0× |
| Midground (imagery, cards) | 0.4–0.6× |
| Background (video, texture) | 0.1–0.3× |

Two layers are enough; three is the ceiling (vestibular safety — see §7). The `raf-lerp-parallax` primitive already implements the mechanics; these ratios are the *taste*.

## 5. Narrative shape of a single animation

Deliberate animations have acts. Budget by total duration:

| Total duration | Anticipation | Action | Settle |
| --- | --- | --- | --- |
| < 200ms (micro feedback) | skip | 60–70% | 30–40% |
| 200–400ms (interaction) | 0–15% | 40–60% | 30–40% |
| 0.5–1.2s (cinematic entrance) | 10–20% | 40–50% | 35–45% |

- **Anticipation** = a small move *opposite* the main action (a button dips 2–3% before popping; a panel leans back before sliding in). 10–20% of the main action's magnitude. Skip it on high-frequency elements — anticipation is drama, and drama is for rare moments.
- **Settle** = the ease-out tail plus any follow-through. An animation that ends at full speed feels cut off; this is what strong ease-out curves (expo-out) buy you for free.
- **Enter/exit asymmetry**: exits run 30–50% *shorter* than entrances and mirror the path (out the way it came in, faster). An exit as slow as its entrance feels like the UI won't let go.

## 6. Direction carries meaning

Pick the motion direction to match the message, not at random:

| Direction | Reads as | Use for |
| --- | --- | --- |
| Rise (translateY ↑ into place) | growth, arrival, optimism | entrances, success, reveals |
| Sink (translateY ↓) | settling, completion, dismissal | exits, collapse, "filed away" |
| Rightward | progression, next | forward navigation, steppers |
| Leftward | regression, back | back navigation, undo |
| Scale out (grow) | emergence, importance | popovers from trigger, focus moments |
| Scale in (shrink) | dismissal, de-emphasis | close, minimize |
| Shake (small x oscillation) | refusal, error | invalid input — pair with color, never scale |

This is why the DNA's entrance is fade + *rise*: arrival. Reversing a semantic direction (a success toast that sinks in from above and exits downward) is a legitimate review finding.

## 7. Context adaptation

- **Platform tempo**: scale durations ≈ ×0.8 on mobile (smaller distances, faster expectations), ×1.0 desktop, ×1.2–1.3 on TV/kiosk viewing distance. Displacement scales with container: on narrow (<400px) containers cap travel at ~20% of container width.
- **Vestibular safety** (beyond `prefers-reduced-motion`): avoid spinning elements larger than ~100px, parallax deeper than 2–3 layers, and full-screen zoom/position transitions. These trigger discomfort even for users who never touch the OS setting.
- **Cognitive consistency**: the same interaction always plays the same animation. A dropdown that opens differently in two places makes the UI feel haunted.
- **The 100th-viewing test**: any animation on a repeated path must be *invisible on the 100th viewing* — if you can imagine sighing at it, shorten or delete it (frequency filter, interaction-standards §1).
- **Pausable long motion**: anything auto-playing longer than ~5s (marquee, ambient loop, video) needs a pause affordance or must stop off-viewport (`IntersectionObserver` / `animation-play-state`).

## 8. Choreography recipes (composed moments)

| Moment | Order & timing |
| --- | --- |
| Dashboard/page load | shell (0ms) → nav (60ms) → primary content (120ms) → secondary cards stagger 30–60ms each → charts/data last. Never all at once; never > ~600ms total to interactive. |
| Modal open | overlay fades (150ms) ∥ panel scales 0.96→1 + fade (200ms, ease-out); content inside does **not** re-stagger. Exit: both together, 120–150ms. |
| List update (add/remove) | removed item collapses first (150ms), survivors slide into place (200ms, ease-in-out), new item enters last (200ms, ease-out). One thing at a time. |
| Tab switch | outgoing fades 80–100ms → incoming fades/slides 2–6px, 150ms. Indicator moves in parallel, spring or ease-in-out. No full-panel slides between adjacent tabs. |
| Accordion | chevron rotates ∥ panel height via `grid-template-rows: 0fr→1fr` wrapper (not `height` on the content), content fades in 50ms behind the expand. |
| Success celebration | rare-moment budget: primary confirmation (scale-pop with 5–10% overshoot) → secondary sparkle/confetti at 30–50% amplitude → settle. Errors get **zero** overshoot — never bounce bad news. |

---

**Lint coverage**: none of this is mechanically lintable — it is exactly the judgment layer `review-motion` (cohesion, missed opportunities) and the builder's self-critique (Purpose/Tempo/Cohesion axes) apply. The linter's M-rules still govern each individual element.
