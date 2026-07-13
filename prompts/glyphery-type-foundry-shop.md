# Glyphery Type Foundry Shop

- **ID:** `glyphery-type-foundry-shop`
- **Category:** Storefront
- **Type:** storefront-digital-goods
- **Profile:** `ecommerce`

---

Build a single-page storefront for "Glyphery" — an independent digital type foundry selling font licenses — with a live type-tester on every family card, a license picker, and a slide-in cart. Typography-forward but conversion-focused; browsing and licensing both stay snappy. Use React + Vite + Tailwind CSS + TypeScript + lucide-react. Default Tailwind config, no other UI libraries.

FONTS (Google Fonts, load via `<link>` in index.html — stand-ins for Glyphery's fictional proprietary families, swap for real webfont files in production)
- Display/UI: Space Grotesk (500/700) — nav, headings, prices
- Body: Inter (400/500) — everything else; prices `tabular-nums`
- Specimen stand-ins (loaded for the live tester, all weights 400–700 unless noted): Inter (for "Glyphery Sans"), Fraunces (for "Fjord Serif"), Space Grotesk (for "Nordic Grotesk"), JetBrains Mono (for "Halide Mono")

COLORS (CSS variables on :root — ink-paper family, exactly two accents)
- --paper: #FFFFFF · --wash: #F5F5F5 · --border: #E5E5E5 · --ink: #111111
- --signal: #4F46E5 (accent — CTA, selected license, variable-font badge) · --sale: #E11D48 (unused on this page — reserved for future sale states)
- Text tiers: ink 100% / 70% / 55%

GLOBAL CSS (paste verbatim)
```css
@keyframes card-rise { from { opacity: 0; transform: translateY(12px); } to { opacity: 1; transform: none; } }
.card { animation: card-rise 0.35s cubic-bezier(0.23, 1, 0.32, 1) backwards; }

.license-card { transition: border-color 140ms cubic-bezier(0.23, 1, 0.32, 1), background-color 140ms cubic-bezier(0.23, 1, 0.32, 1); }
.license-card:active { transform: scale(0.98); transition: transform 140ms cubic-bezier(0.23, 1, 0.32, 1); }

.price-swap { transition: opacity 140ms cubic-bezier(0.23, 1, 0.32, 1); }

@keyframes bump { 0% { transform: scale(1); } 40% { transform: scale(1.35); } 100% { transform: scale(1); } }
.cart-badge[data-bumped="true"] { animation: bump 0.3s cubic-bezier(0.34, 1.56, 0.64, 1); }
.add { transition: transform 140ms cubic-bezier(0.23, 1, 0.32, 1), background-color 140ms cubic-bezier(0.23, 1, 0.32, 1); }
.add:active { transform: scale(0.97); }

.scrim { opacity: 0; pointer-events: none; transition: opacity 200ms cubic-bezier(0.4, 0, 0.2, 1); }
.scrim[data-open="true"] { opacity: 1; pointer-events: auto; }

.drawer { transform: translateX(100%); transition: transform 280ms cubic-bezier(0.23, 1, 0.32, 1); }
.drawer[data-open="true"] { transform: translateX(0); }

@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { animation-duration: 0.01ms !important; animation-iteration-count: 1 !important; transition-duration: 0.01ms !important; }
}
```

NAVBAR (sticky top-0, z-20, bg-[var(--paper)]/95 backdrop-blur-sm, border-b border-[var(--border)])
- max-w-6xl mx-auto px-6 h-16 flex items-center justify-between
- Left: "GLYPHERY" — Space Grotesk 700 text-xl tracking-tight
- Center (hidden md:flex, text-sm 70%): Typefaces · Foundry · Journal — hover ink 100%, color-only 150ms
- Right: cart button (`ShoppingBag`, `aria-label="Cart, 0 items"`) with `cart-badge` count badge (`bg-[var(--signal)] text-white text-[10px] rounded-full w-4 h-4 grid place-items-center tabular-nums absolute -top-1 -right-1`, verbatim bump keyframe); `rounded-lg p-2`, hover bg-[var(--wash)] 140ms, `active:scale-[0.97]`

HERO (max-w-6xl mx-auto px-6 py-16 text-center)
- H1: "Type, done properly." — Space Grotesk 700 text-5xl md:text-7xl tracking-tight leading-[1.0]
- Subtext (max-w-xl mx-auto mt-4, text-base 70%): "Four independent families. One license model. Test every weight before you buy."
- Entrance: H1 + subtext fade-rise 12px, 0.35s cubic-bezier(0.23, 1, 0.32, 1), stagger 50ms — once, on load

TYPE FAMILY GRID (max-w-6xl mx-auto px-6 pb-16, grid grid-cols-1 lg:grid-cols-2 gap-6)
- 4 family cards, `.card` (verbatim), reveal stagger 50ms via IntersectionObserver once; each `rounded-xl border border-[var(--border)] p-6 bg-[var(--paper)]`:
  - Header row (flex justify-between items-start): family name Space Grotesk 700 text-2xl (rendered in that family's own stand-in font) + "Variable" badge (only on variable families) `rounded-lg bg-[var(--signal)] text-white text-[11px] font-medium px-2 py-0.5`
  - Meta line (text-xs 55% mt-1): "{weight count} weights · {style count} styles" e.g. "9 weights · 2 widths"
  - LIVE TYPE-TESTER (mt-4): `<input>` `w-full rounded-lg border border-[var(--border)] px-3 py-2 text-sm mb-3` placeholder "Type to test {family name}", `aria-label="Type-tester for {family name}"`; bound via `onChange` to a preview `<div>` `mt-2 text-3xl md:text-4xl leading-tight break-words` styled `fontFamily: {family's stand-in font}` — preview text = input value, falling back to the family's default sample "The quick fox jumps." when the input is empty; no animation on keystroke, the preview updates on every render (state, not transition)
  - LICENSE PICKER (mt-5, `role="radiogroup" aria-label="License for {family name}"`, grid grid-cols-3 gap-2): 3 `.license-card` (verbatim) buttons — "Desktop" / "Web" / "App" — `rounded-lg border p-3 text-center`; unselected = `border-[var(--border)]`; selected = `border-[var(--signal)] bg-[var(--signal)]/5`; each shows license name text-sm font-medium + price `tabular-nums` text-xs 70% below it; default selection = "Desktop"
  - Footer row (mt-5 flex items-center justify-between): price `price-swap` (verbatim class) Space Grotesk text-xl `tabular-nums` reflecting the selected license — crossfades 140ms on license change (text swap, fixed height) + "Add to cart" `.add` `rounded-lg bg-[var(--signal)] text-white px-5 py-2.5 text-sm font-medium` `aria-label="Add {family name} {selected license} license to cart"`; on click bumps the nav cart badge and label swaps to "Added ✓" for 1.5s
- Families:
  - Glyphery Sans — variable, 9 weights · 2 widths — Desktop $149 · Web $249 · App $349
  - Fjord Serif — 6 weights, not variable — Desktop $129 · Web $199 · App $299
  - Nordic Grotesk — variable, 12 weights — Desktop $179 · Web $279 · App $399
  - Halide Mono — 4 weights, not variable — Desktop $89 · Web $149 · App $219

CART DRAWER (fixed inset-y-0 right-0 z-30, `.drawer` class, verbatim, `w-full max-w-md bg-[var(--paper)] border-l border-[var(--border)] p-6 flex flex-col`, `role="dialog" aria-label="Cart"`)
- Scrim: `.scrim` (verbatim) `fixed inset-0 bg-black/40 z-20`, closes drawer on click
- Header (flex justify-between items-center): "Your cart" Space Grotesk 700 text-xl + close button (`X`, `aria-label="Close cart"`) `rounded-lg p-2`, hover bg-[var(--wash)] 140ms, `active:scale-[0.97]`
- Line items (flex-1 overflow-y-auto mt-6 divide-y divide-[var(--border)]): each row py-4 flex justify-between text-sm — family name + license type 55% below it, price `tabular-nums` font-medium
- Footer (border-t border-[var(--border)] pt-4 mt-4): subtotal row "Subtotal" + `tabular-nums` font-medium text-lg, then "Checkout" `.add` full-width `rounded-lg bg-[var(--signal)] text-white px-6 py-3.5 font-medium`, `active:scale-[0.97]`
- Opens whenever an item is added to cart (`data-open="true"`); `translateX(100%)→0`, 280ms cubic-bezier(0.23, 1, 0.32, 1); scrim fades 200ms cubic-bezier(0.4, 0, 0.2, 1) in parallel

FOOTER (border-t border-[var(--border)], py-12, max-w-6xl mx-auto px-6, flex justify-between, text-sm 55%)
- "Glyphery — an independent type foundry." + links Contact / Journal / Instagram (`aria-label` on icon-only links)

ANIMATIONS (complete list — testing a typeface never waits)
- Entrances: card-rise 0.35s cubic-bezier(0.23, 1, 0.32, 1), stagger 50ms, IntersectionObserver once (hero on load)
- License selection: border-color/background-color 140ms + price crossfade 140ms (fixed height, no layout shift)
- Cart drawer: translateX 280ms cubic-bezier(0.23, 1, 0.32, 1); scrim opacity 200ms cubic-bezier(0.4, 0, 0.2, 1), in parallel
- Cart badge bump 0.3s cubic-bezier(0.34, 1.56, 0.64, 1) on add
- Press: `active:scale-[0.97]` on every button, `active:scale-[0.98]` on license cards
- Type-tester preview updates instantly on keystroke — no transition, no debounce; nothing loops

RESPONSIVE
- Mobile: family grid 1-col, license picker stays 3-col within the card (compress padding, not columns), cart drawer becomes full-width (`max-w-full`), nav center links hidden (hamburger `Menu` button, `aria-label="Menu"`); no horizontal scroll

KEY DEPENDENCIES
`react@^18` `react-dom@^18` `typescript@^5` `vite@^5` `tailwindcss@^3` `lucide-react@latest`

CONSTRAINTS: ecommerce snap — entrances 0.25–0.5s, interactions ≤ 280ms; easing only from {cubic-bezier(0.23,1,0.32,1) · cubic-bezier(0.4,0,0.2,1) · cubic-bezier(0.34,1.56,0.64,1)}, never ease-in. Animate only transform/opacity (border-color/background-color state swaps ≤150ms are the documented paint exception). Exactly TWO accents: `--signal` for action, selection, and the variable-font badge; `--sale` reserved and unused on this page. No decorative gradients, no video, no blobs — the typography is the drama. Layer contract: content z-10 → nav z-20 → scrim z-20 → drawer z-30. Respect `prefers-reduced-motion`. Fonts are open-licensed Google Fonts standing in for Glyphery's fictional proprietary families — replace with real webfont files in production. ARIA: `radiogroup` on each license picker, `role="dialog"` on the cart drawer, labels on every icon-only button and type-tester input; prices `tabular-nums` everywhere.
