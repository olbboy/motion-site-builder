# Afterglow Camp — Sunset Kit

- **ID:** `afterglow-camp-kit`
- **Category:** Curated camp kit product page
- **Type:** product-page
- **Profile:** `ecommerce`

---

Build a single-page product page for "Afterglow Camp" — a compact two-person sunset kit organized around shade, supper, and a clean pack-out before dark. Use React + Vite + Tailwind CSS + TypeScript + lucide-react. Default Tailwind config, no other UI libraries.

SELECTED PEXELS MEDIA
- Source: [Hạ Long Bay sunset reflection](https://www.pexels.com/photo/majestic-sunset-over-vietnam-s-ha-long-bay-34635621/) by Ama Journey.
- Download to `/media/vietnam/pexels-34635621.jpg`; use `<img src="/media/vietnam/pexels-34635621.jpg" alt="Orange sunset reflected between dark limestone islands in Hạ Long Bay, Vietnam">`.
- Hero crop 16:9 `object-cover object-[50%_52%]`; preserve the orange reflection as the vertical visual spine.

FONTS
- Display: Fraunces 600; body: DM Sans 400/500/600; inventory/specs: Space Mono 500.

COLORS
- `--sand:#F6F0E5 --surface:#FFFFFF --ink:#211C18 --muted:#716961`; `--ember:#C85A2B` action accent; `--night:#2D3552` stock/weather-note accent.

GLOBAL CSS
```css
@keyframes kit-rise { from { opacity:0; transform:translateY(14px); } to { opacity:1; transform:none; } }
.kit-rise { animation:kit-rise .35s cubic-bezier(0.23, 1, 0.32, 1) backwards; }
.pressable { transition:transform 130ms cubic-bezier(0.23, 1, 0.32, 1); }
.pressable:active { transform:scale(.97); }
@media (hover:hover) and (pointer:fine) { .kit-card:hover { transform:translateY(-4px); } }
@media (prefers-reduced-motion:reduce) { *,*::before,*::after { animation-duration:.01ms!important; animation-iteration-count:1!important; transition-duration:.01ms!important; } }
```

NAV
- Wordmark "AFTERGLOW CAMP"; Shop / Kit list / Pack-out / Journal; right cart. Announcement "Fictional kit · sample storefront".

HERO
- Selected image top `min-h-[68vh]`, scrim from black/55 to transparent, explicit z layers. Copy bottom-left: label "KIT 02 · TWO PEOPLE · 6.8 KG"; H1 `text-5xl md:text-7xl leading-[.95] text-white` "Dinner, shade, and a clean exit."; sample price 5,900,000 ₫; CTA "Build the sample kit".

WHAT'S IN THE KIT
- Six product tiles using CSS line illustrations and exact names, so no fake photography: Low Table 1.8kg; Two Ground Chairs 2.4kg; Shade Wing 1.1kg; Supper Box 0.8kg; Twin Lanterns 0.4kg; Pack-out Roll 0.3kg.
- Each `.kit-card rounded-xl border p-5`; show replace/remove switch, role, weight, and sample component price. Recalculate total weight/price with `aria-live=polite`; no animated counters.

PACKING LAYERS
- Four stacked horizontal diagrams: Wet / Food / Light / Leave-no-trace. Clicking layer expands native `<details>` content; no animated height. Use static 10-cell capacity bars.

FIELD MOOD, NOT PRODUCT PROOF
- Split section uses selected photo in 4:3 and text clearly stating the image establishes the sunset context and does not depict the kit. Four planning prompts: sunset time / tide / access / pack-out deadline—no live data.

ADD-ONS
- Three cards with local placeholders: `/media/products/afterglow-tarp.jpg`, `afterglow-flask.jpg`, `afterglow-groundsheet.jpg`; designed fallback if absent. Quick add buttons.

STICKY BUY BAR
- Bottom z-30 on mobile and after hero on desktop: current kit count, total weight, sample price, CTA "Add sample kit"; press .97.

ANIMATIONS
- Tiles .35s/50ms; selected photo static; total updates opacity 150ms; card hover -4px gated; sticky CTA press .97. No carousel, autoplay, animated sunset, or count-up.

RESPONSIVE
- Hero 4:5; tiles 1→2→3; packing layers full width; buy bar compact; nav links hidden. Prevent content behind sticky bar with bottom padding.

KEY DEPENDENCIES
`react@^18` `react-dom@^18` `typescript@^5` `vite@^5` `tailwindcss@^3` `lucide-react@latest`

CONSTRAINTS: fictional product and sample prices; exactly two accents; no claim photo shows products, video, gradients, blobs, autoplay, or weight/price animation. Missing add-on images use designed fallbacks. Only transform/opacity animate; labeled switches/details, reduced motion, source and credit visible.
