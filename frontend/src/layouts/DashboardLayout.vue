<script setup lang="ts">
import { computed } from 'vue'
import { RouterView, useRoute } from 'vue-router'
import BaseHeader from '@/components/BaseHeader.vue'
import BaseSidebar from '@/components/BaseSidebar.vue'
import { useWorkspaceStore } from '@/stores/workspace'

const route = useRoute()
const workspaceStore = useWorkspaceStore()

const headerTitle = computed(() =>
  typeof route.meta.headerTitle === 'string' ? route.meta.headerTitle : 'Dashboard',
)

const headerSubtitle = computed(() => {
  const subtitle =
    typeof route.meta.headerSubtitle === 'string'
      ? route.meta.headerSubtitle
      : 'Track workspace activity and keep flows moving.'

  if (!workspaceStore.organizationName) {
    return subtitle
  }

  return `${workspaceStore.organizationName} · ${subtitle}`
})

const headerAvatarLabel = computed(() => {
  if (workspaceStore.organizationName) {
    return getInitials(workspaceStore.organizationName)
  }

  return typeof route.meta.headerAvatarLabel === 'string' ? route.meta.headerAvatarLabel : 'BF'
})

function getInitials(name: string) {
  return name
    .split(/\s+/)
    .filter(Boolean)
    .slice(0, 2)
    .map((part) => part[0]?.toUpperCase() ?? '')
    .join('')
}
</script>

<template>
  <div>
    <main class="dashboard-layout">
      <BaseSidebar />
      <div class="dashboard-layout-content">
        <BaseHeader
          :avatar-label="headerAvatarLabel"
          :title="headerTitle"
          :subtitle="headerSubtitle"
        />
        <RouterView />
      </div>
    </main>
  </div>
</template>

<style scoped>
:global(html),
:global(body),
:global(#app) {
  min-height: 100%;
  margin: 0;
}

.dashboard-layout {
  --dashboard-shell: #fbfeff;
  --dashboard-sky: #aeeeff;
  --dashboard-accent: #34cbbf;
  --dashboard-panel: #fbfbfc;
  --dashboard-panel-soft: #f4f6f8;
  --dashboard-line: rgb(18 33 36 / 10%);

  display: grid;
  grid-template-columns: 204px minmax(0, 1fr);
  min-height: 100vh;
  min-height: 100dvh;
  color: #172224;
  background: var(--dashboard-shell);
}

.dashboard-layout-content {
  position: relative;
  isolation: isolate;
  min-width: 0;
  min-height: calc(100vh - 32px);
  min-height: calc(100dvh - 32px);
  margin: 16px;
  overflow: hidden;
  background:
    linear-gradient(180deg, rgb(255 255 255 / 92%) 0%, rgb(251 251 252 / 96%) 30%, var(--dashboard-panel) 100%),
    var(--dashboard-panel);
  border: 1px solid rgb(255 255 255 / 76%);
  border-radius: 18px;
  box-shadow:
    0 26px 72px rgb(18 33 36 / 8%),
    0 0 0 1px var(--dashboard-line),
    inset 0 1px 0 rgb(255 255 255 / 96%);
}

.dashboard-layout-content::before {
  position: absolute;
  inset: 0;
  z-index: 0;
  pointer-events: none;
  content: '';
  background:
    radial-gradient(42rem 18rem at 12% 0%, rgb(255 255 255 / 78%) 0%, transparent 64%),
    linear-gradient(90deg, rgb(244 246 248 / 82%), transparent 22%),
    linear-gradient(180deg, rgb(226 232 236 / 18%) 0 1px, transparent 1px 100%);
  opacity: 0.9;
}

.dashboard-layout-content > * {
  position: relative;
  z-index: 1;
}

@media (max-width: 760px) {
  .dashboard-layout {
    grid-template-columns: minmax(0, 1fr);
    padding-bottom: calc(88px + env(safe-area-inset-bottom, 0px));
  }

  .dashboard-layout-content {
    min-height: calc(100vh - 24px);
    min-height: calc(100dvh - 24px);
    margin: 12px;
    border-radius: 16px;
  }
}
</style>
