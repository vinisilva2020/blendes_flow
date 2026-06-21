<script setup lang="ts">
import { ref, watch } from 'vue'
import { X } from '@lucide/vue'

const props = defineProps<{
  errorMessage?: string
  isOpen: boolean
  isPending?: boolean
}>()

const emit = defineEmits<{
  close: []
  create: [name: string]
}>()

const name = ref('')
const wasSubmitted = ref(false)

watch(
  () => props.isOpen,
  (isOpen) => {
    if (!isOpen) {
      name.value = ''
      wasSubmitted.value = false
    }
  },
)

function closeDialog() {
  if (props.isPending) {
    return
  }

  emit('close')
}

function submitForm() {
  wasSubmitted.value = true

  if (!name.value.trim()) {
    return
  }

  emit('create', name.value.trim())
}
</script>

<template>
  <div
    v-if="isOpen"
    class="fixed inset-0 z-50 grid place-items-center bg-[#071113]/42 px-5 py-8 backdrop-blur-[6px]"
    role="presentation"
    @click.self="closeDialog"
  >
    <section
      class="w-full max-w-[430px] rounded-lg border border-[#d8e6e9] bg-white p-5 text-left shadow-[0_28px_80px_rgb(7_17_19_/_22%)]"
      role="dialog"
      aria-modal="true"
      aria-labelledby="create-organization-title"
    >
      <header class="flex items-start justify-between gap-4">
        <div>
          <h2 id="create-organization-title" class="m-0 text-xl font-black text-[#071113]">
            New organization
          </h2>
          <p class="mt-2 text-sm font-bold leading-5 text-[#62777d]">
            Create a workspace for a team, operation, or improvement flow.
          </p>
        </div>

        <button
          class="inline-flex size-9 cursor-pointer items-center justify-center rounded-lg border border-[#d8e6e9] bg-white text-[#62777d] transition-[border-color,color,transform] hover:border-[#8adff3] hover:text-[#246b78] active:scale-[0.96] disabled:cursor-not-allowed disabled:opacity-60"
          type="button"
          aria-label="Close dialog"
          :disabled="isPending"
          @click="closeDialog"
        >
          <X :size="16" :stroke-width="2.4" aria-hidden="true" />
        </button>
      </header>

      <form class="mt-5 grid gap-4" novalidate @submit.prevent="submitForm">
        <label class="grid gap-2">
          <span class="text-xs font-black uppercase tracking-[0.08em] text-[#62777d]">
            Organization name
          </span>
          <input
            v-model.trim="name"
            class="min-h-11 w-full rounded-lg border border-[#d8e6e9] bg-white px-3 text-sm font-bold text-[#172224] outline-none transition-[border-color,box-shadow] placeholder:text-[#9aaeb2] focus:border-[#8adff3] focus:shadow-[0_0_0_4px_rgb(174_238_255_/_26%)]"
            type="text"
            name="organizationName"
            autocomplete="organization"
            placeholder="Organization name"
            :aria-invalid="wasSubmitted && !name.trim()"
            aria-describedby="organization-name-error"
          />
        </label>

        <p
          v-if="wasSubmitted && !name.trim()"
          id="organization-name-error"
          class="m-0 text-xs font-bold leading-4 text-[#9f2f25]"
          role="alert"
        >
          Enter an organization name to continue.
        </p>

        <p
          v-if="errorMessage"
          class="m-0 rounded-lg bg-[#fff1f0] px-3.5 py-3 text-sm font-bold leading-5 text-[#9f2f25] shadow-[inset_0_0_0_1px_rgb(159_47_37_/_14%)]"
          role="alert"
        >
          {{ errorMessage }}
        </p>

        <div class="mt-1 flex justify-end gap-2">
          <button
            class="inline-flex min-h-10 cursor-pointer items-center justify-center rounded-lg border border-[#d8e6e9] bg-white px-4 text-sm font-black text-[#62777d] transition-[border-color,color,transform] hover:border-[#8adff3] hover:text-[#246b78] active:scale-[0.96] disabled:cursor-not-allowed disabled:opacity-60"
            type="button"
            :disabled="isPending"
            @click="closeDialog"
          >
            Cancel
          </button>

          <button
            class="inline-flex min-h-10 cursor-pointer items-center justify-center rounded-lg bg-[#246b78] px-4 text-sm font-black text-white shadow-[0_12px_26px_rgb(18_33_36_/_14%)] transition-[transform,opacity,background-color] hover:bg-[#1f5f6d] active:scale-[0.96] disabled:cursor-not-allowed disabled:opacity-60"
            type="submit"
            :disabled="isPending"
          >
            {{ isPending ? 'Creating...' : 'Create organization' }}
          </button>
        </div>
      </form>
    </section>
  </div>
</template>
