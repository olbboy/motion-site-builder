# PawPal Adoption Day

- **ID:** `pawpal-adoption-day`
- **Category:** Event / Campaign
- **Type:** campaign
- **Profile:** `playful`

---

Build a single-page campaign microsite for "PawPal Adoption Day" — a city shelter's one-Saturday adoption drive. Forty dogs, zero fees, one park. Warm playful color, bouncy springs, confetti energy. Use React + Vite + Tailwind CSS + TypeScript + lucide-react. Default Tailwind config, no other UI libraries.

FONTS (Google Fonts, load via `<link>` in index.html)
- Display: Paytone One (400) — headlines, date/venue, step numbers
- Body: Inter (400/500/600/700) — everything else, especially the RSVP form

COLORS (CSS variables on :root — warm-shelter family, distinct from candy/neon palettes; decorative color IS the identity here)
- --cream: #FFFBF2 (background) · --ink: #20242B (foreground)
- Accents (all four earn their keep): --sunbeam: #FFB454 (primary CTA, step numbers) · --clover: #2DD4A7 (temperament tags, success) · --blueberry: #5B8DEF (links, form focus) · --blush: #FF6F91 (highlights, sponsor strip)
- Hard-shadow trick: solid offset shadows in ink (`shadow-[0_6px_0_#20242B]`), never soft blurs — shadows stay neutral so the four accents stay exactly four

GLOBAL CSS (paste verbatim)
```css
@keyframes pop-in { from { opacity: 0; transform: scale(0.9) translateY(12px); } to { opacity: 1; transform: none; } }
.pop { animation: pop-in 0.5s cubic-bezier(0.18, 0.89, 0.32, 1.28) backwards;   /* back-out overshoot */
       transition: transform 160ms cubic-bezier(0.34, 1.56, 0.64, 1); }
.pop:active { transform: scale(0.94); }
@media (hover: hover) { .pop:hover { transform: scale(1.06) rotate(-1.5deg); } }

@keyframes float-y { 0%,100% { transform: translateY(0) rotate(-4deg); } 50% { transform: translateY(-6px) rotate(-4deg); } }
.sticker { animation: float-y 3s cubic-bezier(0.65, 0, 0.35, 1) infinite;
           transition: transform 200ms cubic-bezier(0.34, 1.56, 0.64, 1); }
@media (hover: hover) { .sticker:hover { transform: scale(1.08) rotate(3deg); } }

@media (prefers-reduced-motion: reduce) {
  .sticker { animation: none; }
  *, *::before, *::after { animation-duration: 0.01ms !important; animation-iteration-count: 1 !important; transition-duration: 0.01ms !important; }
}
```

CONFETTI-DOT DECOR (z-[5], `aria-hidden="true"`, pointer-events-none — static wallpaper, hero only)
- 14 small circles scattered across the hero (`absolute rounded-full`, sizes w-3 h-3 to w-6 h-6), colors cycling `--sunbeam` / `--clover` / `--blueberry` / `--blush` at opacity-40, fixed inline `top`/`left` percentages and fixed `rotate(…deg)` per dot — a hand-placed confetti pattern, never generated at runtime, never animated
- Two soft glows: `w-96 h-96 rounded-full bg-[var(--sunbeam)]/15 blur-3xl` top-right, `w-72 h-72 rounded-full bg-[var(--blueberry)]/15 blur-3xl` bottom-left

NAVBAR (z-20, max-w-6xl mx-auto px-6 py-5, flex justify-between)
- Left: "PawPal" — Paytone One text-2xl, with a small lucide `PawPrint` icon (w-6 h-6, `--blush`) before the wordmark
- Links (hidden md:flex, Inter 600 text-sm): The Dogs · How it Works · RSVP — hover = marker underline: `scaleX` pseudo-element h-1 bg-[var(--sunbeam)] rounded-full, `transform-origin: left`, 0→1 in 200ms cubic-bezier(0.23, 1, 0.32, 1), gated `@media (hover: hover) and (pointer: fine)`
- Right: "RSVP" `rounded-full bg-[var(--ink)] text-[var(--cream)] px-5 py-2 text-sm font-bold`, hover scale 1.06 (spring 160ms), `active:scale-[0.94]`

HERO (z-10, max-w-5xl mx-auto px-6 pt-16 pb-24, text-center)
- Staggered `.pop` entrance via `animation-delay`: sticker 0ms → H1 90ms → date row 180ms → CTA row 270ms
- Sticker (paste verbatim): `<span className="sticker inline-block rounded-2xl bg-[var(--blush)] px-3 py-1 text-sm font-black text-white">RAIN OR SHINE</span>`
- H1 — Paytone One, text-5xl md:text-7xl leading-[0.95]: "40 dogs." on line 1, "0 adoption fees." on line 2 with "0" wrapped in a `rounded-2xl bg-[var(--sunbeam)] text-[var(--ink)] px-3 inline-block -rotate-1`
- Sub (Inter text-lg, ink 85%, max-w-xl mx-auto mt-6): "One Saturday. Meet, play, and go home with your new best friend — vet-checked, chipped, and already asking for a walk."
- Date/venue row (mt-4, Inter 700 text-base text-[var(--blueberry)]): "Sat, Aug 22 · 10am–4pm · Riverside Commons Park"
- CTA row (mt-8, flex justify-center gap-4): `<button className="pop rounded-full bg-[var(--sunbeam)] px-8 py-4 text-lg font-bold text-[var(--ink)] shadow-[0_6px_0_#20242B]">RSVP — I'm coming</button>` + secondary text link "See the dogs" (ink, marker underline on hover)

ADOPTABLE PETS GRID (max-w-6xl mx-auto px-6 py-24)
- H2 `.pop` when in view: "Meet a few of the Saturday crew" — Paytone One text-4xl md:text-5xl, "Saturday" in `--blueberry`
- 6 cards, grid sm:grid-cols-2 lg:grid-cols-3 gap-6, entering `.pop` via IntersectionObserver once, stagger 90ms (`animation-delay: 0/90/…/450ms`), each `rounded-2xl bg-white border-4 border-[var(--ink)] overflow-hidden`:
  1. Biscuit, age 2 — Goofy · Cuddly · Leash-trained
  2. Nutmeg, age 5 — Calm · Great with kids · Nap champion
  3. Ranger, age 1 — Energetic · Ball-obsessed · Loud snorer
  4. Pepper, age 7 — Gentle · Senior · Prefers naps to hikes
  5. Waffles, age 3 — Mischievous · Escape artist · Big personality
  6. Clementine, age 4 — Shy at first · Loyal · Good with cats
- Each: photo `<img src="{YOUR_IMAGE_URL_N}" alt="{Name}, a {age}-year-old dog available for adoption">` aspect-[4/3] object-cover, name+age row Paytone One text-xl px-5 pt-4 ("Biscuit · 2 yrs"), 3 temperament pills (px-5 pb-5 flex gap-2 flex-wrap, `rounded-full bg-[var(--clover)]/25 text-[var(--ink)] px-2.5 py-1 text-xs font-bold`)
- Card hover (gated `@media (hover: hover) and (pointer: fine)`): `scale(1.04) rotate(1deg)` spring 200ms cubic-bezier(0.34, 1.56, 0.64, 1); press `active:scale-[0.96]`; alternate cards pre-rotated ±1deg

HOW IT WORKS (bg-[var(--ink)] text-[var(--cream)] py-24, rounded-t-[3rem])
- H2: "Three steps to a new best friend" — Paytone One text-4xl, "friend" in `--sunbeam`
- 3 steps, grid md:grid-cols-3 gap-8, `.pop` in view stagger 90ms, each text-center:
  1. Step number "1" (Paytone One text-6xl `--sunbeam`) · "RSVP" · "Takes 20 seconds, no account needed."
  2. Step number "2" (`--clover`) · "Meet your match" · "Real time in our playpens, not a rushed 5-minute intro."
  3. Step number "3" (`--blush`) · "Walk out with a leash" · "Not a waitlist — approved adopters go home same day."

RSVP FORM (max-w-2xl mx-auto px-6 py-24)
- H2 `.pop` in view: "Reserve your spot" — Paytone One text-3xl md:text-4xl
- Form row (grid sm:grid-cols-2 gap-4, mt-8): "Name" input, "Email" input (`rounded-xl border-2 border-[var(--ink)]/15 px-4 py-3 text-sm`, focus ring `--blueberry` 2px, transition border-color/box-shadow 150ms cubic-bezier(0.23, 1, 0.32, 1))
- Below (mt-4): "How many dogs are you willing to fall in love with?" — select with options "Just one" / "Two, tops" / "Ask my landlord" (same input styling)
- Submit (mt-6, full width): `<button className="pop rounded-full bg-[var(--sunbeam)] px-8 py-4 text-lg font-bold text-[var(--ink)] shadow-[0_6px_0_#20242B]" aria-label="Reserve my spot at PawPal Adoption Day">Reserve my spot</button>`
- Reassurance line (text-xs ink 55% mt-3 text-center): "We'll never sell your info. We will absolutely send you dog photos."

SPONSOR STRIP (max-w-6xl mx-auto px-6 pb-24)
- Label: "Made possible by" — Inter 700 text-sm ink 55% uppercase tracking-[0.1em] text-center
- 4 sponsor wordmarks (mt-6, flex flex-wrap justify-center gap-x-10 gap-y-4, Inter 700 text-lg ink 60%, grayscale-ish via ink/60 color only — no logos, text only): "Riverside Vet Clinic" · "Pawsome Pet Supply" · "Elm Street Coffee" · "Commons Realty Group"

FOOTER (py-10, max-w-6xl mx-auto px-6, flex justify-between, Inter text-sm ink 85%)
- "© City of Riverside Animal Shelter" + links Volunteer / Donate / Directions (`aria-label` on icon links); sticker "★ good dogs only" rotated −3deg

ANIMATIONS (complete list)
- Entrances: `.pop` 0.5s back-out cubic-bezier(0.18, 0.89, 0.32, 1.28), stagger 90ms, once per element (load for hero, IntersectionObserver for below-fold)
- Idle: `.sticker` float-y 3s loop (reduced-motion: none)
- Hover: spring scale ≤1.06 + rotate ≤3deg, 160–200ms cubic-bezier(0.34, 1.56, 0.64, 1), always gated behind `@media (hover: hover)`
- Press: `active:scale-[0.94]` on buttons, `active:scale-[0.96]` on pet cards, `active:scale-[0.98]` on text links
- Form fields: border-color/box-shadow 150ms cubic-bezier(0.23, 1, 0.32, 1) on focus (paint-only, not layout)
- Confetti-dot decor: no animation, ever (static wallpaper)

RESPONSIVE
- Mobile: hero text-5xl, pets grid 1→2→3, how-it-works stacks, RSVP form fields stack to 1 column, sponsor strip wraps; confetti dots repositioned to stay within `overflow-hidden` hero bounds; no horizontal scroll

KEY DEPENDENCIES
`react@^18` `react-dom@^18` `typescript@^5` `vite@^5` `tailwindcss@^3` `lucide-react@latest`

CONSTRAINTS: playful maximalism, engineered — all four accents and the confetti-dot decor are intentional (this profile inverts the cinematic no-decor rule), but motion still only animates transform/opacity (border-color/box-shadow paint swaps ≤150ms on form focus are the documented exception), easing only from {cubic-bezier(0.34,1.56,0.64,1) · cubic-bezier(0.18,0.89,0.32,1.28) · cubic-bezier(0.23,1,0.32,1) · cubic-bezier(0.65,0,0.35,1)}, never ease-in, no `transition: all`, and every entrance starts at scale 0.9 or above — nothing pops in from zero. Bounce is for deliberate moments (entrances, CTA, stickers) — nav links and step numbers don't wobble. Respect `prefers-reduced-motion` (stickers stop dead). Replace `{YOUR_IMAGE_URL_*}` with pet photography you have rights to, with real descriptive `alt` text. "PawPal" and all pets/sponsors are fictional. ARIA labels on icon-only links and the RSVP submit button; confetti decor is `aria-hidden`; form inputs have associated `<label>` elements.
