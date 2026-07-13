# Quill Billing & Usage

- **ID:** `quill-billing-usage`
- **Category:** Billing
- **Type:** settings
- **Profile:** `product-ui`

---

Build a single-page billing-and-usage settings page for "Quill" — a writing-collaboration SaaS — where every meter, invoice, and upgrade path feels calm and precise. Use React + Vite + Tailwind CSS + TypeScript + lucide-react + @radix-ui/react-dialog + @radix-ui/react-dropdown-menu. Default Tailwind config, no other UI libraries.

FONTS
- Everything: Inter (Google Fonts, 400/500/600) — `font-family: 'Inter', system-ui, sans-serif` on html/body
- All prices, usage counts, and dates get `tabular-nums`

COLORS (CSS variables on :root; `.dark` on `<html>` overrides)
- Light: --background: #FFFFFF · --wash: #F8FAFC · --border: #E2E8F0 · --foreground: #0F172A · --muted-foreground: #64748B
- Semantic accents (light): --brand: #2563EB · --success: #16A34A · --warning: #D97706 · --danger: #DC2626
- Dark: --background: #0F172A · --wash: #1E293B · --border: #334155 · --foreground: #E2E8F0 · accents: #3B82F6 / #22C55E / #F59E0B / #EF4444
- Usage meter fill: `--brand` under 80% of quota, `--warning` 80–99%, `--danger` at/over 100% (color swap is instant, not transitioned — a meter shouldn't ease into "danger")

GLOBAL CSS (paste verbatim)
```css
@keyframes quill-rise { from { opacity: 0; transform: translateY(6px); } to { opacity: 1; transform: none; } }
.section-enter { animation: quill-rise 0.24s cubic-bezier(0.23, 1, 0.32, 1) backwards; }

.meter-fill { transform: scaleX(0); transform-origin: left; transition: transform 300ms cubic-bezier(0.23, 1, 0.32, 1); }
.meter-fill[data-visible="true"] { transform: scaleX(var(--usage-ratio)); }

.invoice-row { transition: background-color 120ms cubic-bezier(0.23, 1, 0.32, 1); }
@media (hover: hover) and (pointer: fine) { .invoice-row:hover { background: var(--wash); } }

.pressable { transition: transform 140ms cubic-bezier(0.23, 1, 0.32, 1); }
.pressable:active { transform: scale(0.97); }

.menu-pop { transform: scale(0.96); opacity: 0; transform-origin: top right;
            transition: transform 150ms cubic-bezier(0.23, 1, 0.32, 1), opacity 150ms cubic-bezier(0.23, 1, 0.32, 1); }
.menu-pop[data-state="open"] { transform: scale(1); opacity: 1; }

.modal-overlay { opacity: 0; transition: opacity 150ms cubic-bezier(0.23, 1, 0.32, 1); }
.modal-overlay[data-state="open"] { opacity: 1; }
.modal-panel { transform: scale(0.96) translateY(8px); opacity: 0; /* modal keeps the default center origin — it owns the screen */
               transition: transform 180ms cubic-bezier(0.23, 1, 0.32, 1), opacity 180ms cubic-bezier(0.23, 1, 0.32, 1); }
.modal-panel[data-state="open"] { transform: scale(1) translateY(0); opacity: 1; }

@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { animation-duration: 0.01ms !important; animation-iteration-count: 1 !important; transition-duration: 0.01ms !important; }
}
```

PAGE FRAME (max-w-4xl mx-auto px-6 py-10; content z-10, modal z-30)
- Page header: "Billing & usage" text-2xl font-semibold + subtext "Manage your Quill Pro subscription and payment methods." text-sm text-[var(--muted-foreground)]

CURRENT PLAN CARD (`.section-enter`, `rounded-xl border border-[var(--border)] bg-[var(--wash)] p-6 mt-6`)
- "Quill Pro" font-semibold text-lg + "$79/month" text-sm 56% + "Renews Aug 1, 2026" text-xs 56%
- "Upgrade plan" button top-right (`.pressable`, bg `--brand` text-white rounded-md px-4 py-2 text-sm font-medium) → opens the upgrade modal

USAGE METERS (`.section-enter`, animation-delay 40ms via inline style, `rounded-xl border border-[var(--border)] bg-[var(--background)] p-6 mt-4`, grid gap-6)
- Three meters, each: label (text-sm font-medium) + count (`14,208 / 20,000 API calls` tabular-nums text-sm 56%) + track `h-1.5 rounded-full bg-[var(--wash)]` containing `.meter-fill rounded-full`
  1. API calls — 14,208 / 20,000 — 71% — `--brand` fill
  2. Seats — 18 / 25 — 72% — `--brand` fill
  3. Storage — 412 GB / 500 GB — 82% — `--warning` fill (crossed the 80% line)
- Fills use `data-visible="true"` set once via IntersectionObserver when the section scrolls into view — each animates ONCE, never replays on re-render or tab refocus; `--usage-ratio` set inline per meter (`0.71`, `0.72`, `0.82`)

INVOICE HISTORY (`.section-enter`, animation-delay 80ms, `rounded-xl border border-[var(--border)] bg-[var(--background)] mt-4`)
- Header row: "Invoice history" font-medium p-4 border-b
- 5 `.invoice-row` rows (verbatim class — static on mount, no entrance stagger; invoice history is scanned often, not celebrated), each `px-4 py-3 border-b border-[var(--border)] grid grid-cols-[1fr_1fr_100px_100px_40px] items-center gap-4 text-sm`
- Data (invoice / date / amount / status):
  1. INV-2026-0031 · Jul 1, 2026 · $79.00 · Paid
  2. INV-2026-0030 · Jun 1, 2026 · $79.00 · Paid
  3. INV-2026-0029 · May 1, 2026 · $79.00 · Paid
  4. INV-2026-0028 · Apr 1, 2026 · $49.00 · Paid
  5. INV-2026-0027 · Mar 3, 2026 · $49.00 · Failed
- Status chips: Paid = `--success` tint · Failed = `--danger` tint, `rounded-md px-2 py-0.5 text-xs font-medium`
- Row hover = background-color only, 120ms, gated `@media (hover: hover)`; download icon button (`Download`, `.pressable`, `aria-label="Download invoice"`) appears on the far right of every row (always visible, not hover-revealed — hidden-until-hover controls are a frequent source of missed clicks)

PAYMENT METHODS (`.section-enter`, animation-delay 120ms, `rounded-xl border border-[var(--border)] bg-[var(--background)] p-4 mt-4`)
- Header: "Payment methods" font-medium mb-3
- Row 1: "Visa ending in 4242" text-sm + "Expires 08/27" text-xs 56% + "Default" chip (`--brand` tint) + `⋯` menu trigger
- Row 2: "Mastercard ending in 1881" text-sm + "Expires 02/26" text-xs 56% + `⋯` menu trigger
- `⋯` trigger opens `.menu-pop` (verbatim class, `transform-origin: top right`) with items "Set as default" / "Remove" (danger text) — scale 0.96→1 + opacity, 150ms

UPGRADE MODAL (Radix Dialog)
- Overlay: `.modal-overlay` `fixed inset-0 bg-black/40`
- Panel: `.modal-panel` `rounded-xl bg-[var(--background)] p-6 max-w-md shadow-xl`, default centered transform-origin — the modal is the one exception to trigger-origin scaling, it owns the screen
- Content: "Upgrade to Quill Business" text-xl font-semibold + "$199/month" text-sm 56% + feature list (`Check` icon + text, text-sm): "Unlimited API calls" / "100 seats" / "2 TB storage" / "Priority support" + buttons "Cancel" (secondary) / "Upgrade now" (`.pressable`, bg `--brand` text-white) → closes modal, fires the toast

TOAST (fixed bottom-6 right-6, z-30, `role="status"`)
- "Upgraded to Quill Business." — `rounded-lg border bg-[var(--background)] px-4 py-3 text-sm shadow-lg` with `CheckCircle2` in `--success`
- `@starting-style`: from `opacity: 0; transform: translateY(8px)`, 200ms cubic-bezier(0.23, 1, 0.32, 1), auto-dismiss 3.5s

ANIMATIONS (complete list)
- Section entrances: `.section-enter` 0.24s, staggered by section (0 / 40 / 80 / 120ms) — plan card, meters, invoices, payment methods, in that order
- Meter fills: scaleX 0 → ratio, 300ms cubic-bezier(0.23, 1, 0.32, 1), transform-origin left, ONCE per meter on first scroll-into-view
- Menu pop / dropdown: 150ms scale-from-trigger · modal: overlay opacity 150ms, panel scale+translateY+opacity 180ms center-origin · toast 200ms `@starting-style`
- Everything else (invoice rows, status chips, download buttons): static or color-only

RESPONSIVE
- Below sm: invoice/payment rows collapse to stacked layout (label above value); usage meters go full-width single column; modal panel becomes `w-[calc(100%-2rem)]` with `mx-4`

KEY DEPENDENCIES
`react@^18` `react-dom@^18` `typescript@^5` `vite@^5` `tailwindcss@^3` `lucide-react@latest` `@radix-ui/react-dialog@^1` `@radix-ui/react-dropdown-menu@^2`

CONSTRAINTS: product-ui restraint — every interaction ≤ 250ms, entrances 0.15–0.35s; easing only from {cubic-bezier(0.23,1,0.32,1) · cubic-bezier(0.4,0,0.2,1) · cubic-bezier(0.34,1.56,0.64,1)}; never an ease-in start. Animate only transform/opacity — documented paint-only exceptions: background-color on invoice-row hover, opacity on the modal overlay (never width/height/top/left/margin; meters move via `transform: scaleX`, never `width`). Popovers/menus scale from their trigger via explicit `transform-origin`; the upgrade modal is the exception, center-origin is correct there. Press feedback on every pressable. No decorative gradients, no video. Light + dark via `.dark`. Respect `prefers-reduced-motion` (block above). ARIA: `aria-label` on icon-only buttons, `role="status"` on the toast, focus trap + `aria-modal` on the dialog. All numeric values are `tabular-nums`.
