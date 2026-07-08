<script setup lang="ts">
import { computed, type Component } from 'vue'
import {
  LayoutDashboard,
  Settings,
  UsersRound,
  Workflow,
  ChartNoAxesCombined,
  Star,
  CircleUserRound,
} from '@lucide/vue'
import { useRoute, type RouteLocationRaw } from 'vue-router'

import { usePreferencesStore } from '@/stores/preferences'
import { useWorkspaceStore } from '@/stores/workspace'

import DashboardHeader from '@/components/DashboardHeader.vue'
import DashboardSidebar from '@/components/DashboardSidebar.vue'

type DashboardRouteName = 'dashboard' | 'flows' | 'metrics' | 'company' | 'profile' | 'settings'

type DashboardPage = {
  breadcrumbs: string[]
  icon: Component
  isHiddenFromNavigation?: boolean
  label: string
  routeName: DashboardRouteName
  title: string
  to: RouteLocationRaw
}

type FavoritePage = {
  icon: Component
  label: string
  to: RouteLocationRaw
}

const dashboardPages: DashboardPage[] = [
  {
    breadcrumbs: ['Dashboard', 'Overview'],
    icon: LayoutDashboard,
    label: 'Overview',
    routeName: 'dashboard',
    title: 'Overview',
    to: { name: 'dashboard' },
  },
  {
    breadcrumbs: ['Dashboard', 'Flows'],
    icon: Workflow,
    label: 'Flows',
    routeName: 'flows',
    title: 'Flows',
    to: { name: 'flows' },
  },
  {
    breadcrumbs: ['Dashboard', 'Company'],
    icon: UsersRound,
    label: 'Company',
    routeName: 'company',
    title: 'Company',
    to: { name: 'company' },
  },
  {
    breadcrumbs: ['Dashboard', 'Profile'],
    icon: CircleUserRound,
    isHiddenFromNavigation: true,
    label: 'Profile',
    routeName: 'profile',
    title: 'Profile',
    to: { name: 'profile' },
  },
  {
    breadcrumbs: ['Dashboard', 'Settings'],
    icon: Settings,
    label: 'Settings',
    routeName: 'settings',
    title: 'Settings',
    to: { name: 'settings' },
  },
]

const favoritePages: FavoritePage[] = [
  { icon: Star, label: 'Pinned flows', to: { name: 'flows' } },
  {
    icon: ChartNoAxesCombined,
    label: 'Weekly metrics',
    to: { name: 'metrics' },
  },
  { icon: UsersRound, label: 'Company board', to: { name: 'company' } },
]

const overviewPage = dashboardPages[0]!

const preferencesStore = usePreferencesStore()
const route = useRoute()
const workspaceStore = useWorkspaceStore()

const currentPage = computed<DashboardPage>(
  () => dashboardPages.find((page) => page.routeName === route.name) ?? overviewPage,
)

const workspaceName = computed(() => workspaceStore.organizationName || 'Current workspace')

const navigationItems = computed(() =>
  dashboardPages
    .filter((page) => !page.isHiddenFromNavigation)
    .map((page) => ({
      icon: page.icon,
      isActive: page.routeName === route.name,
      label: page.label,
      to: page.to,
    })),
)

function toggleSidebar() {
  preferencesStore.toggleSidebar()
}
</script>

<template>
  <main
    class="grid min-h-screen gap-0 bg-slate-100 bg-[radial-gradient(ellipse_at_12%_0%,rgb(59_130_246_/_0.10)_0%,rgb(239_246_255_/_0.36)_34%,rgb(255_255_255_/_0)_68%),linear-gradient(180deg,rgb(239_246_255_/_0.56)_0%,rgb(255_255_255_/_0)_100%)] bg-[length:360px_164px,100%_220px] bg-left-top bg-no-repeat text-slate-900 antialiased transition-[grid-template-columns,background-color,color] duration-200 ease-out max-lg:grid-cols-[76px_minmax(0,1fr)] max-md:grid-cols-1 max-md:p-2 motion-reduce:transition-none dark:bg-slate-950 dark:bg-[radial-gradient(ellipse_at_12%_0%,rgb(14_165_233_/_0.16)_0%,rgb(15_23_42_/_0.52)_34%,rgb(2_6_23_/_0)_68%),linear-gradient(180deg,rgb(15_23_42_/_0.82)_0%,rgb(2_6_23_/_0)_100%)] dark:text-slate-100"
    :class="
      preferencesStore.isSidebarCollapsed
        ? 'grid-cols-[76px_minmax(0,1fr)]'
        : 'grid-cols-[220px_minmax(0,1fr)]'
    "
    aria-labelledby="dashboard-title"
  >
    <DashboardSidebar
      :enable-floating-tips="preferencesStore.enableFloatingTips"
      :favorite-items="favoritePages"
      :is-favorites-open="preferencesStore.isFavoritesOpen"
      :items="navigationItems"
      :workspace-name="workspaceName"
      :is-collapsed="preferencesStore.isSidebarCollapsed"
      @toggle-favorites="preferencesStore.toggleFavorites"
    />

    <section
      class="grid min-h-screen min-w-0 grid-rows-[auto_1fr] overflow-hidden border-y border-r border-slate-200 bg-slate-50 transition-[background-color,border-color] duration-200 max-md:min-h-[calc(100vh-16px)] max-md:rounded-2xl max-md:border dark:border-slate-800 dark:bg-slate-950"
      aria-label="Dashboard workspace"
    >
      <DashboardHeader
        :breadcrumbs="currentPage.breadcrumbs"
        :is-sidebar-collapsed="preferencesStore.isSidebarCollapsed"
        :title="currentPage.title"
        @toggle-sidebar="toggleSidebar"
      >
        <template #actions>
          <slot name="header-actions" />
        </template>
      </DashboardHeader>
      <div class="min-h-0 bg-slate-50 p-6 transition-colors duration-200 md:p-8 dark:bg-slate-950">
        <slot />
      </div>
    </section>
  </main>
</template>
