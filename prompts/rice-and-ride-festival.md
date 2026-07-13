# Rice & Ride — Riverside Festival

- **ID:** `rice-and-ride-festival`
- **Category:** Community cycling and food festival
- **Type:** event
- **Profile:** `playful`

---

Build a single-page event site for "Rice & Ride" — a fictional riverside festival pairing a gentle community ride, field-edge food stalls, repair workshops, and boat-side music. Use React + Vite + Tailwind CSS + TypeScript + lucide-react. Default Tailwind config, no other UI libraries.

SELECTED PEXELS MEDIA
- Source: [Farmer, rice field, river, and boats](https://www.pexels.com/photo/farmer-in-a-rice-field-by-the-river-with-boats-30228484/) by Vũ Bụi.
- Download to `/media/vietnam/pexels-30228484.jpg`; use `<img src="/media/vietnam/pexels-30228484.jpg" alt="A farmer working beside a green rice field and calm river lined with wooden boats">`.
- Poster crop 4:5 `object-cover object-[48%_52%]`; keep the person, field edge, and boats visible; never place text over the person.

FONTS
- Display: Paytone One 400; body: Space Grotesk 400/500/700; schedule: IBM Plex Mono 500.

COLORS
- `--rice:#FFF4C7 --ink:#18332B --tomato:#F05A3D --river:#1EB5C3 --leaf:#53A451 --sun:#F5C542`; roles: CTA / route / food / time.

GLOBAL CSS
```css
@keyframes festival-pop { from { opacity:0; transform:scale(.91) translateY(24px) rotate(1deg); } to { opacity:1; transform:none; } }
.festival-pop { animation:festival-pop .55s cubic-bezier(0.18, 0.89, 0.32, 1.28) backwards; }
.pressable { transition:transform 170ms cubic-bezier(0.34, 1.56, 0.64, 1); }
.pressable:active { transform:scale(.94); }
@media (hover:hover) and (pointer:fine) { .ticket:hover { transform:scale(1.05) rotate(-1deg); } }
@media (prefers-reduced-motion:reduce) { *,*::before,*::after { animation-duration:.01ms!important; animation-iteration-count:1!important; transition-duration:.01ms!important; } }
```

HERO POSTER
- `min-h-[92svh] bg-[var(--rice)]`; nav with wordmark, Schedule / Route / Food / Care, tomato CTA "Get a day pass".
- Split layout: left H1 `text-6xl md:text-[112px] leading-[.88]` "RICE / & RIDE"; badge "FICTIONAL FESTIVAL · 19 JUL · 06:30–20:00"; sub "A 22 km no-drop loop, a long lunch, and the repair skills to ride home.".
- Right selected photo in `rounded-[36px] border-4 border-[var(--ink)]`; frame includes a separate bottom caption bar, never over the subject. Static wheel/leaf doodles z-5.

TICKET STRIP
- Three `.ticket` options: Ride only 180,000 ₫; Ride + lunch 320,000 ₫; Full day 460,000 ₫. Mark every price "sample event copy". Perforated edge via CSS radial background is allowed in playful profile but remains static.

SCHEDULE
- Tabs All / Ride / Food / Workshop / Music with `aria-selected`; 8 exact events from 06:30 check-in to 19:15 acoustic boat-side set. Schedule cards fade 180ms when filtering; no stagger on every filter change.

ROUTE MAP WITHOUT A MAP
- Honest route narrative, not geospatial drawing: Start gate → River shade → Field turn → Repair stop → Lunch lawn → Home bridge. Six numbered cards in a serpentine CSS grid; each has distance-to-next and surface type.

WORKSHOP MENU
- Four cards: Fix a flat 25m / Brake check 20m / Load a bike 15m / Rain-ready layers 20m. Booking button opens a native dialog with time slots and attendee name.

COMMUNITY CODE
- Big four: Ask before portraits / Buy from named stalls / Carry your bottle / No rider left. Each uses icon + text and a unique role color.

FINAL CTA
- River-cyan panel: "Ride slow enough to taste lunch." CTA "Get the sample pass"; footer labels event and brands fictional and credits the selected photo.

ANIMATIONS
- Festival pop .55s/90ms; gated ticket hover scale 1.05; press .94/170ms; schedule filter opacity 180ms; dialog scale .96→1 200ms. No marquee, confetti loop, countdown timer, or photo motion.

RESPONSIVE
- Hero stacks; photo 4:5; tickets one column; schedule filters horizontally scroll inside their own row; serpentine route becomes vertical; dialog full-screen below sm.

KEY DEPENDENCIES
`react@^18` `react-dom@^18` `typescript@^5` `vite@^5` `tailwindcss@^3` `lucide-react@latest`

CONSTRAINTS: clearly fictional event and sample pricing; four functional accents; no real organizer claims, autoplay, carousel, infinite motion, or fake map. Only transform/opacity animate; reduced motion; accessible tabs/dialog/forms; Pexels source and credit visible.
