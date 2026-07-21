# Ledgerline Changelog

- **ID:** `ledgerline-changelog`
- **Category:** Docs / Changelog
- **Type:** changelog
- **Profile:** `editorial`

---

Build a single-page product changelog for "Ledgerline" — an API for programmatic accounting. Documentation typography: calm, scannable, permanent-feeling. Use React + Vite + Tailwind CSS + TypeScript + @tailwindcss/typography + lucide-react. Default Tailwind config (plus the typography plugin), no other UI libraries.

FONTS (Google Fonts, load via `<link>` in index.html)
- Display: Source Serif 4 (500/600) — page title, version headings
- Body + UI: Inter (400/500/600) — prose, nav, badges
- Code: ui-monospace stack (`ui-monospace, 'SF Mono', monospace`) — inline code and blocks

COLORS (CSS variables on :root — paper family, light only)
- --paper: #FFFFFF · --wash: #F5F4EF · --ink: #1A1A1A · --accent: #1D4ED8 (the ONLY accent hue)
- Text tiers: ink 100% / 75% / 60%; rules `#1A1A1A` at 10%

GLOBAL CSS (paste verbatim)
```css
@keyframes ed-reveal { from { opacity: 0; transform: translateY(12px); } to { opacity: 1; transform: none; } }
.reveal { animation: ed-reveal 0.55s cubic-bezier(0.22, 1, 0.36, 1) backwards; }

@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { animation-duration: 0.01ms !important; animation-iteration-count: 1 !important; transition-duration: 0.01ms !important; }
}
```

HEADER (sticky top-0, z-20, bg-[var(--paper)]/95 backdrop-blur-sm, border-b border-[#1A1A1A]/10)
- Left: "Ledgerline" Inter font-semibold + "/ Changelog" ink 60%
- Right: links Docs · API status · "Subscribe via RSS" (`Rss` icon, `aria-label="RSS feed"`) — text-sm ink 75%, hover ink 100% (color only, 150ms); press `active:scale-[0.98]`
- Persistent chrome: nothing in the header animates on load

PAGE GRID (max-w-6xl mx-auto px-6, lg:grid lg:grid-cols-[220px_1fr] gap-12, pt-16)

LEFT SIDEBAR (sticky top-24, self-start, hidden below lg, `<nav aria-label="Versions">`)
- Title "Releases" — Inter text-xs uppercase tracking-[0.12em] ink 60%
- Version links: v3.2.0 · v3.1.0 · v3.0.0 · v2.9.4 · v2.9.0 — `block border-l-2 border-transparent py-1 pl-3 text-sm text-neutral-500 transition-colors duration-150 data-[active=true]:border-[var(--accent)] data-[active=true]:text-neutral-900`
- IntersectionObserver sets `data-active` on the entry currently in view; smooth-scroll on click; never scroll-jack

MAIN COLUMN
- Page title block (staggered `.reveal` on load: title 0ms → dek 100ms): "What's new in Ledgerline" — Source Serif 4 text-4xl md:text-5xl leading-[1.1]; dek "Every change to the API, the SDKs, and the dashboard. Updated with each release." — Inter text-lg ink 75%
- Then a vertical stack of RELEASE ENTRIES, each `.reveal` once when scrolled into view (IntersectionObserver, threshold 0.15) — one entry at a time, no stagger inside an entry

RELEASE ENTRY (repeat 5×, `<section id="v3-2-0">`, pb-12 mb-12 border-b border-[#1A1A1A]/10)
- Meta row: version "v3.2.0" — Source Serif 4 text-2xl font-semibold, with an anchor-link button (`Link` icon, opacity-0, revealed on entry hover — gated `@media (hover: hover) and (pointer: fine)`, opacity 150ms; click copies the URL and fires the toast; `aria-label="Copy link to v3.2.0"`) + date "June 30, 2026" Inter text-sm ink 60%
- Category badges: `rounded-md px-2 py-0.5 text-xs font-medium` — "Added" = `bg-[var(--accent)]/10 text-[var(--accent)]` · "Changed" / "Fixed" / "Deprecated" = `bg-[var(--wash)] text-[#1A1A1A]/75` (neutral — the accent stays singular)
- Body in prose (paste verbatim):
```tsx
<div className="prose prose-neutral max-w-[65ch] prose-headings:font-serif
                prose-p:leading-relaxed prose-code:before:content-none prose-code:after:content-none">
  {/* entry content */}
</div>
```
- Inline code: `rounded bg-[var(--wash)] px-1.5 py-0.5 text-[0.85em]`; code blocks: `rounded-lg bg-[var(--wash)] p-4 text-sm overflow-x-auto`
- Entry content (write realistic changelog copy), e.g. v3.2.0: Added — `POST /v1/journals/bulk` batch endpoint (up to 500 entries); idempotency keys on all mutating routes. Changed — webhook retries now back off exponentially (1s → 32s). Fixed — `balance_at` off-by-one on UTC midnight queries.
- v3.1.0: Added — Python SDK `ledgerline-py@1.0`. Deprecated — `GET /v1/ledger/export` (use async exports). …and 3 more entries in the same voice

TOAST (fixed bottom-6 right-6, z-30, `role="status"`)
- "Link copied" — `rounded-lg border border-[#1A1A1A]/10 bg-[var(--paper)] px-4 py-3 text-sm shadow-md` with `Check` in `--accent`
- `@starting-style` transition: from `opacity: 0; transform: translateY(8px)`, 200ms cubic-bezier(0.16, 1, 0.3, 1), interruptible; auto-dismiss 2.5s

FOOTER (border-t border-[#1A1A1A]/10, py-12, max-w-6xl mx-auto px-6)
- "Ledgerline — double-entry, single API." Inter text-sm ink 60% + email-subscribe form: input `rounded-md border border-[#1A1A1A]/10 bg-[var(--paper)] px-3 py-2 text-sm w-64` + button "Get release notes" `rounded-md bg-[var(--ink)] text-white px-4 py-2 text-sm font-medium`, hover bg ink 75% (150ms), press `active:scale-[0.98]`

ANIMATIONS (complete list — docs stay still)
- Load: title + dek, 0.55s, delays 0/100ms
- Scroll: one `.reveal` per release entry, 0.55s cubic-bezier(0.22, 1, 0.36, 1), once
- Hover: color-only on links/nav 150ms; anchor-link icon opacity 150ms (gated)
- Toast 200ms `@starting-style` · Press `active:scale-[0.98]` everywhere pressable
- Nothing loops; the page is as calm as a ledger should be

RESPONSIVE
- Below lg: sidebar hidden (versions reachable by scroll); px-6; title text-4xl; code blocks scroll horizontally in their own container — the page never scrolls sideways

KEY DEPENDENCIES
`react@^18` `react-dom@^18` `typescript@^5` `vite@^5` `tailwindcss@^3` `@tailwindcss/typography@^0.5` `lucide-react@latest`

CONSTRAINTS: editorial restraint — reveals 0.4–0.8s, easing from {cubic-bezier(0.16,1,0.3,1) · cubic-bezier(0.22,1,0.36,1) · cubic-bezier(0.65,0,0.35,1)}, never ease-in; animate only transform/opacity (sidebar/nav color transitions are the sole paint exception). ONE accent hue (#1D4ED8); every other badge and rule is neutral. No video, no glass, no gradients, no marquee. Respect `prefers-reduced-motion` (block above). Semantic HTML: `<section>` per release with stable `id` anchors, `<nav aria-label>`, `role="status"` on the toast, `aria-label` on icon-only buttons. Never apply `overflow-x: hidden` to `html`/`body` or a root wrapper — it creates a scroll container and silently breaks `position: sticky`; contain any horizontal bleed with `overflow-x: clip` on the overflowing section instead.
