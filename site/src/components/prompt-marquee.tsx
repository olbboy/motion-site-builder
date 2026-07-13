// Two counter-scrolling strips of prompt names set in the display serif —
// borderless type with an edge fade, not a row of chips. Content is
// duplicated 2× per row so the -50% translate wraps seamlessly. Both loops
// are stopped by the prefers-reduced-motion block in index.css.
const ROW_A = [
  'Halcyon', 'Aphelion', 'Monolith', 'Verdant', 'SkyElite Jets',
  'PulseGrid Analytics', 'Aperture Settings',
]
const ROW_B = [
  'Meridian Longread', 'Ledgerline', 'FizzPop Soda', 'PixelJam Fest',
  'Arcadia Goods', 'Maison Ondes', 'Motion Site Builder',
]

function Row({ names, reverse }: { names: string[]; reverse?: boolean }) {
  return (
    <div className={`${reverse ? 'animate-marquee-reverse' : 'animate-marquee'} flex w-max items-baseline`}>
      {[...names, ...names].map((name, index) => (
        <span key={`${name}-${index}`} className="flex items-baseline whitespace-nowrap">
          <span className="font-display text-2xl italic text-white/30 md:text-3xl">{name}</span>
          <span className="mx-6 text-sm text-accent/60" aria-hidden="true">✦</span>
        </span>
      ))}
    </div>
  )
}

export default function PromptMarquee() {
  return (
    <section
      className="marquee-mask relative z-10 space-y-5 overflow-hidden border-y border-white/5 py-10"
      aria-hidden="true"
    >
      <Row names={ROW_A} />
      <Row names={ROW_B} reverse />
    </section>
  )
}
