<script setup lang="ts">
import type { Component } from 'vue'
import { Blend, ChevronRight, FolderClosed, FolderOpen } from '@lucide/vue'
import type { RouteLocationRaw } from 'vue-router'

type SidebarItem = {
  icon: Component
  isActive?: boolean
  label: string
  to: RouteLocationRaw
}

defineProps<{
  favoriteItems: SidebarItem[]
  enableFloatingTips?: boolean
  isCollapsed: boolean
  isFavoritesOpen: boolean
  items: SidebarItem[]
  workspaceName: string
}>()

const emit = defineEmits<{
  toggleFavorites: []
}>()
</script>

<template>
  <aside
    class="grid min-h-screen min-w-0 grid-rows-[auto_auto_1fr_auto] gap-5 overflow-hidden border-r border-slate-200 bg-white px-3 py-4 text-slate-900 transition-[background-color,border-color,color] duration-200 max-lg:items-center max-lg:px-2 max-md:hidden dark:border-slate-800 dark:bg-slate-900 dark:text-slate-100"
    :class="{ 'items-center px-2': isCollapsed }"
    aria-label="Application navigation"
  >
    <RouterLink
      class="group relative flex min-h-11 items-center overflow-hidden rounded-xl text-slate-900 no-underline outline-none transition-[background-color,border-color,color,transform,box-shadow] duration-150 ease-out focus-visible:ring-4 focus-visible:ring-blue-100 max-lg:justify-center max-lg:gap-0 motion-reduce:transition-none dark:text-slate-100 dark:focus-visible:ring-blue-950"
      :class="isCollapsed ? 'justify-center gap-0' : 'gap-2.5'"
      :to="{ name: 'home' }"
      aria-label="Blendes Flow home"
    >
      <span
        class="grid size-10 shrink-0 place-items-center rounded-xl border border-blue-100 bg-blue-50 text-blue-700 shadow-sm dark:border-blue-400/20 dark:bg-blue-400/10 dark:text-blue-300"
      >
        <Blend :size="22" :stroke-width="2.4" aria-hidden="true" />
      </span>

      <span
        class="min-w-0 overflow-hidden text-sm leading-none font-semibold whitespace-nowrap transition-[max-width,opacity,transform] duration-150 ease-out motion-reduce:transition-none max-lg:max-w-0 max-lg:-translate-x-1 max-lg:opacity-0"
        :class="
          isCollapsed ? 'max-w-0 -translate-x-1 opacity-0' : 'max-w-32 translate-x-0 opacity-100'
        "
        :aria-hidden="isCollapsed"
      >
        Blendes Flow
      </span>

      <span
        v-if="isCollapsed && enableFloatingTips"
        class="pointer-events-none absolute top-1/2 left-[calc(100%+10px)] z-50 -translate-y-1/2 rounded-lg border border-slate-200 bg-white px-2 py-1 text-xs leading-none font-semibold whitespace-nowrap text-slate-700 opacity-0 shadow-sm transition-opacity duration-150 group-hover:opacity-100 group-focus-visible:opacity-100 motion-reduce:transition-none dark:border-slate-700 dark:bg-slate-900 dark:text-slate-200"
        role="tooltip"
      >
        Blendes Flow
      </span>
    </RouterLink>

    <div class="grid min-h-0 content-start gap-5">
      <section class="grid gap-2" aria-labelledby="sidebar-actions-title">
        <small
          id="sidebar-actions-title"
          class="px-2 text-[0.68rem] font-semibold tracking-[0.08em] text-slate-400 uppercase dark:text-slate-500"
          :class="{ hidden: isCollapsed }"
        >
          Actions
        </small>

        <nav class="grid content-start gap-1.5" aria-label="Workspace sections">
          <RouterLink
            v-for="item in items"
            :key="item.label"
            class="group relative flex min-h-11 items-center gap-2 rounded-xl border border-transparent bg-transparent px-3 text-sm font-medium text-slate-600 no-underline outline-none transition-[background-color,border-color,color,transform,box-shadow] duration-150 ease-out hover:border-blue-200 hover:bg-blue-50 hover:text-blue-700 focus-visible:border-blue-300 focus-visible:ring-4 focus-visible:ring-blue-100 active:scale-[0.96] motion-reduce:transition-none max-lg:w-12 max-lg:justify-center max-lg:px-0 dark:text-slate-300 dark:hover:border-blue-400/20 dark:hover:bg-blue-400/10 dark:hover:text-blue-200 dark:focus-visible:border-blue-400/40 dark:focus-visible:ring-blue-950"
            :class="[
              item.isActive
                ? 'border-blue-200 bg-blue-50 text-blue-700 dark:border-blue-400/30 dark:bg-blue-400/10 dark:text-blue-200'
                : '',
              isCollapsed ? 'w-12 justify-center px-0' : '',
            ]"
            :to="item.to"
          >
            <component :is="item.icon" :size="18" :stroke-width="2.15" aria-hidden="true" />

            <span class="max-lg:hidden" :class="{ hidden: isCollapsed }">
              {{ item.label }}
            </span>

            <span
              v-if="isCollapsed && enableFloatingTips"
              class="pointer-events-none absolute top-1/2 left-[calc(100%+10px)] z-50 -translate-y-1/2 rounded-lg border border-slate-200 bg-white px-2 py-1 text-xs leading-none font-semibold whitespace-nowrap text-slate-700 opacity-0 shadow-sm transition-opacity duration-150 group-hover:opacity-100 group-focus-visible:opacity-100 motion-reduce:transition-none dark:border-slate-700 dark:bg-slate-900 dark:text-slate-200"
              role="tooltip"
            >
              {{ item.label }}
            </span>
          </RouterLink>
        </nav>
      </section>

      <section class="grid gap-1.5" aria-label="Favorites folder">
        <button
          class="group relative flex min-h-11 cursor-pointer items-center gap-2 rounded-xl border border-transparent bg-transparent px-3 text-sm font-medium text-slate-600 outline-none transition-[background-color,border-color,color,transform,box-shadow] duration-150 ease-out hover:border-blue-200 hover:bg-blue-50 hover:text-blue-700 focus-visible:border-blue-300 focus-visible:ring-4 focus-visible:ring-blue-100 active:scale-[0.96] motion-reduce:transition-none max-lg:w-12 max-lg:justify-center max-lg:px-0 dark:text-slate-300 dark:hover:border-blue-400/20 dark:hover:bg-blue-400/10 dark:hover:text-blue-200 dark:focus-visible:border-blue-400/40 dark:focus-visible:ring-blue-950"
          :class="isCollapsed ? 'w-12 justify-center px-0' : 'w-full justify-start'"
          type="button"
          :aria-expanded="isFavoritesOpen"
          aria-controls="sidebar-favorites-list"
          :aria-label="isFavoritesOpen ? 'Close favorites folder' : 'Open favorites folder'"
          @click="emit('toggleFavorites')"
        >
          <FolderOpen v-if="isFavoritesOpen" :size="18" :stroke-width="2.15" aria-hidden="true" />
          <FolderClosed v-else :size="18" :stroke-width="2.15" aria-hidden="true" />

          <span class="max-lg:hidden" :class="{ hidden: isCollapsed }">Favorites</span>

          <ChevronRight
            :size="15"
            :stroke-width="2.3"
            class="ml-auto text-slate-400 transition-transform duration-150 ease-out motion-reduce:transition-none max-lg:hidden dark:text-slate-500"
            :class="[isFavoritesOpen ? 'rotate-90' : '', { hidden: isCollapsed }]"
            aria-hidden="true"
          />

          <span
            v-if="isCollapsed && enableFloatingTips"
            class="pointer-events-none absolute top-1/2 left-[calc(100%+10px)] z-50 -translate-y-1/2 rounded-lg border border-slate-200 bg-white px-2 py-1 text-xs leading-none font-semibold whitespace-nowrap text-slate-700 opacity-0 shadow-sm transition-opacity duration-150 group-hover:opacity-100 group-focus-visible:opacity-100 motion-reduce:transition-none dark:border-slate-700 dark:bg-slate-900 dark:text-slate-200"
            role="tooltip"
          >
            Favorites
          </span>
        </button>

        <Transition
          enter-active-class="transition duration-150 ease-out motion-reduce:transition-none"
          enter-from-class="-translate-y-1 opacity-0"
          enter-to-class="translate-y-0 opacity-100"
          leave-active-class="transition duration-100 ease-in motion-reduce:transition-none"
          leave-from-class="translate-y-0 opacity-100"
          leave-to-class="-translate-y-1 opacity-0"
        >
          <nav
            v-if="isFavoritesOpen"
            id="sidebar-favorites-list"
            class="grid content-start gap-1"
            :class="isCollapsed ? '' : 'ml-3 border-l border-slate-200 pl-2 dark:border-slate-700'"
            aria-label="Favorite sections"
          >
            <RouterLink
              v-for="item in favoriteItems"
              :key="item.label"
              class="group relative flex min-h-10 items-center gap-2 rounded-lg border border-transparent bg-transparent px-2 text-[0.8rem] font-medium text-slate-600 no-underline outline-none transition-[background-color,border-color,color,transform,box-shadow] duration-150 ease-out hover:border-blue-200 hover:bg-blue-50 hover:text-blue-700 focus-visible:border-blue-300 focus-visible:ring-4 focus-visible:ring-blue-100 active:scale-[0.96] motion-reduce:transition-none max-lg:w-12 max-lg:justify-center max-lg:px-0 dark:text-slate-300 dark:hover:border-blue-400/20 dark:hover:bg-blue-400/10 dark:hover:text-blue-200 dark:focus-visible:border-blue-400/40 dark:focus-visible:ring-blue-950"
              :class="[
                item.isActive
                  ? 'border-blue-200 bg-blue-50 text-blue-700 dark:border-blue-400/30 dark:bg-blue-400/10 dark:text-blue-200'
                  : '',
                isCollapsed ? 'w-12 justify-center px-0' : '',
              ]"
              :to="item.to"
            >
              <component :is="item.icon" :size="15" :stroke-width="2.15" aria-hidden="true" />

              <span class="max-lg:hidden" :class="{ hidden: isCollapsed }">
                {{ item.label }}
              </span>

              <span
                v-if="isCollapsed && enableFloatingTips"
                class="pointer-events-none absolute top-1/2 left-[calc(100%+10px)] z-50 -translate-y-1/2 rounded-lg border border-slate-200 bg-white px-2 py-1 text-xs leading-none font-semibold whitespace-nowrap text-slate-700 opacity-0 shadow-sm transition-opacity duration-150 group-hover:opacity-100 group-focus-visible:opacity-100 motion-reduce:transition-none dark:border-slate-700 dark:bg-slate-900 dark:text-slate-200"
                role="tooltip"
              >
                {{ item.label }}
              </span>
            </RouterLink>
          </nav>
        </Transition>
      </section>
    </div>
  </aside>
</template>
