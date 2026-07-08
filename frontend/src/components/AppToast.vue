<script setup lang="ts">
import { computed } from 'vue'
import { AlertCircle, CheckCircle2, X } from '@lucide/vue'

const props = defineProps<{
  message?: string
  tone?: 'success' | 'error'
}>()

const emit = defineEmits<{
  dismiss: []
}>()

const isVisible = computed(() => Boolean(props.message))
const icon = computed(() => (props.tone === 'error' ? AlertCircle : CheckCircle2))
const liveRole = computed(() => (props.tone === 'error' ? 'alert' : 'status'))
const liveMode = computed(() => (props.tone === 'error' ? 'assertive' : 'polite'))
const toneClasses = computed(() =>
  props.tone === 'error'
    ? 'border-rose-100 bg-rose-50 text-rose-800'
    : 'border-emerald-100 bg-emerald-50 text-emerald-800',
)
</script>

<template>
  <Transition
    enter-active-class="transition duration-180 ease-out motion-reduce:transition-none"
    enter-from-class="-translate-y-2 opacity-0"
    enter-to-class="translate-y-0 opacity-100"
    leave-active-class="transition duration-140 ease-in motion-reduce:transition-none"
    leave-from-class="translate-y-0 opacity-100"
    leave-to-class="-translate-y-2 opacity-0"
  >
    <div
      v-if="isVisible"
      class="flex items-start justify-between gap-3 rounded-lg border px-3.5 py-3 text-sm leading-5 font-medium shadow-[0_10px_30px_rgb(15_23_42_/_0.06)]"
      :class="toneClasses"
      :role="liveRole"
      :aria-live="liveMode"
    >
      <span class="flex min-w-0 items-start gap-2">
        <component
          :is="icon"
          class="mt-0.5 size-4 shrink-0"
          :stroke-width="2.2"
          aria-hidden="true"
        />
        <span class="min-w-0">{{ message }}</span>
      </span>

      <button
        class="-my-1 grid size-7 shrink-0 cursor-pointer place-items-center rounded-md outline-none transition-[background-color,box-shadow,transform] duration-150 hover:bg-white/70 focus-visible:ring-4 focus-visible:ring-white/80 active:scale-[0.96] motion-reduce:transition-none"
        type="button"
        aria-label="Dismiss message"
        @click="emit('dismiss')"
      >
        <X :size="14" :stroke-width="2.2" aria-hidden="true" />
      </button>
    </div>
  </Transition>
</template>
