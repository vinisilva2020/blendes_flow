<script setup lang="ts">
import { ArrowRight, Activity, WavesHorizontal } from '@lucide/vue'
import BaseNavbar from '@/layouts/navbar/BaseNavbar.vue';
import Features from './Features.vue';
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

    <Features />
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
}
</style>
