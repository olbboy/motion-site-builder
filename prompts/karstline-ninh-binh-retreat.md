# Karstline — Ninh Bình Retreat

- **ID:** `karstline-ninh-binh-retreat`
- **Category:** Low-impact travel retreat
- **Type:** landing
- **Profile:** `cinematic`

---

Build a single-page booking landing for "Karstline" — a six-room Ninh Bình retreat designed around dawn paddles, limestone silhouettes, and unhurried time. Use React + Vite + Tailwind CSS + TypeScript + Framer Motion + lucide-react. Default Tailwind config, no other UI libraries.

SELECTED PEXELS MEDIA
- Source: [Ninh Bình rice field and river at sunset](https://www.pexels.com/photo/green-rice-field-2131956/) by Quang Nguyen Vinh.
- Download to `/media/vietnam/pexels-2131956.jpg`; use `<img src="/media/vietnam/pexels-2131956.jpg" alt="Sun rays crossing rice fields, river, and limestone karsts in Ninh Bình, Vietnam">`.
- Hero crop 16:9 `object-cover object-[50%_54%]`; reserve the lower-left 42% for copy and keep the sunbeam visible at all breakpoints.

FONTS
- Display: Instrument Serif 400; body: Manrope 400/500/600; labels: Azeret Mono 500.

COLORS
- `--night:#080A08` · `--ivory:#F5F0E6` · `--mist:rgba(245,240,230,.62)` · single accent `--sun:#F2C66D`.

GLOBAL CSS
```css
@keyframes karst-reveal { from { opacity:0; transform:translateY(24px); clip-path:inset(0 0 22% 0); } to { opacity:1; transform:none; clip-path:inset(0); } }
.karst-reveal { animation:karst-reveal .9s cubic-bezier(0.16, 1, 0.3, 1) backwards; }
.pressable { transition:transform 150ms cubic-bezier(0.16, 1, 0.3, 1); }
.pressable:active { transform:scale(.97); }
@media (hover:hover) and (pointer:fine) { .room-card:hover img { transform:scale(1.035); } }
@media (prefers-reduced-motion:reduce) { *,*::before,*::after { animation-duration:.01ms!important; animation-iteration-count:1!important; transition-duration:.01ms!important; scroll-behavior:auto!important; } }
```

SECTION ORDER
1. Six rooms between stone and water. 2. A day measured by light. 3. Sleep inside the landscape. 4. Leave less than you found.

HERO
- Full viewport image z-0, left-to-right scrim z-[1], content z-10, nav z-20. Nav is transparent with wordmark "KARSTLINE", links Stay / Rhythm / Stewardship, and bordered CTA "Check dates".
- Copy aligned bottom-left: eyebrow "TRÀNG AN · NINH BÌNH"; H1 `text-6xl md:text-[112px] tracking-[-.055em] leading-[.86]` text "Wake where / stone meets light."; subtext "Six rooms. Two wooden boats. One limestone valley before breakfast.".
- Booking bar `max-w-4xl grid grid-cols-[1fr_1fr_1fr_auto]` with Arrival / Nights / Guests and button "Find a quiet date"; `bg-black/45 backdrop-blur-xl border border-white/15 rounded-2xl`. Use native date/select controls with labels.

RHYTHM OF A DAY
- Paper-dark section `#0E110E`; horizontal time rail with four stops: 05:40 Dawn paddle, 09:10 Garden breakfast, 15:30 Cave shade, 18:05 Rice-field supper.
- On desktop, rail progress uses `scaleX` tied to section scroll; mobile renders a static vertical rail. Each stop reveals .65s with 100ms stagger.

ROOMS
- Three editorial image-free cards to avoid inventing media: "Water Room", "Reed Room", "Stone Room"; use line diagrams made from CSS borders only. Each card includes 42 m² / 2 guests / river-facing deck and price "from 4,800,000 ₫" in tabular nums.
- Cards `rounded-2xl border border-white/12 p-7 min-h-[360px]` with number, floor-plan diagram, amenities, CTA "See room"; hover translateY(-4px) gated, press .97.

STEWARDSHIP LEDGER
- Split layout: H2 "Leave less than you found." and four audited metrics: 92% local payroll, 71% greywater reused, 0 single-use plastic, 1% revenue to wetland restoration. No count-up animation; numbers reveal as a group.

FINAL BOOKING
- Reuse the hero photo in a 21:9 strip with `object-position:50% 68%`, heavy `bg-black/45` scrim; H2 "The valley is loudest before the day begins." and CTA "Check six-room availability".
- Footer contains photo source and photographer credit.

ANIMATIONS
- Hero .9s expo-out, 120ms stagger; time rail scaleX only; room/card reveal .65s once; hover translateY(-4px)/180ms and press .97/150ms. Gate scroll motion with `useReducedMotion()`.

RESPONSIVE
- Mobile booking bar stacks, hero H1 `text-6xl`, nav links hidden, rail vertical/static, room grid one column. Preserve sunbeam and karsts; no horizontal scroll.

KEY DEPENDENCIES
`react@^18` `react-dom@^18` `typescript@^5` `vite@^5` `tailwindcss@^3` `framer-motion@^11` `lucide-react@latest`

CONSTRAINTS: one gold accent; no video, blobs, radial gradients, carousel, or synthetic room photography. The selected landscape photo is the only photographic asset. Only transform/opacity/filter animate; explicit z-layers; reduced-motion safe; form controls labeled; nav and icon buttons have ARIA labels.
