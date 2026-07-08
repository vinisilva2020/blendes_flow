<script setup lang="ts">
import type { LucideIcon } from '@lucide/vue'

import CounterInfoCard from './CounterInfoCard.vue'

type CountInfoCard = {
  description: string
  icon: LucideIcon
  label: string
  toneClass: string
  value: number
}

withDefaults(
  defineProps<{
    ariaLabel?: string
    cards: CountInfoCard[]
  }>(),
  {
    ariaLabel: 'Summary indicators',
  },
)
</script>

<template>
  <section class="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-4" :aria-label="ariaLabel">
    <CounterInfoCard
      v-for="card in cards"
      :key="card.label"
      :description="card.description"
      :icon="card.icon"
      :label="card.label"
      :tone-class="card.toneClass"
      :value="card.value"
    />
  </section>
</template>
