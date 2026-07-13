# Limestone Carry — Travel Gear Store

- **ID:** `limestone-carry-travel-gear`
- **Category:** Modular travel gear storefront
- **Type:** ecommerce
- **Profile:** `ecommerce`

---

Build a single-page storefront for "Limestone Carry" — modular soft luggage designed for boats, wet docks, and short limestone-bay expeditions. Use React + Vite + Tailwind CSS + TypeScript + lucide-react + Embla Carousel. Default Tailwind config, no other UI libraries.

SELECTED PEXELS MEDIA
- Source: [Hạ Long Bay limestone cliffs](https://www.pexels.com/photo/ha-long-bay-in-vietnam-26854908/) by Chu Phi.
- Download to `/media/vietnam/pexels-26854908.jpg`; use `<img src="/media/vietnam/pexels-26854908.jpg" alt="Lush limestone cliffs rising from calm water in Hạ Long Bay, Vietnam">`.
- Hero crop 16:9 `object-cover object-[52%_48%]`; preserve the cliff/water seam and keep lower-left copy over a 42% black scrim.

FONTS
- Display: Inter Tight 600/700; body: Inter 400/500/600; specs: IBM Plex Mono 500.

COLORS
- `--bg:#F7F7F3 --surface:#FFFFFF --ink:#18201D --muted:#68706C`; accents: `--brand:#315E4A` for action and `--signal:#E36A3D` only for low-stock/service notices.

GLOBAL CSS
```css
@keyframes product-rise { from { opacity:0; transform:translateY(14px); } to { opacity:1; transform:none; } }
.product-rise { animation:product-rise .35s cubic-bezier(0.23, 1, 0.32, 1) backwards; }
.pressable { transition:transform 130ms cubic-bezier(0.23, 1, 0.32, 1); }
.pressable:active { transform:scale(.97); }
@media (hover:hover) and (pointer:fine) { .product-card:hover { transform:translateY(-4px); } }
@media (prefers-reduced-motion:reduce) { *,*::before,*::after { animation-duration:.01ms!important; animation-iteration-count:1!important; transition-duration:.01ms!important; } }
```

NAV (z-20)
- Announcement "Free repair assessment for 5 years"; main nav logo, Bags / Modules / Field notes / Repairs, search, account, cart with badge. Icon buttons labeled.

HERO (media z-0, scrim z-[1], content z-10)
- Selected image `min-h-[72vh]`; left copy: mono "WATERLINE SERIES · 2026"; H1 `text-5xl md:text-7xl leading-[.95]` "Pack for the transfer, not the terminal."; sub "Soft-sided modules sized for narrow decks, wet landings, and one clean change of clothes."; CTA "Shop Waterline" and secondary "See the system".

MODULAR SYSTEM
- Four product cards, each with local placeholder paths and required alt text: `/media/products/limestone-deck-38.jpg` Deck 38L 3,900,000 ₫; `/media/products/limestone-cube-12.jpg` Dry Cube 12L 1,250,000 ₫; `/media/products/limestone-sling-4.jpg` Tide Sling 4L 980,000 ₫; `/media/products/limestone-roll.jpg` Map Roll 650,000 ₫.
- Missing product image must render a designed neutral panel with product name, never broken image. Cards show capacity, material, price, quick add; hover lift -4px gated, press .97.

SYSTEM BUILDER
- Accessible 3-step configurator: Trip length 1/2/4 nights; Transfer Boat/Train/Motorbike; Weather Dry/Mixed/Monsoon. Result lists exact modules and sample total; updates with 160ms opacity only.

FIELD PROOF
- Split: selected landscape photo in 4:3 crop right, left has four specs: 420D recycled nylon; taped base seam; 18 cm deck clearance; repairable hardware. Do not imply the photograph depicts the product.

REPAIR LEDGER
- Four service steps with turnaround samples; expandable details use native `<details>` and no animated height. CTA "Start a repair request".

CART DRAWER
- Right drawer z-30, translateX 100→0 over 200ms; line items, quantity stepper, subtotal, checkout button. Full focus trap and Escape close.

ANIMATIONS
- Products .35s/50ms stagger; cart 200ms; system result fade 160ms; hover -4px gated; press .97/130ms. Embla uses drag/translate only, no autoplay.

RESPONSIVE
- Hero 4:5 crop with text bottom; product grid 1→2→4; builder stacks; cart full width below sm; nav categories hidden behind menu.

KEY DEPENDENCIES
`react@^18` `react-dom@^18` `typescript@^5` `vite@^5` `tailwindcss@^3` `lucide-react@latest` `embla-carousel-react@^8`

CONSTRAINTS: fictional brand and sample prices; exactly two accents. No video, decorative gradients, blobs, autoplay carousel, or claim that source photo shows products. Product placeholders must be replaced with owned media. Only transform/opacity animate; cart accessibility, reduced motion, Pexels source/credit in field proof and footer.
