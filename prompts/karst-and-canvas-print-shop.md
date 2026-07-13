# Karst & Canvas — Graphic Poster Shop

- **ID:** `karst-and-canvas-print-shop`
- **Category:** Graphic landscape poster studio
- **Type:** product-page
- **Profile:** `ecommerce`

---

Build a single-page graphic-poster shop for "Karst & Canvas" — one licensed Hạ Long landscape transformed into three authored compositions through typography, duotone color, contour drawing, and field-note graphics. Use React + Vite + Tailwind CSS + TypeScript + lucide-react + Embla Carousel. Default Tailwind config, no other UI libraries.

SELECTED PEXELS MEDIA
- Source: [Green limestone cliffs in Hạ Long Bay](https://www.pexels.com/photo/majestic-limestone-cliffs-of-ha-long-bay-in-vietnam-35157921/) by Jennifer.
- Download to `/media/vietnam/pexels-35157921.jpg`; use `<img src="/media/vietnam/pexels-35157921.jpg" alt="Green limestone cliffs meeting tranquil blue water in Hạ Long Bay, Vietnam">`.
- Source crops from the same file: Wide 3:2 `object-[50%_50%]`; Quiet Left 4:5 `object-[34%_52%]`; Cliff Study 4:5 `object-[70%_48%]`. These are inputs, never standalone products. Every printable composition must materially transform the image with the specified graphic system; never offer a photo-only or unaltered option. Never upscale beyond the downloaded original's safe print resolution.

FONTS
- Display: Fraunces 500/600; body: Inter 400/500/600; edition data: IBM Plex Mono 400/500.

COLORS
- `--paper:#FAF9F5 --surface:#FFFFFF --ink:#1C1D1A --muted:#6B6D67`; accents `--pine:#2F5C49` for selection/CTA and `--oxide:#A75438` reserved for low-stock edition notices.

GLOBAL CSS
```css
@keyframes print-rise { from { opacity:0; transform:translateY(12px); } to { opacity:1; transform:none; } }
.print-rise { animation:print-rise .35s cubic-bezier(0.23, 1, 0.32, 1) backwards; }
.pressable { transition:transform 130ms cubic-bezier(0.23, 1, 0.32, 1); }
.pressable:active { transform:scale(.97); }
@media (hover:hover) and (pointer:fine) { .thumb:hover { transform:translateY(-3px); } }
@media (prefers-reduced-motion:reduce) { *,*::before,*::after { animation-duration:.01ms!important; animation-iteration-count:1!important; transition-duration:.01ms!important; } }
```

NAV
- Wordmark "KARST & CANVAS"; links Editions / Paper / Provenance; right search, account, cart. Announcement "Printed to order · sample edition".

PRODUCT HERO
- Desktop `grid-cols-[1.15fr_.85fr] gap-10 max-w-7xl px-6 py-10`.
- Left Embla carousel with three materially transformed designs, each inside a white mat but no fake room mockup. Composition 01 "Contour Type" uses the Wide crop at 72% opacity, a 2px pine contour SVG drawn over the cliff, and the words "LIMESTONE / 20.75° N" occupying 28% of the poster. Composition 02 "Duotone Tide" maps shadows to `#1C1D1A` and highlights to `#D7DFD2`, adds an oxide 12mm edition bar, and uses the Quiet Left crop. Composition 03 "Field Notes" uses the Cliff Study crop inside a 7-column editorial grid with location, source, and three observation captions. Thumbnail buttons use the composition names; no autoplay or fade plugin.
- Right sticky purchase panel: eyebrow "TRANSFORMED STUDY 01"; H1 "Limestone / After Rain" `text-5xl md:text-6xl`; source line "Source photograph by Jennifer via Pexels · graphic treatment by Karst & Canvas"; sample price from 1,900,000 ₫.
- Radio groups: Composition Contour Type/Duotone Tide/Field Notes; Size 30×45/50×75/70×105 cm; Paper Smooth cotton/Cold press; Frame Unframed/Black oak. Update sample price instantly and announce via `aria-live=polite`.
- CTA "Add print to cart", delivery estimate, edition note "Open edition · printed to order".

PRINT DETAIL
- Zoom-free detail grid showing the photo layer, graphic layer, and final composition side-by-side. The source-photo panel is visibly watermarked "SOURCE PREVIEW · NOT FOR SALE". Paper texture is represented by a neutral CSS swatch—not a fabricated macro photograph. Captions list transformation recipe and color-management disclaimer.

PROVENANCE
- Timeline: selected on Pexels → downloaded locally → composition transformed → proof approved → printed to order. Include clickable source, photographer, alt text, local path, a direct link to the current Pexels license, and a visible rule: "No unaltered or standalone source-photo sales." Add a license-check date field generated at build time.

PAPER COMPARISON
- Accessible two-column table for weight, surface, optical brighteners, max size. No invented sustainability certification; label all specs "configure with printer" until verified.

CART DRAWER
- z-30 translateX 200ms; composition thumbnail, size, paper, frame, quantity, sample subtotal; checkout button labeled "Continue with sample order".

ANIMATIONS
- Hero .35s/50ms; carousel native translate; selection opacity 150ms; thumb hover -3px; cart 200ms; press .97. No image zoom on hover, autoplay, or animated paper texture.

RESPONSIVE
- Purchase panel non-sticky; hero stacks image first; carousel 4:5; radio groups wrap; provenance becomes vertical; cart full width.

KEY DEPENDENCIES
`react@^18` `react-dom@^18` `typescript@^5` `vite@^5` `tailwindcss@^3` `lucide-react@latest` `embla-carousel-react@^8`

CONSTRAINTS: use one selected source photograph only and never sell or present it as an unaltered/standalone print. Every product is a materially transformed graphic poster with mandatory typography plus contour, duotone, or field-note treatment. Exactly two accents; all pricing/specs clearly sample or unverified. No video, fake room renders, decorative gradients, blobs, autoplay, image hover zoom, or ownership claim over the source photo. Only transform/opacity animate; accessible radios/cart/carousel; reduced motion and complete Pexels provenance.
