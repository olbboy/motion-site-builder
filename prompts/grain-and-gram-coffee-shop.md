# Grain & Gram Coffee Shop

- **ID:** `grain-and-gram-coffee-shop`
- **Category:** Storefront
- **Type:** storefront-subscription
- **Profile:** `ecommerce`

---

Build a single-page storefront + subscription builder for "Grain & Gram" — a specialty coffee roaster selling bagged beans and a build-your-own subscription. Warm, imagery-first, conversion-focused; filtering and building a subscription both stay instant. Use React + Vite + Tailwind CSS + TypeScript + lucide-react. Default Tailwind config, no other UI libraries.

FONTS (Google Fonts, load via `<link>` in index.html)
- Display: Fraunces (400/600) — headlines, bean names, section titles
- Body: Inter (400/500) — everything else; all prices `tabular-nums`

COLORS (CSS variables on :root — roast-warm family, exactly two accents)
- --paper: #FBF8F3 · --wash: #F1EAE0 · --border: #E8DFD0 · --ink: #2A1E17
- --amber: #C6742A (accent — CTA, active filter, selected) · --moss: #4B6B3A ("save 15%" subscription badge ONLY)
- Text tiers: ink 100% / 70% / 55%

GLOBAL CSS (paste verbatim)
```css
@keyframes card-rise { from { opacity: 0; transform: translateY(12px); } to { opacity: 1; transform: none; } }
.card { animation: card-rise 0.35s cubic-bezier(0.23, 1, 0.32, 1) backwards;
        transition: transform 200ms cubic-bezier(0.23, 1, 0.32, 1), opacity 150ms cubic-bezier(0.4, 0, 0.2, 1); }
.card .alt { opacity: 0; transition: opacity 200ms cubic-bezier(0.23, 1, 0.32, 1); }
.card[data-filtered-out="true"] { opacity: 0; transform: scale(0.96); pointer-events: none; position: absolute; }
@media (hover: hover) and (pointer: fine) {
  .card:hover { transform: translateY(-4px); }
  .card:hover .alt { opacity: 1; }
}

.chip { transition: background-color 150ms cubic-bezier(0.4, 0, 0.2, 1), color 150ms cubic-bezier(0.4, 0, 0.2, 1), border-color 150ms cubic-bezier(0.4, 0, 0.2, 1); }
.chip:active { transform: scale(0.97); }

@keyframes bump { 0% { transform: scale(1); } 40% { transform: scale(1.35); } 100% { transform: scale(1); } }
.cart-badge[data-bumped="true"] { animation: bump 0.3s cubic-bezier(0.34, 1.56, 0.64, 1); }
.add { transition: transform 140ms cubic-bezier(0.23, 1, 0.32, 1), background-color 140ms cubic-bezier(0.23, 1, 0.32, 1); }
.add:active { transform: scale(0.97); }

.price-swap { transition: opacity 140ms cubic-bezier(0.23, 1, 0.32, 1); }

@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { animation-duration: 0.01ms !important; animation-iteration-count: 1 !important; transition-duration: 0.01ms !important; }
}
```

NAVBAR (sticky top-0, z-20, bg-[var(--paper)]/95 backdrop-blur-sm, border-b border-[var(--border)])
- max-w-6xl mx-auto px-6 h-16 flex items-center justify-between
- Left: "GRAIN & GRAM" — Fraunces 600 text-lg tracking-tight
- Center (hidden md:flex, text-sm 70%): Beans · Subscriptions · Brew guides — hover ink 100%, color-only 150ms
- Right: cart button (`ShoppingBag`, `aria-label="Cart, 0 items"`) with `cart-badge` count badge (`bg-[var(--amber)] text-white text-[10px] rounded-full w-4 h-4 grid place-items-center tabular-nums absolute -top-1 -right-1`, verbatim bump keyframe); `rounded-lg p-2`, hover bg-[var(--wash)] 140ms, `active:scale-[0.97]`

HERO (max-w-6xl mx-auto px-6 py-12, grid md:grid-cols-[3fr_2fr] gap-4)
- Left tile: `rounded-xl overflow-hidden relative aspect-[4/3] md:aspect-auto` — `<img src="{YOUR_IMAGE_URL_HERO}" alt="Roaster checking a batch of beans as they drop from the roasting drum">` object-cover; overlay bottom-left p-8: H1 "Roasted Tuesday. Shipped Wednesday." Fraunces 600 text-4xl md:text-6xl text-white leading-[1.05] + CTA "Shop this week's roast" `rounded-lg bg-white text-[var(--ink)] px-6 py-3 text-sm font-medium mt-4`, hover bg-[var(--wash)] 140ms, `active:scale-[0.97]`; scrim = bottom gradient black/45→transparent
- Right tile: `rounded-xl bg-[var(--wash)] p-8 flex flex-col justify-between` — "Build a subscription" Fraunces 600 text-2xl + "Never run out. Cancel anytime." 70% + text link "Start below ↓" (`--amber`, underline on hover)
- Entrance: both tiles + H1 + CTA fade-rise 12px, 0.35s cubic-bezier(0.23, 1, 0.32, 1), stagger 50ms — once, on load

ROAST-LEVEL FILTER (max-w-6xl mx-auto px-6 pt-12, flex gap-2 flex-wrap, `role="group" aria-label="Filter by roast level"`)
- 5 chips (paste verbatim `.chip` class): "All" (default active) · "Light" · "Medium" · "Medium-Dark" · "Dark" — `rounded-full border px-4 py-2 text-sm font-medium`; inactive = `border-[var(--border)]` ink 70%; active = `bg-[var(--ink)] text-white border-[var(--ink)]`
- On click: non-matching bean cards get `data-filtered-out="true"` (verbatim rule above — opacity/scale 150ms, then removed from flow) while matching cards stay in place; no page reflow jump

BEAN GRID (max-w-6xl mx-auto px-6 py-8)
- 6 bean cards, grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6, reveal stagger 50ms via IntersectionObserver once; card (paste verbatim):
```tsx
<a className="card block" href={b.href} aria-label={b.name} data-roast={b.roast}>
  <div className="relative aspect-square overflow-hidden rounded-xl bg-[var(--wash)]">
    <img src={b.img} className="h-full w-full object-cover" alt="" />
    <img src={b.altImg} className="alt absolute inset-0 h-full w-full object-cover" alt="" />
  </div>
  <div className="mt-3">
    <div className="flex justify-between text-sm">
      <span className="font-medium text-[var(--ink)]">{b.name}</span>
      <span className="tabular-nums font-medium text-[var(--ink)]">{b.price}</span>
    </div>
    <p className="text-xs text-[var(--ink)]/70 mt-1">{b.origin} · {b.roast} roast</p>
    <p className="text-xs text-[var(--ink)]/55 mt-0.5">{b.notes}</p>
  </div>
</a>
```
- Beans: Yirgacheffe, Ethiopia — Light — "Jasmine, bergamot, white peach" — $19 / 250g · Gedeb, Ethiopia — Light — "Blackcurrant, honey, lemon verbena" — $21 / 250g · Huila, Colombia — Medium — "Brown sugar, red apple, almond" — $17 / 250g · Tarrazú, Costa Rica — Medium — "Caramel, orange zest, walnut" — $17 / 250g · Mogiana, Brazil — Medium-Dark — "Hazelnut, milk chocolate, molasses" — $16 / 250g · Mandailing, Sumatra — Dark — "Cedar, dark chocolate, tobacco" — $18 / 250g

SUBSCRIPTION BUILDER PANEL (max-w-4xl mx-auto px-6 py-16, `rounded-xl bg-[var(--wash)] p-8`, `<section aria-labelledby="subscribe-heading">`)
- Title `id="subscribe-heading"`: "Build your subscription" — Fraunces 600 text-3xl + badge "Save 15%" `rounded-lg bg-[var(--moss)] text-white text-xs font-medium px-2 py-0.5 ml-2 align-middle`
- Row 1 — bean select: native `<select>` `rounded-lg border border-[var(--border)] bg-white px-3 py-2.5 text-sm w-full`, options = the 6 bean names, default "Yirgacheffe, Ethiopia"
- Row 2 — grid grid-cols-2 gap-4 mt-4: frequency `<select aria-label="Delivery frequency">` (Every 2 weeks / Every 4 weeks, default "Every 4 weeks") + grind `<select aria-label="Grind">` (Whole bean / Drip / Espresso / French press, default "Whole bean") — same select classes as Row 1
- Price line (mt-6, flex items-baseline gap-2): one-time price 55% `line-through text-sm` "$19" + subscription price `price-swap` (verbatim class) Fraunces text-2xl `tabular-nums` "$16.15" — crossfades 140ms whenever bean/frequency changes (text swap only, fixed height); helper text below, text-xs 55%: "Recalculates automatically — subscribers save 15% on every bag"
- CTA: "Subscribe & save" `.add` full-width `rounded-lg bg-[var(--amber)] text-white px-6 py-3.5 font-medium mt-6`, hover 8% darker (background-color 140ms), `active:scale-[0.97]`; on click bumps cart badge, label swaps to "Added ✓" for 1.5s

BREW-GUIDE TEASER ROW (max-w-6xl mx-auto px-6 py-16)
- Title: "New to brewing?" Fraunces 600 text-2xl
- 3 cards, grid grid-cols-1 md:grid-cols-3 gap-6, `.card` reveal (verbatim, no hover crossfade needed — single image): `rounded-xl overflow-hidden aspect-[4/3]` `<img src="{YOUR_IMAGE_URL_GUIDE_N}" alt="…">`, caption below: title font-medium + "5 min read" text-xs 55% — "Pour-over, step by step" · "French press without the sludge" · "Dialing in espresso at home"

REVIEWS STRIP (max-w-6xl mx-auto px-6 pb-16)
- 3 review cards, grid md:grid-cols-3 gap-6, `.card` reveal stagger 50ms: `rounded-xl bg-[var(--wash)] p-6` — 5× lucide `Star` w-4 h-4 fill `--amber` + quote Inter text-sm 70% leading-relaxed + name text-xs 55%
  - "The Gedeb tastes like a fruit stand. I've never said that about coffee before." — Priya M.
  - "Subscription just works — it shows up two days before I run out, every time." — Owen K.
  - "Mogiana is my everyday cup now. Rich without being bitter." — Sana R.

FOOTER (border-t border-[var(--border)], py-12, max-w-6xl mx-auto px-6)
- 3 columns text-sm: Shop / Subscriptions / "Roast notes, monthly" newsletter — input `rounded-lg border border-[var(--border)] px-3 py-2 text-sm` + button "Sign up" `add rounded-lg bg-[var(--ink)] text-white px-4 py-2 text-sm font-medium`
- Bottom row: "© Grain & Gram" 55% + Instagram icon link (`aria-label="Instagram"`)

ANIMATIONS (complete list — browsing and building both stay instant)
- Entrances: card-rise 0.35s cubic-bezier(0.23, 1, 0.32, 1), stagger 50ms, IntersectionObserver once (hero on load)
- Filter chips: active state color-swap 150ms cubic-bezier(0.4, 0, 0.2, 1); filtered-out cards fade+scale 150ms cubic-bezier(0.4, 0, 0.2, 1), then removed from flow
- Hover: bean card lift −4px + alt-image crossfade 200ms — gated for touch
- Subscription price crossfade 140ms on every selector change (fixed height, no layout shift)
- Cart badge bump 0.3s cubic-bezier(0.34, 1.56, 0.64, 1) on add
- Press: `active:scale-[0.97]` on every button and chip
- No idle loops, no marquee, no parallax

RESPONSIVE
- Mobile: hero stacks, filter chips wrap and scroll if needed (no hidden overflow), bean grid 1-col, subscription builder selects stack to grid-cols-1, brew-guide/reviews stack, nav center links hidden (hamburger `Menu` button, `aria-label="Menu"`); no horizontal scroll

KEY DEPENDENCIES
`react@^18` `react-dom@^18` `typescript@^5` `vite@^5` `tailwindcss@^3` `lucide-react@latest`

CONSTRAINTS: ecommerce snap — entrances 0.25–0.5s, interactions ≤ 280ms; easing only from {cubic-bezier(0.23,1,0.32,1) · cubic-bezier(0.4,0,0.2,1) · cubic-bezier(0.34,1.56,0.64,1)}, never ease-in. Animate only transform/opacity (background-color/border-color state swaps ≤150ms are the documented paint exception). Exactly TWO accents: `--amber` for action and selection, `--moss` reserved for the subscription-savings badge only. No decorative gradients, no video, no blobs — the roast photography and tasting notes do the selling. Layer contract: media z-0 → badge z-[15] → nav z-20. Respect `prefers-reduced-motion`. Replace `{YOUR_IMAGE_URL_*}` with photography you have rights to, with real `alt` text. ARIA: `group` on the filter row, `aria-label` on every select and icon-only button; prices `tabular-nums` everywhere. Never apply `overflow-x: hidden` to `html`/`body` or a root wrapper — it creates a scroll container and silently breaks `position: sticky`; contain any horizontal bleed with `overflow-x: clip` on the overflowing section instead.
