import { Hammer, ScanLine, Sparkles } from 'lucide-react'
import Reveal from './reveal'

const REPO = 'https://github.com/olbboy/motion-site-builder/tree/main/skills'

const SKILLS = [
  {
    icon: Hammer,
    name: 'motion-site-builder',
    tag: 'build',
    body: 'Plan → Build → Validate in 15 steps. Emits a runnable React project or a portable one-shot prompt for Bolt, Lovable, v0 or Cursor.',
    invoke: '"Build a cinematic hero for my AI startup"',
    href: `${REPO}/motion-site-builder`,
  },
  {
    icon: ScanLine,
    name: 'review-motion',
    tag: 'review',
    body: 'Strict diff review of a change — a Before/After table keyed to the rules, then a decisive Block or Approve. No vibes.',
    invoke: '"Review the motion in this component"',
    href: `${REPO}/review-motion`,
  },
  {
    icon: Sparkles,
    name: 'improve-motion',
    tag: 'audit',
    body: 'Audit a whole codebase and hand back self-contained fix plans a cheaper model can execute — each scoped to one file and rule.',
    invoke: '"Improve the animations in this app"',
    href: `${REPO}/improve-motion`,
  },
]

export default function SkillsSuite() {
  return (
    <section id="skills" className="relative z-10 mx-auto max-w-6xl scroll-mt-24 px-6 py-28">
      <Reveal>
        <p className="eyebrow mb-4">04 · The suite</p>
        <h2 className="font-display mb-4 text-4xl tracking-tight text-white md:text-5xl">
          One engine. <em className="italic text-accent">Three</em> skills.
        </h2>
        <p className="mb-14 max-w-xl text-white/60">
          Build, review, and audit — sharing one linter, one token set, one standard. Method skills,
          not copies.
        </p>
      </Reveal>
      <Reveal delay={120}>
        {/* one shared panel with rules between cells — a single object, not three more cards */}
        <div className="panel grid overflow-hidden rounded-2xl md:grid-cols-3 md:divide-x md:divide-white/10">
          {SKILLS.map((skill) => (
            <a
              key={skill.name}
              href={skill.href}
              className="group flex flex-col border-t border-white/10 p-8 transition-colors first:border-t-0 hover:bg-white/[0.04] active:scale-[0.99] md:border-t-0"
            >
              <div className="flex items-center justify-between">
                <skill.icon size={24} className="text-accent" aria-hidden="true" />
                <span className="rounded-full border border-white/15 px-2.5 py-0.5 font-mono text-[11px] uppercase tracking-wider text-white/50">
                  {skill.tag}
                </span>
              </div>
              <h3 className="mt-5 font-mono text-lg font-medium text-white">{skill.name}</h3>
              <p className="mt-2.5 flex-1 text-sm leading-relaxed text-white/60">{skill.body}</p>
              <p className="mt-6 font-mono text-xs leading-relaxed text-white/50">
                <span className="text-accent">›</span> {skill.invoke}
              </p>
            </a>
          ))}
        </div>
      </Reveal>
    </section>
  )
}
