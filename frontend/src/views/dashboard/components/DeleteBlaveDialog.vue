<script setup lang="ts">
import { LoaderCircle, Trash2, X } from '@lucide/vue'

import type { Blave } from '@/domains/blaves/contracts'

const props = defineProps<{
  blave: Blave | null
  errorMessage?: string
  isOpen: boolean
  isPending?: boolean
}>()

const emit = defineEmits<{
  close: []
  confirm: []
}>()

function closeDialog() {
  if (props.isPending) {
    return
  }

  emit('close')
}
</script>

<template>
  <Teleport to="body">
    <div
      v-if="isOpen && blave"
      class="fixed inset-0 z-50 grid place-items-center bg-slate-950/40 px-5 py-8 backdrop-blur-[6px]"
      role="presentation"
      @click.self="closeDialog"
      @keydown.esc="closeDialog"
    >
      <section
        class="w-full max-w-[420px] rounded-xl border border-slate-200/80 bg-white p-5 text-left shadow-[0_28px_80px_rgb(15_23_42_/_20%)] dark:border-slate-800 dark:bg-slate-900 dark:shadow-[0_28px_80px_rgb(0_0_0_/_35%)]"
        role="dialog"
        aria-modal="true"
        aria-labelledby="delete-blave-title"
        aria-describedby="delete-blave-description"
      >
        <header class="flex items-start justify-between gap-4">
          <div class="min-w-0">
            <span
              class="grid size-10 place-items-center rounded-lg border border-rose-100 bg-rose-50 text-rose-600"
              aria-hidden="true"
            >
              <Trash2 :size="18" :stroke-width="2.2" />
            </span>
            <h2
              id="delete-blave-title"
              class="mt-4 text-lg leading-6 font-semibold text-slate-950 dark:text-slate-50"
            >
              Remove flow?
            </h2>
          </div>

          <button
            class="grid size-10 shrink-0 cursor-pointer place-items-center rounded-lg border border-slate-200/80 bg-white text-slate-500 outline-none transition-[border-color,background-color,color,transform,box-shadow] duration-150 hover:border-slate-300 hover:text-slate-950 focus-visible:ring-4 focus-visible:ring-rose-100 active:scale-[0.96] disabled:cursor-not-allowed disabled:opacity-60 motion-reduce:transition-none dark:border-slate-700 dark:bg-slate-900 dark:text-slate-400 dark:hover:border-slate-600 dark:hover:bg-slate-800 dark:hover:text-slate-50 dark:focus-visible:ring-rose-950"
            type="button"
            aria-label="Close dialog"
            :disabled="isPending"
            @click="closeDialog"
          >
            <X :size="16" :stroke-width="2.2" aria-hidden="true" />
          </button>
        </header>

        <p
          id="delete-blave-description"
          class="mt-3 text-sm leading-6 font-medium text-slate-600 dark:text-slate-400"
        >
          This will permanently remove
          <strong class="font-semibold text-slate-950 dark:text-slate-50"
            >"{{ blave.title }}"</strong
          >
          from this workspace. This action cannot be undone.
        </p>

        <p
          v-if="errorMessage"
          class="mt-4 rounded-lg border border-rose-100 bg-rose-50 px-3 py-2.5 text-sm leading-5 font-medium text-rose-700"
          role="alert"
        >
          {{ errorMessage }}
        </p>

        <div class="mt-5 flex flex-wrap justify-end gap-2">
          <button
            class="inline-flex min-h-10 cursor-pointer items-center justify-center rounded-lg border border-slate-200/80 bg-white px-4 text-sm font-semibold text-slate-700 outline-none transition-[border-color,background-color,color,transform,box-shadow] duration-150 hover:border-slate-300 hover:text-slate-950 focus-visible:ring-4 focus-visible:ring-slate-200/80 active:scale-[0.96] disabled:cursor-not-allowed disabled:opacity-60 motion-reduce:transition-none dark:border-slate-700 dark:bg-slate-900 dark:text-slate-200 dark:hover:border-slate-600 dark:hover:bg-slate-800 dark:hover:text-slate-50 dark:focus-visible:ring-slate-700"
            type="button"
            :disabled="isPending"
            @click="closeDialog"
          >
            Cancel
          </button>

          <button
            class="inline-flex min-h-10 cursor-pointer items-center justify-center gap-2 rounded-lg bg-rose-600 px-4 text-sm font-semibold text-white outline-none transition-[background-color,transform,opacity,box-shadow] duration-150 hover:bg-rose-700 focus-visible:ring-4 focus-visible:ring-rose-100 active:scale-[0.96] disabled:cursor-not-allowed disabled:opacity-60 motion-reduce:transition-none"
            type="button"
            :disabled="isPending"
            @click="emit('confirm')"
          >
            <LoaderCircle
              v-if="isPending"
              :size="15"
              class="animate-spin motion-reduce:animate-none"
              :stroke-width="2.2"
              aria-hidden="true"
            />
            {{ isPending ? 'Removing...' : 'Remove flow' }}
          </button>
        </div>
      </section>
    </div>
  </Teleport>
</template>
