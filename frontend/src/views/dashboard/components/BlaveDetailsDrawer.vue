<script setup lang="ts">
import { computed, nextTick, ref, watch } from 'vue'
import { ArrowUpRight, Check, Clock3, Lock, RotateCcw, X } from '@lucide/vue'

import { getBlaveMovements, type Blave, type BlaveMovementStatus } from '@/domains/blaves/contracts'

import { movementMeta, movementOrder, movementStatusLabels } from './blaves'

const props = defineProps<{
  blave: Blave | null
  isOpen: boolean
}>()

const emit = defineEmits<{
  close: []
}>()

const closeButton = ref<HTMLButtonElement | null>(null)

const selectedMovement = computed(() =>
  props.blave ? movementMeta[props.blave.current_movement ?? 'BOUNDGROUND'] : null,
)

const movementsByName = computed(
  () =>
    new Map(
      (props.blave ? getBlaveMovements(props.blave) : []).map((movement) => [
        movement.movement,
        movement,
      ]),
    ),
)

const readableStatus = computed(() => {
  if (!props.blave?.status) {
    return 'Draft'
  }

  return props.blave.status
    .toLowerCase()
    .split('_')
    .map((part) => `${part.charAt(0).toUpperCase()}${part.slice(1)}`)
    .join(' ')
})

watch(
  () => props.isOpen,
  async (isOpen) => {
    if (!isOpen) {
      return
    }

    await nextTick()
    closeButton.value?.focus()
  },
)

function formatDate(value?: string | null) {
  if (!value) {
    return 'Not completed'
  }

  return new Intl.DateTimeFormat('en', {
    day: '2-digit',
    month: 'short',
    year: 'numeric',
  }).format(new Date(value))
}

function getStatusIcon(status?: BlaveMovementStatus) {
  if (status === 'COMPLETED') {
    return Check
  }

  if (status === 'ACTIVE') {
    return Clock3
  }

  if (status === 'INVALIDATED') {
    return RotateCcw
  }

  return Lock
}
</script>

<template>
  <Teleport to="body">
    <Transition
      enter-active-class="transition-opacity duration-150 ease-out motion-reduce:transition-none"
      enter-from-class="opacity-0"
      enter-to-class="opacity-100"
      leave-active-class="transition-opacity duration-150 ease-in motion-reduce:transition-none"
      leave-from-class="opacity-100"
      leave-to-class="opacity-0"
    >
      <div
        v-if="isOpen && blave"
        class="fixed inset-0 z-50 bg-slate-950/28 backdrop-blur-[2px]"
        aria-hidden="true"
        @click="emit('close')"
      ></div>
    </Transition>

    <Transition
      enter-active-class="transition-transform duration-200 ease-out motion-reduce:transition-none"
      enter-from-class="translate-x-full"
      enter-to-class="translate-x-0"
      leave-active-class="transition-transform duration-160 ease-in motion-reduce:transition-none"
      leave-from-class="translate-x-0"
      leave-to-class="translate-x-full"
    >
      <aside
        v-if="isOpen && blave && selectedMovement"
        class="fixed inset-y-0 right-0 z-50 grid w-full max-w-[440px] grid-rows-[auto_1fr] overflow-hidden border-l border-slate-200 bg-white text-slate-950 shadow-[0_24px_70px_rgb(15_23_42_/_0.18)] max-sm:max-w-full dark:border-slate-800 dark:bg-slate-900 dark:text-slate-50 dark:shadow-[0_24px_70px_rgb(0_0_0_/_0.34)]"
        role="dialog"
        aria-modal="true"
        :aria-labelledby="`blave-drawer-${blave.id}-title`"
        @keydown.esc="emit('close')"
      >
        <header class="border-b border-slate-200 px-5 py-5 dark:border-slate-800">
          <div class="flex items-start justify-between gap-4">
            <div class="min-w-0">
              <p
                class="text-xs leading-none font-semibold tracking-[0.08em] text-slate-500 uppercase dark:text-slate-400"
              >
                Flow details
              </p>
              <h2
                :id="`blave-drawer-${blave.id}-title`"
                class="mt-2 text-xl leading-7 font-semibold text-slate-950 dark:text-slate-50"
              >
                {{ blave.title }}
              </h2>
            </div>

            <button
              ref="closeButton"
              class="grid size-10 shrink-0 cursor-pointer place-items-center rounded-xl border border-transparent text-slate-500 outline-none transition-[border-color,background-color,color,box-shadow,transform] duration-150 ease-out hover:border-slate-200 hover:bg-slate-50 hover:text-slate-950 focus-visible:border-blue-300 focus-visible:ring-4 focus-visible:ring-blue-100 active:scale-[0.96] motion-reduce:transition-none dark:text-slate-400 dark:hover:border-slate-700 dark:hover:bg-slate-800 dark:hover:text-slate-50 dark:focus-visible:ring-blue-950"
              type="button"
              aria-label="Close details"
              @click="emit('close')"
            >
              <X :size="18" :stroke-width="2.1" aria-hidden="true" />
            </button>
          </div>
        </header>

        <div class="min-h-0 overflow-y-auto px-5 py-5">
          <section aria-labelledby="blave-description-title">
            <div class="flex items-center gap-3">
              <div
                class="grid size-14 shrink-0 place-items-center rounded-lg border text-2xl leading-none font-black"
                :class="selectedMovement.accentClass"
                aria-hidden="true"
              >
                {{ selectedMovement.letter }}
              </div>

              <div class="min-w-0 flex-1">
                <p class="text-xs leading-none font-semibold text-slate-500 dark:text-slate-400">
                  Current movement
                </p>
                <p
                  class="mt-1 truncate text-sm leading-5 font-semibold text-slate-950 dark:text-slate-50"
                >
                  {{ selectedMovement.label }}
                </p>
              </div>

              <RouterLink
                class="inline-flex h-8 shrink-0 cursor-pointer items-center gap-1.5 rounded-md border border-blue-200 bg-blue-50 px-2.5 text-xs leading-none font-semibold text-blue-700 outline-none transition-[border-color,background-color,color,box-shadow,transform] duration-150 ease-out hover:border-blue-300 hover:bg-blue-100 hover:text-blue-800 focus-visible:border-blue-300 focus-visible:ring-4 focus-visible:ring-blue-100 active:scale-[0.97] motion-reduce:transition-none dark:border-blue-400/30 dark:bg-blue-400/10 dark:text-blue-200 dark:hover:border-blue-400/45 dark:hover:bg-blue-400/15 dark:hover:text-blue-100 dark:focus-visible:ring-blue-950"
                :aria-label="`Open canvas for ${blave.title}`"
                :to="{ name: 'canvas', params: { blaveId: blave.id } }"
              >
                <ArrowUpRight :size="14" :stroke-width="2.2" aria-hidden="true" />
                Open Canvas
              </RouterLink>
            </div>

            <h3 id="blave-description-title" class="mt-5 text-sm leading-none font-semibold">
              Description
            </h3>
            <p class="mt-2 text-sm leading-6 text-slate-600 dark:text-slate-400">
              {{ blave.description || selectedMovement.description }}
            </p>
          </section>

          <dl class="mt-6 grid grid-cols-2 gap-3">
            <div
              class="rounded-lg border border-slate-200 bg-slate-50 px-3 py-3 dark:border-slate-800 dark:bg-slate-950"
            >
              <dt class="text-xs leading-none font-semibold text-slate-500 dark:text-slate-400">
                Flow status
              </dt>
              <dd class="mt-1 text-sm leading-5 font-semibold text-slate-950 dark:text-slate-50">
                {{ readableStatus }}
              </dd>
            </div>
            <div
              class="rounded-lg border border-slate-200 bg-slate-50 px-3 py-3 dark:border-slate-800 dark:bg-slate-950"
            >
              <dt class="text-xs leading-none font-semibold text-slate-500 dark:text-slate-400">
                Version
              </dt>
              <dd class="mt-1 text-sm leading-5 font-semibold text-slate-950 dark:text-slate-50">
                v{{ blave.version_number ?? 1 }}
              </dd>
            </div>
            <div
              class="rounded-lg border border-slate-200 bg-slate-50 px-3 py-3 dark:border-slate-800 dark:bg-slate-950"
            >
              <dt class="text-xs leading-none font-semibold text-slate-500 dark:text-slate-400">
                Updated
              </dt>
              <dd class="mt-1 text-sm leading-5 font-semibold text-slate-950 dark:text-slate-50">
                {{ formatDate(blave.updated_at) }}
              </dd>
            </div>
          </dl>

          <section class="mt-7" aria-labelledby="movement-timeline-title">
            <h3 id="movement-timeline-title" class="text-sm leading-none font-semibold">
              BlendES path
            </h3>

            <ol class="mt-4 space-y-3">
              <li
                v-for="movementName in movementOrder"
                :key="movementName"
                class="flex gap-3 rounded-lg border border-slate-200 bg-white px-3 py-3 dark:border-slate-800 dark:bg-slate-950"
              >
                <div
                  class="grid size-9 shrink-0 place-items-center rounded-md border text-sm leading-none font-black"
                  :class="movementMeta[movementName].accentClass"
                  aria-hidden="true"
                >
                  {{ movementMeta[movementName].letter }}
                </div>

                <div class="min-w-0 flex-1">
                  <div class="flex min-w-0 items-center justify-between gap-3">
                    <p
                      class="truncate text-sm leading-5 font-semibold text-slate-950 dark:text-slate-50"
                    >
                      {{ movementMeta[movementName].label }}
                    </p>
                    <component
                      :is="getStatusIcon(movementsByName.get(movementName)?.status)"
                      class="size-4 shrink-0 text-slate-500 dark:text-slate-400"
                      :stroke-width="2.15"
                      aria-hidden="true"
                    />
                  </div>
                  <p class="mt-1 text-xs leading-4 text-slate-500 dark:text-slate-400">
                    {{
                      movementStatusLabels[movementsByName.get(movementName)?.status ?? 'LOCKED']
                    }}
                    - {{ formatDate(movementsByName.get(movementName)?.completed_at) }}
                  </p>
                </div>
              </li>
            </ol>
          </section>
        </div>
      </aside>
    </Transition>
  </Teleport>
</template>
