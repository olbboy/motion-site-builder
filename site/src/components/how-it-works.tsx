import Reveal from './reveal'

/**
 * The method as an editorial-style numbered rail — giant ghost serif numerals
 * that ignite violet on hover — instead of another wall of glass cards.
 * Shape variety between sections is deliberate.
 */
const STEPS = [
  {
    title: 'Profile',
    body: 'Pick 1 of 5 design languages — cinematic, product-ui, editorial, playful, ecommerce. The linter and tools then enforce that taste.',
  },
  {
    title: 'Plan',
    body: 'Archetype, palette, and a scroll story that reads Hook → Proof → Detail → CTA — before any code.',
  },
  {
    title: 'Build',
    body: 'Adapt the nearest of 92 reference prompts with verbatim glass, glow, and easing primitives — never paraphrased.',
  },
  {
    title: 'Validate',
    body: 'A 17-rule motion linter scores every file — reduced-motion, GPU-only transforms, and ARIA are errors, not afterthoughts.',
  },
]

export default function HowItWorks() {
  return (
    <section id="how" className="relative z-10 mx-auto max-w-6xl scroll-mt-24 px-6 py-28">
      <Reveal>
        <p className="eyebrow mb-4">03 · The method</p>
        <h2 className="font-display mb-4 max-w-2xl text-4xl tracking-tight text-white md:text-5xl">
          Pick a profile. Plan. Build. Validate.
        </h2>
        <p className="mb-14 max-w-xl text-white/60">
          Taste becomes a system — a deterministic pipeline, not a lucky prompt.
        </p>
      </Reveal>
      <div className="max-w-3xl">
        {STEPS.map((step, index) => (
          <Reveal key={step.title} delay={index * 80}>
            <div className="group grid grid-cols-[84px_1fr] items-start gap-6 border-t border-white/10 py-9 last:border-b md:grid-cols-[128px_1fr] md:gap-10">
              <span
                className="font-display text-6xl leading-none text-white/25 transition-colors duration-300 group-hover:text-accent md:text-8xl"
                aria-hidden="true"
              >
                0{index + 1}
              </span>
              <div className="pt-1 md:pt-3">
                <h3 className="text-xl font-medium text-white md:text-2xl">{step.title}</h3>
                <p className="mt-2.5 max-w-xl text-sm leading-relaxed text-white/60 md:text-base">
                  {step.body}
                </p>
              </div>
            </div>
          </Reveal>
        ))}
      </div>
    </section>
  )
}
