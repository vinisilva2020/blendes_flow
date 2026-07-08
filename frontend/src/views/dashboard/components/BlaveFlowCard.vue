<script setup lang="ts">
import { computed } from 'vue'
import { ArrowUpRight, LoaderCircle, PencilLine, Star, Trash2 } from '@lucide/vue'

import { getBlaveMovements, type Blave } from '@/domains/blaves/contracts'

import { movementMeta, movementStatusLabels } from './blaves'

const props = defineProps<{
  blave: Blave
  isFavoritePending?: boolean
  isRemovePending?: boolean
}>()

const emit = defineEmits<{
  edit: [blave: Blave]
  open: [blave: Blave]
  remove: [blave: Blave]
  toggleFavorite: [blave: Blave]
}>()

const currentMovement = computed(() => movementMeta[props.blave.current_movement ?? 'BOUNDGROUND'])
const activeMovementStatus = computed(() =>
  getBlaveMovements(props.blave).find(
    (movement) => movement.movement === props.blave.current_movement,
  ),
)

const statusLabel = computed(
  () => movementStatusLabels[activeMovementStatus.value?.status ?? 'ACTIVE'],
)
</script>

<template>
  <article
    class="group grid min-h-[156px] overflow-hidden rounded-lg border border-slate-200 bg-white shadow-[0_1px_2px_rgb(15_23_42_/_0.04)] transition-[border-color,background-color,box-shadow,transform] duration-150 ease-out hover:-translate-y-0.5 hover:border-slate-300 hover:shadow-[0_14px_34px_rgb(15_23_42_/_0.08)] motion-reduce:transition-none motion-reduce:hover:translate-y-0 dark:border-slate-800 dark:bg-slate-900 dark:hover:border-slate-700 dark:hover:shadow-[0_18px_42px_rgb(0_0_0_/_24%)]"
    :aria-labelledby="`blave-${blave.id}-title`"
  >
    <div class="grid grid-rows-[1fr_auto]">
      <div class="px-3.5 pt-3.5 pb-3">
        <header class="flex min-w-0 items-start gap-3">
          <div
            class="grid size-9 shrink-0 place-items-center rounded-md border text-base leading-none font-black"
            :class="currentMovement.accentClass"
            aria-hidden="true"
          >
            {{ currentMovement.letter }}
          </div>

          <div class="min-w-0 flex-1">
            <div class="flex min-w-0 items-start gap-2">
              <h2
                :id="`blave-${blave.id}-title`"
                class="min-w-0 flex-1 truncate text-sm leading-5 font-semibold text-slate-950 dark:text-slate-50"
              >
                {{ blave.title }}
              </h2>
              <button
                class="-mr-1 -mt-1 grid size-8 shrink-0 cursor-pointer place-items-center rounded-md text-slate-400 outline-none transition-[background-color,color,box-shadow,transform] duration-150 ease-out hover:bg-blue-50 hover:text-blue-700 focus-visible:ring-4 focus-visible:ring-blue-100 active:scale-[0.96] motion-reduce:transition-none dark:text-slate-500 dark:hover:bg-blue-400/10 dark:hover:text-blue-200 dark:focus-visible:ring-blue-950"
                type="button"
                :aria-label="`Edit ${blave.title}`"
                @click="emit('edit', blave)"
              >
                <PencilLine :size="15" :stroke-width="2.1" aria-hidden="true" />
              </button>
            </div>
            <p class="mt-1 line-clamp-2 text-xs leading-4 text-slate-500 dark:text-slate-400">
              {{ blave.description || currentMovement.description }}
            </p>
          </div>
        </header>

        <div class="mt-4 flex min-w-0 flex-wrap items-center gap-2">
          <span
            class="inline-flex max-w-full items-center rounded-full border border-slate-200 bg-slate-50 px-2 py-1 text-[11px] leading-none font-semibold text-slate-600 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-300"
          >
            {{ currentMovement.label }}
          </span>
          <span
            class="inline-flex max-w-full items-center rounded-full border border-slate-200 bg-white px-2 py-1 text-[11px] leading-none font-semibold text-slate-500 dark:border-slate-700 dark:bg-slate-900 dark:text-slate-400"
          >
            {{ statusLabel }}
          </span>
        </div>
      </div>

      <footer
        class="flex flex-wrap items-center gap-2 border-t border-slate-200 bg-slate-50/80 px-3.5 py-2.5 dark:border-slate-800 dark:bg-slate-950/70"
      >
        <button
          class="inline-flex h-8 cursor-pointer items-center gap-1.5 rounded-md border border-slate-200 bg-white px-2.5 text-xs leading-none font-semibold text-slate-700 outline-none transition-[border-color,background-color,color,box-shadow,transform] duration-150 ease-out hover:border-blue-200 hover:bg-blue-50 hover:text-blue-700 focus-visible:border-blue-300 focus-visible:ring-4 focus-visible:ring-blue-100 active:scale-[0.97] motion-reduce:transition-none dark:border-slate-700 dark:bg-slate-900 dark:text-slate-200 dark:hover:border-blue-400/30 dark:hover:bg-blue-400/10 dark:hover:text-blue-200 dark:focus-visible:ring-blue-950"
          type="button"
          :aria-label="`Open ${blave.title}`"
          @click="emit('open', blave)"
        >
          <ArrowUpRight :size="14" :stroke-width="2.2" aria-hidden="true" />
          Open
        </button>

        <button
          class="inline-flex h-8 cursor-pointer items-center gap-1.5 rounded-md border px-2.5 text-xs leading-none font-semibold outline-none transition-[border-color,background-color,color,box-shadow,transform,opacity] duration-150 ease-out focus-visible:ring-4 focus-visible:ring-blue-100 active:scale-[0.97] disabled:cursor-not-allowed disabled:opacity-60 motion-reduce:transition-none"
          :class="
            blave.is_favorite
              ? 'border-orange-200 bg-orange-50 text-orange-400 hover:border-orange-300 hover:bg-orange-100 dark:border-orange-300/30 dark:bg-orange-400/10 dark:text-orange-300 dark:hover:bg-orange-400/15'
              : 'border-slate-200 bg-white text-slate-600 hover:border-blue-200 hover:bg-blue-50 hover:text-blue-700 dark:border-slate-700 dark:bg-slate-900 dark:text-slate-300 dark:hover:border-blue-400/30 dark:hover:bg-blue-400/10 dark:hover:text-blue-200'
          "
          type="button"
          :disabled="isFavoritePending"
          :aria-pressed="blave.is_favorite"
          :aria-label="
            blave.is_favorite ? `Remove ${blave.title} from favorites` : `Favorite ${blave.title}`
          "
          @click="emit('toggleFavorite', blave)"
        >
          <LoaderCircle
            v-if="isFavoritePending"
            :size="14"
            class="animate-spin motion-reduce:animate-none"
            :stroke-width="2.2"
            aria-hidden="true"
          />
          <Star
            v-else
            :size="14"
            :fill="blave.is_favorite ? 'currentColor' : 'none'"
            :stroke-width="2.15"
            aria-hidden="true"
          />
          {{ blave.is_favorite ? 'Favorited' : 'Favorite' }}
        </button>

        <button
          class="ml-auto inline-flex h-8 cursor-pointer items-center gap-1.5 rounded-md border border-rose-100 bg-white px-2.5 text-xs leading-none font-semibold text-rose-600 outline-none transition-[border-color,background-color,color,box-shadow,transform,opacity] duration-150 ease-out hover:border-rose-200 hover:bg-rose-50 hover:text-rose-700 focus-visible:border-rose-200 focus-visible:ring-4 focus-visible:ring-rose-100 active:scale-[0.97] disabled:cursor-not-allowed disabled:opacity-60 motion-reduce:transition-none dark:border-rose-400/20 dark:bg-slate-900 dark:text-rose-300 dark:hover:border-rose-400/35 dark:hover:bg-rose-500/10 dark:hover:text-rose-200 dark:focus-visible:ring-rose-950"
          type="button"
          :disabled="isRemovePending"
          :aria-label="`Remove ${blave.title}`"
          @click="emit('remove', blave)"
        >
          <LoaderCircle
            v-if="isRemovePending"
            :size="14"
            class="animate-spin motion-reduce:animate-none"
            :stroke-width="2.2"
            aria-hidden="true"
          />
          <Trash2 v-else :size="14" :stroke-width="2.15" aria-hidden="true" />
          Remove
        </button>
      </footer>
    </div>
  </article>
</template>
