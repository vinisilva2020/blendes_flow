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
  const backgroundAlpha = 0.14 + intensity * 0.48
  const borderAlpha = 0.08 + intensity * 0.18
  const textColor = intensity > 0.76 ? 'rgb(255 255 255)' : 'rgb(30 64 175)'

  return {
    backgroundColor: `rgb(37 99 235 / ${backgroundAlpha.toFixed(2)})`,
    borderColor: `rgb(37 99 235 / ${borderAlpha.toFixed(2)})`,
    color: textColor,
  }
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
                :title="`${row.facet} / ${layer.description}: ${row.values[layer.key]} risks`"
              >
                {{ row.values[layer.key] }}
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>
