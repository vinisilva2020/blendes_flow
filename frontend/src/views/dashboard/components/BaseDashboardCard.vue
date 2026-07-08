<script setup lang="ts">
import { useId, type Component } from 'vue'

defineProps<{
  icon: Component
  title: string
}>()

defineSlots<{
  actions?(): unknown
  default(): unknown
}>()

const titleId = useId()
</script>

<template>
  <article
    class="overflow-hidden rounded-xl border border-slate-200/70 bg-white px-4 py-4 text-slate-950 transition-[background-color,border-color,color] duration-200 dark:border-slate-800 dark:bg-slate-900 dark:text-slate-50"
    :aria-labelledby="titleId"
  >
    <header class="flex items-center justify-between gap-4">
      <div class="flex min-w-0 items-center gap-3">
        <component
          :is="icon"
          class="size-5 shrink-0 text-slate-500 dark:text-slate-400"
          :stroke-width="2.15"
          aria-hidden="true"
        />
        <h2
          :id="titleId"
          class="truncate text-base leading-none font-semibold text-slate-950 dark:text-slate-50"
        >
          {{ title }}
        </h2>
      </div>

      <slot name="actions" />
    </header>

    <div class="mt-4 h-px bg-slate-200/70 dark:bg-slate-800" aria-hidden="true"></div>

    <div class="mt-5">
      <slot />
    </div>
  </article>
</template>
