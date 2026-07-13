# Arcadia Goods Storefront

- **ID:** `arcadia-goods-storefront`
- **Category:** Storefront
- **Type:** storefront
- **Profile:** `ecommerce`

---

Build a single-page storefront home for "Arcadia Goods" — outdoor gear made to outlast trends. Imagery-first, conversion-focused; browsing stays snappy. Use React + Vite + Tailwind CSS + TypeScript + lucide-react. Default Tailwind config, no other UI libraries.

FONTS (Google Fonts, load via `<link>` in index.html)
- Display: Inter Tight (600/700) — headlines, section titles
- Body: Inter (400/500) — everything else; all prices `tabular-nums`

COLORS (CSS variables on :root — retail-light family, exactly two accents)
- --background: #FFFFFF · --wash: #FAFAFA · --border: #F4F4F5 · --foreground: #18181B
- --brand: #111827 (near-black — buttons, links) · --sale: #E11D48 (sale badges and prices ONLY)
- Text tiers: foreground 100% / 70% / 55%

GLOBAL CSS (paste verbatim)
```css
@keyframes card-rise { from { opacity: 0; transform: translateY(12px); } to { opacity: 1; transform: none; } }
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

ANNOUNCEMENT BAR (bg-[var(--brand)] text-white text-center text-xs font-medium py-2)
- "Free shipping over $75 · Returns until Jan 31" — static, no marquee (persistent chrome doesn't perform)

NAVBAR (sticky top-0, z-20, bg-[var(--background)]/95 backdrop-blur-sm, border-b border-[var(--border)])
- max-w-7xl mx-auto px-6 h-16 flex items-center justify-between
- Left: "ARCADIA" — Inter Tight 700 text-xl tracking-tight
- Center (hidden md:flex, text-sm 70%): Packs · Shelter · Trail kitchen · Sale (`--sale` colored) — hover = foreground 100%, color-only 150ms
- Right: search (`Search`, `aria-label="Search"`), account (`User`, `aria-label="Account"`), cart button (`ShoppingBag`, `aria-label="Cart, 2 items"`) with count badge `cart-badge absolute -top-1 -right-1 w-4 h-4 rounded-full bg-[var(--sale)] text-white text-[10px] grid place-items-center tabular-nums` — bumps (verbatim keyframe) whenever an item is added
- All icon buttons `rounded-lg p-2`, hover bg-[var(--wash)] 140ms, `active:scale-[0.97]`

HERO (max-w-7xl mx-auto px-6 py-8, grid md:grid-cols-[3fr_2fr] gap-4)
- Left tile: `rounded-xl overflow-hidden relative aspect-[4/3] md:aspect-auto` — `<img src="{YOUR_IMAGE_URL_HERO}" alt="Hiker crossing a ridgeline at dawn">` object-cover; overlay content bottom-left p-8: H1 "Built for the long trail." Inter Tight 700 text-4xl md:text-6xl text-white leading-[1.0] + CTA "Shop the fall drop" `rounded-lg bg-white text-[var(--foreground)] px-6 py-3 text-sm font-medium mt-4`, hover bg-[var(--wash)] 140ms, `active:scale-[0.97]`; scrim = bottom gradient black/45→transparent for text legibility
- Right tile: `rounded-xl bg-[var(--wash)] p-8 flex flex-col justify-between` — "New: Cinder Stove 2" Inter Tight 600 text-2xl + "970 g. Boils in 90 seconds." 70% + text link "See it →" (`--brand`, underline on hover)
- Entrance: both tiles + H1 + CTA fade-rise 16px, 0.4s cubic-bezier(0.23, 1, 0.32, 1), stagger 50ms (delays 0/50/100/150ms) — once, on load

CATEGORY TILES (max-w-7xl mx-auto px-6 py-12, grid grid-cols-2 md:grid-cols-4 gap-4)
- Packs · Shelter · Trail kitchen · Apparel — each `rounded-xl overflow-hidden relative aspect-square`, `<img src="{YOUR_IMAGE_URL_CAT_N}" alt="…">` object-cover, label bottom-left `bg-[var(--background)]/90 backdrop-blur-sm rounded-lg px-3 py-1.5 text-sm font-medium m-3`
- Hover (gated `@media (hover: hover) and (pointer: fine)`): inner image `scale(1.04)`, 250ms cubic-bezier(0.23, 1, 0.32, 1) — the tile itself doesn't move; press `active:scale-[0.98]`
- Reveal: card-rise 0.35s via IntersectionObserver once, stagger 50ms

PRODUCT GRID (max-w-7xl mx-auto px-6 pb-16)
- Header row: "Bestsellers" Inter Tight 600 text-2xl + "View all" text-sm link
- 8 product cards, grid grid-cols-2 lg:grid-cols-4 gap-x-4 gap-y-8, reveal stagger 50ms via IntersectionObserver once; card markup (paste verbatim):
```tsx
<a className="card block" href={p.href} aria-label={p.name}>
  <div className="relative aspect-square overflow-hidden rounded-xl bg-zinc-100">
    <img src={p.img} className="h-full w-full object-cover" alt="" />
    <img src={p.altImg} className="alt absolute inset-0 h-full w-full object-cover" alt="" />
  </div>
  <div className="mt-3 flex justify-between text-sm">
    <span className="text-zinc-900">{p.name}</span>
    <span className="tabular-nums font-medium text-zinc-900">{p.price}</span>
  </div>
</a>
```
- Products: Ridgeline 38 Pack $148 · Cinder Stove 2 $89 · Tarn 2P Tent $329 · Fault Line Shell $189 (SALE $139) · Switchback Poles $72 · Ember Quilt $210 · Cache Dry Bag $28 · Overlook Cap $32
- Sale items: badge `absolute top-2 left-2 z-[15] rounded-lg bg-[var(--sale)] text-white text-xs font-medium px-2 py-0.5` "−26%"; price shows sale price in `--sale` + original struck-through 55%
- Under each card: quick "Add" button `add rounded-lg border border-[var(--border)] w-full py-2 text-sm font-medium mt-2` (verbatim `.add` class), hover bg-[var(--wash)], click → cart badge bump + button text swaps to "Added ✓" for 1.5s (text swap only, no layout shift — fixed height)

FEATURE BAND (bg-[var(--wash)] py-12)
- max-w-7xl mx-auto px-6 grid grid-cols-1 md:grid-cols-3 gap-8, each: lucide icon (`Truck`/`RefreshCw`/`Shield`) + "Free shipping $75+" / "60-day trail test" / "Lifetime repairs" font-medium + one-liner 70% — reveal 0.35s stagger 50ms once

FOOTER (border-t border-[var(--border)], py-12, max-w-7xl mx-auto px-6)
- 4 columns text-sm: Shop / Support / Company / "Get 10% off" newsletter — input `rounded-lg border border-[var(--border)] px-3 py-2 text-sm` + button "Sign up" `add rounded-lg bg-[var(--brand)] text-white px-4 py-2 text-sm font-medium`
- Bottom row: "© Arcadia Goods" 55% + payment icons (`aria-hidden`)

ANIMATIONS (complete list — browsing never waits)
- Entrances: card-rise 0.35s cubic-bezier(0.23, 1, 0.32, 1), stagger 50ms, IntersectionObserver once (hero on load)
- Hover: card lift −4px + alt-image crossfade 200ms; category image zoom 1.04 250ms — all gated for touch
- Cart badge bump 0.3s cubic-bezier(0.34, 1.56, 0.64, 1) on add
- Press: `active:scale-[0.97]` on every button, `active:scale-[0.98]` on tiles/links
- No idle loops, no marquee, no parallax — imagery sells, motion confirms

RESPONSIVE
- Mobile: hero stacks (image tile then promo tile), category 2-col, product grid 2-col, nav center links hidden (hamburger `Menu` button, `aria-label="Menu"`), footer stacks; no horizontal scroll

KEY DEPENDENCIES
`react@^18` `react-dom@^18` `typescript@^5` `vite@^5` `tailwindcss@^3` `lucide-react@latest`

CONSTRAINTS: ecommerce snap — entrances 0.25–0.5s, interactions ≤ 280ms; easing only from {cubic-bezier(0.23,1,0.32,1) · cubic-bezier(0.4,0,0.2,1) · cubic-bezier(0.34,1.56,0.64,1)}, never ease-in. Animate only transform/opacity (background-color on button hover is the documented paint exception). Exactly TWO accents: `--brand` for action, `--sale` for urgency — nothing else is colored. Product imagery does the talking: no decorative gradients, no video, no blobs. Layer contract: media z-0 → badge z-[15] → nav z-20. Respect `prefers-reduced-motion`. Replace `{YOUR_IMAGE_URL_*}` and product `img`/`altImg` with photography you have rights to. ARIA labels on all icon-only buttons and product-card links; prices `tabular-nums` everywhere.
