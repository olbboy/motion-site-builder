# Component Catalog — Verbatim Primitives

Copy these EXACTLY — do not paraphrase values. Section headers (`## N. name`) are machine-extracted by `motion_get_template`, keep them stable.

## 1. liquid-glass

The signature glass primitive (plain CSS in `index.css`):

```css
.liquid-glass {
  background: rgba(255, 255, 255, 0.01);
  background-blend-mode: luminosity;
  backdrop-filter: blur(4px);
  -webkit-backdrop-filter: blur(4px);
  border: none;
  box-shadow: inset 0 1px 1px rgba(255, 255, 255, 0.1);
  position: relative;
  overflow: hidden;
}
.liquid-glass::before {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: inherit;
  padding: 1.4px;
  background: linear-gradient(180deg,
    rgba(255,255,255,0.45) 0%, rgba(255,255,255,0.15) 20%,
    rgba(255,255,255,0) 40%, rgba(255,255,255,0) 60%,
    rgba(255,255,255,0.15) 80%, rgba(255,255,255,0.45) 100%);
  -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  -webkit-mask-composite: xor;
  mask-composite: exclude;
  pointer-events: none;
}
```

## 2. text-glow

```css
.text-glow {
  text-shadow: 0 0 40px rgba(255, 255, 255, 0.4),
               0 0 80px rgba(255, 255, 255, 0.2),
               0 0 120px rgba(255, 255, 255, 0.1);
}
.button-glow {
  box-shadow: 0 0 20px rgba(255, 255, 255, 0.3),
              0 0 40px rgba(255, 255, 255, 0.1);
}
```

## 3. entrance-keyframes

CSS-only staggered entrance (no Framer needed):

```css
@keyframes fade-up {
  from { opacity: 0; transform: translateY(24px); filter: blur(6px); }
  to   { opacity: 1; transform: translateY(0);   filter: blur(0); }
}
.animate-fade-up {
  animation: fade-up 0.8s cubic-bezier(0.16, 1, 0.3, 1) backwards;
}
.delay-1 { animation-delay: 0.1s; }
.delay-2 { animation-delay: 0.25s; }
.delay-3 { animation-delay: 0.4s; }
```

Usage order: headline (no delay) → subtext `.delay-2` → CTA `.delay-3`. Framer variant: `initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.6, delay: 0.1 * i, ease: [0.16, 1, 0.3, 1] }}`.

## 4. video-background

```tsx
<div className="absolute inset-0 z-0" aria-hidden="true">
  <video
    autoPlay muted loop playsInline
    poster="/poster.jpg"
    className="w-full h-full object-cover"
    src={VIDEO_URL}
  />
  {/* optional contrast overlay */}
  <div className="absolute inset-0 bg-black/30 z-[1]" />
</div>
```

Supply your own licensed/AI-generated `VIDEO_URL` — corpus CDN links expire.

## 5. video-crossfade-loop

Seamless loop via JS (never CSS transition on `<video>`):

```tsx
// On timeupdate: when remaining time <= 0.55s, fade opacity to 0 over 500ms (rAF).
// On ended: opacity 0 → wait 100ms → currentTime = 0 → play() → fade back to 1 over 500ms.
// Guard with a ref so the fade never re-triggers mid-flight.
const fadingOutRef = useRef(false);
useEffect(() => {
  const v = videoRef.current;
  if (!v) return;
  const fade = (from: number, to: number, ms: number) => {
    const start = performance.now();
    const step = (t: number) => {
      const p = Math.min((t - start) / ms, 1);
      v.style.opacity = String(from + (to - from) * p);
      if (p < 1) requestAnimationFrame(step);
    };
    requestAnimationFrame(step);
  };
  const onTime = () => {
    if (v.duration - v.currentTime <= 0.55 && !fadingOutRef.current) {
      fadingOutRef.current = true;
      fade(1, 0, 500);
    }
  };
  const onEnded = () => setTimeout(() => {
    v.currentTime = 0; v.play(); fade(0, 1, 500); fadingOutRef.current = false;
  }, 100);
  v.addEventListener('timeupdate', onTime);
  v.addEventListener('ended', onEnded);
  return () => { v.removeEventListener('timeupdate', onTime); v.removeEventListener('ended', onEnded); };
}, []);
```

Note: drop `loop` attribute when using manual crossfade (they conflict); keep `autoPlay muted playsInline poster`.

## 6. glass-nav-pill

```tsx
<nav className="relative z-20 px-6 py-6" aria-label="Main">
  <div className="liquid-glass rounded-full max-w-5xl mx-auto px-6 py-3 flex items-center justify-between">
    <div className="flex items-center">
      <span className="text-white font-semibold text-lg">{BRAND}</span>
      <div className="hidden md:flex items-center gap-8 ml-8">
        {links.map(l => (
          <a key={l} href="#" className="text-white/80 hover:text-white text-sm font-medium transition-colors">{l}</a>
        ))}
      </div>
    </div>
    <button className="liquid-glass rounded-full px-6 py-2 text-white text-sm font-medium hover:bg-white/5 transition-colors">
      {CTA}
    </button>
  </div>
</nav>
```

## 7. hero-block

```tsx
<main className="relative z-10 flex-1 flex flex-col items-center justify-center px-6 py-12 text-center -translate-y-[10%]">
  <h1
    className="animate-fade-up text-glow text-5xl md:text-8xl text-white tracking-tight leading-[0.95]"
    style={{ fontFamily: "'Instrument Serif', serif" }}
  >
    {HEADLINE_PART} <em className="italic">{EMPHASIS}</em>
  </h1>
  <p className="animate-fade-up delay-2 text-white/70 max-w-xl mt-6 leading-relaxed">{SUBTEXT}</p>
  <button className="animate-fade-up delay-3 mt-8 bg-white text-black rounded-full px-8 py-3.5 text-base font-medium transition-transform hover:scale-[1.03]">
    {CTA_LABEL}
  </button>
</main>
```

## 8. raf-lerp-parallax

Hand-rolled smooth parallax (alternative to Framer):

```ts
// useLerpScroll — smooth follower of window.scrollY
export function useLerpScroll(factor = 0.1) {
  const ref = useRef<HTMLElement>(null);
  useEffect(() => {
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
    let target = 0, current = 0, raf = 0;
    const onScroll = () => { target = window.scrollY; };
    const tick = () => {
      current += (target - current) * factor;
      if (ref.current) ref.current.style.transform = `translate3d(0, ${current * -0.15}px, 0)`;
      raf = requestAnimationFrame(tick);
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    raf = requestAnimationFrame(tick);
    return () => { window.removeEventListener('scroll', onScroll); cancelAnimationFrame(raf); };
  }, [factor]);
  return ref;
}
```

Apply `will-change: transform` on the target element only.

## 9. sticky-stack-cards

```tsx
// Each card i of n, inside a sticky container:
const targetScale = 1 - (n - 1 - i) * 0.03;
// Framer: useScroll({ target: containerRef, offset: ['start start', 'end end'] })
// scale: useTransform(scrollYProgress, [i / n, 1], [1, targetScale])
// Card: position sticky, top offset increases slightly per index (top: `calc(8vh + ${i * 24}px)`)
```

## 10. scroll-char-reveal

```tsx
// Split text into chars; map scroll progress to per-char opacity 0.2 → 1
{chars.map((c, i) => {
  const start = i / chars.length, end = start + 1 / chars.length;
  const opacity = useTransform(scrollYProgress, [start, end], [0.2, 1]);
  return <motion.span key={i} style={{ opacity }}>{c}</motion.span>;
})}
```

## 11. reduced-motion-boilerplate

Mandatory in every project (`index.css`):

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

React: gate rAF loops and parallax behind `useReducedMotion()` (Framer) or `matchMedia('(prefers-reduced-motion: reduce)')`.

## 12. iphone-frame

App Showcase archetype (plain HTML/CSS):

```css
.stage { display: flex; gap: 48px; justify-content: center; align-items: center;
         transform-origin: center; /* JS: scale = min(1, innerWidth / stageNaturalWidth) */ }
.iphone {
  width: 370px; height: 790px; border-radius: 56px;
  background: #000; border: 4px solid #1a1a1a;
  box-shadow: 0 24px 80px rgba(0,0,0,0.5);
  position: relative; overflow: hidden;
}
.iphone .dynamic-island {
  position: absolute; top: 12px; left: 50%; transform: translateX(-50%);
  width: 120px; height: 34px; border-radius: 20px; background: #000; z-index: 50;
}
.iphone .statusbar { position: absolute; top: 0; left: 0; right: 0; height: 54px;
  display: flex; justify-content: space-between; align-items: center; padding: 18px 28px 0; z-index: 40; }
```

Gate entrance animations behind: `loadeddata` (videos) + `document.fonts.ready` + 5s safety timeout → then add a `.ready` class to `<body>`.

## 13. press-scale-button

Press feedback on any pressable element — button, styled-link CTA, `role="button"`. Confirms the tap so the UI feels alive (see interaction-standards §4).

```tsx
{/* Tailwind — transition-transform already covers the scale */}
<a className="rounded-full bg-white px-8 py-3.5 text-black transition-transform
              hover:scale-[1.03] active:scale-[0.97]">
  Get Started
</a>
```

```css
/* Plain CSS equivalent */
.button        { transition: transform 160ms cubic-bezier(0.16, 1, 0.3, 1); }
.button:active { transform: scale(0.97); }   /* subtle: 0.95–0.98 */
```

Framer Motion: `whileTap={{ scale: 0.97 }}`. Never `scale(0)`; keep it subtle.

## 14. origin-aware-popover

Popovers / dropdowns / tooltips scale from their **trigger**, not their center. Modals are exempt (they stay centered).

```css
/* Radix UI exposes the trigger origin as a CSS variable */
.popover {
  transform-origin: var(--radix-popover-content-transform-origin);
  transition: transform 175ms cubic-bezier(0.16, 1, 0.3, 1),
              opacity 175ms cubic-bezier(0.16, 1, 0.3, 1);
}
.popover[data-state="closed"] { opacity: 0; transform: scale(0.96); }

/* Base UI: transform-origin: var(--transform-origin); */
```

Tooltips: after the first opens, subsequent ones on the same toolbar should skip the delay + animation (`transition-duration: 0ms`) so the toolbar feels instant.

## 15. interruptible-toast

Rapidly-added UI (toasts, toggles) must be **interruptible** — CSS transitions retarget mid-flight; `@keyframes` restart from zero. Enter without JS via `@starting-style`.

```css
.toast {
  opacity: 1;
  transform: translateY(0);   /* translateY(100%) = the toast's own height, any size */
  transition: opacity 300ms cubic-bezier(0.16, 1, 0.3, 1),
              transform 300ms cubic-bezier(0.16, 1, 0.3, 1);
  @starting-style { opacity: 0; transform: translateY(100%); }
}
```

Legacy fallback: `useEffect(() => setMounted(true), [])` + `data-mounted` attribute. Gesture-driven toasts should use a spring (keeps velocity when the user reverses a swipe).

## 16. hold-to-confirm

Asymmetric timing via `clip-path`: the press fills slowly and deliberately; the release snaps back. Pairs with press-scale.

```css
.confirm          { position: relative; transition: transform 160ms cubic-bezier(0.16,1,0.3,1); }
.confirm:active   { transform: scale(0.97); }
.confirm .fill    { position: absolute; inset: 0; background: var(--accent);
                    clip-path: inset(0 100% 0 0);
                    transition: clip-path 200ms ease-out; }        /* release: fast */
.confirm:active .fill { clip-path: inset(0 0 0 0);
                    transition: clip-path 2s linear; }             /* press: slow, deliberate */
```

On completion (JS `transitionend` while still held) fire the destructive action; otherwise the release snaps the fill back.

---

## Profile primitives

The primitives above are **cinematic**. Below are signature primitives for the other profiles — each uses that profile's tokens (fast ease-out, neutral tracking, its palette). Fetch by name with `motion_get_template`. See `design-profiles.md`.

## 17. product-ui-stat-card

Fast, crisp dashboard metric card (profile: **product-ui**). Fast entrance, press feedback, hover lift gated for touch.

```tsx
{/* index.css */}
@keyframes ui-rise { from { opacity: 0; transform: translateY(6px); } to { opacity: 1; transform: none; } }
.stat { animation: ui-rise 0.22s cubic-bezier(0.23, 1, 0.32, 1) backwards;
        transition: transform 140ms cubic-bezier(0.23, 1, 0.32, 1), box-shadow 140ms cubic-bezier(0.23, 1, 0.32, 1); }
.stat:active { transform: scale(0.98); }
@media (hover: hover) and (pointer: fine) { .stat:hover { transform: translateY(-2px); box-shadow: 0 8px 24px rgb(15 23 42 / 0.08); } }

<button className="stat rounded-xl border border-slate-200 bg-white p-5 text-left" aria-label="Revenue">
  <span className="text-sm text-slate-500">Revenue</span>
  <div className="mt-1 flex items-baseline gap-2">
    <span className="text-2xl font-semibold tabular-nums text-slate-900">$48.2k</span>
    <span className="text-xs font-medium text-emerald-600">+12%</span>   {/* semantic accent */}
  </div>
</button>
```

## 18. product-ui-data-row

Table/list rows that stagger in on mount, ~40ms apart, and press on click (profile: **product-ui**).

```tsx
@keyframes ui-rise { from { opacity: 0; transform: translateY(4px); } to { opacity: 1; transform: none; } }
.row { animation: ui-rise 0.2s cubic-bezier(0.23, 1, 0.32, 1) backwards;
       transition: background-color 120ms cubic-bezier(0.23, 1, 0.32, 1); }
.row:nth-child(1){animation-delay:0ms} .row:nth-child(2){animation-delay:40ms} .row:nth-child(3){animation-delay:80ms}
@media (hover: hover) { .row:hover { background: #F8FAFC; } }

{rows.map((r, i) => (
  <tr key={r.id} className="row border-b border-slate-100">
    <td className="px-4 py-3 text-sm text-slate-900">{r.name}</td>
    <td className="px-4 py-3 text-sm tabular-nums text-slate-600">{r.value}</td>
  </tr>
))}
```

## 19. editorial-prose

Reading column — the star of the editorial profile. Motion stays out of the way; content just reads.

```tsx
{/* uses @tailwindcss/typography */}
<article className="prose prose-neutral mx-auto max-w-[65ch] prose-headings:font-serif
                    prose-headings:tracking-tight prose-p:leading-relaxed">
  <h1>The quiet craft of reading</h1>
  <p>Long-form body set in a serif at a comfortable measure…</p>
</article>
```

```css
/* sections fade + rise once as they enter — gentle, reading-paced */
@keyframes ed-reveal { from { opacity: 0; transform: translateY(12px); } to { opacity: 1; transform: none; } }
.reveal { animation: ed-reveal 0.6s cubic-bezier(0.22, 1, 0.36, 1) backwards; }
@media (prefers-reduced-motion: reduce) { .reveal { animation: none; } }
```

## 20. editorial-sticky-toc

Sticky table-of-contents that highlights the active heading (profile: **editorial**).

```tsx
// IntersectionObserver sets data-active on the current section's TOC link.
<nav className="sticky top-24 hidden lg:block" aria-label="On this page">
  {headings.map(h => (
    <a key={h.id} href={`#${h.id}`}
       className="block border-l-2 border-transparent py-1 pl-3 text-sm text-neutral-500
                  transition-colors duration-150 data-[active=true]:border-neutral-900
                  data-[active=true]:text-neutral-900">
      {h.title}
    </a>
  ))}
</nav>
```

Smooth-scroll on click; never scroll-jack. Progress bar variant: a fixed top bar with `transform: scaleX(var(--p))` bound to scroll (GPU-only).

## 21. playful-pop-cta

Bouncy pop-in CTA (profile: **playful**) — overshoot is on-brand here.

```tsx
@keyframes pop-in { from { opacity: 0; transform: scale(0.9) translateY(12px); } to { opacity: 1; transform: none; } }
.pop { animation: pop-in 0.5s cubic-bezier(0.18, 0.89, 0.32, 1.28) backwards;   /* back-out overshoot */
       transition: transform 160ms cubic-bezier(0.34, 1.56, 0.64, 1); }
.pop:active { transform: scale(0.94); }
@media (hover: hover) { .pop:hover { transform: scale(1.06) rotate(-1.5deg); } }

<button className="pop rounded-full bg-[#FF5C8A] px-8 py-4 text-lg font-bold text-white shadow-[0_6px_0_#B5179E]">
  Let's go →
</button>
```

## 22. playful-sticker-badge

Wobbly sticker/badge with idle float (profile: **playful**).

```css
@keyframes float-y { 0%,100% { transform: translateY(0) rotate(-6deg); } 50% { transform: translateY(-6px) rotate(-6deg); } }
.sticker { animation: float-y 3s ease-in-out infinite; transition: transform 200ms cubic-bezier(0.34,1.56,0.64,1); }
@media (hover: hover) { .sticker:hover { transform: scale(1.08) rotate(3deg); } }
@media (prefers-reduced-motion: reduce) { .sticker { animation: none; } }
```

```tsx
<span className="sticker inline-block rounded-2xl bg-[#FACC15] px-3 py-1 text-sm font-black text-[#1A1A2E]">NEW</span>
```

## 23. ecommerce-product-card

Product card that reveals into the grid, crossfades to the alt shot on hover, and lifts (profile: **ecommerce**).

```tsx
@keyframes card-rise { from { opacity: 0; transform: translateY(12px); } to { opacity: 1; transform: none; } }
.card { animation: card-rise 0.35s cubic-bezier(0.23, 1, 0.32, 1) backwards;
        transition: transform 200ms cubic-bezier(0.23, 1, 0.32, 1); }
.card .alt { opacity: 0; transition: opacity 200ms cubic-bezier(0.23, 1, 0.32, 1); }
@media (hover: hover) and (pointer: fine) {
  .card:hover { transform: translateY(-4px); }
  .card:hover .alt { opacity: 1; }
}

<a className="card block" href={p.href} aria-label={p.name}>
  <div className="relative aspect-square overflow-hidden rounded-xl bg-zinc-100">
    <img src={p.img} className="h-full w-full object-cover" alt="" />
    <img src={p.altImg} className="alt absolute inset-0 h-full w-full object-cover" alt="" />
  </div>
  <div className="mt-3 flex justify-between text-sm">
    <span className="text-zinc-900">{p.name}</span>
    <span className="tabular-nums font-medium text-zinc-900">{p.price}</span>
  </div>
</a>
```

## 24. ecommerce-add-to-cart

Add-to-cart button with crisp press feedback and a badge-count bump (profile: **ecommerce**).

```tsx
@keyframes bump { 0% { transform: scale(1); } 40% { transform: scale(1.35); } 100% { transform: scale(1); } }
.cart-badge[data-bumped="true"] { animation: bump 0.3s cubic-bezier(0.34, 1.56, 0.64, 1); }
.add { transition: transform 140ms cubic-bezier(0.23, 1, 0.32, 1), background-color 140ms cubic-bezier(0.23, 1, 0.32, 1); }
.add:active { transform: scale(0.97); }

<button className="add rounded-lg bg-zinc-900 px-6 py-3 font-medium text-white hover:bg-zinc-800"
        onClick={bumpBadge} aria-label="Add to cart">
  Add to cart
</button>
```

On click, toggle `data-bumped` on the cart badge for one animation cycle (reset on `animationend`).
