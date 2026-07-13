import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// base targets the project GitHub Pages URL (/motion-site-builder/). Vite
// rewrites root-relative asset URLs in index.html to this base, and the dev
// server serves under it too. Override with VITE_BASE for a different host.
export default defineConfig({
  base: process.env.VITE_BASE ?? '/motion-site-builder/',
  plugins: [react()],
})
