# Loam & Kiln Storefront

- **ID:** `loam-and-kiln-storefront`
- **Category:** Storefront
- **Type:** storefront
- **Profile:** `ecommerce`

---

Build a single-page storefront home for "Loam & Kiln" — a handmade ceramics studio shop where every piece is thrown, glazed, and fired by hand. Imagery-first, conversion-focused, earthy and unhurried but never slow to browse. Use React + Vite + Tailwind CSS + TypeScript + lucide-react. Default Tailwind config, no other UI libraries.

FONTS (Google Fonts, load via `<link>` in index.html)
- Display: Fraunces (400/600) — headlines, product names
- Body: Inter (400/500) — everything else; all prices `tabular-nums`

COLORS (CSS variables on :root — clay-cream family, exactly two accents)
- --paper: #FBF7F2 · --wash: #F3EBE0 · --border: #E6D9C6 · --ink: #2B2320
- --glaze: #3F6D5B (glaze green — buttons, links, selected states) · --terra: #B4552F (one-of-one badge and maker accents ONLY)
- Text tiers: ink 100% / 70% / 55%

GLOBAL CSS (paste verbatim)
```css
@keyframes card-rise { from { opacity: 0; transform: translateY(12px); } to { opacity: 1; transform: none; } }
.card { animation: card-rise 0.35s cubic-bezier(0.23, 1, 0.32, 1) backwards;
        transition: transform 200ms cubic-bezier(0.23, 1, 0.32, 1); }
.card .alt { opacity: 0; transition: opacity 200ms cubic-bezier(0.23, 1, 0.32, 1); }
.card .quick-add { opacity: 0; transform: translateY(6px);
                    transition: opacity 200ms cubic-bezier(0.23, 1, 0.32, 1), transform 200ms cubic-bezier(0.23, 1, 0.32, 1); }
@media (hover: hover) and (pointer: fine) {
  .card:hover { transform: translateY(-4px); }
  .card:hover .alt { opacity: 1; }
  .card:hover .quick-add { opacity: 1; transform: none; }
}

@keyframes bump { 0% { transform: scale(1); } 40% { transform: scale(1.35); } 100% { transform: scale(1); } }
.cart-badge[data-bumped="true"] { animation: bump 0.3s cubic-bezier(0.34, 1.56, 0.64, 1); }
.add { transition: transform 140ms cubic-bezier(0.23, 1, 0.32, 1), background-color 140ms cubic-bezier(0.23, 1, 0.32, 1); }
.add:active { transform: scale(0.97); }

@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { animation-duration: 0.01ms !important; animation-iteration-count: 1 !important; transition-duration: 0.01ms !important; }
}
```

ANNOUNCEMENT BAR (bg-[var(--ink)] text-white text-center text-xs font-medium py-2)
- "Handbuilt in small batches · Ships from our Ojai studio every Friday" — static, no marquee

NAVBAR (sticky top-0, z-20, bg-[var(--paper)]/95 backdrop-blur-sm, border-b border-[var(--border)])
- max-w-7xl mx-auto px-6 h-16 flex items-center justify-between
- Left: "LOAM & KILN" — Fraunces 600 text-xl tracking-tight
- Center (hidden md:flex, text-sm 70%): Bowls · Mugs · Vases · The Studio — hover ink 100%, color-only 150ms
- Right: search (`Search`, `aria-label="Search"`), cart button (`ShoppingBag`, `aria-label="Cart, 1 item"`) with `cart-badge` count badge (`bg-[var(--terra)] text-white text-[10px] rounded-full w-4 h-4 grid place-items-center tabular-nums absolute -top-1 -right-1`, verbatim bump keyframe)
- All icon buttons `rounded-lg p-2`, hover bg-[var(--wash)] 140ms, `active:scale-[0.97]`

COLLECTION HERO STRIP (max-w-7xl mx-auto px-6 py-8, grid md:grid-cols-[3fr_2fr] gap-4)
- Left tile: `rounded-xl overflow-hidden relative aspect-[4/3] md:aspect-auto` — `<img src="{YOUR_IMAGE_URL_HERO}" alt="Potter's hands shaping a bowl on the wheel, ash glaze test pieces drying on a shelf behind">` object-cover; overlay bottom-left p-8: H1 "The Ash Glaze Collection" Fraunces 600 text-4xl md:text-6xl text-white leading-[1.05] + CTA "Shop the collection" `rounded-lg bg-white text-[var(--ink)] px-6 py-3 text-sm font-medium mt-4`, hover bg-[var(--wash)] 140ms, `active:scale-[0.97]`; scrim = bottom gradient black/45→transparent
- Right tile: `rounded-xl bg-[var(--wash)] p-8 flex flex-col justify-between` — "New: River Stone Vase" Fraunces 600 text-2xl + "Wood-ash glaze, reduction-fired." 70% + text link "See it →" (`--glaze`, underline on hover)
- Entrance: both tiles + H1 + CTA fade-rise 12px, 0.35s cubic-bezier(0.23, 1, 0.32, 1), stagger 50ms (delays 0/50/100/150ms) — once, on load

PRODUCT GRID (max-w-7xl mx-auto px-6 py-16)
- Header row: "Current kiln" Fraunces 600 text-2xl + "View all" text-sm link
- 8 product cards, grid grid-cols-2 lg:grid-cols-4 gap-x-4 gap-y-8, reveal stagger 50ms via IntersectionObserver once; card markup (paste verbatim):
```tsx
<a className="card block relative" href={p.href} aria-label={p.name}>
  <div className="relative aspect-square overflow-hidden rounded-xl bg-[var(--wash)]">
    <img src={p.img} className="h-full w-full object-cover" alt="" />
    <img src={p.altImg} className="alt absolute inset-0 h-full w-full object-cover" alt="" />
    <span className="absolute top-2 left-2 z-[15] rounded-lg bg-[var(--terra)] text-white text-[11px] font-medium px-2 py-0.5">
      One of one
    </span>
    <button
      className="quick-add add absolute bottom-2 left-2 right-2 rounded-lg bg-white/95 backdrop-blur-sm py-2 text-sm font-medium text-[var(--ink)]"
      onClick={(e) => { e.preventDefault(); bumpBadge(); }}
      aria-label={`Quick add ${p.name}`}
    >
      + Quick add
    </button>
  </div>
  <div className="mt-3 flex justify-between text-sm">
    <span className="text-[var(--ink)]">{p.name}</span>
    <span className="tabular-nums font-medium text-[var(--ink)]">{p.price}</span>
  </div>
</a>
```
- Products (each genuinely one-of-one — no two glaze runs match): Ash Glaze Bowl No. 12 — $68 · Umber Speckle Mug — $34 · River Stone Vase — $96 · Ember Teapot No. 4 — $128 · Moss Rim Bowl — $58 · Sand Dune Vase — $112 · Clay Horizon Mug — $32 · Smoke Glaze Plate — $46
- Quick-add reveals only on hover, gated `@media (hover: hover) and (pointer: fine)` (verbatim `.quick-add` rule above); on touch it stays hidden — tap the card to view the product instead
- On quick-add click: cart badge bumps (verbatim keyframe) + button label swaps to "Added ✓" for 1.5s (fixed height, no layout shift)

MAKER'S-NOTE STRIP (bg-[var(--wash)] py-16)
- max-w-5xl mx-auto px-6 grid md:grid-cols-[1fr_2fr] gap-8 items-center
- Left: `rounded-xl overflow-hidden aspect-square` `<img src="{YOUR_IMAGE_URL_MAKER}" alt="Portrait of Nadia Ostrowski in her studio, apron dusted with clay">` object-cover
- Right: kicker "FROM THE STUDIO" text-xs tracking-[0.14em] 55% + quote Fraunces 400 text-2xl md:text-3xl leading-snug italic: "Every piece leaves the wheel slightly different — a thumbprint, a drip of glaze, a shape that didn't come out quite as planned. We keep them anyway." + attribution "— Nadia Ostrowski, potter & founder" text-sm 70% mt-4
- Reveal: fade-rise 12px 0.35s cubic-bezier(0.23, 1, 0.32, 1), once, IntersectionObserver

FOOTER (border-t border-[var(--border)], py-12, max-w-7xl mx-auto px-6)
- 3 columns text-sm: Shop / The Studio / "Join the glaze list" newsletter — input `rounded-lg border border-[var(--border)] px-3 py-2 text-sm` + button "Sign up" `add rounded-lg bg-[var(--glaze)] text-white px-4 py-2 text-sm font-medium`
- Bottom row: "© Loam & Kiln" 55% + Instagram icon link (`aria-label="Instagram"`)

ANIMATIONS (complete list — browsing never waits)
- Entrances: card-rise 0.35s cubic-bezier(0.23, 1, 0.32, 1), stagger 50ms, IntersectionObserver once (hero on load)
- Hover: card lift −4px + alt-image crossfade 200ms + quick-add reveal (opacity/translateY) 200ms — all gated for touch
- Cart badge bump 0.3s cubic-bezier(0.34, 1.56, 0.64, 1) on add
- Press: `active:scale-[0.97]` on every button, `active:scale-[0.98]` on tiles/links
- No idle loops, no marquee, no parallax — the glaze work sells itself

RESPONSIVE
- Mobile: hero stacks (image tile then promo tile), product grid 2-col, quick-add always hidden below the `hover` breakpoint (tap-through to product instead), nav center links hidden (hamburger `Menu` button, `aria-label="Menu"`), footer stacks; no horizontal scroll

KEY DEPENDENCIES
`react@^18` `react-dom@^18` `typescript@^5` `vite@^5` `tailwindcss@^3` `lucide-react@latest`

CONSTRAINTS: ecommerce snap — entrances 0.25–0.5s, interactions ≤ 280ms; easing only from {cubic-bezier(0.23,1,0.32,1) · cubic-bezier(0.4,0,0.2,1) · cubic-bezier(0.34,1.56,0.64,1)}, never ease-in. Animate only transform/opacity (background-color on button hover is the documented paint exception). Exactly TWO accents: `--glaze` for action, `--terra` for the one-of-one badge — nothing else is colored. Product photography does the talking: no decorative gradients, no video, no blobs. Layer contract: media z-0 → badge z-[15] → nav z-20. Respect `prefers-reduced-motion`. Replace `{YOUR_IMAGE_URL_*}` and product `img`/`altImg` with photography you have rights to, with real `alt` text. ARIA labels on all icon-only buttons and product-card links; prices `tabular-nums` everywhere. Never apply `overflow-x: hidden` to `html`/`body` or a root wrapper — it creates a scroll container and silently breaks `position: sticky`; contain any horizontal bleed with `overflow-x: clip` on the overflowing section instead.
