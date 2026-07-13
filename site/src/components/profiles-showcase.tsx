import { useEffect, useRef, useState } from 'react'
import { motion, useReducedMotion } from 'framer-motion'

/**
 * The site proving it speaks all five languages — as one full-width stage.
 * Each vignette takes the stage in its OWN profile's art direction and tempo:
 * cinematic is slow serif-on-black, product-ui snaps in light slate, editorial
 * reads on paper, playful springs on candy, ecommerce lifts on white.
 *
 * The stage auto-advances every 4s (paused on hover/focus, disabled under
 * reduced motion). Off-brand colors are Tailwind palette utilities (not hex)
 * so the cinematic single-accent rule still holds; all motion is
 * transform/opacity.
 */

const EXPO: [number, number, number, number] = [0.16, 1, 0.3, 1] // cinematic expo-out
const QUINT: [number, number, number, number] = [0.22, 1, 0.36, 1] // quint-out
const CYCLE_MS = 4000

type MockProps = { on: boolean }

// ── cinematic ──────────────────────────────────────────────────────────
function CinematicMock({ on }: MockProps) {
  return (
    <div className="relative flex h-full w-full flex-col items-center justify-center overflow-hidden bg-zinc-950 p-8">
      <motion.div
        className="pointer-events-none absolute left-1/2 top-1/2 h-[130%] w-[70%] -translate-x-1/2 -translate-y-1/2 rounded-full bg-violet-600/25 blur-3xl"
        animate={{ opacity: on ? 1 : 0.35, scale: on ? 1 : 0.9 }}
        transition={{ duration: 0.9, ease: EXPO }}
      />
      <span className="relative rounded-full border border-white/15 px-3 py-1 text-[11px] text-white/60">
        A24 FILMS · PRESENTS
      </span>
      <motion.p
        className="font-display relative mt-5 text-center text-4xl leading-none text-white md:text-6xl"
        animate={{ y: on ? 0 : 14, opacity: on ? 1 : 0.6, filter: on ? 'blur(0px)' : 'blur(4px)' }}
        transition={{ duration: 0.9, ease: EXPO }}
      >
        Ship <em className="italic text-violet-300">cinematic</em>
      </motion.p>
      <motion.div
        className="relative mt-8 h-px w-56 bg-white/20"
        animate={{ opacity: on ? 1 : 0.4 }}
        transition={{ duration: 0.9, ease: EXPO }}
      >
        <motion.span
          className="absolute -top-[3px] block h-[7px] w-[7px] rounded-full bg-white"
          animate={{ x: on ? 224 : 0 }}
          transition={{ duration: 3.6, ease: 'linear' }}
        />
      </motion.div>
      <span className="relative mt-3 text-[10px] tracking-[0.3em] text-white/40">00:07 / 00:24</span>
    </div>
  )
}

// ── product-ui ─────────────────────────────────────────────────────────
const BARS = [0.45, 0.7, 0.5, 0.9, 0.65, 1, 0.8, 0.6]
const TILES = [
  { label: 'MRR', value: '$48.2k', delta: '+12%', up: true },
  { label: 'Active', value: '9,412', delta: '+312', up: true },
  { label: 'Churn', value: '2.1%', delta: '−0.4pt', up: true },
]
function ProductUiMock({ on }: MockProps) {
  return (
    <div className="flex h-full w-full flex-col bg-slate-50 p-6 text-slate-900 md:p-8">
      <div className="flex items-center justify-between">
        <span className="text-xs text-slate-400">
          Workspaces / Acme / <span className="font-medium text-slate-900">Overview</span>
        </span>
        <span className="flex h-4 w-7 items-center rounded-full bg-sky-500 px-0.5">
          <motion.span
            className="h-3 w-3 rounded-full bg-white"
            animate={{ x: on ? 12 : 0 }}
            transition={{ duration: 0.18, ease: QUINT }}
          />
        </span>
      </div>
      <div className="mt-4 grid grid-cols-3 gap-3">
        {TILES.map((t, i) => (
          <motion.div
            key={t.label}
            className="rounded-lg border border-slate-200 bg-white p-3"
            animate={{ y: on ? 0 : 6, opacity: on ? 1 : 0.5 }}
            transition={{ duration: 0.2, delay: i * 0.04, ease: QUINT }}
          >
            <span className="text-[10px] font-medium text-slate-500">{t.label}</span>
            <div className="flex items-baseline gap-1.5">
              <span className="text-base font-semibold tabular-nums md:text-lg">{t.value}</span>
              <span className="text-[10px] font-medium text-emerald-600">{t.delta}</span>
            </div>
          </motion.div>
        ))}
      </div>
      <div className="mt-4 flex min-h-0 flex-1 items-end gap-1.5 rounded-lg border border-slate-200 bg-white p-3">
        {BARS.map((h, i) => (
          <motion.span
            key={i}
            className="h-full flex-1 origin-bottom rounded-sm bg-sky-500/80"
            animate={{ scaleY: on ? h : h * 0.3 }}
            transition={{ duration: 0.22, delay: i * 0.03, ease: QUINT }}
          />
        ))}
      </div>
    </div>
  )
}

// ── editorial ──────────────────────────────────────────────────────────
const LINES = ['w-full', 'w-11/12', 'w-full', 'w-10/12', 'w-full', 'w-4/6']
const TOC = ['The refresh reflex', 'Rooms with one door', 'What the loaf knows']
function EditorialMock({ on }: MockProps) {
  return (
    <div className="grid h-full w-full grid-cols-[1fr] gap-8 bg-stone-50 p-6 text-stone-800 md:grid-cols-[1fr_180px] md:p-10">
      <div>
        <span className="text-[10px] font-medium uppercase tracking-[0.18em] text-amber-700">
          Field notes · Issue 14
        </span>
        <p className="font-display mt-2 text-2xl leading-tight text-stone-900 md:text-4xl">
          The quiet craft of reading
        </p>
        <motion.span
          className="mt-3 block h-0.5 w-16 origin-left bg-amber-600"
          animate={{ scaleX: on ? 1 : 0.25 }}
          transition={{ duration: 0.6, ease: QUINT }}
        />
        <div className="mt-4 flex gap-3">
          <span className="font-display text-4xl leading-none text-amber-700 md:text-5xl">W</span>
          <div className="mt-1 flex-1 space-y-2">
            {LINES.map((w, i) => (
              <motion.div
                key={i}
                className={`h-1.5 rounded-full bg-stone-300 ${w}`}
                animate={{ opacity: on ? 1 : 0.45, y: on ? 0 : 4 }}
                transition={{ duration: 0.55, delay: i * 0.07, ease: QUINT }}
              />
            ))}
          </div>
        </div>
      </div>
      <div className="hidden border-l border-stone-200 pl-4 md:block">
        <span className="text-[10px] uppercase tracking-[0.14em] text-stone-400">On this page</span>
        <div className="mt-3 space-y-2">
          {TOC.map((t, i) => (
            <motion.p
              key={t}
              className={`text-xs ${i === 0 ? 'border-l-2 border-stone-900 pl-2 text-stone-900' : 'pl-2 text-stone-400'}`}
              animate={{ opacity: on ? 1 : 0.5 }}
              transition={{ duration: 0.55, delay: i * 0.07, ease: QUINT }}
            >
              {t}
            </motion.p>
          ))}
        </div>
      </div>
    </div>
  )
}

// ── playful ────────────────────────────────────────────────────────────
const DOTS = ['bg-emerald-300', 'bg-sky-300', 'bg-rose-300', 'bg-amber-300']
function PlayfulMock({ on }: MockProps) {
  return (
    <div className="relative flex h-full w-full flex-col items-start justify-center overflow-hidden bg-fuchsia-500 p-8 md:p-12">
      <span
        className="pointer-events-none absolute -right-10 -top-10 h-48 w-48 rounded-full bg-amber-300/40 blur-2xl"
        aria-hidden="true"
      />
      <motion.span
        className="inline-block rounded-2xl bg-amber-300 px-3 py-1 text-sm font-black text-fuchsia-950"
        animate={{ scale: on ? 1.08 : 1, rotate: on ? 4 : -6 }}
        transition={{ type: 'spring', stiffness: 400, damping: 11 }}
      >
        NEW!
      </motion.span>
      <motion.p
        className="mt-4 text-4xl font-black leading-[0.95] text-white md:text-6xl"
        animate={{ scale: on ? 1 : 0.94, rotate: on ? 0 : -1 }}
        transition={{ type: 'spring', stiffness: 300, damping: 13 }}
      >
        Make it <span className="text-amber-300">loud</span>
      </motion.p>
      <div className="mt-5 flex items-center gap-2">
        {DOTS.map((c, i) => (
          <motion.span
            key={i}
            className={`h-4 w-4 rounded-full ${c}`}
            animate={{ y: on ? 0 : 10, opacity: on ? 1 : 0.5 }}
            transition={{ type: 'spring', stiffness: 500, damping: 12, delay: i * 0.05 }}
          />
        ))}
        <motion.span
          className="ml-3 rounded-full bg-fuchsia-950 px-5 py-2 text-sm font-bold text-white shadow-[0_5px_0_rgba(0,0,0,0.35)]"
          animate={{ rotate: on ? -2 : 0, scale: on ? 1.04 : 1 }}
          transition={{ type: 'spring', stiffness: 350, damping: 12 }}
        >
          Let&rsquo;s go →
        </motion.span>
      </div>
    </div>
  )
}

// ── ecommerce ──────────────────────────────────────────────────────────
const PRODUCTS = [
  { name: 'Aero Runner', price: '$128' },
  { name: 'Trail Mid', price: '$146' },
  { name: 'Court Low', price: '$98' },
]
function EcommerceMock({ on }: MockProps) {
  return (
    <div className="flex h-full w-full flex-col bg-white p-6 text-zinc-900 md:p-8">
      <div className="flex items-center justify-between text-xs">
        <span className="font-semibold tracking-tight">ARCADIA</span>
        <span className="relative" aria-hidden="true">
          Cart
          <motion.span
            className="absolute -right-3.5 -top-1.5 grid h-4 w-4 place-items-center rounded-full bg-rose-600 text-[9px] font-bold text-white"
            animate={{ scale: on ? 1 : 0.5, opacity: on ? 1 : 0 }}
            transition={{ type: 'spring', stiffness: 500, damping: 14 }}
          >
            1
          </motion.span>
        </span>
      </div>
      <div className="mt-4 grid flex-1 grid-cols-3 gap-3">
        {PRODUCTS.map((p, i) => (
          <motion.div
            key={p.name}
            className="flex flex-col"
            animate={{ y: on ? (i === 0 ? -4 : 0) : 10, opacity: on ? 1 : 0.5 }}
            transition={{ duration: 0.3, delay: i * 0.05, ease: QUINT }}
          >
            <div className="relative flex-1 overflow-hidden rounded-lg bg-gradient-to-br from-zinc-100 to-zinc-300">
              {i === 0 && (
                <motion.span
                  className="absolute inset-x-1.5 bottom-1.5 rounded-full bg-zinc-900 py-1 text-center text-[10px] font-medium text-white"
                  animate={{ y: on ? 0 : 26, opacity: on ? 1 : 0 }}
                  transition={{ duration: 0.22, ease: QUINT }}
                  aria-hidden="true"
                >
                  Add to cart
                </motion.span>
              )}
            </div>
            <div className="mt-1.5 flex items-center justify-between text-[10px] md:text-[11px]">
              <span>{p.name}</span>
              <span className="font-semibold tabular-nums">{p.price}</span>
            </div>
          </motion.div>
        ))}
      </div>
    </div>
  )
}

type Profile = {
  key: string
  tempo: string
  signature: string
  Mock: (p: MockProps) => JSX.Element
}

const PROFILES: Profile[] = [
  { key: 'cinematic', tempo: '0.5–1.2s · expo-out', signature: 'Video-first · glass · serif · one accent', Mock: CinematicMock },
  { key: 'product-ui', tempo: '<250ms · crisp', signature: 'Dashboards · semantic color · light + dark', Mock: ProductUiMock },
  { key: 'editorial', tempo: 'reading-paced', signature: 'Prose-first · restrained · paper & ink', Mock: EditorialMock },
  { key: 'playful', tempo: 'springy · bouncy', signature: 'Multi-accent · maximalist · high-contrast', Mock: PlayfulMock },
  { key: 'ecommerce', tempo: 'snappy · 0.2–0.35s', signature: 'Product grid · quick-view · convert', Mock: EcommerceMock },
]

export default function ProfilesStage() {
  const reduce = useReducedMotion() ?? false
  const [active, setActive] = useState(0)
  const [paused, setPaused] = useState(false)
  const [cycle, setCycle] = useState(0) // re-keys the tab progress bar on every advance
  const stageRef = useRef<HTMLDivElement>(null)

  const autoplay = !reduce && !paused
  useEffect(() => {
    if (!autoplay) return
    const id = setInterval(() => {
      setActive((a) => (a + 1) % PROFILES.length)
      setCycle((c) => c + 1)
    }, CYCLE_MS)
    return () => clearInterval(id)
  }, [autoplay])

  const select = (index: number) => {
    setActive(index)
    setCycle((c) => c + 1)
  }

  const onTabsKeyDown = (e: React.KeyboardEvent) => {
    if (e.key !== 'ArrowRight' && e.key !== 'ArrowLeft') return
    e.preventDefault()
    const next = e.key === 'ArrowRight' ? (active + 1) % PROFILES.length : (active - 1 + PROFILES.length) % PROFILES.length
    select(next)
    const tab = document.getElementById(`profile-tab-${PROFILES[next].key}`)
    tab?.focus()
  }

  const current = PROFILES[active]

  return (
    <div id="profiles" className="mx-auto w-full max-w-6xl scroll-mt-28 text-left">
      <p className="eyebrow mb-5 text-center">01 · The range — one engine, five design languages</p>
      <div
        onPointerEnter={() => setPaused(true)}
        onPointerLeave={() => setPaused(false)}
        onFocusCapture={() => setPaused(true)}
        onBlurCapture={() => setPaused(false)}
      >
          {/* tabs */}
          <div
            role="tablist"
            aria-label="Design profiles"
            onKeyDown={onTabsKeyDown}
            className="grid grid-cols-2 gap-2 sm:grid-cols-3 md:flex md:flex-wrap md:justify-center"
          >
            {PROFILES.map((p, i) => {
              const isActive = i === active
              return (
                <button
                  key={p.key}
                  id={`profile-tab-${p.key}`}
                  role="tab"
                  aria-selected={isActive}
                  aria-controls="profile-stage"
                  tabIndex={isActive ? 0 : -1}
                  onClick={() => select(i)}
                  className={`relative overflow-hidden rounded-full px-5 py-2 font-mono text-sm transition-colors active:scale-[0.97] ${
                    isActive ? 'liquid-glass text-white' : 'text-white/55 hover:text-white/85'
                  }`}
                >
                  {p.key}
                  {isActive && autoplay && (
                    <motion.span
                      key={cycle}
                      className="absolute inset-x-1.5 bottom-[3px] block h-px origin-left bg-white/45"
                      initial={{ scaleX: 0 }}
                      animate={{ scaleX: 1 }}
                      transition={{ duration: CYCLE_MS / 1000, ease: 'linear' }}
                      aria-hidden="true"
                    />
                  )}
                </button>
              )
            })}
          </div>

          {/* stage — all five vignettes stay mounted; the active one fades up */}
          <div
            ref={stageRef}
            id="profile-stage"
            role="tabpanel"
            aria-label={`${current.key} — ${current.signature}`}
            className="panel relative mt-6 h-[360px] overflow-hidden rounded-2xl md:h-[420px]"
          >
            {PROFILES.map((p, i) => {
              const isActive = i === active
              return (
                <motion.div
                  key={p.key}
                  className="absolute inset-0"
                  style={{ pointerEvents: isActive ? 'auto' : 'none' }}
                  aria-hidden={!isActive}
                  initial={false}
                  animate={{ opacity: isActive ? 1 : 0, scale: isActive ? 1 : 0.985 }}
                  transition={{ duration: 0.7, ease: EXPO }}
                >
                  <p.Mock on={isActive && !reduce} />
                </motion.div>
              )
            })}
          </div>

          {/* caption */}
          <div className="mt-4 flex flex-col items-center justify-between gap-2 text-sm sm:flex-row">
            <p className="text-white/60">
              <span className="font-mono text-white">{current.key}</span>
              <span className="text-white/40"> — {current.signature}</span>
            </p>
            <span className="whitespace-nowrap rounded-full border border-white/15 px-3 py-1 font-mono text-[11px] text-white/50">
              {current.tempo}
            </span>
          </div>
      </div>
    </div>
  )
}
