# Bay Bounce — Island Club

- **ID:** `bay-bounce-island-club`
- **Category:** Small-group bay day club
- **Type:** campaign
- **Profile:** `playful`

---

Build a single-page campaign for "Bay Bounce" — a small-group day club mixing slow cruising, kayak loops, floating lunch, and swim stops among limestone islands. Use React + Vite + Tailwind CSS + TypeScript + lucide-react. Default Tailwind config, no other UI libraries.

SELECTED PEXELS MEDIA
- Source: [Cruise boats among Hạ Long karsts](https://www.pexels.com/photo/scenic-cruise-on-ha-long-bay-vietnam-37324365/) by Frank van Dijk.
- Download to `/media/vietnam/pexels-37324365.jpg`; use `<img src="/media/vietnam/pexels-37324365.jpg" alt="Boats navigating calm water between green limestone karsts in Hạ Long Bay, Vietnam">`.
- Hero crop 3:2 `object-cover object-[50%_52%]`; preserve boats and two framing karsts.

FONTS
- Display: Anton 400; body: DM Sans 400/500/700; labels: Space Mono 700.

COLORS
- `--foam:#F7FFF7 --navy:#13233A --splash:#26C6DA --mango:#FFB82E --coral:#FF607C --kelp:#3CA66B`; roles: water / time / CTA / route.

GLOBAL CSS
```css
@keyframes splash-in { from { opacity:0; transform:scale(.9) translateY(26px); } to { opacity:1; transform:none; } }
.splash-in { animation:splash-in .5s cubic-bezier(0.18, 0.89, 0.32, 1.28) backwards; }
.pressable { transition:transform 160ms cubic-bezier(0.34, 1.56, 0.64, 1); }
.pressable:active { transform:scale(.94); }
@media (hover:hover) and (pointer:fine) { .bounce-card:hover { transform:translateY(-6px) rotate(-1deg); } }
@media (prefers-reduced-motion:reduce) { *,*::before,*::after { animation-duration:.01ms!important; animation-iteration-count:1!important; transition-duration:.01ms!important; } }
```

HERO
- Cream canvas with static wavy cyan border at top/bottom. Nav: "BAY BOUNCE" life-ring wordmark, links Loop / Lunch / Swim / Safety, coral CTA "Save a float".
- `max-w-7xl grid md:grid-cols-2`; left mango badge "12 PEOPLE MAX"; H1 `text-7xl md:text-[116px] leading-[.88] uppercase` "BIG BAY. / TINY CREW."; copy "One bright day threaded between karsts—with time to paddle, eat, float, and do absolutely nothing.".
- Right selected photo `rounded-[44px] border-4 border-[var(--navy)] shadow-[14px_16px_0_var(--splash)]`; overlay three static sticker bubbles "KAYAK", "LUNCH", "SWIM".

DAY LOOP
- Wavy but static route line connecting 08:10 Harbor hello → 09:20 Karst paddle → 12:00 Floating lunch → 14:15 Swim cove → 17:10 Home glow. Each stop is a `.bounce-card` with icon, time, exact one-line copy.
- Route line is SVG, no draw animation; cards pop once .5s/80ms stagger.

WHAT FITS ON BOARD
- Bento grid: 12 seats / 8 kayaks / 4 shade canopies / 1 giant fruit tray / 0 loudspeakers. Use oversized numbers, tabular nums, and CSS illustrations.

PICK YOUR PACE
- Accessible segmented control with `aria-pressed`: Float / Paddle / Mix. Result panel changes activity allocation: Float 70/20/10, Paddle 25/60/15, Mix 40/40/20. Use static 10-cell bars, not animated widths.

SAFETY, BUT FRIENDLY
- Four cards: life jackets sized on shore; weather call at 06:00; guide ratio 1:6; route changes beat risky promises. Warning icon paired with text, never color alone.

BOOKING CTA
- Navy panel with mango title "Bring sunscreen. Leave the schedule."; date select, guests stepper 1–12, CTA "Hold my float". Demo price "from 1,850,000 ₫ / guest" explicitly labeled sample copy.
- Footer shows Pexels source and photographer.

ANIMATIONS
- Pop .5s/80ms; card hover translateY -6px rotate -1° gated; press .94/160ms; result opacity 180ms. No bobbing icons, infinite wave motion, marquee, or autoplay.

RESPONSIVE
- H1 text-7xl; hero photo after copy; route becomes vertical; bento 2 columns; booking fields stack; stickers stay inside image bounds.

KEY DEPENDENCIES
`react@^18` `react-dom@^18` `typescript@^5` `vite@^5` `tailwindcss@^3` `lucide-react@latest`

CONSTRAINTS: four-role palette, loud typography, controlled motion. No video, carousel, infinite animation, false safety certification, or live pricing claim. Only transform/opacity animate; static segmented bars; labeled inputs; reduced motion; source credit visible.
