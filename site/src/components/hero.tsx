import ProfilesStage from './profiles-showcase'
import Reveal from './reveal'

// Entrance choreography uses the CSS .animate-fade-up/.delay-* classes from
// index.css, which are collapsed by its prefers-reduced-motion block.
// The five-language stage is the hero's product surface — the page leads with
// the thing itself, not a promise of it.
export default function Hero() {
  return (
    <section className="relative z-10 flex flex-col items-center px-6 pb-24 pt-14 text-center md:pt-20">
      <div className="animate-fade-up liquid-glass flex items-center gap-2 rounded-full px-4 py-1.5">
        <span className="bg-accent inline-block h-1.5 w-1.5 rounded-full" aria-hidden="true" />
        <span className="eyebrow !text-white/60">Open source · MIT · 5 design languages</span>
      </div>
      <h1
        className="animate-fade-up delay-1 text-glow font-display mt-8 text-5xl leading-[0.95] tracking-tight text-white md:text-8xl"
      >
        Motion UI that looks
        <br />
        <em className="italic text-accent">designed</em>, not generated.
      </h1>
      <p className="animate-fade-up delay-2 mt-6 max-w-lg text-lg leading-relaxed text-white/70 [text-wrap:balance]">
        Build new motion UI, review a change, or turn an existing app into
        executable improvement plans — all grounded by one 17-rule linter.
      </p>
      <div className="animate-fade-up delay-3 mt-8 flex flex-col gap-4 sm:flex-row">
        <a
          href="#profiles"
          className="rounded-full bg-white px-8 py-3.5 text-base font-medium text-black transition-transform hover:scale-[1.03] active:scale-[0.97]"
        >
          Explore the profiles
        </a>
        <a
          href="https://github.com/olbboy/motion-site-builder"
          className="inline-flex items-center justify-center px-4 py-3.5 text-base font-medium text-white/60 transition-colors hover:text-white/90 active:scale-[0.98]"
        >
          View on GitHub →
        </a>
      </div>
      <Reveal delay={160} className="mt-16 w-full md:mt-20">
        <ProfilesStage />
      </Reveal>
    </section>
  )
}
