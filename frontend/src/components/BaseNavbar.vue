<script setup lang="ts">
import { ref } from 'vue'
import { ArrowRight, Blend, Menu, X } from '@lucide/vue'
import labiseLogo from '@/assets/img/labise_favicon.png'
const isMobileMenuOpen = ref(false)

const navItems = [
  { label: 'Features', href: '#features' },
  { label: 'Process', href: '#process' },
  { label: 'About', href: '#about' },
]

function toggleMobileMenu() {
  isMobileMenuOpen.value = !isMobileMenuOpen.value
}

function closeMobileMenu() {
  isMobileMenuOpen.value = false
}
</script>

<template>
  <nav class="navbar" aria-label="Primary navigation">
    <div class="navbar-start">
      <a class="brand" href="#home" aria-label="Blendes Flow home" @click="closeMobileMenu">
        <Blend class="brand-icon" :size="20" :stroke-width="2.2" aria-hidden="true" />
        <span>Blendes Flow</span>
      </a>

      <div class="nav-links" aria-label="Main sections">
        <a v-for="item in navItems" :key="item.href" :href="item.href">{{ item.label }}</a>
      </div>
    </div>

    <div class="navbar-actions">
      <div class="organization-pill" aria-label="Project organization: LabiSe">
        <img class="organization-logo" :src="labiseLogo" alt="" aria-hidden="true" />
        <span class="organization-name">LabiSe</span>
      </div>

      <a class="get-started" href="#get-started">
        <span>Get Started</span>
        <ArrowRight class="get-started-icon" :size="13" :stroke-width="2.2" aria-hidden="true" />
      </a>

      <button
        class="mobile-menu"
        :class="{ 'is-open': isMobileMenuOpen }"
        type="button"
        aria-label="Toggle navigation menu"
        aria-controls="mobile-navigation"
        :aria-expanded="isMobileMenuOpen"
        @click="toggleMobileMenu"
      >
        <Menu
          class="mobile-menu-icon menu-icon-open"
          :size="20"
          :stroke-width="2.2"
          aria-hidden="true"
        />
        <X
          class="mobile-menu-icon menu-icon-close"
          :size="20"
          :stroke-width="2.2"
          aria-hidden="true"
        />
      </button>
    </div>

    <div
      v-if="isMobileMenuOpen"
      id="mobile-navigation"
      class="mobile-panel"
      aria-label="Mobile navigation"
    >
      <a v-for="item in navItems" :key="item.href" :href="item.href" @click="closeMobileMenu">
        {{ item.label }}
      </a>
      <a class="mobile-panel-cta" href="#get-started" @click="closeMobileMenu">
        <span>Get Started</span>
        <ArrowRight :size="15" :stroke-width="2.3" aria-hidden="true" />
      </a>
    </div>
  </nav>
</template>

<style scoped>
.navbar {
  position: sticky;
  top: 0;
  z-index: 5;
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  margin: 0;
  padding: 14px clamp(24px, 5vw, 72px);
  color: #ffffff;
  background: rgb(7 17 19 / 54%);
  box-shadow:
    0 1px 0 rgb(255 255 255 / 11%),
    0 18px 44px rgb(0 0 0 / 13%);
  backdrop-filter: blur(18px) saturate(130%);
  animation: navbar-enter 720ms cubic-bezier(0.16, 1, 0.3, 1) both;
}

.navbar-start {
  display: flex;
  align-items: center;
  gap: clamp(28px, 5vw, 76px);
  min-width: 0;
}

.brand,
.nav-links a,
.get-started {
  color: inherit;
  text-decoration: none;
}

.navbar-actions {
  display: flex;
  align-items: center;
  gap: 10px;
  min-width: 0;
}

.organization-pill {
  display: inline-flex;
  align-items: center;
  gap: 9px;
  min-height: 42px;
  padding: 4px 14px 4px 7px;
  color: #ffffff;
  background: rgb(255 255 255 / 8%);
  border-radius: 999px;
  box-shadow:
    0 12px 28px rgb(0 0 0 / 17%),
    inset 0 1px 0 rgb(255 255 255 / 11%);
  backdrop-filter: blur(12px) saturate(125%);
}

.organization-logo {
  display: block;
  width: 30px;
  height: 30px;
  padding: 3px;
  object-fit: contain;
  background: rgb(255 255 255 / 92%);
  outline: 1px solid rgb(255 255 255 / 10%);
  border-radius: 999px;
}

.organization-name {
  color: #ffffff;
  font-size: 0.84rem;
  font-weight: 850;
  line-height: 1;
}

.brand {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  min-height: 40px;
  font-size: clamp(1.18rem, 1.55vw, 1.42rem);
  font-weight: 800;
  line-height: 1;
  text-wrap: balance;
  transition:
    opacity 180ms ease,
    transform 180ms ease;
}

.brand-icon {
  flex: 0 0 auto;
  color: #aeeeff;
}

.nav-links {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 4px;
  background: rgb(255 255 255 / 7%);
  border-radius: 999px;
  box-shadow:
    inset 0 1px 0 rgb(255 255 255 / 8%),
    inset 0 -1px 0 rgb(0 0 0 / 14%);
}

.nav-links a,
.get-started,
.mobile-menu,
.mobile-panel a {
  font-size: 0.82rem;
  font-weight: 700;
  line-height: 1;
  text-transform: none;
  transition:
    background 180ms ease,
    box-shadow 180ms ease,
    color 180ms ease,
    opacity 180ms ease,
    transform 180ms ease;
}

.nav-links a {
  position: relative;
  display: inline-flex;
  align-items: center;
  min-height: 40px;
  padding: 0 15px;
  color: rgb(255 255 255 / 78%);
  border-radius: 999px;
}

.nav-links a:hover,
.nav-links a:focus-visible {
  color: #ffffff;
  background: rgb(255 255 255 / 11%);
  box-shadow: inset 0 1px 0 rgb(255 255 255 / 12%);
}

.brand:hover,
.brand:focus-visible {
  opacity: 0.86;
  transform: translateY(-1px);
}

.get-started {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  min-height: 42px;
  padding: 0 8px 0 17px;
  white-space: nowrap;
  background: #f6fbfc;
  color: #071113;
  border-radius: 999px;
  box-shadow:
    0 12px 28px rgb(0 0 0 / 24%),
    inset 0 1px 0 rgb(255 255 255 / 84%);
}

.get-started:hover,
.get-started:focus-visible {
  transform: translateY(-1px);
  box-shadow:
    0 16px 34px rgb(0 0 0 / 3%),
    0 0 20px rgb(174 238 255 / 18%),
    inset 0 1px 0 rgb(255 255 255 / 84%);
}

.brand:active,
.nav-links a:active,
.get-started:active,
.mobile-menu:active {
  transform: scale(0.96);
}

.get-started-icon {
  flex: 0 0 auto;
  box-sizing: content-box;
  padding: 6px;
  color: #071113;
  background: rgb(7 17 19 / 8%);
  border-radius: 999px;
}

.mobile-menu {
  display: none;
  place-items: center;
  position: relative;
  width: 42px;
  height: 42px;
  padding: 0;
  color: #ffffff;
  cursor: pointer;
  background: rgb(255 255 255 / 10%);
  border: 0;
  border-radius: 999px;
  box-shadow: inset 0 1px 0 rgb(255 255 255 / 11%);
}

.mobile-menu-icon {
  position: absolute;
  inset: 11px;
  opacity: 0;
  filter: blur(4px);
  transform: scale(0.25);
  transition:
    filter 180ms cubic-bezier(0.2, 0, 0, 1),
    opacity 180ms cubic-bezier(0.2, 0, 0, 1),
    transform 180ms cubic-bezier(0.2, 0, 0, 1);
}

.menu-icon-open,
.mobile-menu.is-open .menu-icon-close {
  opacity: 1;
  filter: blur(0);
  transform: scale(1);
}

.mobile-menu.is-open .menu-icon-open {
  opacity: 0;
  filter: blur(4px);
  transform: scale(0.25);
}

.mobile-panel {
  display: none;
}

@keyframes navbar-enter {
  from {
    opacity: 0;
    transform: translateY(-12px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
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
  .navbar {
    padding-top: 12px;
    padding-bottom: 12px;
  }
}

@media (prefers-reduced-motion: reduce) {
  .navbar {
    animation: soft-fade-enter 420ms ease-out both;
  }
}

@media (max-width: 680px) {
  .navbar {
    align-items: center;
    gap: 12px;
    padding: 14px 20px;
  }

  .navbar-start {
    min-width: 0;
  }

  .nav-links {
    display: none;
  }

  .get-started {
    display: none;
  }

  .mobile-menu {
    display: grid;
  }

  .mobile-panel {
    position: absolute;
    top: calc(100% + 8px);
    right: 20px;
    left: 20px;
    z-index: 4;
    display: grid;
    gap: 6px;
    padding: 8px;
    background: rgb(7 17 19 / 88%);
    border-radius: 8px;
    box-shadow:
      0 22px 54px rgb(0 0 0 / 34%),
      inset 0 1px 0 rgb(255 255 255 / 12%);
    backdrop-filter: blur(18px) saturate(130%);
    animation: mobile-panel-enter 180ms cubic-bezier(0.16, 1, 0.3, 1) both;
  }

  .mobile-panel a {
    display: flex;
    align-items: center;
    justify-content: space-between;
    min-height: 44px;
    padding: 0 13px;
    color: rgb(255 255 255 / 84%);
    text-decoration: none;
    border-radius: 6px;
  }

  .mobile-panel a:hover,
  .mobile-panel a:focus-visible {
    color: #ffffff;
    background: rgb(255 255 255 / 10%);
    box-shadow: inset 0 1px 0 rgb(255 255 255 / 10%);
  }

  .mobile-panel a:active {
    transform: scale(0.96);
  }

  .mobile-panel .mobile-panel-cta {
    color: #071113;
    background: #f6fbfc;
    box-shadow: inset 0 1px 0 rgb(255 255 255 / 84%);
  }
}

@media (max-width: 360px) {
  .organization-pill {
    width: 42px;
    justify-content: center;
    padding: 4px;
  }

  .organization-name {
    display: none;
  }

  .mobile-panel {
    right: 12px;
    left: 12px;
  }
}

@keyframes mobile-panel-enter {
  from {
    opacity: 0;
    filter: blur(4px);
    transform: translateY(-6px) scale(0.985);
  }

  to {
    opacity: 1;
    filter: blur(0);
    transform: translateY(0) scale(1);
  }
}
</style>
