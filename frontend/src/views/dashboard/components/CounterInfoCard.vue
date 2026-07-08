<script setup lang="ts">
import { MoreVertical, type LucideIcon } from '@lucide/vue'

defineProps<{
  description: string
  icon: LucideIcon
  label: string
  toneClass: string
  value: number
}>()
</script>

<template>
  <article
    class="group flex items-center justify-between gap-4 rounded-2xl border border-white/80 bg-white px-5 py-5 text-slate-950 shadow-[0_18px_45px_rgb(15_23_42_/_0.06)] ring-1 ring-slate-950/[0.03] transition duration-200 ease-out"
  >
    <div class="flex min-w-0 items-center gap-4">
      <div
        class="grid size-11 shrink-0 place-items-center rounded-full border shadow-[inset_0_1px_0_rgb(255_255_255_/_0.72)]"
        :class="toneClass"
        aria-hidden="true"
      >
        <component :is="icon" class="size-5" :stroke-width="2.1" />
      </div>

      <div class="min-w-0">
        <h2 class="truncate text-sm leading-6 font-semibold tracking-normal text-slate-950">
          <span class="tabular-nums">{{ value }}</span>
          {{ label }}
        </h2>
        <p class="mt-0.5 truncate text-sm leading-5 font-medium text-slate-500">
          {{ description }}
        </p>
      </div>
    </div>
  </article>
</template>
