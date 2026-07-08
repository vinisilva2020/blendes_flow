<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import { TriangleAlert, X } from '@lucide/vue'

const props = defineProps<{
  errorMessage?: string
  isOpen: boolean
  isPending?: boolean
  organizationName: string
}>()

const emit = defineEmits<{
  close: []
  confirm: []
}>()

const confirmationName = ref('')

const canDelete = computed(
  () => confirmationName.value === props.organizationName && !props.isPending,
)

watch(
  () => props.isOpen,
  (isOpen) => {
    if (!isOpen) {
      confirmationName.value = ''
    }
  },
)

function closeDialog() {
  if (props.isPending) {
    return
  }

  emit('close')
}

function confirmDelete() {
  if (!canDelete.value) {
    return
  }

  emit('confirm')
}
</script>

<template>
  <Teleport to="body">
    <div
      v-if="isOpen"
      class="fixed inset-0 z-50 grid place-items-center bg-slate-950/40 px-5 py-8 backdrop-blur-[6px]"
      role="presentation"
      @click.self="closeDialog"
    >
      <section
        class="w-full max-w-[460px] rounded-2xl border border-slate-200/70 bg-white p-5 text-left shadow-[0_28px_80px_rgb(15_23_42_/_20%)] dark:border-slate-800 dark:bg-slate-900 dark:shadow-[0_28px_80px_rgb(0_0_0_/_35%)]"
        role="dialog"
        aria-modal="true"
        aria-labelledby="delete-organization-title"
      >
        <header class="flex items-start justify-between gap-4">
          <div class="flex min-w-0 items-start gap-3">
            <span
              class="grid size-10 shrink-0 place-items-center rounded-xl border border-red-100 bg-red-50 text-red-600"
              aria-hidden="true"
            >
              <TriangleAlert :size="18" :stroke-width="2.2" />
            </span>

            <div class="min-w-0">
              <h2
                id="delete-organization-title"
                class="text-lg leading-6 font-semibold text-balance text-slate-950 dark:text-slate-50"
              >
                Delete organization
              </h2>
              <p
                class="mt-2 text-sm leading-6 font-medium text-pretty text-slate-600 dark:text-slate-400"
              >
                This action permanently removes the organization context and can impact related
                workspace data.
              </p>
            </div>
          </div>

          <button
            class="grid size-10 shrink-0 cursor-pointer place-items-center rounded-xl border border-slate-200/70 bg-white text-slate-500 outline-none transition-[border-color,background-color,color,transform,box-shadow] duration-150 hover:border-slate-300 hover:text-slate-950 focus-visible:ring-4 focus-visible:ring-slate-200/80 active:scale-[0.96] disabled:cursor-not-allowed disabled:opacity-60 dark:border-slate-700 dark:bg-slate-900 dark:text-slate-400 dark:hover:border-slate-600 dark:hover:bg-slate-800 dark:hover:text-slate-50 dark:focus-visible:ring-slate-700"
            type="button"
            aria-label="Close dialog"
            :disabled="isPending"
            @click="closeDialog"
          >
            <X :size="16" :stroke-width="2.2" aria-hidden="true" />
          </button>
        </header>

        <div
          class="mt-5 rounded-xl border border-slate-200/70 bg-slate-50/70 p-3 dark:border-slate-800 dark:bg-slate-950"
        >
          <p class="text-xs leading-5 font-semibold text-slate-500 dark:text-slate-400">
            Organization
          </p>
          <p
            class="mt-1 truncate text-sm leading-5 font-semibold text-slate-950 dark:text-slate-50"
          >
            {{ organizationName }}
          </p>
        </div>

        <form class="mt-5 grid gap-4" novalidate @submit.prevent="confirmDelete">
          <label class="grid gap-2">
            <span class="text-sm leading-5 font-semibold text-slate-700 dark:text-slate-200">
              Type the organization name to confirm deletion.
            </span>
            <input
              v-model="confirmationName"
              class="min-h-11 w-full rounded-xl border border-slate-200/80 bg-white px-3 text-sm font-medium text-slate-950 outline-none transition-[background-color,border-color,color,box-shadow] duration-150 placeholder:text-slate-400 focus:border-red-300 focus:shadow-[0_0_0_4px_rgb(254_226_226_/_70%)] disabled:cursor-not-allowed disabled:bg-slate-50 disabled:text-slate-500 dark:border-slate-700 dark:bg-slate-950 dark:text-slate-50 dark:placeholder:text-slate-500 dark:focus:border-red-400/50 dark:focus:shadow-[0_0_0_4px_rgb(127_29_29_/_36%)] dark:disabled:bg-slate-800"
              type="text"
              autocomplete="off"
              :disabled="isPending"
              :placeholder="organizationName"
            />
          </label>

          <p
            v-if="errorMessage"
            class="rounded-xl border border-red-100 bg-red-50 px-3 py-2.5 text-sm leading-5 font-medium text-red-700"
            role="alert"
          >
            {{ errorMessage }}
          </p>

          <div class="flex flex-wrap justify-end gap-2">
            <button
              class="inline-flex min-h-10 cursor-pointer items-center justify-center rounded-xl border border-slate-200/80 bg-white px-4 text-sm font-semibold text-slate-700 outline-none transition-[border-color,background-color,color,transform,box-shadow] duration-150 hover:border-slate-300 hover:text-slate-950 focus-visible:ring-4 focus-visible:ring-slate-200/80 active:scale-[0.96] disabled:cursor-not-allowed disabled:opacity-60 dark:border-slate-700 dark:bg-slate-900 dark:text-slate-200 dark:hover:border-slate-600 dark:hover:bg-slate-800 dark:hover:text-slate-50 dark:focus-visible:ring-slate-700"
              type="button"
              :disabled="isPending"
              @click="closeDialog"
            >
              Cancel
            </button>

            <button
              class="inline-flex min-h-10 cursor-pointer items-center justify-center rounded-xl bg-red-500 px-4 text-sm font-semibold text-white outline-none transition-[background-color,transform,opacity,box-shadow] duration-150 hover:bg-red-600 focus-visible:ring-4 focus-visible:ring-red-100 active:scale-[0.96] disabled:cursor-not-allowed disabled:opacity-60"
              type="submit"
              :disabled="!canDelete"
            >
              {{ isPending ? 'Deleting...' : 'Delete organization' }}
            </button>
          </div>
        </form>
      </section>
    </div>
  </Teleport>
</template>
