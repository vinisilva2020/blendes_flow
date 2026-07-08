<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, shallowRef, watch } from 'vue'
import { ArcElement, Chart, DoughnutController, Tooltip, type ChartConfiguration } from 'chart.js'

type ChangeSignalKey = 'progress' | 'partialProgress' | 'noProgress' | 'regression'

type ChangeSignalDatum = {
  description: string
  key: ChangeSignalKey
  label: string
  value: number
}

const props = defineProps<{
  signals: readonly ChangeSignalDatum[]
}>()

Chart.register(DoughnutController, ArcElement, Tooltip)

const chartCanvas = shallowRef<HTMLCanvasElement | null>(null)
const chart = shallowRef<Chart<'doughnut'> | null>(null)

const signalColors: Record<ChangeSignalKey, string> = {
  progress: '#16a34a',
  partialProgress: '#f59e0b',
  noProgress: '#94a3b8',
  regression: '#dc2626',
}

const signalSoftColors: Record<ChangeSignalKey, string> = {
  progress: '#dcfce7',
  partialProgress: '#fef3c7',
  noProgress: '#f1f5f9',
  regression: '#fee2e2',
}

const totalSignals = computed(() =>
  props.signals.reduce((total, signal) => total + Math.max(0, signal.value), 0),
)

const dominantSignal = computed(() => {
  if (totalSignals.value === 0) {
    return null
  }

  return [...props.signals].sort((first, second) => second.value - first.value)[0]
})

const chartData = computed(() => ({
  backgroundColor: props.signals.map((signal) => signalColors[signal.key]),
  data: props.signals.map((signal) => Math.max(0, signal.value)),
  labels: props.signals.map((signal) => signal.label),
}))

const visibleSignals = computed(() =>
  props.signals.map((signal) => ({
    ...signal,
    color: signalColors[signal.key],
    percent: totalSignals.value === 0 ? 0 : Math.round((signal.value / totalSignals.value) * 100),
    softColor: signalSoftColors[signal.key],
  })),
)

function getChartConfig(): ChartConfiguration<'doughnut'> {
  return {
    data: {
      datasets: [
        {
          backgroundColor: chartData.value.backgroundColor,
          borderColor: '#ffffff',
          borderRadius: 6,
          borderWidth: 3,
          data: chartData.value.data,
          hoverBorderWidth: 3,
          hoverOffset: 8,
          spacing: 2,
        },
      ],
      labels: chartData.value.labels,
    },
    options: {
      animation: {
        duration: window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 0 : 650,
        easing: 'easeOutQuart',
      },
      cutout: '68%',
      maintainAspectRatio: false,
      plugins: {
        tooltip: {
          backgroundColor: '#0f172a',
          bodyColor: '#f8fafc',
          borderColor: '#1e293b',
          borderWidth: 1,
          callbacks: {
            label(context) {
              const value = Number(context.raw ?? 0)
              const percentage =
                totalSignals.value === 0 ? 0 : Math.round((value / totalSignals.value) * 100)

              return ` ${context.label}: ${value} signals (${percentage}%)`
            },
          },
          displayColors: true,
          padding: 12,
          titleColor: '#cbd5e1',
        },
      },
      responsive: true,
    },
    type: 'doughnut',
  }
}

function renderChart() {
  if (!chartCanvas.value || totalSignals.value === 0) {
    return
  }

  chart.value?.destroy()
  chart.value = new Chart(chartCanvas.value, getChartConfig())
}

watch(
  () => props.signals,
  () => {
    if (!chart.value) {
      renderChart()
      return
    }

    chart.value.data.labels = chartData.value.labels
    const [dataset] = chart.value.data.datasets

    if (!dataset) {
      renderChart()
      return
    }

    dataset.data = chartData.value.data
    dataset.backgroundColor = chartData.value.backgroundColor
    chart.value.update()
  },
  { deep: true },
)

onMounted(renderChart)

onBeforeUnmount(() => {
  chart.value?.destroy()
})
</script>

<template>
  <div class="grid gap-5 md:grid-cols-[minmax(180px,0.82fr)_minmax(0,1fr)] md:items-center">
    <div
      class="relative mx-auto aspect-square w-full max-w-[240px]"
      role="img"
      :aria-label="`Doughnut chart showing ${totalSignals} change signals across progress, partial progress, no progress, and regression.`"
    >
      <canvas
        v-if="totalSignals > 0"
        ref="chartCanvas"
        class="h-full w-full"
        aria-hidden="true"
      ></canvas>

      <div
        v-else
        class="grid h-full w-full place-items-center rounded-full border border-dashed border-slate-300 bg-slate-50 text-center"
      >
        <p class="max-w-28 text-xs leading-5 font-medium text-slate-500">No signals recorded</p>
      </div>

      <div class="pointer-events-none absolute inset-0 grid place-items-center">
        <div class="text-center">
          <p
            class="text-3xl leading-none font-semibold tracking-normal text-slate-950 tabular-nums"
          >
            {{ totalSignals }}
          </p>
          <p
            class="mt-1 text-[0.66rem] leading-none font-semibold tracking-[0.14em] text-slate-400 uppercase"
          >
            Signals
          </p>
        </div>
      </div>
    </div>

    <div class="min-w-0">
      <div
        v-if="dominantSignal"
        class="mb-4 rounded-lg border border-slate-200 bg-slate-50 px-3 py-2.5"
      >
        <p
          class="text-[0.68rem] leading-none font-semibold tracking-[0.12em] text-slate-400 uppercase"
        >
          Leading condition
        </p>
        <p class="mt-1.5 text-sm leading-5 font-semibold text-slate-950">
          {{ dominantSignal.label }}
        </p>
        <p class="mt-1 text-xs leading-5 text-slate-500">
          {{ dominantSignal.description }}
        </p>
      </div>

      <ul class="grid gap-2" aria-label="Change signal breakdown">
        <li
          v-for="signal in visibleSignals"
          :key="signal.key"
          class="grid grid-cols-[auto_minmax(0,1fr)_auto] items-center gap-3 rounded-lg border border-slate-200/70 px-3 py-2 transition-colors hover:border-slate-300 hover:bg-slate-50"
        >
          <span
            class="size-2.5 rounded-full ring-4"
            :style="{ backgroundColor: signal.color, '--tw-ring-color': signal.softColor }"
            aria-hidden="true"
          ></span>

          <span class="min-w-0">
            <span class="block truncate text-sm leading-5 font-medium text-slate-900">
              {{ signal.label }}
            </span>
            <span class="block truncate text-xs leading-4 text-slate-500">
              {{ signal.description }}
            </span>
          </span>

          <span class="text-right">
            <span class="block text-sm leading-5 font-semibold text-slate-950 tabular-nums">
              {{ signal.value }}
            </span>
            <span class="block text-[0.68rem] leading-4 font-medium text-slate-400 tabular-nums">
              {{ signal.percent }}%
            </span>
          </span>
        </li>
      </ul>
    </div>
  </div>
</template>
