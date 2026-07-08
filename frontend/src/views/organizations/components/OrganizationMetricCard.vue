<script setup lang="ts">
import type { Component } from 'vue'

defineProps<{
  icon: Component
  iconClass: string
  progressClass: string
  title: string
  value: number
}>()
</script>

<template>
  <article
    class="rounded-xl border border-slate-200/70 bg-white p-4 text-slate-950 dark:border-slate-800 dark:bg-slate-900 dark:text-slate-50"
  >
    <div class="flex items-start justify-between gap-4">
      <div class="min-w-0">
        <p class="truncate text-sm leading-5 font-semibold text-slate-600 dark:text-slate-400">
          {{ title }}
        </p>
        <p
          class="mt-2 text-2xl leading-none font-semibold tabular-nums text-slate-950 dark:text-slate-50"
        >
          {{ value }}%
        </p>
      </div>

      <span
        class="grid size-10 shrink-0 place-items-center rounded-xl border"
        :class="iconClass"
        aria-hidden="true"
      >
        <component :is="icon" class="size-5" :stroke-width="2.1" />
      </span>
    </div>

    <div class="mt-5 flex items-center gap-3">
      <div
        class="h-2 min-w-0 flex-1 overflow-hidden rounded-full bg-slate-100 dark:bg-slate-800"
        role="progressbar"
        :aria-label="title"
        :aria-valuenow="value"
        aria-valuemin="0"
        aria-valuemax="100"
      >
        <div
          class="h-full rounded-full transition-[width] duration-300 ease-out motion-reduce:transition-none"
          :class="progressClass"
          :style="{ width: `${value}%` }"
        ></div>
      </div>
      <span
        class="w-10 text-right text-xs leading-none font-semibold tabular-nums text-slate-500 dark:text-slate-400"
      >
        {{ value }}%
      </span>
    </div>
  </article>
</template>
