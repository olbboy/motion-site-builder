import { useEffect, useRef } from 'react'

/**
 * Cinematic ambient backdrop — owned, procedural media standing in for the
 * profile's {YOUR_VIDEO_URL}. Three aurora curtains, each drawn as dozens of
 * thin filament polylines flowing horizontally (anisotropic — it reads as
 * directed light, not blurry blobs), with a soft edge vignette for legibility.
 *
 * Perf: capped at ~30fps and DPR 1.5, paused when the tab is hidden.
 * prefers-reduced-motion renders a single static frame.
 */

type Band = {
  yc: number // curtain center, fraction of height
  amp: number // undulation amplitude, fraction of height
  spread: number // filament spread, fraction of height
  lines: number
  speed: number
  rgb: string
  alpha: number
}

const BANDS: Band[] = [
  { yc: 0.26, amp: 0.09, spread: 0.16, lines: 44, speed: 0.55, rgb: '139, 92, 246', alpha: 0.1 },
  { yc: 0.52, amp: 0.13, spread: 0.22, lines: 56, speed: 0.38, rgb: '115, 66, 226', alpha: 0.085 },
  { yc: 0.78, amp: 0.07, spread: 0.13, lines: 36, speed: 0.72, rgb: '88, 46, 178', alpha: 0.1 },
]

const FRAME_MS = 33 // ~30fps — plenty for slow ambient drift, kind to the main thread

function filamentY(band: Band, x: number, time: number, line: number, h: number): number {
  return (
    (band.yc +
      Math.sin(x * 0.0016 + time * band.speed * 7 + line * 0.17) * band.amp * 0.55 +
      Math.sin(x * 0.0007 - time * band.speed * 5 + line * 0.045) * band.amp) *
    h
  )
}

export default function AuroraBackground() {
  const canvasRef = useRef<HTMLCanvasElement>(null)

  useEffect(() => {
    const canvas = canvasRef.current
    if (!canvas) return
    const ctx = canvas.getContext('2d')
    if (!ctx) return

    const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches
    const dpr = Math.min(window.devicePixelRatio || 1, 1.5)
    let raf = 0
    let hidden = false
    let last = 0

    const resize = () => {
      canvas.width = canvas.clientWidth * dpr
      canvas.height = canvas.clientHeight * dpr
    }

    const draw = (t: number) => {
      const { width: w, height: h } = canvas
      ctx.clearRect(0, 0, w, h)
      // ambient bloom first — a soft violet ellipse behind the content cluster
      const bloom = ctx.createRadialGradient(w * 0.5, h * 0.4, 0, w * 0.5, h * 0.4, Math.max(w, h) * 0.5)
      bloom.addColorStop(0, 'rgba(115, 66, 226, 0.16)')
      bloom.addColorStop(0.55, 'rgba(115, 66, 226, 0.05)')
      bloom.addColorStop(1, 'rgba(115, 66, 226, 0)')
      ctx.fillStyle = bloom
      ctx.fillRect(0, 0, w, h)
      ctx.globalCompositeOperation = 'lighter'
      ctx.lineWidth = Math.max(1, dpr)
      const time = t * 0.00009
      const step = Math.max(18, w / 56)

      for (const band of BANDS) {
        for (let i = 0; i < band.lines; i++) {
          const rel = i / (band.lines - 1) - 0.5 // -0.5..0.5 across the curtain
          // filaments near the curtain's core glow brighter than its fringes
          const coreGlow = 1 - Math.abs(rel) * 1.6
          if (coreGlow <= 0) continue
          const off = rel * band.spread * h
          ctx.strokeStyle = `rgba(${band.rgb}, ${band.alpha * coreGlow})`
          ctx.beginPath()
          for (let x = -step; x <= w + step; x += step) {
            const y = filamentY(band, x, time, i, h) + off
            if (x === -step) ctx.moveTo(x, y)
            else ctx.lineTo(x, y)
          }
          ctx.stroke()
        }
        // one white core filament per curtain for a specular shimmer
        ctx.strokeStyle = 'rgba(255, 255, 255, 0.09)'
        ctx.beginPath()
        for (let x = -step; x <= w + step; x += step) {
          const y = filamentY(band, x, time, 0, h)
          if (x === -step) ctx.moveTo(x, y)
          else ctx.lineTo(x, y)
        }
        ctx.stroke()
      }

      // edge vignette keeps the display type legible over the brightest filaments
      ctx.globalCompositeOperation = 'source-over'
      const vg = ctx.createRadialGradient(
        w * 0.5, h * 0.38, Math.min(w, h) * 0.28,
        w * 0.5, h * 0.5, Math.max(w, h) * 0.75,
      )
      vg.addColorStop(0, 'rgba(12, 12, 12, 0)')
      vg.addColorStop(1, 'rgba(12, 12, 12, 0.55)')
      ctx.fillStyle = vg
      ctx.fillRect(0, 0, w, h)
    }

    const loop = (now: number) => {
      if (!hidden && now - last >= FRAME_MS) {
        last = now
        draw(now)
      }
      raf = requestAnimationFrame(loop)
    }

    const onVisibility = () => {
      hidden = document.hidden
    }

    resize()
    window.addEventListener('resize', resize)

    if (reduceMotion) {
      draw(24000) // one static frame at a pleasant phase — the curtains hold still
    } else {
      document.addEventListener('visibilitychange', onVisibility)
      raf = requestAnimationFrame(loop)
    }

    return () => {
      cancelAnimationFrame(raf)
      window.removeEventListener('resize', resize)
      document.removeEventListener('visibilitychange', onVisibility)
    }
  }, [])

  return (
    <div className="fixed inset-0 z-0" aria-hidden="true">
      <canvas ref={canvasRef} className="h-full w-full" />
      {/* contrast overlay keeps text tiers readable over the brightest filaments */}
      <div className="absolute inset-0 z-[1] bg-black/40" />
    </div>
  )
}
