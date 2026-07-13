import { MotionConfig } from 'framer-motion'
import AuroraBackground from './components/aurora-background'
import Navbar from './components/navbar'
import Hero from './components/hero'
import StatsStrip from './components/stats-strip'
import Showcase from './components/showcase'
import HowItWorks from './components/how-it-works'
import SkillsSuite from './components/skills-suite'
import McpTools from './components/mcp-tools'
import PromptMarquee from './components/prompt-marquee'
import FinalCta from './components/final-cta'

export default function App() {
  return (
    // reducedMotion="user" makes every framer-motion animation respect
    // prefers-reduced-motion globally, in addition to the CSS media block.
    <MotionConfig reducedMotion="user">
      <div className="relative min-h-screen overflow-x-clip">
        <AuroraBackground />
        <Navbar />
        <main>
          {/* Hook+Range (the stage lives in the hero) → Proof → Method → Ecosystem → Corpus → CTA */}
          <Hero />
          <StatsStrip />
          <Showcase />
          <HowItWorks />
          <SkillsSuite />
          <McpTools />
          <PromptMarquee />
          <FinalCta />
        </main>
      </div>
    </MotionConfig>
  )
}
