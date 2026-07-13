# Harvest Hands — River Essay

- **ID:** `harvest-hands-river-essay`
- **Category:** Collaborative agriculture essay
- **Type:** longread
- **Profile:** `editorial`

---

Build a single-page editorial essay for "Harvest Hands" — a visual account of coordination at the exact edge where rice field, riverbank, and boats meet. Use React + Vite + Tailwind CSS + TypeScript + `@tailwindcss/typography` + lucide-react. Default Tailwind config, no other UI libraries.

SELECTED PEXELS MEDIA
- Source: [Rice harvest beside a river](https://www.pexels.com/photo/rural-farmers-harvesting-rice-by-river-30228485/) by Vũ Bụi.
- Download to `/media/vietnam/pexels-30228485.jpg`; use `<img src="/media/vietnam/pexels-30228485.jpg" alt="Farmers in conical hats gathering rice beside a green river lined with wooden boats">`.
- Lead crop 16:9 `object-cover object-[50%_52%]`; keep workers, crop rows, and at least three boats inside the frame.

FONTS
- Display: Source Serif 4 600; body: Newsreader 400/600; annotation: IBM Plex Sans 400/500.

COLORS
- `--paper:#F8F6EF` · `--ink:#191C18` · `--muted:#6C7169` · single accent `--leaf:#416A45`.

GLOBAL CSS
```css
@keyframes essay-in { from { opacity:0; transform:translateY(16px); } to { opacity:1; transform:none; } }
.essay-in { animation:essay-in .6s cubic-bezier(0.22, 1, 0.36, 1) backwards; }
.pressable { transition:transform 140ms cubic-bezier(0.16, 1, 0.3, 1); }
.pressable:active { transform:scale(.98); }
@media (prefers-reduced-motion:reduce) { *,*::before,*::after { animation-duration:.01ms!important; animation-iteration-count:1!important; transition-duration:.01ms!important; } }
```

LEAD PACKAGE
- Top utility line: "FIELD WORK / PHOTO ESSAY / 06 MIN" and an icon-only share button with `aria-label="Copy article link"`.
- `max-w-6xl py-16`; H1 `max-w-4xl text-6xl md:text-[96px] leading-[1]` "A harvest is a choreography."; dek "One frame holds at least five systems: hands, tools, water, boats, and the timing that keeps them together.".
- Selected image `aspect-[16/9]` in semantic figure; caption states what is visible and links source/photographer without guessing location or identities.

ANNOTATED FRAME
- Reuse the same image in a wide `relative` figure with five accessible numbered buttons placed at normalized percentages. Button labels: Field edge / Work group / Rice bundles / Boat line / River channel.
- Activating a button updates a caption panel below, not a floating tooltip: 180ms opacity crossfade, `aria-live=polite`; annotations describe visible composition only. The image itself never zooms or pans.

ESSAY
- `max-w-[760px] prose-xl`; three sections: "Many hands, one threshold" / "The river as working space" / "What the frame cannot tell us".
- Each 220–300 words. The third section explicitly distinguishes observation from inference and avoids romanticizing or identifying subjects.
- Pull quote is authored essay copy: "Coordination is the infrastructure we rarely photograph.".

COMPOSITION LEDGER
- Static table with columns Layer / Visible evidence / Unknown: People / clustered work / names and relationships; Crop / bundled rice / yield and ownership; Water / boats at bank / route and destination. Use `<table>` with caption and responsive scroll only inside the table wrapper.

ENDNOTE
- Dark green `bg-[#1F2E22] text-[#F8F6EF]` block: H2 "Look closely. Claim carefully."; link to Sources and next essay. Repeat source and credit.

ANIMATIONS
- Lead and sections .6s/80ms stagger; annotation caption opacity 180ms; no hover zoom, parallax, auto-advance, animated path, or count-up.

RESPONSIVE
- H1 text-6xl; lead and annotated frames 4:3; annotation buttons 44×44; table wrapper gets local horizontal scroll; prose stays 38–72 characters per line.

KEY DEPENDENCIES
`react@^18` `react-dom@^18` `typescript@^5` `vite@^5` `tailwindcss@^3` `@tailwindcss/typography@^0.5` `lucide-react@latest`

CONSTRAINTS: one leaf-green accent, evidence-aware copy, no invented names, quotes, yields, or locations. No video, glass, gradients, carousel, or decorative motion. Semantic article/figure/table markup; keyboard-accessible annotations; only transform/opacity animate; preserve Pexels source and reduced motion.
