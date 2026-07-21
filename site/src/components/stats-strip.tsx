import { useEffect, useState } from 'react'
import { useInViewOnce } from './reveal'

const STATS = [
  { value: 5, label: 'design profiles' },
  { value: 20, label: 'motion lint rules' },
  { value: 54, label: 'curated prompts' },
  { value: 8, label: 'MCP tools' },
]

/** Counts 0 → target once the strip enters the viewport (900ms, quart-out —
 *  text swaps only, no layout properties). Reduced motion jumps straight to
 *  the final value. */
function useCountUp(target: number, started: boolean) {
  const [value, setValue] = useState(0)
  useEffect(() => {
    if (!started) return
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
      setValue(target)
      return
    }
    let raf = 0
    const t0 = performance.now()
    const tick = (now: number) => {
      const p = Math.min((now - t0) / 900, 1)
      setValue(Math.round(target * (1 - Math.pow(1 - p, 4))))
      if (p < 1) raf = requestAnimationFrame(tick)
    }
    raf = requestAnimationFrame(tick)
    return () => cancelAnimationFrame(raf)
  }, [started, target])
  return value
}

function Stat({ value, label, started }: { value: number; label: string; started: boolean }) {
  const shown = useCountUp(value, started)
  return (
    <div className="px-4">
      {/* min-width in ch prevents any layout shift while the number counts */}
      <div className="font-display text-6xl tracking-tight text-white md:text-7xl" style={{ minWidth: `${String(value).length}ch` }}>
        {shown}
      </div>
      <div className="mt-2 text-xs uppercase tracking-[0.18em] text-white/50">{label}</div>
    </div>
  )
}

export default function StatsStrip() {
  const { ref, inView } = useInViewOnce<HTMLDivElement>()
  return (
    <section className="relative z-10 border-t border-white/5 py-16">
      <div
        ref={ref}
        className={`reveal ${inView ? 'is-in' : ''} mx-auto grid max-w-4xl grid-cols-2 gap-y-10 px-6 text-center md:grid-cols-4 md:divide-x md:divide-white/10`}
      >
        {STATS.map((stat) => (
          <Stat key={stat.label} value={stat.value} label={stat.label} started={inView} />
        ))}
      </div>
    </section>
  )
}
