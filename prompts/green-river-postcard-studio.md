# Green River — Postcard Studio

- **ID:** `green-river-postcard-studio`
- **Category:** Interactive postcard maker
- **Type:** creative-tool
- **Profile:** `playful`

---

Build a single-page interactive postcard maker for "Green River Studio" — a playful tool that lets visitors crop one Vietnamese river photograph, choose a paper treatment, write 180 characters, and export a print-ready preview locally. Use React + Vite + Tailwind CSS + TypeScript + lucide-react. Default Tailwind config, no other UI libraries.

SELECTED PEXELS MEDIA
- Source: [Lush Vietnamese river landscape](https://www.pexels.com/photo/serene-river-landscape-in-vietnam-s-lush-greenery-36578782/) by Jolenne 87.
- Download to `/media/vietnam/pexels-36578782.jpg`; use `<img src="/media/vietnam/pexels-36578782.jpg" alt="A calm river reflecting dense green tropical vegetation in Vietnam">`.
- Default crop 3:2 `object-cover object-[50%_52%]`; offer only three preset focal positions Left bank / Center reflection / Right canopy—no freeform drag library.

FONTS
- Display: Bricolage Grotesque 700; body: DM Sans 400/500/700; stamp text: Space Mono 700.

COLORS
- `--desk:#FFF3D9 --ink:#1E2935 --pink:#FF668A --blue:#3E8BFF --green:#38A169 --yellow:#F6C945`; roles: action / selection / success / stamps.

GLOBAL CSS
```css
@keyframes studio-pop { from { opacity:0; transform:scale(.93) translateY(18px); } to { opacity:1; transform:none; } }
.studio-pop { animation:studio-pop .5s cubic-bezier(0.18, 0.89, 0.32, 1.28) backwards; }
.pressable { transition:transform 160ms cubic-bezier(0.34, 1.56, 0.64, 1); }
.pressable:active { transform:scale(.94); }
@media (hover:hover) and (pointer:fine) { .tool:hover { transform:translateY(-3px); } }
@media (prefers-reduced-motion:reduce) { *,*::before,*::after { animation-duration:.01ms!important; animation-iteration-count:1!important; transition-duration:.01ms!important; } }
```

APP HEADER
- Wordmark "GREEN RIVER / POSTCARD LAB"; tiny badge "LOCAL PREVIEW"; buttons Reset and Export PNG. Export is a specified UI state only unless the builder implements canvas safely; if not implemented, show a clear toast "Export wiring required" rather than fake a download.

WORKBENCH
- Desktop `grid-cols-[320px_minmax(0,1fr)] gap-8 max-w-7xl`; tool panel left, live postcard preview right. Warm desk background with static paper-cut shapes z-5.

TOOL PANEL
- Section 1 Crop: three 44px buttons Left bank / Center reflection / Right canopy using `aria-pressed`; set exact object positions 32%/50%/68%.
- Section 2 Paper: Clean / Warm / Risograph. Treatments are CSS-only: Clean none; Warm `sepia(.12) saturate(.9)`; Risograph `grayscale(.15) contrast(1.08) saturate(.75)` plus a static blue/pink 1px border offset, no animated filter.
- Section 3 Message: textarea maxLength 180, live count `aria-live=polite`; alignment left/center; text color ink/white.
- Section 4 Stamp: River / Hello / 2026, decorative and `aria-hidden` in preview; controls remain labeled.

POSTCARD PREVIEW
- Front card fixed 3:2 within responsive stage; selected photo fills canvas; message sits within 12% safe area and never overlaps source credit printed at bottom-right in 10px.
- Flip button toggles front/back; back is cream with address lines, message, and fake stamp. Flip uses opacity crossfade + rotateY only if perspective remains keyboard-safe; reduced motion uses opacity only. Toggle button text changes "Show back"/"Show front".

PRESET RECIPES
- Three buttons below preview: Quiet morning / Green everywhere / Wish you were slower. Applying a preset updates crop/treatment/message with one 180ms fade, never auto-cycles.

SOURCE DRAWER
- Accessible disclosure includes source URL, photographer, alt text, local filename, and reminder not to hotlink.

ANIMATIONS
- Initial .5s pop; controls press .94/160ms; gated tool hover -3px; preview changes opacity 180ms; optional flip 240ms ease-in-out, reduced motion opacity only. No floating stamp, infinite grain, carousel, or cursor trail.

RESPONSIVE
- Tools above preview; preview width `min(100%,900px)`; controls 44px min; textarea full width; static decor clipped. No page overflow.

KEY DEPENDENCIES
`react@^18` `react-dom@^18` `typescript@^5` `vite@^5` `tailwindcss@^3` `lucide-react@latest`

CONSTRAINTS: exactly four functional accents; no server upload, fake successful export, third-party cropper, video, carousel, or infinite animation. Work locally with the selected image; preserve source credit inside preview metadata. Only transform/opacity/filter animate; accessible pressed states, live count, reduced motion.
