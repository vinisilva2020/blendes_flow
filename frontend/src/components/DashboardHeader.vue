<script setup lang="ts">
import { computed } from 'vue'
import { Bell, Share2, SquareChevronLeft, SquareChevronRight, Star } from '@lucide/vue'

import DashboardAccountMenu from '@/components/DashboardAccountMenu.vue'

const props = defineProps<{
  breadcrumbs: string[]
  isSidebarCollapsed: boolean
  title: string
}>()

const emit = defineEmits<{
  toggleSidebar: []
}>()

defineSlots<{
  actions?(): unknown
}>()

const breadcrumbItems = computed(() => props.breadcrumbs.filter(Boolean))
</script>

<template>
  <header
    class="grid min-h-16 grid-cols-[minmax(0,1fr)_auto] items-center gap-4 border-b border-slate-200 bg-white px-4 py-2.5 transition-[background-color,border-color] duration-200 md:px-6 dark:border-slate-800 dark:bg-slate-900"
    aria-label="Workspace header"
  >
    <div class="flex min-w-0 items-center gap-3" aria-label="Context navigation">
      <button
        class="grid size-10 shrink-0 cursor-pointer place-items-center rounded-xl border border-transparent bg-transparent text-slate-600 outline-none transition-[background-color,border-color,color,transform,box-shadow] duration-150 ease-out hover:border-blue-200 hover:bg-blue-50 hover:text-blue-700 focus-visible:border-blue-300 focus-visible:ring-4 focus-visible:ring-blue-100 active:scale-[0.96] motion-reduce:transition-none max-md:hidden dark:text-slate-300 dark:hover:border-blue-400/20 dark:hover:bg-blue-400/10 dark:hover:text-blue-200 dark:focus-visible:border-blue-400/40 dark:focus-visible:ring-blue-950"
        type="button"
        :aria-label="isSidebarCollapsed ? 'Expand sidebar' : 'Collapse sidebar'"
        :title="isSidebarCollapsed ? 'Expand sidebar' : 'Collapse sidebar'"
        :aria-pressed="isSidebarCollapsed"
        @click="emit('toggleSidebar')"
      >
        <SquareChevronRight
          v-if="isSidebarCollapsed"
          :size="16"
          :stroke-width="2.1"
          aria-hidden="true"
        />
        <SquareChevronLeft v-else :size="16" :stroke-width="2.1" aria-hidden="true" />
      </button>

      <div class="min-w-0">
        <nav
          class="flex min-w-0 items-center gap-1.5 overflow-hidden text-xs leading-none font-semibold whitespace-nowrap text-slate-600 dark:text-slate-400"
          aria-label="Breadcrumb"
        >
          <span
            v-for="(item, index) in breadcrumbItems"
            :key="item"
            class="inline-flex min-w-0 items-center gap-1.5 first:overflow-hidden first:text-ellipsis"
            :class="
              index === breadcrumbItems.length - 1 ? 'text-slate-800 dark:text-slate-200' : ''
            "
            :aria-current="index === breadcrumbItems.length - 1 ? 'page' : undefined"
          >
            <span v-if="index > 0" class="text-slate-300 dark:text-slate-600" aria-hidden="true"
              >/</span
            >
            {{ item }}
          </span>
        </nav>
        <h1
          id="dashboard-title"
          class="mt-1 overflow-hidden text-lg leading-tight font-semibold text-balance text-ellipsis whitespace-nowrap text-slate-900 dark:text-slate-50"
        >
          {{ title }}
        </h1>
      </div>
    </div>

    <div class="flex min-w-0 items-center justify-end gap-2" aria-label="Global actions">
      <slot name="actions" />
      <DashboardAccountMenu />
      <button
        class="grid size-10 shrink-0 cursor-pointer place-items-center rounded-xl border border-transparent bg-transparent text-slate-600 outline-none transition-[background-color,border-color,color,transform,box-shadow] duration-150 ease-out hover:border-blue-200 hover:bg-blue-50 hover:text-blue-700 focus-visible:border-blue-300 focus-visible:ring-4 focus-visible:ring-blue-100 active:scale-[0.96] motion-reduce:transition-none max-[720px]:hidden dark:text-slate-300 dark:hover:border-blue-400/20 dark:hover:bg-blue-400/10 dark:hover:text-blue-200 dark:focus-visible:border-blue-400/40 dark:focus-visible:ring-blue-950"
        type="button"
        aria-label="Favorite page"
        title="Favorite page"
      >
        <Star :size="15" :stroke-width="2.1" aria-hidden="true" />
      </button>
      <button
        class="grid size-10 shrink-0 cursor-pointer place-items-center rounded-xl border border-transparent bg-transparent text-slate-600 outline-none transition-[background-color,border-color,color,transform,box-shadow] duration-150 ease-out hover:border-blue-200 hover:bg-blue-50 hover:text-blue-700 focus-visible:border-blue-300 focus-visible:ring-4 focus-visible:ring-blue-100 active:scale-[0.96] motion-reduce:transition-none max-[720px]:hidden dark:text-slate-300 dark:hover:border-blue-400/20 dark:hover:bg-blue-400/10 dark:hover:text-blue-200 dark:focus-visible:border-blue-400/40 dark:focus-visible:ring-blue-950"
        type="button"
        aria-label="Share page"
        title="Share page"
      >
        <Share2 :size="15" :stroke-width="2.1" aria-hidden="true" />
      </button>
      <button
        class="grid size-10 shrink-0 cursor-pointer place-items-center rounded-xl border border-transparent bg-transparent text-slate-600 outline-none transition-[background-color,border-color,color,transform,box-shadow] duration-150 ease-out hover:border-blue-200 hover:bg-blue-50 hover:text-blue-700 focus-visible:border-blue-300 focus-visible:ring-4 focus-visible:ring-blue-100 active:scale-[0.96] motion-reduce:transition-none dark:text-slate-300 dark:hover:border-blue-400/20 dark:hover:bg-blue-400/10 dark:hover:text-blue-200 dark:focus-visible:border-blue-400/40 dark:focus-visible:ring-blue-950"
        type="button"
        aria-label="Open notifications"
        title="Open notifications"
      >
        <Bell :size="15" :stroke-width="2.1" aria-hidden="true" />
      </button>
    </div>
  </header>
</template>
