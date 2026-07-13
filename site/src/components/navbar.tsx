import { Github } from 'lucide-react'

// Hover/press transitions here are collapsed by the prefers-reduced-motion
// block in index.css.

const REPO = 'https://github.com/olbboy/motion-site-builder'

const LINKS = [
  { label: 'Profiles', href: '#profiles' },
  { label: 'How it works', href: '#how' },
  { label: 'Skills', href: '#skills' },
  { label: 'Tools', href: '#tools' },
]

/** Brand mark — the signature easing curve, cubic-bezier(0.16, 1, 0.3, 1),
 *  with its playhead at rest. Mirrors /logo.svg (kept inline so the navbar
 *  needs no fetch and the curve stays crisp at 22px). */
function BrandMark({ size = 22 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 64 64" fill="none" aria-hidden="true">
      <rect width="64" height="64" rx="15" fill="#0C0C0C" />
      <rect x="0.75" y="0.75" width="62.5" height="62.5" rx="14.25" stroke="white" strokeOpacity="0.14" strokeWidth="1.5" />
      <path d="M16 46 C21.12 18 25.6 18 48 18" stroke="var(--accent)" strokeWidth="5.5" strokeLinecap="round" />
      <circle cx="48" cy="18" r="4.2" fill="white" />
    </svg>
  )
}

export default function Navbar() {
  return (
    <nav className="sticky top-0 z-30 px-6 pt-5" aria-label="Main">
      <div className="mx-auto flex h-[52px] max-w-5xl items-center justify-between rounded-full border border-white/10 bg-white/[0.04] px-5 shadow-[0_8px_32px_rgba(0,0,0,0.4)] backdrop-blur-xl">
        <div className="flex items-center">
          <BrandMark />
          <span className="ml-2.5 text-[15px] font-semibold tracking-tight text-white">
            Motion Site Builder
          </span>
          <div className="ml-8 hidden items-center gap-7 md:flex">
            {LINKS.map((link) => (
              <a
                key={link.label}
                href={link.href}
                className="text-[13px] font-medium text-white/60 transition-colors hover:text-white/90"
              >
                {link.label}
              </a>
            ))}
          </div>
        </div>
        <a
          href={REPO}
          className="bg-accent flex items-center gap-2 rounded-full px-4 py-1.5 text-[13px] font-medium text-white shadow-[0_0_0_1px_rgba(115,66,226,0.4),0_8px_24px_rgba(115,66,226,0.3)] transition-transform hover:scale-[1.03] active:scale-[0.97]"
          aria-label="Star Motion Site Builder on GitHub"
        >
          <Github size={15} aria-hidden="true" />
          Star on GitHub
        </a>
      </div>
    </nav>
  )
}
