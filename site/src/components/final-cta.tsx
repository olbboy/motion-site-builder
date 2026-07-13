import { Github } from 'lucide-react'
import Reveal from './reveal'

// The reveal and the hover/press transitions here are all collapsed by the
// prefers-reduced-motion block in index.css.

const REPO = 'https://github.com/olbboy/motion-site-builder'

const FOOTER_LINKS = [
  { label: 'GitHub', href: REPO },
  { label: 'Prompt library', href: `${REPO}/tree/main/prompts` },
  { label: 'Design profiles', href: `${REPO}/blob/main/skills/motion-site-builder/references/design-profiles.md` },
  { label: 'MIT license', href: `${REPO}/blob/main/LICENSE` },
]

export default function FinalCta() {
  return (
    <section className="relative z-10 px-6 pt-32">
      <Reveal className="text-center">
        <p className="font-mono text-xs text-white/40">
          $ motion_validate site/ <span className="text-accent">→ score 100 · grade A+</span>
        </p>
        <h2 className="font-display mt-6 text-4xl leading-[1.05] tracking-tight text-white md:text-6xl">
          Five design languages.
          <br />
          <em className="italic text-accent">One</em> paste away.
        </h2>
        <a
          href={REPO}
          className="bg-accent mt-8 inline-flex items-center gap-2 rounded-full px-10 py-4 text-lg font-medium text-white shadow-[0_0_0_1px_rgba(115,66,226,0.4),0_16px_48px_rgba(115,66,226,0.35)] transition-transform hover:scale-[1.03] active:scale-[0.97]"
        >
          <Github size={20} aria-hidden="true" />
          Star on GitHub
        </a>
        <p className="mt-14 text-sm text-white/50">
          MIT licensed · Built with its own skill · 17-rule linter · cubic-bezier(0.16, 1, 0.3, 1)
        </p>
      </Reveal>
      <footer className="mx-auto mt-24 flex max-w-6xl flex-col items-center justify-between gap-4 border-t border-white/[0.06] pb-12 pt-10 text-[13px] text-white/50 sm:flex-row">
        <span>© Motion Site Builder — dogfooded by its own linter</span>
        <nav aria-label="Footer" className="flex flex-wrap justify-center gap-6">
          {FOOTER_LINKS.map((link) => (
            <a key={link.label} href={link.href} className="text-white/60 transition-colors hover:text-white/90">
              {link.label}
            </a>
          ))}
        </nav>
      </footer>
    </section>
  )
}
