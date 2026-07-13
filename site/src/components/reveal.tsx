import { useEffect, useRef, useState, type ReactNode } from 'react'

/**
 * Scroll-reveal that cannot strand content invisible. The old framer-motion
 * whileInView left whole sections at opacity 0 when the user deep-linked or
 * scrolled fast (the observer never saw them "enter"). This hook:
 *   1. shows immediately anything already at/above the viewport on mount, and
 *   2. observes the rest with a forgiving bottom margin.
 * The visual comes from the CSS .reveal/.is-in transition (interruptible),
 * collapsed by the prefers-reduced-motion block in index.css.
 */
export function useInViewOnce<T extends HTMLElement>() {
  const ref = useRef<T | null>(null)
  const [inView, setInView] = useState(false)

  useEffect(() => {
    const el = ref.current
    if (!el) return
    if (el.getBoundingClientRect().top < window.innerHeight * 0.92 || !('IntersectionObserver' in window)) {
      setInView(true)
      return
    }
    const io = new IntersectionObserver(
      (entries) => {
        if (entries.some((e) => e.isIntersecting)) {
          setInView(true)
          io.disconnect()
        }
      },
      { rootMargin: '0px 0px -8% 0px' },
    )
    io.observe(el)
    return () => io.disconnect()
  }, [])

  return { ref, inView }
}

type RevealProps = {
  children: ReactNode
  className?: string
  /** transition-delay in ms — keep within the cinematic stagger budget (80–200ms steps) */
  delay?: number
}

export default function Reveal({ children, className = '', delay = 0 }: RevealProps) {
  const { ref, inView } = useInViewOnce<HTMLDivElement>()
  return (
    <div
      ref={ref}
      className={`reveal ${inView ? 'is-in' : ''} ${className}`}
      style={delay ? { transitionDelay: `${delay}ms` } : undefined}
    >
      {children}
    </div>
  )
}
