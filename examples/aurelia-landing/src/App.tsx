import { useRef, useState, type FormEvent, type ReactNode } from 'react'
import {
  motion,
  useScroll,
  useTransform,
  useReducedMotion,
  type MotionValue,
} from 'framer-motion'
import { Watch } from 'lucide-react'

const EASE = [0.16, 1, 0.3, 1] as const
const PLAYFAIR = { fontFamily: "'Playfair Display', serif" }

/* Bring your own media — replace with assets you have rights to.
   The prompt asks for a static macro close-up of a balance wheel ticking. */
const VIDEO_URL = '{YOUR_VIDEO_URL}'
const POSTER_URL = '{YOUR_POSTER_URL}'
const IMAGE_URL_1 = '{YOUR_IMAGE_URL_1}'

/* Scroll reveal wrapper — base whileInView props from the spec, skipped
   entirely under reduced motion so content renders at its final state. */
function Reveal({ children, delay = 0, className }: { children: ReactNode; delay?: number; className?: string }) {
  const reduced = useReducedMotion()
  if (reduced) return <div className={className}>{children}</div>
  return (
    <motion.div
      className={className}
      initial={{ opacity: 0, y: 28, filter: 'blur(6px)' }}
      whileInView={{ opacity: 1, y: 0, filter: 'blur(0px)' }}
      viewport={{ once: true, amount: 0.3 }}
      transition={{ duration: 0.9, ease: EASE, delay }}
    >
      {children}
    </motion.div>
  )
}

function Eyebrow({ children }: { children: ReactNode }) {
  return <p className="text-xs tracking-[0.22em] text-[#C9A227] mb-4">{children}</p>
}

const CARDS = [
  { numeral: '01', title: 'Mainplate & Bridges', description: 'Hand-beveled German silver, black-polished by hand under a loupe — eighteen hours per bridge.' },
  { numeral: '02', title: 'Escapement', description: 'A free-sprung balance beating at 21,600 vph, regulated over six weeks before it ever sees a case.' },
  { numeral: '03', title: 'Micro-Rotor', description: 'A 950-platinum rotor, half the thickness of a standard automatic, so the caliber stays 4.1mm thin.' },
  { numeral: '04', title: 'Case & Crystal', description: '38mm of 950 platinum, box-domed sapphire front and back — the movement is meant to be seen, not hidden.' },
]

function MovementCard({ index, total, numeral, title, description, progress }: {
  index: number
  total: number
  numeral: string
  title: string
  description: string
  progress: MotionValue<number>
}) {
  const reduced = useReducedMotion()
  const targetScale = 1 - (total - 1 - index) * 0.03
  const scale = useTransform(progress, [index / total, 1], [1, targetScale])
  return (
    <motion.div
      className="panel rounded-2xl grid md:grid-cols-2 gap-10 p-6 md:p-14 max-w-5xl mx-auto items-center sticky"
      style={{ top: `calc(8vh + ${index * 24}px)`, scale: reduced ? 1 : scale }}
    >
      <div className="text-6xl md:text-9xl text-[#C9A227]/20 leading-none" style={PLAYFAIR}>{numeral}</div>
      <div className="text-left">
        <h3 className="text-2xl md:text-3xl text-[#F7F2E7]" style={PLAYFAIR}>{title}</h3>
        <p className="text-sm text-[#F7F2E7]/65 mt-3 max-w-sm">{description}</p>
      </div>
    </motion.div>
  )
}

const SPECS: [string, string][] = [
  ['Movement', 'Manual-wind, in-house'],
  ['Power reserve', '72 hours'],
  ['Frequency', '21,600 vph (3 Hz)'],
  ['Jewels', '31'],
  ['Case', '38mm · 950 platinum'],
  ['Crystal', 'Sapphire, box-domed front & back'],
  ['Water resistance', '30m'],
  ['Production', '1 per year, individually numbered'],
]

function SpecRow({ label, value }: { label: string; value: string }) {
  return (
    <div className="px-5 md:px-8 py-5 flex items-center justify-between text-sm border-b border-[#F7F2E7]/10 last:border-b-0 hover:bg-white/[0.02] transition-colors">
      <span className="text-[#F7F2E7]/60">{label}</span>
      <span className="text-[#F7F2E7] font-medium tabular-nums">{value}</span>
    </div>
  )
}

function WaitlistForm() {
  const [email, setEmail] = useState('')
  const [status, setStatus] = useState<'idle' | 'loading' | 'success'>('idle')
  const submit = (e: FormEvent) => {
    e.preventDefault()
    if (status !== 'idle') return
    setStatus('loading')
    setTimeout(() => {
      setStatus('success')
      setTimeout(() => setStatus('idle'), 3000)
    }, 600)
  }
  const label = status === 'success' ? "You're on the list" : 'Request an allocation'
  return (
    <form onSubmit={submit} className="mt-8 flex flex-col sm:flex-row gap-3">
      <input
        type="email"
        required
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        placeholder="you@domain.com"
        aria-label="Email address"
        className="liquid-glass rounded-full px-6 py-3.5 text-sm text-[#F7F2E7] placeholder-[#F7F2E7]/40 flex-1 bg-transparent focus-visible:outline focus-visible:outline-2 focus-visible:outline-[#C9A227]"
      />
      <button
        type="submit"
        disabled={status === 'loading'}
        className="bg-[#C9A227] text-[#0B0906] rounded-full px-8 py-3.5 text-sm font-medium transition-transform hover:scale-[1.03] active:scale-[0.97] disabled:opacity-50 disabled:cursor-not-allowed"
      >
        {status === 'loading' ? 'Requesting…' : label}
      </button>
    </form>
  )
}

export default function App() {
  const containerRef = useRef<HTMLDivElement>(null)
  const { scrollYProgress } = useScroll({ target: containerRef, offset: ['start start', 'end end'] })

  return (
    <div className="min-h-screen bg-[#0B0906] text-[#F7F2E7]">
      <nav aria-label="Primary" className="sticky top-0 z-20 px-6 py-5">
        <div className="liquid-glass rounded-full max-w-5xl mx-auto px-6 py-3 flex items-center justify-between">
          <span className="flex items-center gap-2">
            <Watch size={16} className="text-[#C9A227]" aria-hidden="true" />
            <span className="text-lg font-semibold tracking-tight text-[#F7F2E7]">Aurelia</span>
          </span>
          <span className="hidden md:flex gap-8 ml-8">
            <a href="#philosophy" className="text-sm text-[#F7F2E7]/70 hover:text-[#F7F2E7] transition-colors">Philosophy</a>
            <a href="#movement" className="text-sm text-[#F7F2E7]/70 hover:text-[#F7F2E7] transition-colors">The Movement</a>
            <a href="#specifications" className="text-sm text-[#F7F2E7]/70 hover:text-[#F7F2E7] transition-colors">Specifications</a>
          </span>
          <a
            href="#waitlist"
            className="bg-[#C9A227] text-[#0B0906] rounded-full px-6 py-2 text-sm font-medium transition-transform hover:scale-[1.03] active:scale-[0.97]"
          >
            Join the waitlist
          </a>
        </div>
      </nav>

      <section id="hero" className="relative z-10 h-screen flex flex-col items-center justify-center text-center px-6 -mt-[88px]">
        <video
          autoPlay
          muted
          loop
          playsInline
          poster={POSTER_URL}
          aria-hidden="true"
          className="absolute inset-0 h-full w-full object-cover z-0"
          src={VIDEO_URL}
        />
        <div className="absolute inset-0 z-[1] bg-gradient-to-t from-[#0B0906] via-[#0B0906]/20 to-[#0B0906]/70" />
        <div className="relative z-10">
          <p className="animate-unveil text-xs tracking-[0.22em] text-[#C9A227] mb-5">ONE MOVEMENT. ONE YEAR. NO EXCEPTIONS.</p>
          <h1
            className="animate-unveil-delay-1 text-glow text-5xl sm:text-7xl md:text-8xl leading-[0.95] tracking-tight text-[#F7F2E7]"
            style={PLAYFAIR}
          >
            Time, <em className="italic">unhurried</em>.
          </h1>
          <p className="animate-unveil-delay-2 text-sm sm:text-base text-[#F7F2E7]/65 max-w-md mx-auto mt-5 leading-relaxed">
            Aurelia designs a single wristwatch movement each year — hand-finished, individually numbered, and never repeated.
          </p>
          <div className="animate-unveil-delay-3 mt-8 flex flex-col sm:flex-row gap-3 items-center justify-center">
            <a
              href="#waitlist"
              className="bg-[#C9A227] text-[#0B0906] rounded-full px-8 py-3.5 text-base font-medium transition-transform hover:scale-[1.03] active:scale-[0.97]"
            >
              Join the 2027 waitlist
            </a>
            <a
              href="#movement"
              className="liquid-glass rounded-full px-6 py-3.5 text-base text-[#F7F2E7] transition-transform hover:scale-[1.03] active:scale-[0.97]"
            >
              See the movement →
            </a>
          </div>
        </div>
      </section>

      <section id="philosophy" className="py-28 max-w-6xl mx-auto px-6 grid md:grid-cols-2 gap-16 items-center">
        <Reveal>
          <Eyebrow>01 · Why scarcity is the point</Eyebrow>
          <h2 className="text-4xl md:text-5xl leading-[1.05]" style={PLAYFAIR}>
            We build <em className="italic">one</em> thing, once.
          </h2>
          <p className="mt-6 max-w-lg text-base text-[#F7F2E7]/70 leading-relaxed">
            Every Aurelia atelier ships a single caliber a year — no variants, no reissues, no second batch. The watchmaker
            who starts a movement in January is the one who cases it in December.
          </p>
          <p className="mt-4 max-w-lg text-base text-[#F7F2E7]/70 leading-relaxed">
            We turned down three retailers this year. An atelier that says yes to everyone eventually says yes to nothing in
            particular.
          </p>
        </Reveal>
        <Reveal delay={0.1}>
          <img
            src={IMAGE_URL_1}
            alt="The watchmaker's bench at the Aurelia atelier"
            className="rounded-2xl aspect-[4/5] object-cover w-full"
            loading="lazy"
          />
        </Reveal>
      </section>

      <section id="movement" className="py-28 text-center">
        <Reveal>
          <Eyebrow>02 · Inside Caliber AUR-01</Eyebrow>
          <h2 className="text-4xl md:text-5xl mb-16" style={PLAYFAIR}>
            Four parts. <em className="italic">One</em> year.
          </h2>
        </Reveal>
        <div ref={containerRef} className="relative h-[400vh] px-6">
          {CARDS.map((card, i) => (
            <MovementCard key={card.numeral} index={i} total={CARDS.length} progress={scrollYProgress} {...card} />
          ))}
        </div>
      </section>

      <section id="specifications" className="py-28 max-w-3xl mx-auto px-6">
        <Reveal>
          <Eyebrow>03 · Caliber AUR-01 — specifications</Eyebrow>
          <h2 className="text-4xl md:text-5xl mb-10" style={PLAYFAIR}>
            Every number, <em className="italic">accounted for</em>.
          </h2>
        </Reveal>
        <Reveal delay={0.1}>
          <div className="panel rounded-2xl">
            {SPECS.map(([label, value]) => (
              <SpecRow key={label} label={label} value={value} />
            ))}
          </div>
        </Reveal>
      </section>

      <section id="waitlist" className="py-32 text-center max-w-xl mx-auto px-6">
        <Reveal>
          <Eyebrow>04 · Reserve your allocation</Eyebrow>
          <h2 className="text-4xl md:text-6xl leading-[1.05]" style={PLAYFAIR}>
            The 2027 movement. <em className="italic">One</em> collector.
          </h2>
          <WaitlistForm />
          <p className="mt-4 text-xs text-[#F7F2E7]/50">
            No deposit today. Confirmed collectors are contacted in production order, one email, once a year.
          </p>
        </Reveal>
        <footer className="border-t border-[#F7F2E7]/10 pt-8 pb-10 mt-20 flex flex-col sm:flex-row justify-between gap-4 text-xs text-[#F7F2E7]/50">
          <span>© Aurelia — one movement, one year.</span>
          <span className="flex gap-6 justify-center">
            <a href="#philosophy" className="hover:text-[#F7F2E7] transition-colors">Philosophy</a>
            <a href="#waitlist" className="hover:text-[#F7F2E7] transition-colors">Instagram</a>
            <a href="#waitlist" className="hover:text-[#F7F2E7] transition-colors">Press</a>
          </span>
        </footer>
      </section>
    </div>
  )
}
