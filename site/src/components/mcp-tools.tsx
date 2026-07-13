import { Terminal } from 'lucide-react'
import Reveal from './reveal'

/** The MCP server rendered as the thing it is — a terminal session — instead
 *  of eight identical glass rows. Lines reveal with a cinematic stagger. */
const TOOLS = [
  { name: 'motion_list_profiles', desc: 'the five design languages' },
  { name: 'motion_get_tokens', desc: 'easings, palette & deps per profile' },
  { name: 'motion_suggest_pattern', desc: 'the right motion pattern for an intent' },
  { name: 'motion_easing_rationale', desc: 'which curve, how fast, and why' },
  { name: 'motion_get_template', desc: 'verbatim primitives — glass, glow, keyframes' },
  { name: 'motion_find_reference', desc: 'nearest of 92 corpus prompts' },
  { name: 'motion_validate', desc: 'lint a code string → score + grade' },
  { name: 'motion_validate_file', desc: 'lint a file on disk' },
]

export default function McpTools() {
  return (
    <section id="tools" className="relative z-10 mx-auto max-w-5xl scroll-mt-24 px-6 py-28">
      <Reveal>
        <div className="mb-12 flex flex-col items-center text-center">
          <p className="eyebrow mb-4 inline-flex items-center gap-2">
            <Terminal size={13} aria-hidden="true" />
            05 · Zero-dependency MCP server
          </p>
          <h2 className="font-display text-4xl tracking-tight text-white md:text-5xl">
            <em className="italic text-accent">8</em> tools your agent can call
          </h2>
          <p className="mt-4 max-w-xl text-white/60">
            Taste, exposed as an API — every taste-bearing tool takes a{' '}
            <code className="font-mono text-white/80">profile</code> argument.
          </p>
        </div>
      </Reveal>
      <Reveal delay={120}>
        <div className="panel overflow-hidden rounded-2xl font-mono text-sm">
          {/* window chrome */}
          <div className="flex items-center gap-1.5 border-b border-white/10 px-5 py-3.5">
            <span className="h-3 w-3 rounded-full bg-white/15" aria-hidden="true" />
            <span className="h-3 w-3 rounded-full bg-white/15" aria-hidden="true" />
            <span className="h-3 w-3 rounded-full bg-white/15" aria-hidden="true" />
            <span className="ml-3 text-xs text-white/40">motion-site-tools — stdio</span>
          </div>
          <div className="p-6 md:p-8">
            <p className="text-white/70">
              <span className="text-white/35">$ </span>
              python3 skills/motion-site-builder/scripts/server.py
              <span className="text-accent"> · connected</span>
            </p>
            <div className="mt-6 grid gap-x-10 gap-y-3 sm:grid-cols-2">
              {TOOLS.map((tool, index) => (
                <Reveal key={tool.name} delay={index * 60}>
                  <p className="min-w-0">
                    <span className="text-accent" aria-hidden="true">▸ </span>
                    <code className="text-white">{tool.name}</code>
                    <span className="block pl-4 text-xs leading-relaxed text-white/45 sm:pl-0 sm:text-[13px]">
                      {tool.desc}
                    </span>
                  </p>
                </Reveal>
              ))}
            </div>
            <p className="mt-7 text-xs leading-relaxed text-white/50">
              every taste-bearing tool takes profile=&lt;cinematic·product-ui·editorial·playful·ecommerce&gt;
            </p>
          </div>
        </div>
      </Reveal>
    </section>
  )
}
