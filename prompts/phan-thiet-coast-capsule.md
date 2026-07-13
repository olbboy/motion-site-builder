# Phan Thiết Coast — Travel Capsule

- **ID:** `phan-thiet-coast-capsule`
- **Category:** Coastal travel apparel capsule
- **Type:** storefront
- **Profile:** `ecommerce`

---

Build a single-page storefront for "Phan Thiết Coast" — a five-piece fictional travel capsule tuned for salt air, scooter wind, sun, and one small weekender. Use React + Vite + Tailwind CSS + TypeScript + lucide-react + Embla Carousel. Default Tailwind config, no other UI libraries.

SELECTED PEXELS MEDIA
- Source: [Phan Thiết coastal road, flowers, and sea](https://www.pexels.com/photo/peaceful-coastal-landscape-in-phan-thiet-vietnam-37051053/) by Ngoc Nguyen.
- Download to `/media/vietnam/pexels-37051053.jpg`; use `<img src="/media/vietnam/pexels-37051053.jpg" alt="A quiet coastal road with green hills, bougainvillea, and blue sea in Phan Thiết, Vietnam">`.
- Hero crop 3:2 `object-cover object-[55%_52%]`; keep the road as a lead-in line and retain bougainvillea color at frame edge.

FONTS
- Display: Poppins 600/700; body: Inter 400/500/600; product codes: IBM Plex Mono 500.

COLORS
- `--salt:#FAFAF7 --surface:#FFFFFF --ink:#202421 --muted:#6D746F`; accents `--coast:#176F78` for action and `--bloom:#CF5C72` only for capsule tags.

GLOBAL CSS
```css
@keyframes coast-rise { from { opacity:0; transform:translateY(12px); } to { opacity:1; transform:none; } }
.coast-rise { animation:coast-rise .3s cubic-bezier(0.23, 1, 0.32, 1) backwards; }
.pressable { transition:transform 130ms cubic-bezier(0.23, 1, 0.32, 1); }
.pressable:active { transform:scale(.97); }
@media (hover:hover) and (pointer:fine) { .product-card:hover { transform:translateY(-4px); } }
@media (prefers-reduced-motion:reduce) { *,*::before,*::after { animation-duration:.01ms!important; animation-iteration-count:1!important; transition-duration:.01ms!important; } }
```

NAV
- Announcement "Fictional capsule · product media required"; main nav Women / Men / Objects / Field guide, logo "PHAN THIẾT COAST", search/account/cart.

HERO
- Bento `grid md:grid-cols-[1.45fr_.55fr] gap-3 p-3`: selected landscape photo left, right coral-tinted static panel.
- Photo tile `min-h-[72vh]` with bottom scrim and copy: badge "COAST 05"; H1 `text-5xl md:text-7xl text-white leading-[.95]` "Five pieces. One road south."; CTA "Shop the sample capsule".
- Right panel lists exact packing formula: Overshirt / Air tee / Pull-on trouser / Shade cap / Weekender; sample bundle 6,400,000 ₫.

CAPSULE GRID
- Five cards with local image targets and alt requirements: `/media/products/ptc-overshirt.jpg`, `ptc-air-tee.jpg`, `ptc-trouser.jpg`, `ptc-shade-cap.jpg`, `ptc-weekender.jpg`. Missing files show a neutral color block, product name, and "Product image required".
- Each card: product code, name, two colors, sample price, quick add. Gated lift -4px, press .97. No hover image swap unless both owned images exist.

PACK 3 WAYS
- Tabs Road morning / Beach noon / Town evening; each specifies a combination of the five products using line-item list and a 4:5 selected-photo crop only as place context. `role=tablist`, 160ms opacity transition.

MATERIAL NOTES
- Table Material / Weight / Finish / Care; label all specs fictional placeholders to replace. Add accessible native details for "Why no sustainability badges yet?" explaining claims require verification.

SIZE DRAWER + CART DRAWER
- Size guide right drawer and cart right drawer, one open at a time; translateX 200ms, focus trap, Escape close. Sizes XS–XL in labeled table; unit switch cm/in changes values instantly without motion.

FIELD GUIDE
- Selected photo full-width 21:9 with caption "Place reference, not product campaign photography" and Pexels provenance. Link "Read the coastal packing checklist".

ANIMATIONS
- Hero/grid .3s/50ms; tabs 160ms opacity; drawers 200ms; hover -4px gated; press .97. Embla only for mobile product row, drag/translate, no autoplay.

RESPONSIVE
- Bento stacks; hero photo 4:5; product grid becomes Embla below sm and grid above; tabs scroll locally; drawers full width; sticky mobile cart button.

KEY DEPENDENCIES
`react@^18` `react-dom@^18` `typescript@^5` `vite@^5` `tailwindcss@^3` `lucide-react@latest` `embla-carousel-react@^8`

CONSTRAINTS: fictional capsule, sample prices, and placeholder specs; exactly two accents. Landscape photo is context only. No video, decorative gradients, blobs, autoplay, fake product imagery, or unverified environmental claim. Only transform/opacity animate; product fallbacks required; accessible tabs/drawers/tables, reduced motion, Pexels credit.
