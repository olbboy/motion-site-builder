import { useState } from 'react'
import { ArrowUpRight, FileText } from 'lucide-react'
import Reveal from './reveal'

/**
 * Proof section — real sites generated from the library's prompts and published
 * live. Cards are self-hosted thumbnails (site/public/showcase/<id>.png) that
 * link out to the live build; a second link opens the exact prompt in the repo.
 * External hosts (lovable.app) set frame-ancestors, so we thumbnail → click-out
 * rather than iframe. Motion is transform/opacity only, and every transition
 * here is collapsed by the prefers-reduced-motion block in index.css.
 */

const REPO_PROMPTS = 'https://github.com/olbboy/motion-site-builder/blob/main/prompts'

type Profile = 'cinematic' | 'product-ui' | 'editorial' | 'playful' | 'ecommerce'

type Item = {
  id: string
  title: string
  tagline: string
  profile: Profile
  prompt: string // filename under prompts/
  url: string // live published build
}

// Live builds — generated from these prompts, published on Lovable.
const ITEMS: Item[] = [
  { id: 'skyelite', title: 'SkyElite', tagline: 'Private-jet membership', profile: 'cinematic', prompt: 'skyelite-hero.md', url: 'https://msb-skyelite.lovable.app/' },
  { id: 'pulsegrid', title: 'PulseGrid', tagline: 'Subscription analytics', profile: 'product-ui', prompt: 'pulsegrid-analytics-dashboard.md', url: 'https://pulsegrid-pulse-stream.lovable.app/' },
  { id: 'aperture', title: 'Aperture', tagline: 'Workspace settings', profile: 'product-ui', prompt: 'aperture-team-settings.md', url: 'https://aperture-settings-hub.lovable.app/' },
  { id: 'meridian', title: 'Meridian', tagline: 'Slow-journalism longread', profile: 'editorial', prompt: 'meridian-longread-article.md', url: 'https://msb-meridian.lovable.app/' },
  { id: 'ledgerline', title: 'Ledgerline', tagline: 'API changelog', profile: 'editorial', prompt: 'ledgerline-changelog.md', url: 'https://ledger-recap.lovable.app/' },
  { id: 'fizzpop', title: 'FizzPop', tagline: 'Craft-soda landing', profile: 'playful', prompt: 'fizzpop-soda-landing.md', url: 'https://msb-fizzpop.lovable.app/' },
  { id: 'pixeljam', title: 'PixelJam', tagline: 'Arcade-fest event', profile: 'playful', prompt: 'pixeljam-arcade-fest.md', url: 'https://msb-pixeljam.lovable.app/' },
  { id: 'arcadia', title: 'Arcadia Goods', tagline: 'Outdoor-gear storefront', profile: 'ecommerce', prompt: 'arcadia-goods-storefront.md', url: 'https://msb-arcadia.lovable.app/' },
  { id: 'maison', title: 'Maison Ondes', tagline: 'Boutique fragrance page', profile: 'ecommerce', prompt: 'maison-ondes-product-page.md', url: 'https://msb-maison.lovable.app/' },
  { id: 'aurelia', title: 'Aurelia', tagline: 'Haute-horlogerie waitlist', profile: 'cinematic', prompt: 'aurelia-landing.md', url: 'https://aurelia-one-a-year.lovable.app/' },
  { id: 'relay', title: 'Relay', tagline: 'On-call incident console', profile: 'product-ui', prompt: 'relay-incident-console.md', url: 'https://incident-whisper-44.lovable.app/' },
  { id: 'praxis', title: 'Praxis', tagline: 'Developer documentation', profile: 'editorial', prompt: 'praxis-docs-page.md', url: 'https://praxis-docu-shine.lovable.app/' },
  { id: 'bloop', title: 'Bloop', tagline: 'Analog synth plugin', profile: 'playful', prompt: 'bloop-synth-plugin.md', url: 'https://bloop-neon-groove.lovable.app/' },
  { id: 'glyphery', title: 'Glyphery', tagline: 'Digital type foundry', profile: 'ecommerce', prompt: 'glyphery-type-foundry-shop.md', url: 'https://glyphery-type-shop.lovable.app/' },
]

const FILTERS: Array<{ key: Profile | 'all'; label: string }> = [
  { key: 'all', label: 'all' },
  { key: 'cinematic', label: 'cinematic' },
  { key: 'product-ui', label: 'product-ui' },
  { key: 'editorial', label: 'editorial' },
  { key: 'playful', label: 'playful' },
  { key: 'ecommerce', label: 'ecommerce' },
]

function Card({ item, index }: { item: Item; index: number }) {
  // A thumbnail may not be captured yet; degrade to a tinted placeholder
  // instead of a broken-image icon.
  const [broken, setBroken] = useState(false)
  return (
    <Reveal delay={(index % 3) * 80}>
      <div className="panel group h-full overflow-hidden rounded-2xl">
        <a
          href={item.url}
          target="_blank"
          rel="noopener noreferrer"
          className="relative block aspect-[16/10] overflow-hidden bg-white/[0.02]"
          aria-label={`Open the live ${item.title} build in a new tab`}
        >
          {broken ? (
            <span className="font-display absolute inset-0 flex items-center justify-center text-2xl text-white/25">
              {item.title}
            </span>
          ) : (
            <img
              src={`showcase/${item.id}.png`}
              alt={`${item.title} — built from the ${item.profile} prompt`}
              loading="lazy"
              onError={() => setBroken(true)}
              className="h-full w-full object-cover object-top transition-transform duration-500 group-hover:scale-[1.04]"
            />
          )}
          <span className="absolute right-3 top-3 inline-flex items-center gap-1 rounded-full bg-black/55 px-2.5 py-1 text-[11px] font-medium text-white opacity-0 backdrop-blur-sm transition-opacity duration-200 group-hover:opacity-100">
            View live <ArrowUpRight size={12} aria-hidden="true" />
          </span>
        </a>
        <div className="flex items-start justify-between gap-3 p-5">
          <div className="min-w-0">
            <h3 className="text-[15px] font-medium text-white">{item.title}</h3>
            <p className="mt-0.5 text-sm text-white/50">{item.tagline}</p>
          </div>
          <span className="shrink-0 whitespace-nowrap rounded-full border border-white/15 px-2.5 py-0.5 font-mono text-[11px] text-white/55">
            {item.profile}
          </span>
        </div>
        <div className="flex items-center gap-4 border-t border-white/[0.06] px-5 py-3 text-[13px]">
          <a
            href={item.url}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-1 text-white/70 transition-colors hover:text-white active:scale-[0.98]"
          >
            Live <ArrowUpRight size={13} aria-hidden="true" />
          </a>
          <a
            href={`${REPO_PROMPTS}/${item.prompt}`}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-1 text-white/50 transition-colors hover:text-white/80 active:scale-[0.98]"
          >
            <FileText size={13} aria-hidden="true" /> Prompt
          </a>
        </div>
      </div>
    </Reveal>
  )
}

export default function Showcase() {
  const [filter, setFilter] = useState<Profile | 'all'>('all')
  const shown = filter === 'all' ? ITEMS : ITEMS.filter((i) => i.profile === filter)

  return (
    <section id="showcase" className="relative z-10 mx-auto max-w-6xl scroll-mt-24 px-6 py-28">
      <Reveal>
        <p className="eyebrow mb-4">02 · The proof</p>
        <h2 className="font-display mb-4 text-4xl tracking-tight text-white md:text-5xl">
          Real sites, from these <em className="italic text-accent">prompts</em>.
        </h2>
        <p className="mb-10 max-w-xl text-white/60">
          Each card is a live build generated from a prompt in the library. Open the site, then read
          the exact prompt that produced it.
        </p>
      </Reveal>

      <Reveal delay={80}>
        <div role="tablist" aria-label="Filter by design profile" className="mb-8 flex flex-wrap gap-2">
          {FILTERS.map((f) => {
            const active = filter === f.key
            return (
              <button
                key={f.key}
                role="tab"
                aria-selected={active}
                onClick={() => setFilter(f.key)}
                className={`rounded-full px-4 py-1.5 font-mono text-[13px] transition-colors active:scale-[0.97] ${
                  active ? 'liquid-glass text-white' : 'text-white/45 hover:text-white/80'
                }`}
              >
                {f.label}
              </button>
            )
          })}
        </div>
      </Reveal>

      <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
        {shown.map((item, index) => (
          <Card key={item.id} item={item} index={index} />
        ))}
      </div>
    </section>
  )
}
