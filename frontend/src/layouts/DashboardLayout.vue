<script setup lang="ts">
import { computed } from 'vue'
import { RouterView, useRoute } from 'vue-router'
import BaseHeader from '@/components/BaseHeader.vue'
import BaseSidebar from '@/components/BaseSidebar.vue'

const route = useRoute()

const headerTitle = computed(() =>
  typeof route.meta.headerTitle === 'string' ? route.meta.headerTitle : 'Dashboard',
)

const headerSubtitle = computed(() =>
  typeof route.meta.headerSubtitle === 'string'
    ? route.meta.headerSubtitle
    : 'Track workspace activity and keep flows moving.',
)

const headerAvatarLabel = computed(() =>
  typeof route.meta.headerAvatarLabel === 'string' ? route.meta.headerAvatarLabel : 'BF',
)
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
  display: grid;
  grid-template-columns: 76px minmax(0, 1fr);
  min-height: 100vh;
  min-height: 100dvh;
  color: #172224;
  background: #fbfeff;
}

.dashboard-layout-content {
  min-width: 0;
  min-height: 100vh;
  min-height: 100dvh;
}

@media (max-width: 760px) {
  .dashboard-layout {
    grid-template-columns: minmax(0, 1fr);
    padding-bottom: calc(88px + env(safe-area-inset-bottom, 0px));
  }
}
</style>
