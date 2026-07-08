<script setup lang="ts">
import { computed, reactive, ref, watch } from 'vue'
import { LoaderCircle, Star, X } from '@lucide/vue'
import { z } from 'zod'

import type { Blave, UpdateBlave } from '@/domains/blaves/contracts'

const blaveSchema = z.object({
  title: z
    .string()
    .trim()
    .min(1, 'Enter a flow title to continue.')
    .max(255, 'Use 255 characters or fewer.'),
  is_favorite: z.boolean(),
})

const props = defineProps<{
  blave: Blave | null
  errorMessage?: string
  isOpen: boolean
  isPending?: boolean
}>()

const emit = defineEmits<{
  close: []
  update: [payload: UpdateBlave]
}>()

const form = reactive({
  title: '',
  is_favorite: false,
})

const wasSubmitted = ref(false)
const titleError = computed(() => {
  if (!wasSubmitted.value) {
    return ''
  }

  const result = blaveSchema.shape.title.safeParse(form.title)
  return result.success ? '' : (result.error.issues[0]?.message ?? 'Review the flow title.')
})

watch(
  () => [props.isOpen, props.blave] as const,
  ([isOpen, blave]) => {
    if (isOpen && blave) {
      form.title = blave.title
      form.is_favorite = blave.is_favorite
      wasSubmitted.value = false
    }
  },
  { immediate: true },
)

function closeDialog() {
  if (props.isPending) {
    return
  }

  emit('close')
}

function submitForm() {
  if (props.isPending) {
    return
  }

  wasSubmitted.value = true
  const result = blaveSchema.safeParse({
    title: form.title,
    is_favorite: form.is_favorite,
  })

  if (!result.success) {
    return
  }

  emit('update', result.data)
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
        class="w-full max-w-[460px] rounded-xl border border-slate-200/80 bg-white p-5 text-left shadow-[0_28px_80px_rgb(15_23_42_/_20%)] dark:border-slate-800 dark:bg-slate-900 dark:shadow-[0_28px_80px_rgb(0_0_0_/_35%)]"
        role="dialog"
        aria-modal="true"
        aria-labelledby="edit-blave-title"
      >
        <header class="flex items-start justify-between gap-4">
          <div class="min-w-0">
            <p
              class="text-xs leading-none font-semibold tracking-[0.08em] text-blue-700 uppercase dark:text-blue-300"
            >
              Edit execution
            </p>
            <h2
              id="edit-blave-title"
              class="mt-2 text-lg leading-6 font-semibold text-slate-950 dark:text-slate-50"
            >
              Update flow
            </h2>
            <p class="mt-2 text-sm leading-6 font-medium text-slate-600 dark:text-slate-400">
              Adjust the execution name and favorite state used across the workspace.
            </p>
          </div>

          <button
            class="grid size-10 shrink-0 cursor-pointer place-items-center rounded-lg border border-slate-200/80 bg-white text-slate-500 outline-none transition-[border-color,background-color,color,transform,box-shadow] duration-150 hover:border-slate-300 hover:text-slate-950 focus-visible:ring-4 focus-visible:ring-blue-100 active:scale-[0.96] disabled:cursor-not-allowed disabled:opacity-60 motion-reduce:transition-none dark:border-slate-700 dark:bg-slate-900 dark:text-slate-400 dark:hover:border-slate-600 dark:hover:bg-slate-800 dark:hover:text-slate-50 dark:focus-visible:ring-blue-950"
            type="button"
            aria-label="Close dialog"
            :disabled="isPending"
            @click="closeDialog"
          >
            <X :size="16" :stroke-width="2.2" aria-hidden="true" />
          </button>
        </header>

        <form class="mt-5 grid gap-4" novalidate @submit.prevent="submitForm">
          <label class="grid gap-2">
            <span class="text-sm leading-5 font-semibold text-slate-700 dark:text-slate-200">
              Flow title <span class="text-rose-600" aria-hidden="true">*</span>
            </span>
            <input
              v-model="form.title"
              class="min-h-11 w-full rounded-lg border border-slate-200/80 bg-white px-3 text-sm font-medium text-slate-950 outline-none transition-[background-color,border-color,color,box-shadow] duration-150 placeholder:text-slate-400 focus:border-blue-300 focus:shadow-[0_0_0_4px_rgb(219_234_254_/_80%)] disabled:cursor-not-allowed disabled:bg-slate-50 disabled:text-slate-500 dark:border-slate-700 dark:bg-slate-950 dark:text-slate-50 dark:placeholder:text-slate-500 dark:focus:border-blue-400/50 dark:focus:shadow-[0_0_0_4px_rgb(30_64_175_/_35%)] dark:disabled:bg-slate-800 dark:disabled:text-slate-500"
              type="text"
              name="flowTitle"
              autocomplete="off"
              :disabled="isPending"
              :aria-invalid="Boolean(titleError)"
              aria-describedby="edit-flow-title-error"
              required
            />
          </label>

          <p
            v-if="titleError"
            id="edit-flow-title-error"
            class="text-xs leading-4 font-semibold text-rose-700"
            role="alert"
          >
            {{ titleError }}
          </p>

          <label
            class="flex cursor-pointer items-start gap-3 rounded-lg border border-slate-200/80 bg-slate-50/70 p-3 transition-[border-color,background-color] duration-150 hover:border-blue-200 hover:bg-blue-50/60 dark:border-slate-700 dark:bg-slate-950 dark:hover:border-blue-400/30 dark:hover:bg-blue-400/10"
          >
            <input
              v-model="form.is_favorite"
              class="mt-1 size-4 rounded border-slate-300 text-blue-700 focus:ring-4 focus:ring-blue-100 disabled:cursor-not-allowed dark:border-slate-600 dark:bg-slate-900 dark:focus:ring-blue-950"
              type="checkbox"
              name="favoriteFlow"
              :disabled="isPending"
            />
            <span class="grid gap-1">
              <span
                class="inline-flex items-center gap-1.5 text-sm leading-5 font-semibold text-slate-800 dark:text-slate-100"
              >
                <Star :size="14" :stroke-width="2.2" aria-hidden="true" />
                Favorite execution
              </span>
              <span class="text-xs leading-5 font-medium text-slate-500 dark:text-slate-400">
                Show this execution as a highlighted workspace item.
              </span>
            </span>
          </label>

          <p
            v-if="errorMessage"
            class="rounded-lg border border-rose-100 bg-rose-50 px-3 py-2.5 text-sm leading-5 font-medium text-rose-700"
            role="alert"
          >
            {{ errorMessage }}
          </p>

          <div class="flex flex-wrap justify-end gap-2 pt-1">
            <button
              class="inline-flex min-h-10 cursor-pointer items-center justify-center rounded-lg border border-slate-200/80 bg-white px-4 text-sm font-semibold text-slate-700 outline-none transition-[border-color,background-color,color,transform,box-shadow] duration-150 hover:border-slate-300 hover:text-slate-950 focus-visible:ring-4 focus-visible:ring-slate-200/80 active:scale-[0.96] disabled:cursor-not-allowed disabled:opacity-60 motion-reduce:transition-none dark:border-slate-700 dark:bg-slate-900 dark:text-slate-200 dark:hover:border-slate-600 dark:hover:bg-slate-800 dark:hover:text-slate-50 dark:focus-visible:ring-slate-700"
              type="button"
              :disabled="isPending"
              @click="closeDialog"
            >
              Cancel
            </button>

            <button
              class="inline-flex min-h-10 cursor-pointer items-center justify-center gap-2 rounded-lg bg-blue-700 px-4 text-sm font-semibold text-white outline-none transition-[background-color,transform,opacity,box-shadow] duration-150 hover:bg-blue-800 focus-visible:ring-4 focus-visible:ring-blue-100 active:scale-[0.96] disabled:cursor-not-allowed disabled:opacity-60 motion-reduce:transition-none"
              type="submit"
              :disabled="isPending"
            >
              <LoaderCircle
                v-if="isPending"
                :size="15"
                class="animate-spin motion-reduce:animate-none"
                :stroke-width="2.2"
                aria-hidden="true"
              />
              {{ isPending ? 'Saving...' : 'Save changes' }}
            </button>
          </div>
        </form>
      </section>
    </div>
  </Teleport>
</template>
