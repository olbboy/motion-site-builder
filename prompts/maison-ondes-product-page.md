# Maison Ondes Product Page

- **ID:** `maison-ondes-product-page`
- **Category:** Product Page
- **Type:** product-page
- **Profile:** `ecommerce`

---

Build a single product-detail page for "Maison Ondes" — a boutique fragrance house — selling "Éclat No. 4", an eau de parfum. Boutique-dark, imagery-first, quietly luxurious; every interaction confirms crisply. Use React + Vite + Tailwind CSS + TypeScript + lucide-react + embla-carousel-react. Default Tailwind config, no other UI libraries.

FONTS (Google Fonts, load via `<link>` in index.html)
- Display: Fraunces (400/600) — product name, section titles, prices
- Body: Inter (400/500) — everything else; prices `tabular-nums`

COLORS (CSS variables on :root — boutique-dark family, exactly two accents)
- --noir: #111111 (background) · --panel: #1A1A1A · --ivory: #FAFAFA (foreground) · --line: rgba(250,250,250,0.12)
- --gold: #D4AF37 (accent — ratings, selected states, links) · --rose: #F43F5E (sale/urgency ONLY)
- Text tiers: ivory 100% / 70% / 55%

GLOBAL CSS (paste verbatim)
```css
@keyframes card-rise { from { opacity: 0; transform: translateY(12px); } to { opacity: 1; transform: none; } }
.rise { animation: card-rise 0.35s cubic-bezier(0.23, 1, 0.32, 1) backwards; }

.card { animation: card-rise 0.35s cubic-bezier(0.23, 1, 0.32, 1) backwards;
        transition: transform 200ms cubic-bezier(0.23, 1, 0.32, 1); }
.card .alt { opacity: 0; transition: opacity 200ms cubic-bezier(0.23, 1, 0.32, 1); }
@media (hover: hover) and (pointer: fine) {
  .card:hover { transform: translateY(-4px); }
  .card:hover .alt { opacity: 1; }
}

@keyframes bump { 0% { transform: scale(1); } 40% { transform: scale(1.35); } 100% { transform: scale(1); } }
.cart-badge[data-bumped="true"] { animation: bump 0.3s cubic-bezier(0.34, 1.56, 0.64, 1); }
.add { transition: transform 140ms cubic-bezier(0.23, 1, 0.32, 1), background-color 140ms cubic-bezier(0.23, 1, 0.32, 1); }
.add:active { transform: scale(0.97); }

@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { animation-duration: 0.01ms !important; animation-iteration-count: 1 !important; transition-duration: 0.01ms !important; }
}
```

NAVBAR (sticky top-0, z-20, bg-[var(--noir)]/95 backdrop-blur-sm, border-b border-[var(--line)])
- max-w-6xl mx-auto px-6 h-16 flex items-center justify-between, text-[var(--ivory)]
- Left: "MAISON ONDES" — Fraunces 400 text-lg tracking-[0.2em]
- Center (hidden md:flex, text-sm 70%): Parfums · Discovery sets · Journal — hover ivory 100%, color-only 150ms
- Right: cart button (`ShoppingBag`, `aria-label="Cart, 1 item"`) with `cart-badge` count badge (`bg-[var(--gold)] text-[var(--noir)]`, verbatim bump keyframe); `rounded-lg p-2`, hover bg-[var(--panel)] 140ms, `active:scale-[0.97]`
- Breadcrumb strip under nav (max-w-6xl mx-auto px-6 py-3 text-xs 55%): "Parfums / Eau de parfum / **Éclat No. 4**"

MAIN GRID (max-w-6xl mx-auto px-6 pb-24, lg:grid lg:grid-cols-[7fr_5fr] gap-12; z-10)

GALLERY (left, `.rise` on load)
- embla-carousel-react: 4 slides, each `rounded-xl overflow-hidden aspect-[4/5] bg-[var(--panel)]` with `<img src="{YOUR_IMAGE_URL_N}" alt="Éclat No. 4 — bottle on travertine / macro of glass / in hand / gift box">` object-cover — embla's native translate handles slide motion; no fade plugins
- Prev/next buttons (`ChevronLeft`/`ChevronRight`, `aria-label="Previous image"/"Next image"`): `rounded-full bg-[var(--noir)]/70 backdrop-blur-sm p-2 absolute top-1/2 -translate-y-1/2`, hover bg 90% 140ms, `active:scale-[0.97]`
- Thumbnail row (mt-4, flex gap-3): 4 buttons `rounded-lg overflow-hidden w-16 h-16 border border-transparent`, inactive images opacity-55, active = opacity-100 + `border-[var(--gold)]`; transitions opacity/border-color 140ms cubic-bezier(0.23, 1, 0.32, 1); `aria-label="View image N"`, press `active:scale-[0.97]`

BUY COLUMN (right, staggered `.rise` on load via `animation-delay`: name 0ms → rating 50ms → price 100ms → sizes 150ms → CTA 200ms → accordions 250ms)
- Kicker: "EAU DE PARFUM" — Inter text-xs tracking-[0.18em] 55%
- Name: "Éclat No. 4" — Fraunces 600 text-4xl md:text-5xl leading-[1.0]
- One-liner: "Neroli struck by sea salt; a linen shirt at golden hour." — Inter text-base 70%, italic
- Rating row: 5× lucide `Star` w-4 h-4 fill `--gold` + "4.8 · 214 reviews" text-sm 70% (anchor-links to Reviews)
- Price: "$185" — Fraunces text-3xl `tabular-nums`; when the 30 ml size is selected show "$98"
- SIZE SELECTOR (`role="radiogroup" aria-label="Size"`): 3 pills — "30 ml" / "50 ml" (default) / "100 ml" — `rounded-lg border px-5 py-2.5 text-sm font-medium`; unselected = `border-[var(--line)]` ivory 70%; selected = `border-[var(--gold)] text-[var(--gold)]`; transition border-color/color 140ms cubic-bezier(0.23, 1, 0.32, 1); press `active:scale-[0.97]`; price crossfades on change (opacity 140ms — text swap, fixed height, no layout shift)
- ADD TO CART (paste verbatim, full width, gold variant):
```tsx
<button className="add w-full rounded-lg bg-[var(--gold)] px-6 py-3.5 font-medium text-[var(--noir)]"
        onClick={bumpBadge} aria-label="Add to cart">
  Add to cart — $185
</button>
```
  On click: toggle `data-bumped` on the nav cart badge for one cycle (reset on `animationend`); label swaps to "Added ✓" for 1.5s (fixed height)
- Reassurance row (text-xs 55%, flex gap-4): "Free shipping $120+" · "Sample included" · "30-day returns"
- ACCORDIONS (border-t border-[var(--line)] divide-y divide-[var(--line)], mt-8): "Notes" (open by default) / "The making" / "Shipping & returns"
  - Header button: flex justify-between py-4 text-sm font-medium, chevron rotates 0→180deg, 200ms cubic-bezier(0.23, 1, 0.32, 1), `aria-expanded`
  - Content: height is NOT animated — the panel appears instantly; its inner content fades + rises 8px, 200ms cubic-bezier(0.23, 1, 0.32, 1) (transform/opacity only)
  - "Notes" content: three chip rows — Head: neroli, bergamot · Heart: sea salt accord, jasmine · Base: white musk, driftwood — chips `rounded-lg border border-[var(--line)] px-2.5 py-1 text-xs 70%`

STICKY MOBILE BUY BAR (lg:hidden, fixed bottom-0 inset-x-0, z-30)
- `bg-[var(--panel)]/95 backdrop-blur-sm border-t border-[var(--line)] px-4 py-3 flex items-center justify-between` — "Éclat No. 4 · $185" text-sm + compact `.add` gold button "Add to cart"
- Appears once the gallery scrolls out of view: `translateY(100%)→0`, 250ms cubic-bezier(0.23, 1, 0.32, 1) (IntersectionObserver on the gallery; reverse on scroll back)

REVIEWS (max-w-6xl mx-auto px-6 pb-24, `<section id="reviews">`)
- Title: "What they whisper" — Fraunces 600 text-3xl
- 3 review cards, grid md:grid-cols-3 gap-6, `.rise` via IntersectionObserver once, stagger 50ms (`animation-delay: 0/50/100ms`): `rounded-xl bg-[var(--panel)] p-6` — stars (gold), quote Inter text-sm 70% leading-relaxed, name + "Verified" text-xs 55%
  - "Two sprays outlasted a wedding, a flight, and the argument about the flight." — Camille T.
  - "The salt note is real. It's a beach you can wear to a boardroom." — Hana N.
  - "My third bottle. I no longer accept compliments, I expect them." — Marco V.

CROSS-SELL (max-w-6xl mx-auto px-6 pb-24)
- Title: "Pairs with" — Fraunces 600 text-2xl
- 3 product cards (paste the verbatim `.card` + `.alt` pattern from GLOBAL CSS), grid grid-cols-1 sm:grid-cols-3 gap-6, reveal stagger 50ms:
  - Ondes Discovery Set — $45 · Éclat Body Oil — $62 · Cendre No. 2 — $170
  - Each: primary + alt `<img>` ({YOUR_IMAGE_URL placeholders}), name/price row text-sm, prices `tabular-nums`

FOOTER (border-t border-[var(--line)], py-12, max-w-6xl mx-auto px-6, flex justify-between, text-sm 55%)
- "Maison Ondes — composed in small batches." + links Contact / Stockists / Instagram (`aria-label` on icon-only links)

ANIMATIONS (complete list — luxury is unhurried but never slow)
- Entrances: card-rise/.rise 0.35s cubic-bezier(0.23, 1, 0.32, 1), buy-column stagger 50ms, IntersectionObserver once below the fold
- Gallery: embla translate; thumbnails opacity/border 140ms
- Hover: cross-sell card lift −4px + alt crossfade 200ms (gated); nav color-only 150ms
- Cart badge bump 0.3s cubic-bezier(0.34, 1.56, 0.64, 1) · Accordion chevron 200ms, content fade-rise 200ms · Sticky bar translateY 250ms
- Press: `active:scale-[0.97]` on every pressable
- Nothing loops; the bottle holds the attention

RESPONSIVE
- Below lg: single column (gallery, then buy column), sticky buy bar active, reviews/cross-sell stack; thumbnails scroll horizontally in their own `overflow-x-auto` row; no page-level horizontal scroll

KEY DEPENDENCIES
`react@^18` `react-dom@^18` `typescript@^5` `vite@^5` `tailwindcss@^3` `lucide-react@latest` `embla-carousel-react@^8`

CONSTRAINTS: ecommerce snap on a boutique-dark canvas — entrances 0.25–0.5s, interactions ≤ 280ms; easing only from {cubic-bezier(0.23,1,0.32,1) · cubic-bezier(0.4,0,0.2,1) · cubic-bezier(0.34,1.56,0.64,1)}, never ease-in. Animate only transform/opacity (border-color/background-color state swaps ≤150ms are the documented paint exceptions; accordion height is never animated). Exactly TWO accents: `--gold` for selection and trust, `--rose` reserved for sale states (unused on this page — that's the point). No decorative gradients, no video, no blobs — the product photography is the drama. Layer contract: media z-0 → content z-10 → nav z-20 → sticky bar z-30. Respect `prefers-reduced-motion`. Replace `{YOUR_IMAGE_URL_*}` with photography you have rights to, with real `alt` text. ARIA: `radiogroup` on sizes, `aria-expanded` on accordions, labels on all icon-only buttons; prices `tabular-nums`.
