<script setup lang="ts">
import {
  Activity,
  ArrowRight,
  BarChart3,
  CheckCircle2,
  Gauge,
  GitBranch,
  LineChart,
  ScanSearch,
  ShieldCheck,
  WavesHorizontal,
} from '@lucide/vue'
import BaseNavbar from '@/components/BaseNavbar.vue'

const features = [
  {
    title: 'Signal diagnosis',
    description: 'Spot process variation before it spreads into downstream decisions.',
    icon: ScanSearch,
  },
  {
    title: 'Flow intelligence',
    description: 'Connect movement, context, and evidence in a single operating view.',
    icon: GitBranch,
  },
  {
    title: 'Improvement loop',
    description: 'Prioritize the next action with measurable impact and clean handoffs.',
    icon: Gauge,
  },
]

const steps = ['Capture the wave', 'Compare the pattern', 'Choose the next move']
</script>

<template>
  <main class="landing-page">
    <BaseNavbar />

    <section id="home" class="hero" aria-label="Blendes landing page">
      <div class="hero-content">
        <p class="hero-eyebrow">
          <Activity :size="16" :stroke-width="2.2" aria-hidden="true" />
          Signal clarity for better decisions
        </p>

        <h1>
          Diagnose the wave and
          <span>improve the flow.</span>
        </h1>

        <p class="hero-subtitle">
          Blendes Flow turns complex process signals into a clear path for investigation,
          prioritization, and continuous improvement.
        </p>

        <div class="hero-actions" aria-label="Primary actions">
          <RouterLink class="hero-action hero-action-primary" :to="{ name: 'auth' }">
            <span>Start your diagnosis</span>
            <ArrowRight
              class="hero-action-icon"
              :size="17"
              :stroke-width="2.4"
              aria-hidden="true"
            />
          </RouterLink>

          <RouterLink class="hero-action hero-action-secondary" :to="{ name: 'auth' }">
            <WavesHorizontal :size="18" :stroke-width="2.3" aria-hidden="true" />
            <span>Explore features</span>
          </RouterLink>
        </div>
      </div>
    </section>

    <section id="features" class="feature-band" aria-label="Features">
      <div class="feature-shell">
        <div class="section-heading section-heading-compact">
          <p>Features</p>
        </div>

        <div class="feature-grid">
          <article v-for="feature in features" :key="feature.title" class="feature-card">
            <component
              :is="feature.icon"
              class="feature-icon"
              :size="25"
              :stroke-width="2.1"
              aria-hidden="true"
            />
            <h3>{{ feature.title }}</h3>
            <p>{{ feature.description }}</p>
          </article>
        </div>
      </div>
    </section>

    <section id="process" class="process-band" aria-labelledby="process-title">
      <div class="process-shell">
        <div class="process-copy">
          <p>Process</p>
          <h2 id="process-title">From signal noise to operational clarity.</h2>
          <p>
            Blendes Flow keeps teams focused on the evidence behind each movement, then turns that
            evidence into a smaller, sharper improvement queue.
          </p>
        </div>

        <div class="insight-panel" aria-label="Signal overview">
          <div class="panel-header">
            <span>
              <Activity :size="18" :stroke-width="2.2" aria-hidden="true" />
              Live signal
            </span>
            <strong>86%</strong>
          </div>

          <div class="signal-chart" aria-hidden="true">
            <span class="bar bar-low"></span>
            <span class="bar bar-mid"></span>
            <span class="bar bar-high"></span>
            <span class="bar bar-mid"></span>
            <span class="bar bar-peak"></span>
            <span class="bar bar-high"></span>
            <span class="bar bar-mid"></span>
          </div>

          <ol class="step-list">
            <li v-for="step in steps" :key="step">
              <CheckCircle2 :size="17" :stroke-width="2.2" aria-hidden="true" />
              <span>{{ step }}</span>
            </li>
          </ol>
        </div>
      </div>
    </section>

    <section id="about" class="about-band" aria-labelledby="about-title">
      <div class="about-shell">
        <div>
          <p>About</p>
          <h2 id="about-title">Designed for teams that need diagnosis without friction.</h2>
        </div>

        <div class="about-metrics" aria-label="Blendes Flow highlights">
          <div>
            <BarChart3 :size="22" :stroke-width="2.1" aria-hidden="true" />
            <strong>Pattern-first</strong>
            <span>Analysis stays tied to what is changing.</span>
          </div>
          <div>
            <LineChart :size="22" :stroke-width="2.1" aria-hidden="true" />
            <strong>Action-ready</strong>
            <span>Insights move quickly from readout to queue.</span>
          </div>
          <div>
            <ShieldCheck :size="22" :stroke-width="2.1" aria-hidden="true" />
            <strong>Evidence-led</strong>
            <span>Every improvement starts from a visible signal.</span>
          </div>
        </div>
      </div>
    </section>

    <section id="get-started" class="start-band" aria-labelledby="start-title">
      <div class="start-shell">
        <WavesHorizontal class="start-icon" :size="30" :stroke-width="2.1" aria-hidden="true" />
        <div>
          <p>Get started</p>
          <h2 id="start-title">Bring your next diagnostic flow into focus.</h2>
        </div>
        <a class="start-action" href="/auth">
          <span>Open workspace</span>
          <ArrowRight :size="17" :stroke-width="2.4" aria-hidden="true" />
        </a>
      </div>
    </section>
  </main>
</template>

<style scoped>
:global(*) {
  box-sizing: border-box;
}

:global(html),
:global(body),
:global(#app) {
  min-height: 100%;
  margin: 0;
}

.landing-page {
  min-height: 100vh;
  color: #ffffff;
  background: linear-gradient(180deg, #071113 0%, #0b1718 43%, #f5f8f7 43%, #f5f8f7 100%);
}

.hero {
  position: relative;
  display: grid;
  grid-template-rows: 1fr;
  min-height: clamp(500px, calc(100svh - 118px), 760px);
  overflow: hidden;
  background-image:
    radial-gradient(
      ellipse at 48% 40%,
      rgb(7 17 19 / 36%) 0%,
      rgb(7 17 19 / 58%) 48%,
      rgb(7 17 19 / 86%) 100%
    ),
    linear-gradient(90deg, rgb(3 12 15 / 82%) 0%, rgb(3 12 15 / 34%) 47%, rgb(3 12 15 / 66%) 100%),
    linear-gradient(180deg, rgb(0 0 0 / 20%) 0%, rgb(0 0 0 / 10%) 45%, rgb(0 0 0 / 78%) 100%),
    url('@/assets/img/hero.png');
  background-position: center;
  background-repeat: no-repeat;
  background-size: cover;
  box-shadow: inset 0 -1px 0 rgb(255 255 255 / 10%);
}

.hero-content {
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 0;
  height: 100%;
  width: min(100%, 1180px);
  margin: 0 auto;
  padding: clamp(34px, 5vh, 54px) clamp(24px, 5vw, 72px) clamp(44px, 8vh, 72px);
}

.hero-eyebrow {
  display: inline-flex;
  align-items: center;
  gap: 9px;
  min-height: 40px;
  margin: 0 0 18px;
  padding: 0 16px 0 13px;
  color: rgb(255 255 255 / 88%);
  font-size: 0.84rem;
  font-weight: 800;
  line-height: 1;
  background: rgb(255 255 255 / 10%);
  border-radius: 999px;
  box-shadow:
    0 12px 30px rgb(0 0 0 / 20%),
    inset 0 1px 0 rgb(255 255 255 / 12%);
  backdrop-filter: blur(14px) saturate(125%);
  animation: hero-title-enter 820ms cubic-bezier(0.16, 1, 0.3, 1) 80ms both;
}

.hero-content h1 {
  max-width: 990px;
  margin: 0;
  font-size: clamp(2.75rem, 5.25vw, 5rem);
  font-weight: 800;
  line-height: 0.98;
  letter-spacing: 0;
  text-align: center;
  text-wrap: balance;
  text-shadow: 0 5px 30px rgb(0 0 0 / 48%);
  animation: hero-title-enter 900ms cubic-bezier(0.16, 1, 0.3, 1) 170ms both;
}

.hero-content span {
  display: inline-block;
  color: #aeeeff;
  text-shadow:
    0 5px 26px rgb(0 0 0 / 56%),
    0 0 22px rgb(139 231 255 / 22%);
}

.hero-subtitle {
  max-width: 660px;
  margin: 22px 0 0;
  color: rgb(255 255 255 / 78%);
  font-size: clamp(1rem, 1.4vw, 1.17rem);
  font-weight: 600;
  line-height: 1.65;
  text-align: center;
  text-wrap: pretty;
  text-shadow: 0 4px 22px rgb(0 0 0 / 42%);
  animation: hero-action-enter 860ms cubic-bezier(0.16, 1, 0.3, 1) 250ms both;
}

.hero-actions {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: center;
  gap: 12px;
  margin-top: 30px;
  animation: hero-action-enter 900ms cubic-bezier(0.16, 1, 0.3, 1) 340ms both;
}

.hero-action {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  min-height: 52px;
  padding: 0 24px;
  color: #ffffff;
  font-size: 1rem;
  font-weight: 800;
  line-height: 1;
  text-decoration: none;
  border-radius: 999px;
  outline: 0;
  box-shadow:
    0 14px 34px rgb(0 0 0 / 34%),
    inset 0 1px 0 rgb(255 255 255 / 14%),
    inset 0 -1px 0 rgb(255 255 255 / 7%);
  backdrop-filter: blur(14px) saturate(125%);
  transition:
    background 180ms ease,
    box-shadow 180ms ease,
    color 180ms ease,
    transform 180ms ease;
}

.hero-action-primary {
  color: #071113;
  background: #f6fbfc;
  box-shadow:
    0 15px 34px rgb(0 0 0 / 34%),
    0 0 28px rgb(174 238 255 / 12%),
    inset 0 1px 0 rgb(255 255 255 / 88%);
  animation: hero-action-glow 3000ms ease-in-out 1100ms infinite;
}

.hero-action-secondary {
  background: rgb(23 34 36 / 64%);
  box-shadow:
    0 14px 34px rgb(0 0 0 / 30%),
    inset 0 1px 0 rgb(255 255 255 / 12%);
}

.hero-action:hover,
.hero-action:focus-visible {
  box-shadow:
    0 18px 44px rgb(0 0 0 / 40%),
    0 0 24px rgb(174 238 255 / 14%),
    inset 0 1px 0 rgb(255 255 255 / 18%),
    inset 0 -1px 0 rgb(255 255 255 / 9%);
  transform: translateY(-2px);
}

.hero-action:active {
  transform: scale(0.96);
}

.hero-action-primary span {
  color: #071113;
}

.hero-action-icon {
  flex: 0 0 auto;
  box-sizing: content-box;
  padding: 4px;
  color: #172224;
  background: rgb(7 17 19 / 9%);
  border-radius: 999px;
}

.feature-band,
.process-band,
.about-band,
.start-band {
  position: relative;
  color: #071113;
}

.feature-band {
  padding: 26px clamp(20px, 5vw, 72px) 80px;
  background: #f5f8f7;
}

.feature-shell,
.process-shell,
.about-shell,
.start-shell {
  width: min(100%, 1180px);
  margin: 0 auto;
}

.section-heading,
.process-copy,
.about-shell > div:first-child,
.start-shell > div {
  text-wrap: pretty;
}

.section-heading {
  display: flex;
  align-items: end;
  justify-content: space-between;
  gap: 32px;
  margin-bottom: 24px;
}

.section-heading-compact {
  margin-bottom: 18px;
}

.section-heading p,
.process-copy > p:first-child,
.about-shell > div:first-child p,
.start-shell p {
  margin: 0 0 10px;
  color: #2c6e69;
  font-size: 0.78rem;
  font-weight: 900;
  letter-spacing: 0.08em;
  line-height: 1;
  text-transform: uppercase;
}

.section-heading h2,
.process-copy h2,
.about-shell h2,
.start-shell h2 {
  margin: 0;
  font-size: clamp(1.85rem, 3vw, 3rem);
  font-weight: 850;
  line-height: 1.04;
  letter-spacing: 0;
  text-wrap: balance;
}

.section-heading h2 {
  max-width: 620px;
}

.feature-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 14px;
}

.feature-card {
  min-height: 244px;
  padding: 24px;
  background: #ffffff;
  border-radius: 8px;
  box-shadow:
    0 1px 0 rgb(7 17 19 / 7%),
    0 18px 45px rgb(15 44 43 / 10%);
  transition:
    box-shadow 180ms ease,
    transform 180ms ease;
}

.feature-card:hover {
  transform: translateY(-3px);
  box-shadow:
    0 1px 0 rgb(7 17 19 / 7%),
    0 24px 56px rgb(15 44 43 / 15%);
}

.feature-icon {
  display: block;
  width: 48px;
  height: 48px;
  margin-bottom: 38px;
  padding: 11px;
  color: #0f5753;
  background: #dff8f3;
  border-radius: 8px;
}

.feature-card h3 {
  margin: 0 0 10px;
  font-size: 1.12rem;
  font-weight: 850;
  line-height: 1.15;
}

.feature-card p,
.process-copy p:last-child,
.about-metrics span {
  margin: 0;
  color: rgb(7 17 19 / 68%);
  font-size: 0.98rem;
  font-weight: 600;
  line-height: 1.65;
  text-wrap: pretty;
}

.process-band {
  padding: 84px clamp(20px, 5vw, 72px);
  color: #ffffff;
  background: linear-gradient(135deg, #071113 0%, #0d2e2c 48%, #183b31 100%);
}

.process-shell {
  display: grid;
  grid-template-columns: minmax(0, 0.9fr) minmax(340px, 0.72fr);
  gap: clamp(34px, 6vw, 86px);
  align-items: center;
}

.process-copy h2 {
  max-width: 620px;
}

.process-copy p:last-child {
  max-width: 570px;
  margin-top: 22px;
  color: rgb(255 255 255 / 72%);
}

.insight-panel {
  padding: 16px;
  background: rgb(255 255 255 / 9%);
  border-radius: 8px;
  box-shadow:
    0 22px 60px rgb(0 0 0 / 28%),
    inset 0 1px 0 rgb(255 255 255 / 12%);
  backdrop-filter: blur(18px) saturate(130%);
}

.panel-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 18px;
  min-height: 52px;
  padding: 0 4px 0 8px;
}

.panel-header span {
  display: inline-flex;
  align-items: center;
  gap: 9px;
  color: rgb(255 255 255 / 80%);
  font-weight: 800;
}

.panel-header strong {
  font-size: 2.2rem;
  font-weight: 900;
  font-variant-numeric: tabular-nums;
  line-height: 1;
}

.signal-chart {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  align-items: end;
  gap: 8px;
  height: 176px;
  margin-top: 10px;
  padding: 18px;
  background: rgb(7 17 19 / 40%);
  border-radius: 6px;
  box-shadow: inset 0 1px 0 rgb(255 255 255 / 8%);
}

.bar {
  display: block;
  min-height: 26px;
  border-radius: 5px 5px 2px 2px;
  background: linear-gradient(180deg, #aeeeff 0%, #3dd6c4 100%);
  box-shadow: 0 8px 20px rgb(61 214 196 / 20%);
}

.bar-low {
  height: 38%;
}

.bar-mid {
  height: 56%;
}

.bar-high {
  height: 76%;
}

.bar-peak {
  height: 94%;
  background: linear-gradient(180deg, #ffe08a 0%, #50e3c2 100%);
}

.step-list {
  display: grid;
  gap: 8px;
  margin: 14px 0 0;
  padding: 0;
  list-style: none;
}

.step-list li {
  display: flex;
  align-items: center;
  gap: 10px;
  min-height: 42px;
  padding: 0 12px;
  color: rgb(255 255 255 / 82%);
  font-weight: 800;
  background: rgb(255 255 255 / 8%);
  border-radius: 6px;
}

.step-list svg {
  color: #8cf0df;
  flex: 0 0 auto;
}

.about-band {
  padding: 82px clamp(20px, 5vw, 72px);
  background: #f5f8f7;
}

.about-shell {
  display: grid;
  grid-template-columns: minmax(0, 0.78fr) minmax(0, 1fr);
  gap: clamp(34px, 5vw, 76px);
  align-items: start;
}

.about-metrics {
  display: grid;
  gap: 12px;
}

.about-metrics div {
  display: grid;
  grid-template-columns: auto 1fr;
  gap: 5px 14px;
  padding: 20px;
  background: #ffffff;
  border-radius: 8px;
  box-shadow:
    0 1px 0 rgb(7 17 19 / 7%),
    0 16px 36px rgb(15 44 43 / 9%);
}

.about-metrics svg {
  grid-row: span 2;
  color: #0f5753;
}

.about-metrics strong {
  font-size: 1rem;
  font-weight: 900;
  line-height: 1.1;
}

.start-band {
  padding: 0 clamp(20px, 5vw, 72px) 86px;
  background: #f5f8f7;
}

.start-shell {
  display: grid;
  grid-template-columns: auto 1fr auto;
  gap: 22px;
  align-items: center;
  padding: 28px;
  color: #ffffff;
  background:
    linear-gradient(135deg, rgb(7 17 19 / 92%) 0%, rgb(15 87 83 / 92%) 100%),
    url('@/assets/img/hero.png');
  background-position: center;
  background-size: cover;
  border-radius: 8px;
  box-shadow:
    0 24px 64px rgb(7 17 19 / 18%),
    inset 0 1px 0 rgb(255 255 255 / 12%);
}

.start-icon {
  width: 58px;
  height: 58px;
  padding: 13px;
  color: #071113;
  background: #aeeeff;
  border-radius: 8px;
  box-shadow: 0 12px 24px rgb(174 238 255 / 18%);
}

.start-shell p {
  color: #aeeeff;
}

.start-shell h2 {
  max-width: 680px;
}

.start-action {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 9px;
  min-height: 48px;
  padding: 0 20px;
  color: #071113;
  font-weight: 900;
  line-height: 1;
  text-decoration: none;
  white-space: nowrap;
  background: #f6fbfc;
  border-radius: 999px;
  box-shadow:
    0 14px 30px rgb(0 0 0 / 25%),
    inset 0 1px 0 rgb(255 255 255 / 84%);
  transition:
    box-shadow 180ms ease,
    transform 180ms ease;
}

.start-action:hover,
.start-action:focus-visible {
  transform: translateY(-2px);
  box-shadow:
    0 18px 38px rgb(0 0 0 / 30%),
    0 0 22px rgb(174 238 255 / 20%),
    inset 0 1px 0 rgb(255 255 255 / 84%);
}

.start-action:active {
  transform: scale(0.96);
}

@keyframes hero-action-glow {
  0%,
  100% {
    box-shadow:
      0 15px 34px rgb(0 0 0 / 34%),
      0 0 0 rgb(174 238 255 / 0%),
      inset 0 1px 0 rgb(255 255 255 / 88%);
  }

  50% {
    box-shadow:
      0 15px 34px rgb(0 0 0 / 34%),
      0 0 26px rgb(174 238 255 / 18%),
      inset 0 1px 0 rgb(255 255 255 / 88%);
  }
}

@keyframes hero-title-enter {
  from {
    opacity: 0;
    filter: blur(8px);
    transform: translateY(18px) scale(0.985);
  }

  to {
    opacity: 1;
    filter: blur(0);
    transform: translateY(0) scale(1);
  }
}

@keyframes hero-action-enter {
  from {
    opacity: 0;
    transform: translateY(16px) scale(0.98);
  }

  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

@keyframes soft-fade-enter {
  from {
    opacity: 0;
  }

  to {
    opacity: 1;
  }
}

@media (min-width: 681px) and (max-height: 620px) {
  .hero-content {
    padding-top: 34px;
    padding-bottom: 82px;
  }

  .hero-content h1 {
    max-width: 960px;
    font-size: clamp(2.55rem, 4.45vw, 3.75rem);
    line-height: 0.98;
  }

  .hero-action {
    min-height: 48px;
  }

  .hero-content span {
    white-space: nowrap;
  }
}

@media (prefers-reduced-motion: reduce) {
  .hero-content h1 {
    animation: soft-fade-enter 420ms ease-out both;
  }

  .hero-action {
    animation:
      soft-fade-enter 460ms ease-out 120ms both,
      hero-action-glow 3600ms ease-in-out 900ms infinite;
  }

  .hero-action:hover {
    transform: none;
  }

  .feature-card,
  .start-action {
    transition: none;
  }

  .feature-card:hover,
  .start-action:hover,
  .start-action:focus-visible {
    transform: none;
  }
}

@media (max-width: 900px) {
  .feature-grid,
  .process-shell,
  .about-shell {
    grid-template-columns: 1fr;
  }

  .process-shell {
    gap: 34px;
  }

  .start-shell {
    grid-template-columns: 1fr;
    justify-items: start;
  }
}

@media (max-width: 680px) {
  .hero-content {
    align-items: center;
    justify-content: center;
    min-height: 0;
    padding: 34px 20px 74px;
  }

  .hero-content h1 {
    font-size: clamp(2.36rem, 10.4vw, 3.14rem);
  }

  .hero-subtitle {
    font-size: 1rem;
    line-height: 1.58;
  }

  .hero-actions {
    width: 100%;
  }

  .hero-action {
    width: min(100%, 330px);
    min-height: 50px;
    padding: 0 20px 0 24px;
  }

  .feature-band {
    padding-top: 22px;
    padding-bottom: 62px;
  }

  .feature-card {
    min-height: auto;
  }

  .section-heading {
    display: block;
  }

  .process-band,
  .about-band {
    padding-top: 66px;
    padding-bottom: 66px;
  }

  .insight-panel {
    padding: 12px;
  }

  .signal-chart {
    height: 144px;
    gap: 6px;
    padding: 14px;
  }

  .start-band {
    padding-bottom: 68px;
  }

  .start-shell {
    padding: 22px;
  }

  .start-action {
    width: 100%;
  }
}
</style>
