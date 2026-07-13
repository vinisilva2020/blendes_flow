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
      backgroundColor: 'rgb(248 250 252)',
      borderColor: 'rgb(241 245 249)',
      color: 'rgb(148 163 184)',
    }
  }

  const intensity = value / maxValue.value

  let backgroundColor = ''

  if (intensity <= 0.33) {
    backgroundColor = 'rgb(34 197 94)' // verde
  } else if (intensity <= 0.66) {
    backgroundColor = 'rgb(234 179 8)' // amarelo
  } else {
    backgroundColor = 'rgb(239 68 68)' // vermelho
  }

  return {
    backgroundColor,
    borderColor: backgroundColor,
    color: intensity > 0.66 ? 'white' : 'black',
  }
}

function getIntensityLabel(value: number) {
  if (maxValue.value === 0) {
    return 'No risk'
  }

  const intensity = value / maxValue.value

  if (intensity <= 0.33) {
    return 'Low'
  }

  if (intensity <= 0.66) {
    return 'Medium'
  }

  return 'High'
}

</script>

<template>
  <div>
    <div class="overflow-x-auto">
      <table
        class="w-full min-w-[340px] border-separate border-spacing-1.5"
        aria-label="Facet risk heat map"
      >
        <caption class="sr-only">
          Heat map showing the number of risks for each facet and action layer.
        </caption>
        <thead>
          <tr>
            <th
              scope="col"
              class="w-16 px-1.5 py-1 text-left text-[0.65rem] leading-none font-semibold text-slate-400"
            >
              Facet
            </th>
            <th
              v-for="layer in layers"
              :key="layer.key"
              scope="col"
              class="px-1.5 py-1 text-center"
            >
              <span class="block text-[0.68rem] leading-none font-semibold text-slate-900">
                {{ layer.key }}
              </span>
              <span class="mt-0.5 block text-[0.6rem] leading-none font-medium text-slate-400">
                {{ layer.label }}
              </span>
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="row in rows" :key="row.facet">
            <th
              scope="row"
              class="px-2 py-1 text-left text-[0.68rem] font-semibold tracking-normal text-slate-900"
            >
              {{ row.facet }}
            </th>
            <td v-for="layer in layers" :key="layer.key" class="p-0">
              <div
                class="mx-auto grid size-10 place-items-center rounded-md border text-[0.68rem] font-medium tabular-nums shadow-[inset_0_1px_0_rgb(255_255_255_/_0.35)]"
                :style="getCellStyle(row.values[layer.key])"
                :aria-label="`${row.values[layer.key]} risks in ${row.facet} for ${layer.description}`"
                :title="`Facet: ${row.facet}
Layer: ${layer.description}
Value: ${row.values[layer.key]} risks
Intensity: ${getIntensityLabel(row.values[layer.key])}`"
              >
                {{ row.values[layer.key] }}
              </div>
            </td>
          </tr>
        </tbody>
           </table>
    </div>

    <div
      class="mt-4 flex flex-wrap items-center gap-4 text-xs text-slate-600"
      aria-label="Risk intensity legend"
    >
      <span class="font-semibold text-slate-900">
        Risk intensity:
      </span>

      <div class="flex items-center gap-1.5">
        <span class="size-3 rounded-sm bg-green-500"></span>
        Low
      </div>

      <div class="flex items-center gap-1.5">
        <span class="size-3 rounded-sm bg-yellow-500"></span>
        Medium
      </div>

      <div class="flex items-center gap-1.5">
        <span class="size-3 rounded-sm bg-red-500"></span>
        High
      </div>
    </div>
  </div>
</template>
