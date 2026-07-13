# Praxis Docs

- **ID:** `praxis-docs-page`
- **Category:** Developer Docs
- **Type:** docs
- **Profile:** `editorial`

---

Build a single-page developer documentation page for "Praxis" — a fictional CLI tool for scaffolding and deploying backend services. Documentation typography: calm, scannable, permanent-feeling. Use React + Vite + Tailwind CSS + TypeScript + @tailwindcss/typography + lucide-react. Default Tailwind config (plus the typography plugin), no other UI libraries.

FONTS (Google Fonts, load via `<link>` in index.html)
- Display: Newsreader (500/600) — page title, H2 section headings
- Body + UI: Inter (400/500/600) — prose, sidebar, TOC, buttons
- Code: IBM Plex Mono (400/500) — inline code, code blocks, keyboard hint

COLORS (CSS variables on :root — paper family, light only)
- --paper: #FFFFFF · --wash: #F5F5F7 · --ink: #18181B · --accent: #4338CA (indigo — the ONLY accent hue)
- Text tiers: ink at 100% / 75% / 60%. Rules and borders: `#18181B` at 10%

GLOBAL CSS (paste verbatim)
```css
@keyframes ed-reveal { from { opacity: 0; transform: translateY(12px); } to { opacity: 1; transform: none; } }
.reveal { animation: ed-reveal 0.55s cubic-bezier(0.22, 1, 0.36, 1) backwards; }

@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { animation-duration: 0.01ms !important; animation-iteration-count: 1 !important; transition-duration: 0.01ms !important; }
}
```

HEADER (sticky top-0, z-30, bg-[var(--paper)]/95 backdrop-blur-sm, border-b border-[#18181B]/10 — persistent, no reveal)
- Left: "Praxis" Inter font-semibold text-lg + version chip "v2.4" (`rounded-md bg-[var(--wash)] px-1.5 py-0.5 text-xs`, IBM Plex Mono, ink 60%)
- Center: search trigger button — `rounded-md border border-[#18181B]/15 bg-[var(--wash)] px-3 py-1.5 text-sm text-[#18181B]/60 w-72 flex items-center justify-between` — "Search docs..." + `<kbd className="font-mono text-xs">⌘K</kbd>`. **No animation** — a keyboard shortcut hint is seen 100+ times a day (interaction-standards §1); it opens/closes instantly, no transition of any kind
- Right nav (`<nav aria-label="Site">`, hidden md:flex, gap-6): "Docs" (ink 100%, `aria-current="page"`) · "Changelog" · GitHub icon link (`aria-label="View source on GitHub"`) — Inter text-sm ink 75%, hover ink 100% (color only, 150ms)

PAGE GRID (`<main>` starts here; max-w-7xl mx-auto px-6 pt-10, lg:grid lg:grid-cols-[240px_1fr_200px] gap-10)

LEFT SIDEBAR (`<aside aria-label="Documentation sections">`, sticky top-24 self-start, hidden below lg)
- Three disclosure sections, each a button (`flex w-full items-center justify-between py-1.5 text-xs font-semibold uppercase tracking-[0.1em] text-[#18181B]/60`) + `ChevronRight` icon (`transition-transform duration-150`, rotates 90deg when expanded, `aria-expanded`)
  - "Getting Started" (expanded by default) → links: Installation (active) · Quick Start · Configuration
  - "Commands" (collapsed) → links: init · build · deploy · watch
  - "Guides" (collapsed) → links: CI Integration · Plugin Authoring
- Section body: conditionally rendered (not height-animated); on expand, the revealed `<ul>` fades in via `opacity` only, 150ms `cubic-bezier(0.16, 1, 0.3, 1)` — no height/max-height transition, so nothing but opacity and the chevron's `transform: rotate()` ever animates here
- Link style: `block border-l-2 border-transparent py-1 pl-3 text-sm text-neutral-500 transition-colors duration-150 data-[active=true]:border-[var(--accent)] data-[active=true]:text-neutral-900`

MAIN COLUMN
- Page title block (`.reveal` on load: title 0ms → dek 100ms): "Getting Started with Praxis" — Newsreader text-4xl md:text-5xl leading-[1.1] ink 100%; dek "Install the CLI, scaffold a project, and ship your first build in under five minutes." — Inter text-lg ink 75%
- Prose body (paste verbatim):
```tsx
<div className="prose prose-neutral max-w-[68ch] prose-headings:font-serif
                prose-p:leading-relaxed prose-code:before:content-none prose-code:after:content-none">
  {/* section content */}
</div>
```
  - Opening paragraph (write verbatim): "Praxis is a single binary — no runtime to install, no version manager to configure. Download it, put it on your PATH, and you have a scaffolder, a local dev server, and a deploy client in one command."
  - H2 "Installation" (Newsreader, anchor `id="installation"`) + a code block: `curl -fsSL https://praxis.dev/install.sh | sh` followed by a short paragraph: "This installs the latest stable release to `~/.praxis/bin`. Homebrew and Scoop packages track the same version."
  - H2 "Quick Start" (`id="quick-start"`) + code block: `praxis init my-service && cd my-service && praxis dev` + paragraph: "`praxis dev` starts a local server with hot reload and prints the URL to your terminal."
  - H2 "Configuration" (`id="configuration"`) + inline code example `praxis.config.ts` + paragraph explaining the config file exports a single `defineConfig()` call
  - Each H2 section gets `.reveal` once when scrolled into view (IntersectionObserver threshold 0.15), 0.55s, one section at a time — paragraphs and code blocks inside do not animate individually
- CODE BLOCK component (paste verbatim):
```tsx
<div className="group relative rounded-lg border border-[#18181B]/10 bg-[var(--wash)] p-4 font-mono text-sm overflow-x-auto">
  <pre><code>{/* command */}</code></pre>
  <button
    aria-label="Copy code"
    className="absolute right-3 top-3 rounded-md border border-[#18181B]/10 bg-[var(--paper)]/80 p-1.5
               opacity-0 transition-opacity duration-150 group-hover:opacity-100
               active:scale-[0.94]"
  >
    {/* Copy icon, swaps to Check for 2s after click */}
  </button>
</div>
```
  - The copy button's hover-triggered opacity reveal is gated: wrap `group-hover:opacity-100` usage in `@media (hover: hover) and (pointer: fine)` for the raw-CSS fallback; on touch it stays visible at `opacity-60`
  - Inline code: `rounded bg-[var(--wash)] px-1.5 py-0.5 text-[0.85em] font-mono`

TOAST ("Copied" — fixed bottom-6 right-6, z-40, `role="status"`)
- `rounded-lg border border-[#18181B]/10 bg-[var(--paper)] px-4 py-3 text-sm shadow-md` with `Check` icon in `--accent`, text "Copied"
- `@starting-style` transition: from `opacity: 0; transform: translateY(8px)`, 200ms `cubic-bezier(0.16, 1, 0.3, 1)`, interruptible; auto-dismiss after 2.5s

RIGHT TOC (`<aside aria-label="Table of contents">`, sticky top-24, hidden below xl; paste verbatim)
```tsx
<nav aria-label="On this page" className="sticky top-24 hidden xl:block">
  {headings.map(h => (
    <a key={h.id} href={`#${h.id}`}
       className="block border-l-2 border-transparent py-1 pl-3 text-sm text-neutral-500
                  transition-colors duration-150 data-[active=true]:border-[var(--accent)]
                  data-[active=true]:text-neutral-900">
      {h.title}
    </a>
  ))}
</nav>
```
- IntersectionObserver sets `data-active` on the current section's link; smooth-scroll on click; never scroll-jack

PREV/NEXT FOOTER (border-t border-[#18181B]/10 pt-8 mt-16 flex justify-between gap-4)
- "← Installation" and "Configuration →" — each `rounded-lg border border-[#18181B]/10 p-4 text-sm` with a small ink-60% label above the linked page title; hover border ink/30 (color only, 150ms); press `active:scale-[0.98]`; `aria-label="Previous: Installation"` / `aria-label="Next: Configuration"`

FOOTER (border-t border-[#18181B]/10, py-12, max-w-7xl mx-auto px-6, Inter text-sm ink 60%)
- "Praxis — one binary, no runtime." + links Docs / Changelog / GitHub

ANIMATIONS (complete list — docs stay still)
- Load: page title + dek, 0.55s, delays 0/100ms
- Scroll: one `.reveal` per H2 section, 0.55s `cubic-bezier(0.22, 1, 0.36, 1)`, once
- Sidebar disclosure: chevron `transform: rotate()` 150ms; revealed list fades in via opacity only, 150ms — no height animation anywhere
- Copy button: opacity reveal on hover 150ms (gated); press `active:scale-[0.94]`; toast 200ms `@starting-style`
- TOC + sidebar active-link indicator: color/border-color only, 150ms
- The `⌘K` search hint: **zero animation**, at any state — it is used too often to earn any motion budget
- Nothing loops; the page is as calm as documentation should be

RESPONSIVE
- Below lg: left sidebar hidden (sections reachable via the search trigger); below xl: right TOC hidden; main column becomes single column, px-6; code blocks scroll horizontally inside their own container — the page never scrolls sideways

KEY DEPENDENCIES
`react@^18` `react-dom@^18` `typescript@^5` `vite@^5` `tailwindcss@^3` `@tailwindcss/typography@^0.5` `lucide-react@latest`

CONSTRAINTS: editorial restraint — reveals 0.4–0.8s, easing from {cubic-bezier(0.16,1,0.3,1) · cubic-bezier(0.22,1,0.36,1) · cubic-bezier(0.65,0,0.35,1)}, never ease-in; animate only transform/opacity (sidebar/TOC color transitions are the sole paint exception). ONE accent hue (#4338CA). No video, no glass, no gradients, no marquee. Respect `prefers-reduced-motion` (block above). Semantic HTML: `<main>`, `<aside aria-label>` for both sidebar and TOC, `<nav aria-label>`, `role="status"` on the toast, `aria-expanded` on disclosure buttons, `aria-label` on icon-only buttons.
