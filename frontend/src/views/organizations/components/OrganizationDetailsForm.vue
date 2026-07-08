<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import { z } from 'zod'
import { CircleCheck, CircleMinus, LoaderCircle, Save } from '@lucide/vue'

type FormField = 'name' | 'description'

export type OrganizationDetailsFormValues = {
  description: string
  name: string
}

export type OrganizationDetailsFormPayload = {
  description: string | null
  name: string
}

const props = defineProps<{
  errorMessage?: string
  initialValues: OrganizationDetailsFormValues
  isLoading?: boolean
  isPending?: boolean
  isStatusActive: boolean
  resetKey?: string | number | null
  statusLabel: string
  successMessage?: string
}>()

const emit = defineEmits<{
  submit: [payload: OrganizationDetailsFormPayload]
}>()

const organizationSchema = z.object({
  name: z
    .string()
    .trim()
    .min(2, 'Use at least 2 characters for the organization name.')
    .max(80, 'Keep the organization name under 80 characters.'),
  description: z.string().trim().max(240, 'Keep the description under 240 characters.').optional(),
})

const form = ref<OrganizationDetailsFormValues>({ ...props.initialValues })
const initialForm = ref<OrganizationDetailsFormValues>({ ...props.initialValues })
const touchedFields = ref<Partial<Record<FormField, boolean>>>({})
const wasSubmitted = ref(false)

const validationResult = computed(() => organizationSchema.safeParse(form.value))
const fieldErrors = computed<Partial<Record<FormField, string>>>(() => {
  if (validationResult.value.success) {
    return {}
  }

  return validationResult.value.error.issues.reduce<Partial<Record<FormField, string>>>(
    (errors, issue) => {
      const field = issue.path[0]

      if ((field === 'name' || field === 'description') && !errors[field]) {
        errors[field] = issue.message
      }

      return errors
    },
    {},
  )
})

const hasChanges = computed(
  () =>
    form.value.name !== initialForm.value.name ||
    form.value.description !== initialForm.value.description,
)
const canSave = computed(
  () => hasChanges.value && validationResult.value.success && !props.isPending && !props.isLoading,
)

watch(
  () => props.resetKey,
  () => {
    resetForm(props.initialValues)
  },
)

watch(
  () => props.initialValues,
  (values) => {
    if (!hasChanges.value) {
      resetForm(values)
    }
  },
)

function resetForm(values: OrganizationDetailsFormValues) {
  form.value = { ...values }
  initialForm.value = { ...values }
  touchedFields.value = {}
  wasSubmitted.value = false
}

function touchField(field: FormField) {
  touchedFields.value = {
    ...touchedFields.value,
    [field]: true,
  }
}

function shouldShowError(field: FormField) {
  return Boolean((wasSubmitted.value || touchedFields.value[field]) && fieldErrors.value[field])
}

function submitForm() {
  wasSubmitted.value = true
  touchedFields.value = {
    description: true,
    name: true,
  }

  if (!canSave.value) {
    return
  }

  emit('submit', {
    description: form.value.description.trim() || null,
    name: form.value.name.trim(),
  })
}
</script>

<template>
  <form
    id="organization-details-form"
    class="rounded-3xl bg-white p-2 shadow-[0_0_0_1px_rgb(15_23_42_/_6%),0_10px_28px_rgb(15_23_42_/_5%)] dark:bg-slate-900 dark:shadow-[0_0_0_1px_rgb(51_65_85_/_70%),0_18px_42px_rgb(0_0_0_/_24%)]"
    novalidate
    @submit.prevent="submitForm"
  >
    <div class="rounded-2xl bg-slate-50/80 p-4 sm:p-5 md:p-6 dark:bg-slate-950/70">
      <header class="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
        <div>
          <p
            class="text-xs leading-4 font-semibold tracking-[0.12em] text-blue-600 uppercase dark:text-blue-300"
          >
            Company
          </p>
          <h2
            class="mt-1 text-lg leading-6 font-semibold text-balance text-slate-950 dark:text-slate-50"
          >
            Company information
          </h2>
          <p
            class="mt-1 max-w-2xl text-sm leading-6 font-medium text-pretty text-slate-500 dark:text-slate-400"
          >
            Keep the workspace name and context clear for everyone on the team.
          </p>
        </div>

        <span
          class="inline-flex min-h-8 w-fit items-center gap-1.5 rounded-lg bg-white px-2.5 text-xs font-semibold shadow-[0_0_0_1px_rgb(15_23_42_/_6%)] dark:bg-slate-900 dark:shadow-[0_0_0_1px_rgb(51_65_85_/_70%)]"
          :class="
            isStatusActive
              ? 'text-emerald-700 dark:text-emerald-300'
              : 'text-slate-500 dark:text-slate-400'
          "
        >
          <CircleCheck v-if="isStatusActive" :size="14" :stroke-width="2.3" aria-hidden="true" />
          <CircleMinus v-else :size="14" :stroke-width="2.3" aria-hidden="true" />
          {{ statusLabel }}
        </span>
      </header>

      <div v-if="isLoading" class="mt-6 grid gap-3" aria-label="Loading organization form">
        <span class="h-20 rounded-2xl bg-white dark:bg-slate-900"></span>
        <span class="h-32 rounded-2xl bg-white dark:bg-slate-900"></span>
      </div>

      <div v-else class="mt-6 grid gap-3">
        <label
          class="grid gap-4 rounded-2xl bg-white p-4 shadow-[0_0_0_1px_rgb(15_23_42_/_5%)] md:grid-cols-[minmax(0,1fr)_minmax(260px,360px)] md:items-start dark:bg-slate-900 dark:shadow-[0_0_0_1px_rgb(51_65_85_/_58%)]"
        >
          <span>
            <span class="text-sm leading-5 font-semibold text-slate-800 dark:text-slate-100"
              >Company name</span
            >
            <span
              class="mt-1 block text-sm leading-5 font-medium text-pretty text-slate-500 dark:text-slate-400"
            >
              This name appears in navigation, ownership labels, and workspace activity.
            </span>
          </span>
          <span class="grid gap-2">
            <input
              v-model="form.name"
              class="min-h-11 w-full rounded-xl border bg-white px-3 text-sm font-medium text-slate-950 outline-none transition-[background-color,border-color,color,box-shadow] duration-150 placeholder:text-slate-400 focus:border-blue-300 focus:shadow-[0_0_0_4px_rgb(219_234_254_/_85%)] disabled:cursor-not-allowed disabled:bg-slate-50 dark:bg-slate-950 dark:text-slate-50 dark:placeholder:text-slate-500 dark:focus:border-blue-400/50 dark:focus:shadow-[0_0_0_4px_rgb(30_64_175_/_35%)] dark:disabled:bg-slate-800"
              :class="
                shouldShowError('name')
                  ? 'border-red-200 dark:border-red-400/50'
                  : 'border-slate-200/80 dark:border-slate-700'
              "
              type="text"
              name="organizationName"
              autocomplete="organization"
              placeholder="Acme Operations"
              :aria-invalid="shouldShowError('name')"
              aria-describedby="organization-name-error"
              :disabled="isPending"
              @blur="touchField('name')"
            />
            <span
              v-if="shouldShowError('name')"
              id="organization-name-error"
              class="text-xs leading-4 font-medium text-red-600"
              role="alert"
            >
              {{ fieldErrors.name }}
            </span>
          </span>
        </label>

        <label
          class="grid gap-4 rounded-2xl bg-white p-4 shadow-[0_0_0_1px_rgb(15_23_42_/_5%)] md:grid-cols-[minmax(0,1fr)_minmax(260px,360px)] md:items-start dark:bg-slate-900 dark:shadow-[0_0_0_1px_rgb(51_65_85_/_58%)]"
        >
          <span>
            <span class="text-sm leading-5 font-semibold text-slate-800 dark:text-slate-100"
              >Description</span
            >
            <span
              class="mt-1 block text-sm leading-5 font-medium text-pretty text-slate-500 dark:text-slate-400"
            >
              Optional context for the workspace and the team behind it.
            </span>
          </span>
          <span class="grid gap-2">
            <textarea
              v-model="form.description"
              class="min-h-28 w-full resize-y rounded-xl border bg-white px-3 py-2.5 text-sm leading-6 font-medium text-slate-950 outline-none transition-[background-color,border-color,color,box-shadow] duration-150 placeholder:text-slate-400 focus:border-blue-300 focus:shadow-[0_0_0_4px_rgb(219_234_254_/_85%)] disabled:cursor-not-allowed disabled:bg-slate-50 dark:bg-slate-950 dark:text-slate-50 dark:placeholder:text-slate-500 dark:focus:border-blue-400/50 dark:focus:shadow-[0_0_0_4px_rgb(30_64_175_/_35%)] dark:disabled:bg-slate-800"
              :class="
                shouldShowError('description')
                  ? 'border-red-200 dark:border-red-400/50'
                  : 'border-slate-200/80 dark:border-slate-700'
              "
              name="organizationDescription"
              placeholder="Short context for this company"
              :aria-invalid="shouldShowError('description')"
              aria-describedby="organization-description-error"
              :disabled="isPending"
              @blur="touchField('description')"
            ></textarea>
            <span class="flex items-start justify-between gap-3">
              <span
                v-if="shouldShowError('description')"
                id="organization-description-error"
                class="text-xs leading-4 font-medium text-red-600"
                role="alert"
              >
                {{ fieldErrors.description }}
              </span>
              <span
                class="ml-auto text-xs leading-4 font-medium tabular-nums text-slate-400 dark:text-slate-500"
                aria-hidden="true"
              >
                {{ form.description.length }}/240
              </span>
            </span>
          </span>
        </label>
      </div>

      <div v-if="errorMessage || successMessage" class="mt-5 grid gap-3" aria-live="polite">
        <p
          v-if="errorMessage"
          class="rounded-xl border border-red-100 bg-red-50 px-3 py-2.5 text-sm leading-5 font-medium text-red-700"
          role="alert"
        >
          {{ errorMessage }}
        </p>
        <p
          v-if="successMessage"
          class="rounded-xl border border-emerald-100 bg-emerald-50 px-3 py-2.5 text-sm leading-5 font-medium text-emerald-700"
        >
          {{ successMessage }}
        </p>
      </div>

      <footer class="mt-6 flex justify-end border-t border-slate-200/70 pt-5 dark:border-slate-800">
        <button
          class="inline-flex min-h-10 w-full cursor-pointer items-center justify-center gap-2 rounded-xl bg-blue-600 px-4 text-sm font-semibold text-white outline-none transition-[background-color,scale,opacity,box-shadow] duration-150 hover:bg-blue-700 focus-visible:ring-4 focus-visible:ring-blue-100 active:scale-[0.96] disabled:cursor-not-allowed disabled:opacity-50 sm:w-auto sm:min-w-40 motion-reduce:transition-none"
          type="submit"
          :disabled="!canSave"
        >
          <LoaderCircle
            v-if="isPending"
            class="size-4 animate-spin"
            :stroke-width="2.2"
            aria-hidden="true"
          />
          <Save v-else :size="15" :stroke-width="2.2" aria-hidden="true" />
          Save company
        </button>
      </footer>
    </div>
  </form>
</template>
