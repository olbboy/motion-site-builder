# Landing Page (`site/`)

The repo's own marketing page — dogfooded from [prompts/motion-site-builder-landing.md](../prompts/motion-site-builder-landing.md) via the skill's code mode. Every source file scores 100/A+ on the bundled motion linter.

One deliberate adaptation from the prompt: the `{YOUR_VIDEO_URL}` background is implemented as a procedural canvas aurora ([src/components/aurora-background.tsx](src/components/aurora-background.tsx)) — owned media, zero licensing risk, works offline, honors `prefers-reduced-motion`.

```bash
npm install
npm run dev      # http://localhost:5173
npm run build    # typecheck + production bundle
```

Stack: Vite · React 18 · TypeScript · Tailwind (default config) · Framer Motion · lucide-react.
