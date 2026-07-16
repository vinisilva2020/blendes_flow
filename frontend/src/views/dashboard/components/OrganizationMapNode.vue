<script setup lang="ts">
import { Building2, CircleDot, Network } from '@lucide/vue'

import type { OrganizationNode } from './organization-map'

defineOptions({ name: 'OrganizationMapNode' })

defineProps<{
  node: OrganizationNode
  compact?: boolean
}>()

const kindLabels = {
  organization: 'Organization',
  department: 'Department',
  operation: 'Operation',
} as const

const kindIcons = {
  organization: Building2,
  department: Network,
  operation: CircleDot,
}
</script>

<template>
  <li class="relative flex flex-col items-center">
    <article
      class="relative z-10 flex min-w-0 items-center gap-3 rounded-xl bg-white px-3 py-2.5 text-left shadow-[0_1px_2px_rgb(15_23_42_/_0.06),0_8px_22px_rgb(15_23_42_/_0.07)] ring-1 ring-slate-950/6 dark:bg-slate-900 dark:shadow-[0_8px_24px_rgb(0_0_0_/_24%)] dark:ring-white/10"
      :class="compact ? 'w-[184px]' : 'w-[210px] sm:w-[226px]'"
    >
      <span
        class="grid size-9 shrink-0 place-items-center rounded-lg"
        :class="{
          'bg-blue-700 text-white': node.kind === 'organization',
          'bg-cyan-50 text-cyan-700 dark:bg-cyan-400/10 dark:text-cyan-300':
            node.kind === 'department',
          'bg-violet-50 text-violet-700 dark:bg-violet-400/10 dark:text-violet-300':
            node.kind === 'operation',
        }"
      >
        <component :is="kindIcons[node.kind]" :size="16" :stroke-width="2.1" aria-hidden="true" />
      </span>
      <span class="min-w-0">
        <span
          class="block text-[10px] leading-4 font-bold tracking-[0.09em] text-slate-400 uppercase dark:text-slate-500"
        >
          {{ kindLabels[node.kind] }}
        </span>
        <strong
          class="block truncate text-sm leading-5 font-semibold text-slate-900 dark:text-slate-50"
        >
          {{ node.name }}
        </strong>
        <span
          v-if="node.owner && !compact"
          class="block truncate text-xs leading-4 text-slate-500 dark:text-slate-400"
        >
          {{ node.owner }}
        </span>
      </span>
    </article>

    <template v-if="node.children?.length">
      <span class="h-6 w-px bg-slate-300 dark:bg-slate-700" aria-hidden="true"></span>
      <ul
        class="relative flex w-max gap-5 px-2 before:absolute before:top-0 before:right-[calc(113px+0.5rem)] before:left-[calc(113px+0.5rem)] before:h-px before:bg-slate-300 dark:before:bg-slate-700"
      >
        <OrganizationMapNode
          v-for="child in node.children"
          :key="child.id"
          :node="child"
          :compact="compact"
        />
      </ul>
    </template>
  </li>
</template>
