<script setup lang="ts">
import { computed } from 'vue'

type Facet = 'WHY' | 'WHEN' | 'WHO' | 'WITH' | 'WHEREBY' | 'IN' | 'OUT'
type LayerKey = 'OP' | 'TA' | 'ST'

type HeatMapLayer = {
  description: string
  key: LayerKey
  label: string
}

type HeatMapRow = {
  facet: Facet
  values: Record<LayerKey, number>
}

const props = defineProps<{
  layers: readonly HeatMapLayer[]
  rows: readonly HeatMapRow[]
}>()

const maxValue = computed(() =>
  Math.max(0, ...props.rows.flatMap((row) => props.layers.map((layer) => row.values[layer.key]))),
)

function getCellStyle(value: number) {
  if (value === 0 || maxValue.value === 0) {
    return {
      backgroundColor: 'rgb(255 255 255)',
      borderColor: 'rgb(226 232 240)',
      color: 'rgb(148 163 184)',
    }
  }

  const intensity = value / maxValue.value

  let backgroundColor = ''

  if (intensity <= 0.2) {
  backgroundColor = 'rgb(254, 226, 226)' // nível 1 
} else if (intensity <= 0.4) {
  backgroundColor = 'rgb(252, 165, 165)' // nível 2
} else if (intensity <= 0.6) {
  backgroundColor = 'rgb(248, 113, 113)' // nível 3
} else if (intensity <= 0.8) {
  backgroundColor = 'rgb(239, 68, 68)' // nível 4
} else {
  backgroundColor = 'rgb(185, 28, 28)' // nível 5 
}
  return {
  backgroundColor,
  borderColor: 'rgba(255,255,255,0.35)',
  color: intensity > 0.6 ? 'white' : 'rgb(15 23 42)',
}
}

function getIntensityLabel(value: number) {
  if (value === 0 || maxValue.value === 0) {
    return 'No risk'
  }

  const intensity = value / maxValue.value

  if (intensity <= 0.2) {
    return 'Very Low'
  }

  if (intensity <= 0.4) {
    return 'Low'
  }

  if (intensity <= 0.6) {
    return 'Medium'
  }

  if (intensity <= 0.8) {
    return 'High'
  }

  return 'Critical'
}

</script>

<template>
  <div class="w-full">
    <div
      class="grid w-full grid-cols-[120px_repeat(3,minmax(0,1fr))] overflow-hidden rounded-xl border border-slate-300 dark:border-slate-800"
      aria-label="Facet risk heat map"
    >
      <!-- Header -->
      <div
        class="flex items-center border-b border-r border-slate-300 bg-slate-50 px-3 py-2 text-xs font-semibold uppercase tracking-wide text-slate-700 dark:border-slate-800 dark:bg-slate-950 dark:text-slate-300"
      >
        Facet
      </div>

      <div
        v-for="layer in layers"
        :key="layer.key"
        class="flex items-center justify-center border-b border-r border-slate-300 bg-slate-50 px-3 py-3 text-center dark:border-slate-800 dark:bg-slate-950"
      >
        <span
          class="text-xs font-semibold uppercase tracking-wide text-slate-700 dark:text-slate-300"
        >
          {{ layer.label }}
        </span>
      </div>


      <!-- Body -->
      <template v-for="row in rows" :key="row.facet">

        <!-- Facet name -->
        <div
          class="flex items-center border-b border-r border-slate-300 px-4 py-3 text-sm font-semibold tracking-wide text-slate-700 dark:border-slate-800 dark:text-slate-300"
        >
          {{ row.facet }}
        </div>


        <!-- Risk cells -->
        <!-- Risk cells -->
<div
  v-for="layer in layers"
  :key="layer.key"
  class="border-b border-r border-slate-300 dark:border-slate-800"
>
  <div
    class="grid min-h-14 w-full place-items-center rounded-xl border shadow-sm transition-all duration-200 hover:z-10 hover:scale-[1.02] hover:shadow-md"
    :style="{
      ...getCellStyle(row.values[layer.key]),
      boxShadow: 'inset 0 1px 0 rgba(255,255,255,0.18)'
    }"
    :aria-label="`${row.values[layer.key]} risks in ${row.facet} for ${layer.description}`"
    :title="`Facet: ${row.facet}
Layer: ${layer.description}
Value: ${row.values[layer.key]} risks
Intensity: ${getIntensityLabel(row.values[layer.key])}`"
  >
    {{ row.values[layer.key] === 0 ? '—' : row.values[layer.key] }}
  </div>
</div>

      </template>
    </div>


    <!-- Legend -->
    <div
  class="mt-5 flex flex-wrap items-center justify-center gap-8 text-sm"
  aria-label="Risk intensity legend"
>
  <span class="font-medium text-slate-600 dark:text-slate-300">
    Risk intensity:
  </span>

  <div class="flex items-center gap-2">
    <span class="h-3 w-3 rounded-sm border border-slate-200 bg-white"></span>
    <span class="text-slate-700 dark:text-slate-300">
      No risk
    </span>
  </div>

  <div class="flex items-center gap-2">
    <span
      class="h-3 w-3 rounded-sm"
      style="background-color: rgb(254, 226, 226)"
    ></span>
    <span class="text-slate-700 dark:text-slate-300">
      Very Low
    </span>
  </div>

  <div class="flex items-center gap-2">
    <span
      class="h-3 w-3 rounded-sm"
      style="background-color: rgb(252, 165, 165)"
    ></span>
    <span class="text-slate-700 dark:text-slate-300">
      Low
    </span>
  </div>

  <div class="flex items-center gap-2">
    <span
      class="h-3 w-3 rounded-sm"
      style="background-color: rgb(248, 113, 113)"
    ></span>
    <span class="text-slate-700 dark:text-slate-300">
      Medium
    </span>
  </div>

  <div class="flex items-center gap-2">
    <span
      class="h-3 w-3 rounded-sm"
      style="background-color: rgb(239, 68, 68)"
    ></span>
    <span class="text-slate-700 dark:text-slate-300">
      High
    </span>
  </div>

  <div class="flex items-center gap-2">
    <span
      class="h-3 w-3 rounded-sm"
      style="background-color: rgb(185, 28, 28)"
    ></span>
    <span class="text-slate-700 dark:text-slate-300">
      Critical
    </span>
  </div>
</div>
  </div>
</template>
