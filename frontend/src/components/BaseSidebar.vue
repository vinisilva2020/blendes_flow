<script setup lang="ts">
import {
  Blend,
  ChartNoAxesCombined,
  CircleUserRound,
  LayoutDashboard,
  Settings,
  UsersRound,
  Workflow,
} from '@lucide/vue'

const mainItems = [
  { label: 'Dashboard', to: '/dashboard', icon: LayoutDashboard },
  { label: 'Workflows', to: '/dashboard/workflows', icon: Workflow },
  { label: 'Members', to: '/dashboard/members', icon: UsersRound },
  { label: 'Metrics', to: '/dashboard/metrics', icon: ChartNoAxesCombined },
]
</script>

<template>
  <aside class="dashboard-sidebar" aria-label="Dashboard navigation">
    <RouterLink class="sidebar-brand" to="/" aria-label="Blendes Flow home">
      <span class="sidebar-brand-mark">
        <Blend :size="21" :stroke-width="2.2" aria-hidden="true" />
      </span>
      <span class="sidebar-brand-title">Blendes Flow</span>
    </RouterLink>

    <nav class="sidebar-navigation" aria-label="Main dashboard sections">
      <p class="sidebar-section-label">Main</p>

      <RouterLink
        v-for="item in mainItems"
        :key="item.label"
        class="sidebar-action"
        :to="item.to"
        :aria-label="item.label"
      >
        <component :is="item.icon" :size="15" :stroke-width="2.15" aria-hidden="true" />
        <span>{{ item.label }}</span>
      </RouterLink>
    </nav>

    <nav class="sidebar-footer" aria-label="Account navigation">
      <RouterLink class="sidebar-action" to="/dashboard/settings" aria-label="Settings">
        <Settings :size="15" :stroke-width="2.15" aria-hidden="true" />
        <span>Settings</span>
      </RouterLink>

      <RouterLink class="sidebar-action" to="/dashboard/profile" aria-label="Profile">
        <CircleUserRound :size="15" :stroke-width="2.15" aria-hidden="true" />
        <span>Profile</span>
      </RouterLink>
    </nav>
  </aside>
</template>

<style scoped>
.dashboard-sidebar {
  --sidebar-ink: #172224;
  --sidebar-muted: #667b80;
  --sidebar-line: rgb(18 33 36 / 12%);
  --sidebar-accent: #34cbbf;
  --sidebar-accent-deep: #0f5753;

  position: relative;
  box-sizing: border-box;
  isolation: isolate;
  display: flex;
  flex-direction: column;
  align-items: stretch;
  gap: 24px;
  width: 204px;
  min-height: 100vh;
  min-height: 100dvh;
  padding: 18px 14px;
  overflow: visible;
  background: #fbfeff;
}

.sidebar-brand,
.sidebar-action,
.favorite-dot {
  position: relative;
  z-index: 1;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  color: inherit;
  text-decoration: none;
  border: 0;
  outline: 0;
  cursor: pointer;
  transition:
    background 180ms ease,
    box-shadow 180ms ease,
    color 180ms ease,
    opacity 180ms ease,
    transform 180ms ease;
}

.sidebar-brand {
  width: 100%;
  height: 44px;
  justify-content: flex-start;
  gap: 10px;
  padding: 0 10px 0 2px;
  color: #0d5d67;
  background: transparent;
  border-radius: 12px;
}

.sidebar-brand-mark {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 44px;
  height: 44px;
  flex: 0 0 44px;
  background: #f6fffd;
  border-radius: 12px;
  box-shadow:
    inset 0 0 0 1px rgb(15 87 83 / 8%),
    0 10px 22px rgb(36 107 120 / 6%);
}

.sidebar-brand-title {
  min-width: 0;
  overflow: hidden;
  color: #172224;
  font-size: 0.86rem;
  font-weight: 950;
  letter-spacing: 0;
  line-height: 1.05;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.sidebar-navigation,
.sidebar-footer,
.sidebar-favorites {
  position: relative;
  z-index: 1;
  display: grid;
  justify-items: stretch;
  gap: 7px;
  width: 100%;
}

.sidebar-navigation {
  margin-top: 4px;
}

.sidebar-favorites {
  margin-top: auto;
  margin-bottom: auto;
}

.sidebar-footer {
  position: relative;
  gap: 7px;
  margin-top: 0;
  padding-top: 0;
}

.sidebar-section-label {
  margin: 0 10px 8px;
  color: #8da2a7;
  font-size: 0.58rem;
  font-weight: 900;
  letter-spacing: 0.12em;
  line-height: 1;
}

.sidebar-action {
  width: 100%;
  height: 44px;
  justify-content: flex-start;
  gap: 10px;
  padding: 0 12px;
  color: var(--sidebar-muted);
  background: transparent;
  border-radius: 12px;
}

.sidebar-action span {
  min-width: 0;
  overflow: hidden;
  color: inherit;
  font-size: 0.78rem;
  font-weight: 850;
  line-height: 1.1;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.sidebar-action:hover,
.sidebar-action:focus-visible {
  color: var(--sidebar-ink);
  background: #f2fbf9;
  box-shadow:
    inset 0 0 0 1px rgb(15 87 83 / 7%),
    0 8px 18px rgb(18 33 36 / 4%);
}

.sidebar-action.router-link-exact-active {
  color: var(--sidebar-accent-deep);
  background: transparent;
  box-shadow: none;
}

.sidebar-action.router-link-exact-active::before {
  position: absolute;
  left: -6px;
  width: 3px;
  height: 24px;
  content: '';
  background: var(--sidebar-accent);
  border-radius: 999px;
  box-shadow:
    0 0 0 1px rgb(15 87 83 / 14%),
    0 6px 14px rgb(15 87 83 / 10%);
}

.sidebar-brand:active,
.sidebar-action:active,
.favorite-dot:active {
  transform: scale(0.96);
}

.favorite-dot {
  width: 40px;
  height: 40px;
  padding: 0;
  background: transparent;
}

.favorite-dot span {
  width: 8px;
  height: 8px;
  background: var(--favorite-color);
  border-radius: 999px;
  box-shadow: 0 0 16px color-mix(in srgb, var(--favorite-color) 44%, transparent);
}

.favorite-dot::after {
  position: absolute;
  left: calc(100% + 14px);
  z-index: 3;
  padding: 8px 10px;
  color: #ffffff;
  font-size: 0.66rem;
  font-weight: 800;
  line-height: 1;
  white-space: nowrap;
  pointer-events: none;
  background: linear-gradient(180deg, #132326, #071113);
  border-radius: 7px;
  box-shadow:
    0 14px 32px rgb(7 17 19 / 24%),
    inset 0 1px 0 rgb(255 255 255 / 10%);
  content: attr(aria-label);
  opacity: 0;
  transform: translateX(-5px) scale(0.98);
  transform-origin: left center;
  transition:
    opacity 160ms ease,
    transform 160ms ease;
}

.favorite-dot:hover::after,
.favorite-dot:focus-visible::after {
  opacity: 1;
  transform: translateX(0) scale(1);
}

@media (prefers-reduced-motion: reduce) {
  .sidebar-brand,
  .sidebar-action,
  .favorite-dot,
  .sidebar-action span,
  .favorite-dot::after {
    transition: none;
  }
}

@media (max-width: 760px) {
  .dashboard-sidebar {
    position: fixed;
    inset: auto 12px max(12px, env(safe-area-inset-bottom, 0px)) 12px;
    z-index: 20;
    flex-direction: row;
    gap: 8px;
    width: auto;
    min-height: 0;
    max-height: none;
    height: 64px;
    padding: 10px;
    overflow: visible;
    border-radius: 16px;
    background: #fbfeff;
    box-shadow:
      0 18px 44px rgb(18 33 36 / 14%),
      inset 0 1px 0 rgb(255 255 255 / 72%);
  }

  .dashboard-sidebar::after {
    inset: 0;
    width: auto;
    background: none;
    border: 1px solid rgb(18 33 36 / 14%);
    border-radius: inherit;
  }

  .sidebar-brand {
    width: 40px;
    height: 40px;
    justify-content: center;
    gap: 0;
    padding: 0;
    flex: 0 0 40px;
    border-radius: 11px;
  }

  .sidebar-brand-mark {
    width: 40px;
    height: 40px;
    flex-basis: 40px;
    border-radius: 11px;
  }

  .sidebar-brand-title {
    display: none;
  }

  .sidebar-navigation {
    display: flex;
    flex: 1 1 auto;
    justify-items: stretch;
    gap: 6px;
    min-width: 0;
    margin-top: 0;
    padding: 0 2px;
    overflow-x: auto;
    overflow-y: hidden;
    overscroll-behavior-x: contain;
    scrollbar-width: none;
  }

  .sidebar-navigation::-webkit-scrollbar {
    display: none;
  }

  .sidebar-footer {
    display: flex;
    flex: 0 0 auto;
    align-items: center;
    gap: 6px;
    width: auto;
    margin-top: 0;
    padding-top: 0;
    padding-left: 0;
  }

  .sidebar-favorites,
  .sidebar-section-label {
    display: none;
  }

  .sidebar-action,
  .favorite-dot {
    width: 40px;
    height: 40px;
    justify-content: center;
    padding: 0;
    flex: 0 0 40px;
  }

  .sidebar-action span,
  .favorite-dot::after {
    display: none;
  }

  .sidebar-action.router-link-exact-active::before {
    left: 50%;
    bottom: -7px;
    width: 18px;
    height: 3px;
    transform: translateX(-50%);
  }
}

@media (max-width: 420px) {
  .dashboard-sidebar {
    inset: auto 8px max(8px, env(safe-area-inset-bottom, 0px)) 8px;
    gap: 6px;
    height: 60px;
    padding: 8px;
  }

  .sidebar-brand {
    display: none;
  }
}

@media (min-width: 761px) and (max-height: 620px) {
  .dashboard-sidebar {
    gap: 12px;
    padding: 12px 0;
  }

  .sidebar-navigation,
  .sidebar-footer,
  .sidebar-favorites {
    gap: 5px;
  }

  .sidebar-footer {
    padding-top: 12px;
  }

  .sidebar-section-label {
    margin-bottom: 3px;
  }

  .sidebar-favorites {
    margin-top: 8px;
    margin-bottom: 8px;
  }

  .sidebar-action,
  .favorite-dot {
    height: 40px;
  }
}
</style>
