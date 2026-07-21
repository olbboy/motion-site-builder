# Hương Afterglow — Huế Journal

- **ID:** `huong-afterglow-journal`
- **Category:** Place and memory journal
- **Type:** article
- **Profile:** `editorial`

---

Build a single-page journal article for "Hương Afterglow" — a restrained visual meditation on the minutes when Huế's coast, river light, and garden paths share one copper hue. Use React + Vite + Tailwind CSS + TypeScript + `@tailwindcss/typography` + lucide-react. Default Tailwind config, no other UI libraries.

SELECTED PEXELS MEDIA
- Source: [Huế coastal landscape at sunset](https://www.pexels.com/photo/stunning-coastal-view-at-sunset-in-hue-vietnam-35136618/) by Đan.
- Download to `/media/vietnam/pexels-35136618.jpg`; use `<img src="/media/vietnam/pexels-35136618.jpg" alt="Warm sunset light over a green coastal path and water in Huế, Vietnam">`.
- Masthead crop 21:9 `object-cover object-[54%_48%]`; mobile crop 4:5 `object-[64%_50%]` to retain path and horizon.

FONTS
- Display: Cormorant Garamond 500/600 italic; body: Literata 400/600; labels: Inter 500.

COLORS
- `--paper:#F3EFE6` · `--ink:#211D18` · `--muted:#766E65` · single accent `--copper:#9A4D2B`.

GLOBAL CSS
```css
@keyframes afterglow-in { from { opacity:0; transform:translateY(10px); } to { opacity:1; transform:none; } }
.afterglow-in { animation:afterglow-in .65s cubic-bezier(0.16, 1, 0.3, 1) backwards; }
.pressable { transition:transform 140ms cubic-bezier(0.16, 1, 0.3, 1); }
.pressable:active { transform:scale(.98); }
@media (prefers-reduced-motion:reduce) { *,*::before,*::after { animation-duration:.01ms!important; animation-iteration-count:1!important; transition-duration:.01ms!important; } }
```

MASTHEAD
- Quiet header `px-6 py-5`; monogram "HƯƠNG / 07" and links Archive / About / VN.
- H1 above image, centered `text-6xl md:text-[116px] leading-[.92]`: "The color that / stays after sunset."; italicize "stays" without changing color.
- Below: selected image full-bleed 21:9 with caption/source. No text overlay on the photograph.

PROSE SCORE
- Article `max-w-[720px] mx-auto prose prose-xl py-20`; opening drop cap; five short movements marked by exact clock times: 17:31 / 17:38 / 17:46 / 17:53 / 18:02.
- Each movement has one 90–130 word prose block and a narrow margin annotation: Light / Air / Water / Leaves / Memory. Copy is lyrical but explicitly presented as original creative writing, not reportage.
- Insert a full-width typographic interlude after movement 3: `text-4xl md:text-6xl leading-tight` "The horizon does not disappear. It changes tense.".

COLOR NOTATION
- Static five-swatch strip derived from the selected image, all within the copper/neutral family: `#2D3328`, `#6D694C`, `#B26B3D`, `#D6A16A`, `#EEE1CC`; label each with time, hex, and one noun. Treat them as visual sampling, not scientific colorimetry.

LISTENING FOOTNOTE
- Accessible disclosure titled "A note on listening"; native `<details>` preferred, no animated height. Contents explain the page has no autoplay audio and why silence is part of the design.

ENDNOTE
- `border-t border-black/15 py-20 max-w-5xl`; H2 "Return before the color does."; previous/next journal links; photo credit with Pexels page and photographer.

ANIMATIONS
- Masthead .65s/80ms stagger; movement blocks .55s once; no image motion, parallax, sticky scroll, autoplay audio, count-up, or looping effect.

RESPONSIVE
- Masthead H1 text-6xl; image 4:5 with specified focal point; margin notes become inline uppercase labels; swatches become 5 stacked rows. Reading measure stays 38–72 characters.

KEY DEPENDENCIES
`react@^18` `react-dom@^18` `typescript@^5` `vite@^5` `tailwindcss@^3` `@tailwindcss/typography@^0.5` `lucide-react@latest`

CONSTRAINTS: one copper accent and neutral derivatives; no video, glass, gradients, blobs, carousel, autoplay sound, or faux quotations. Semantic article and figure markup; links have visible focus; only transform/opacity animate; preserve Pexels credit and reduced-motion handling. Never apply `overflow-x: hidden` to `html`/`body` or a root wrapper — it creates a scroll container and silently breaks `position: sticky`; contain any horizontal bleed with `overflow-x: clip` on the overflowing section instead.
