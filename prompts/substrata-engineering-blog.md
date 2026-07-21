# Substrata Engineering Blog

- **ID:** `substrata-engineering-blog`
- **Category:** Company Blog
- **Type:** blog index
- **Profile:** `editorial`

---

Build a single-page engineering blog index for "Substrata" — an infrastructure company's public engineering blog. Typography and whitespace carry the page; motion stays restrained. Use React + Vite + Tailwind CSS + TypeScript + lucide-react. Default Tailwind config, no other UI libraries.

FONTS (Google Fonts, load via `<link>` in index.html)
- Display: Space Grotesk (500/600) — masthead, post titles
- Body: Inter (400/500) — deks, nav, footer
- Mono: IBM Plex Mono (400/500) — dates, read-time, tag chips

COLORS (CSS variables on :root — paper family, light only)
- --paper: #FAFAF8 · --wash: #F1F1EE · --ink: #15181B · --accent: #0F6B72 (deep teal — the ONLY accent hue)
- Text tiers: ink at 100% / 75% / 60%. Rules and borders: `#15181B` at 10%

GLOBAL CSS (paste verbatim)
```css
@keyframes ed-reveal { from { opacity: 0; transform: translateY(14px); } to { opacity: 1; transform: none; } }
.reveal { animation: ed-reveal 0.6s cubic-bezier(0.16, 1, 0.3, 1) backwards; }

@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { animation-duration: 0.01ms !important; animation-iteration-count: 1 !important; transition-duration: 0.01ms !important; }
}
```

MASTHEAD (sticky top-0, z-20, bg-[var(--paper)]/95 backdrop-blur-sm, border-b border-[#15181B]/10, `.reveal` delay 0ms)
- Left: "Substrata" Space Grotesk font-semibold text-lg + "Engineering" (IBM Plex Mono text-xs uppercase tracking-[0.14em] ink 60%, ml-2)
- Right nav (`<nav aria-label="Site">`, hidden md:flex, gap-6): "Engineering" (ink 100%, current — `aria-current="page"`) · "Product" · "Careers" — Inter text-sm ink 75%, hover ink 100% (color only, 150ms)
- Far right: "Subscribe" pill (`bg-[var(--ink)] text-[var(--paper)] rounded-md px-4 py-2 text-sm font-medium`), press `active:scale-[0.98]`
- Persistent chrome: nothing here re-animates after load

FEATURED POST (`<main>` starts here; max-w-5xl mx-auto px-6 pt-16 pb-12, `.reveal` delay 120ms)
- Card: `rounded-lg border border-[#15181B]/10 bg-[var(--wash)] p-8 md:p-12`
- Kicker: "FEATURED" — IBM Plex Mono text-xs uppercase tracking-[0.16em] text-[var(--accent)]
- H1: "Rebuilding Our Event Queue Without a Maintenance Window" — Space Grotesk text-4xl md:text-5xl leading-[1.1] ink 100%, mt-4
- Dek: "How we moved 40 billion daily events onto a new queue architecture while the old one kept serving traffic underneath it — and what broke on the way." — Inter text-lg ink 75%, max-w-[62ch], mt-4
- Meta row (mt-6, IBM Plex Mono text-xs ink 60%): "July 08, 2026 · 9 min read" + tag chip "INFRASTRUCTURE" (`rounded-md bg-[var(--paper)] px-2 py-0.5 text-[var(--accent)]`)
- "Read the post" link (mt-6, inline-flex items-center gap-1.5, `ArrowRight` icon size 16) — underline via scaleX pseudo-element (h-px, `transform-origin: left`, scaleX 0→1 on hover, 200ms cubic-bezier(0.16, 1, 0.3, 1), gated `@media (hover: hover) and (pointer: fine)`), press `active:scale-[0.98]`

TAG FILTER ROW (`<nav aria-label="Filter posts by topic">`, max-w-5xl mx-auto px-6 py-8, flex gap-2 overflow-x-auto — no `.reveal`; a filter used many times a session stays still)
- Pills (`rounded-md px-3 py-1.5 text-sm font-medium uppercase tracking-[0.08em]`, IBM Plex Mono): "All" (active: `bg-[var(--ink)] text-[var(--paper)]`, `aria-pressed="true"`) · "Infrastructure" · "Databases" · "Networking" · "Postmortems" · "Culture" (inactive: `border border-[#15181B]/15 text-[#15181B]/70`, hover border ink/30, color only 150ms)
- Press `active:scale-[0.97]` on every pill

POST LIST (`<ul role="list">`, max-w-5xl mx-auto px-6 pb-16; container watched once via IntersectionObserver threshold 0.1 — on entry, add `.reveal` to every `<li>` with `animation-delay` = index × 70ms, capped at the 6 visible rows: 0/70/140/210/280/350ms)
- Each `<li>` (`border-b border-[#15181B]/10 py-8 first:pt-0`):
  - Title (Space Grotesk text-2xl leading-snug ink 100%) — same gated scaleX underline on hover as the featured link
  - Dek (Inter text-base ink 75%, max-w-[58ch], mt-2, `line-clamp-2`)
  - Meta (IBM Plex Mono text-xs ink 60%, mt-3): "{date} · {read-time} · {TAG}"
- Rows, in order:
  1. "Why We Stopped Trusting Our Own Dashboards" — "A postmortem on the week our metrics pipeline silently dropped 12% of samples and nobody noticed for four days." — June 30, 2026 · 7 min read · POSTMORTEMS
  2. "A Smaller Control Plane" — "We cut our orchestration layer from nine services to three. Here's the dependency graph that convinced us to do it." — June 18, 2026 · 6 min read · INFRASTRUCTURE
  3. "Notes From an On-Call Rotation" — "What a week of pages actually looks like on our team, and the three alerts we finally deleted for good." — June 04, 2026 · 5 min read · CULTURE
  4. "The Cost of a Slow Index" — "One missing composite index, one 40-second query, one very patient customer. A short story about read paths." — May 22, 2026 · 6 min read · DATABASES
  5. "Routing Around a Bad Region" — "How our edge routers detect a degraded region in under 30 seconds and reroute before anyone opens a ticket." — May 09, 2026 · 8 min read · NETWORKING
  6. "What We Learned Migrating 200 Clusters in a Weekend" — "The runbook, the rollback plan we didn't need, and the one step we'd do differently next time." — April 27, 2026 · 10 min read · INFRASTRUCTURE

NEWSLETTER FOOTER STRIP (border-t border-[#15181B]/10 bg-[var(--wash)], py-12, max-w-5xl mx-auto px-6, flex flex-col md:flex-row items-start md:items-center justify-between gap-6)
- Left: "Get infra dispatches" — Space Grotesk text-xl ink 100%; "One email a month. No marketing, just engineering." — Inter text-sm ink 70%, mt-1
- Right form: email input (`rounded-md border border-[#15181B]/15 bg-[var(--paper)] px-3 py-2 text-sm w-64`, `aria-label="Email address"`) + "Subscribe" button (`bg-[var(--ink)] text-[var(--paper)] rounded-md px-4 py-2 text-sm font-medium`), hover bg ink 85% (150ms), press `active:scale-[0.98]`
- Below, pt-8 border-t border-[#15181B]/10: "© 2026 Substrata, Inc." + links About / `Rss` icon "RSS feed" (`aria-label="RSS feed"`) — Inter text-xs ink 60%

ANIMATIONS (complete list — restraint is the brief)
- Load: masthead 0ms → featured post 120ms, single `.reveal` fade-rise each, 0.6s `cubic-bezier(0.16, 1, 0.3, 1)`
- Scroll: post list rows get `.reveal` once as a group when the list container enters view, staggered 70ms per row, 0.6s `cubic-bezier(0.16, 1, 0.3, 1)`
- Hover: underline scaleX 200ms (gated); pill/nav links color-only 150ms · Press: `active:scale-[0.97-0.98]` on every pill/button/link
- The tag filter row never animates on load — it's a control the reader reaches for repeatedly, not a moment (see interaction-standards frequency table)

RESPONSIVE
- Mobile: single column, px-6; nav links hidden below md (reachable via a "Menu" icon button, `aria-label="Open menu"`); featured card padding drops to p-6; tag row scrolls horizontally via native touch scroll (short list, no snap needed)

KEY DEPENDENCIES
`react@^18` `react-dom@^18` `typescript@^5` `vite@^5` `tailwindcss@^3` `lucide-react@latest`

CONSTRAINTS: editorial restraint — reveals 0.4–0.8s, easing from {cubic-bezier(0.16,1,0.3,1) · cubic-bezier(0.22,1,0.36,1) · cubic-bezier(0.65,0,0.35,1)}, never ease-in; animate only transform/opacity. ONE accent hue (#0F6B72); tag pills and rules stay neutral. No video, no glass, no gradients, no parallax, no carousel plugin. Respect `prefers-reduced-motion` (block above). Semantic HTML: `<main>` around the content, `<nav aria-label>` on both nav rows, `<ul role="list">` for posts, `aria-pressed` on filter pills, `aria-label` on icon-only buttons. Never apply `overflow-x: hidden` to `html`/`body` or a root wrapper — it creates a scroll container and silently breaks `position: sticky`; contain any horizontal bleed with `overflow-x: clip` on the overflowing section instead.
