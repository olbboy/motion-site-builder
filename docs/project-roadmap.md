# Project Roadmap

Forward-looking backlog. Items graduate into `plans/` when picked up; shipped items move to `CHANGELOG.md`. Several entries adapt ideas from studying [nutlope/hallmark](https://github.com/nutlope/hallmark)'s anti-slop methodology into motion-site's motion-first scope — noted per item.

## Now

- **Dogfood the accountability layer** — run the builder end-to-end on 2–3 fresh briefs to exercise the new Step 0.5 pre-flight, preview gate, self-critique, and `.motion-site/log.json` rotation; feed friction back into `SKILL.md` the way the linter's self-test feeds rules.

## Next

- **Briefs-as-fixtures eval suite** *(hallmark `site/_tests/` pattern)* — a `tests/` (or `examples/briefs/`) directory where each numbered case ships the verbatim brief, the produced output, and a walkthrough of what the workflow inferred and picked. The README doubles as a self-graded findings log: what worked, friction hit while generating, and a prioritized backlog that the next version's changelog answers with commit references. This turns skill regressions into visible documentation instead of anecdotes.
- **`variant` mode for the builder** *(hallmark roadmap)* — produce 2–3 structurally distinct outputs for one brief side-by-side (different archetype + pattern set each, enforced by the diversification axes). "Accepting the first output" is the top cause of template feel.
- **Motion-DNA `study` mode** *(hallmark `study` verb)* — given a URL or screen recording of a site whose motion the user admires, extract the motion DNA (entrance choreography, easing family, stagger rhythm, scroll school, interaction tempo) into a portable spec — never pixel-cloning, with the same refusal posture for paid templates. Output feeds `motion_find_reference` + the builder as a locked system.
- **Per-component duration multipliers** *(hallmark theme-aware motion tokens)* — profiles already set entrance ranges; add a per-component multiplier table (modal vs toast vs tooltip) to `config/*.json` so `motion_easing_rationale` can resolve budget-per-element instead of one flat `ui_max_duration_ms`.

## Later

- **8-state component demo wrapper** *(hallmark component-scope flow)* — when the brief is a single component, emit a `<Component>.preview.html` rendering default / hover / focus-visible / active / disabled / loading / error / success stacked and labelled, with `.is-hover`-style forcing classes so all states render at once.
- **Portable motion spec export** *(hallmark `design.md` / export-formats)* — an opt-in "lock the system" flow that writes the build's easing/duration/stagger tokens as `tokens.css`, Tailwind `@theme`, and DTCG JSON for handoff to other tools.
- **Self-screenshotting validation** *(hallmark live-preview idea)* — extend the runtime smoke step: drive the browser, capture entrance/reduced-motion states, and self-critique against the six axes with real pixels instead of code-only judgment.
- **Named motion anti-pattern catalog** — grow the FORBIDDEN list into a named-tell catalog with a perceptual "why it fails" per tell (negative-capability rules), so review findings teach instead of just block.
