# Fjellrev Shell Product Page

- **ID:** `fjellrev-shell-product-page`
- **Category:** Product Page
- **Type:** product-page
- **Profile:** `ecommerce`

---

Build a single product-detail page for "Fjellrev" — a technical outdoor brand — selling the "Vardø 3L Shell", a 3-layer alpine hardshell jacket. Alpine-light, imagery-first, spec-driven; every interaction confirms crisply. Use React + Vite + Tailwind CSS + TypeScript + lucide-react + embla-carousel-react. Default Tailwind config, no other UI libraries.

FONTS (Google Fonts, load via `<link>` in index.html)
- Display: Inter Tight (600/700) — product name, section titles, prices
- Body: Inter (400/500) — everything else; prices `tabular-nums`

COLORS (CSS variables on :root — alpine-light family, exactly two accents)
- --background: #FFFFFF · --wash: #F5F6F7 · --border: #E4E7EB · --foreground: #0F172A
- --signal: #FF5A1F (accent — CTA, selected states, active-thumb) · --alert: #DC2626 (low-stock/urgency ONLY)
- Text tiers: foreground 100% / 70% / 55%

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

.add { transition: transform 140ms cubic-bezier(0.23, 1, 0.32, 1), background-color 140ms cubic-bezier(0.23, 1, 0.32, 1); }
.add:active { transform: scale(0.97); }

.sticky-bar { transform: translateY(100%); transition: transform 250ms cubic-bezier(0.23, 1, 0.32, 1); }
.sticky-bar[data-visible="true"] { transform: translateY(0); }

@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { animation-duration: 0.01ms !important; animation-iteration-count: 1 !important; transition-duration: 0.01ms !important; }
}
```

NAVBAR (sticky top-0, z-20, bg-[var(--background)]/95 backdrop-blur-sm, border-b border-[var(--border)])
- max-w-6xl mx-auto px-6 h-16 flex items-center justify-between
- Left: "FJELLREV" — Inter Tight 700 text-lg tracking-tight
- Center (hidden md:flex, text-sm 70%): Shells · Insulation · Base layers · Repair — hover foreground 100%, color-only 150ms
- Right: cart button (`ShoppingBag`, `aria-label="Cart, 0 items"`) `rounded-lg p-2`, hover bg-[var(--wash)] 140ms, `active:scale-[0.97]`
- Breadcrumb strip under nav (max-w-6xl mx-auto px-6 py-3 text-xs 55%): "Shells / Hardshell / **Vardø 3L Shell**"

MAIN GRID (max-w-6xl mx-auto px-6 pb-16, lg:grid lg:grid-cols-[7fr_5fr] gap-12; z-10)

GALLERY (left, `.rise` on load)
- embla-carousel-react: 5 slides, each `rounded-xl overflow-hidden aspect-[4/5] bg-[var(--wash)]` with `<img src="{YOUR_IMAGE_URL_N}" alt="Vardø 3L Shell — front on model / back detail / pit-zip close-up / worn on a ridgeline in sleet / packed into its own hood pocket">` object-cover — embla's native translate handles slide motion
- Prev/next buttons (`ChevronLeft`/`ChevronRight`, `aria-label="Previous image"/"Next image"`): `rounded-full bg-[var(--foreground)]/70 backdrop-blur-sm p-2 absolute top-1/2 -translate-y-1/2 text-white`, hover bg 90% 140ms, `active:scale-[0.97]`
- Thumbnail rail (mt-4, flex gap-3): 5 buttons `rounded-lg overflow-hidden w-16 h-16 border-2 border-transparent`, inactive images opacity-55; active-thumb indicator = opacity-100 + `border-[var(--signal)]`, syncing to whichever slide embla currently shows; transitions opacity/border-color 140ms cubic-bezier(0.23, 1, 0.32, 1); `aria-label="View image N"`, press `active:scale-[0.97]`

BUY COLUMN (right, staggered `.rise` on load via `animation-delay`: name 0ms → rating 50ms → price 100ms → color 150ms → size 200ms → CTA 250ms → accordions 300ms)
- Kicker: "HARDSHELL · 3-LAYER" — Inter text-xs tracking-[0.14em] 55%
- Name: "Vardø 3L Shell" — Inter Tight 700 text-4xl md:text-5xl leading-[1.0]
- One-liner: "20,000mm waterproof, 15,000 g/m²/24h breathable, fully taped seams." — Inter text-base 70%
- Rating row: 5× lucide `Star` w-4 h-4 fill `--signal` + "4.7 · 386 reviews" text-sm 70%
- Price: "$379" — Inter Tight text-3xl `tabular-nums`
- COLOR SWATCHES (`role="radiogroup" aria-label="Color"`): 3 circular swatches `rounded-full w-8 h-8 border-2` — "Arctic White" (#F2F1ED) / "Basalt Grey" (#54555A) / "Signal Orange" (#FF5A1F, default selected); unselected border-[var(--border)], selected border-[var(--foreground)] + `ring-2 ring-offset-2 ring-[var(--foreground)]`; transition border-color/box-shadow 140ms cubic-bezier(0.23, 1, 0.32, 1); press `active:scale-[0.97]`
- SIZE SELECTOR (`role="radiogroup" aria-label="Size"`): 6 pills — "XS" · "S" · "M" (default) · "L" · "XL" · "XXL"; `rounded-lg border px-4 py-2.5 text-sm font-medium`; unselected = `border-[var(--border)]` foreground 70%; selected = `border-[var(--signal)] text-[var(--signal)]`; transition border-color/color 140ms cubic-bezier(0.23, 1, 0.32, 1); press `active:scale-[0.97]`; below the pills, text-xs `text-[var(--alert)]`: "Only 2 left in size M" (shown only for the M pill)
- ADD TO CART (paste verbatim, full width, signal variant):
```tsx
<button className="add w-full rounded-lg bg-[var(--signal)] px-6 py-3.5 font-medium text-white"
        onClick={bumpBadge} aria-label="Add to cart">
  Add to cart — $379
</button>
```
  On click: badge on the nav cart icon bumps for one cycle (verbatim `.cart-badge`/`bump` pattern: `@keyframes bump { 0% { transform: scale(1); } 40% { transform: scale(1.35); } 100% { transform: scale(1); } }` on `data-bumped="true"`, reset on `animationend`); label swaps to "Added ✓" for 1.5s (fixed height)
- Reassurance row (text-xs 55%, flex gap-4): "Free shipping $150+" · "60-day returns" · "Repairs for life"
- SPEC / FEATURE ACCORDION (border-t border-[var(--border)] divide-y divide-[var(--border)], mt-8): "Specs" (open by default) / "Construction" / "Fit & sizing"
  - Header button: flex justify-between py-4 text-sm font-medium, chevron rotates 0→180deg, 200ms cubic-bezier(0.23, 1, 0.32, 1), `aria-expanded`
  - Content: height is NOT animated — the panel appears instantly; its inner content fades + rises 8px, 200ms cubic-bezier(0.23, 1, 0.32, 1) (transform/opacity only)
  - "Specs" content: definition rows, label 55% / value `tabular-nums` font-medium — "Waterproof rating: 20,000mm hydrostatic head" · "Breathability: 15,000 g/m²/24h" · "Weight: 410g (size M)" · "Zips: YKK AquaGuard, fully taped seams" · "Pockets: 2 hand, 1 chest, 1 internal"

STICKY ADD-TO-CART BAR (fixed bottom-0 inset-x-0 z-30, `.sticky-bar` class, verbatim above)
- `bg-[var(--background)]/95 backdrop-blur-sm border-t border-[var(--border)] px-6 py-3 flex items-center justify-between max-w-6xl mx-auto`
- Left: thumbnail `w-10 h-10 rounded-lg object-cover` of the selected color + "Vardø 3L Shell · $379" text-sm font-medium
- Right: compact `.add` signal button "Add to cart"
- Appears once the gallery scrolls out of view: `data-visible` toggled by an IntersectionObserver on the gallery block; `translateY(100%)→0`, 250ms cubic-bezier(0.23, 1, 0.32, 1), reverse on scroll back up

CARE & REPAIR (bg-[var(--wash)] py-16)
- max-w-6xl mx-auto px-6 grid grid-cols-1 md:grid-cols-3 gap-8, each: lucide icon (`Droplets`/`Wind`/`Wrench`) + heading font-medium + one-liner 70% — "Wash cold, tumble dry low" / "Reactivate DWR with heat every 20 washes" / "Free repairs for the life of the jacket — send it back, we'll fix it" — reveal 0.35s stagger 50ms once via IntersectionObserver

FOOTER (border-t border-[var(--border)], py-12, max-w-6xl mx-auto px-6, flex justify-between, text-sm 55%)
- "Fjellrev — built for the shoulder season and the storm after it." + links Contact / Dealers / Instagram (`aria-label` on icon-only links)

ANIMATIONS (complete list — technical, never fussy)
- Entrances: card-rise/.rise 0.35s cubic-bezier(0.23, 1, 0.32, 1), buy-column stagger 50ms, IntersectionObserver once below the fold
- Gallery: embla translate; thumbnails opacity/border 140ms; active-thumb indicator syncs on slide change
- Hover: care-icon cards none (static); nav color-only 150ms
- Swatch/size selection border+ring 140ms · Accordion chevron 200ms, content fade-rise 200ms · Sticky bar translateY 250ms
- Cart badge bump 0.3s cubic-bezier(0.34, 1.56, 0.64, 1) on add
- Press: `active:scale-[0.97]` on every pressable
- Nothing loops; the gear holds the attention

RESPONSIVE
- Below lg: single column (gallery, then buy column); thumbnail rail scrolls horizontally in its own `overflow-x-auto` row; sticky add-to-cart bar remains full-width fixed at the bottom on every breakpoint; no page-level horizontal scroll

KEY DEPENDENCIES
`react@^18` `react-dom@^18` `typescript@^5` `vite@^5` `tailwindcss@^3` `lucide-react@latest` `embla-carousel-react@^8`

CONSTRAINTS: ecommerce snap — entrances 0.25–0.5s, interactions ≤ 280ms; easing only from {cubic-bezier(0.23,1,0.32,1) · cubic-bezier(0.4,0,0.2,1) · cubic-bezier(0.34,1.56,0.64,1)}, never ease-in. Animate only transform/opacity (border-color/background-color state swaps ≤150ms are the documented paint exceptions; accordion height is never animated). Exactly TWO accents: `--signal` for action and selection, `--alert` reserved for low-stock urgency only. No decorative gradients, no video, no blobs — the product photography and spec numbers are the drama. Layer contract: media z-0 → content z-10 → nav z-20 → sticky bar z-30. Respect `prefers-reduced-motion`. Replace `{YOUR_IMAGE_URL_*}` with photography you have rights to, with real `alt` text. ARIA: `radiogroup` on color and size, `aria-expanded` on accordions, labels on all icon-only buttons; prices `tabular-nums`. Never apply `overflow-x: hidden` to `html`/`body` or a root wrapper — it creates a scroll container and silently breaks `position: sticky`; contain any horizontal bleed with `overflow-x: clip` on the overflowing section instead.
