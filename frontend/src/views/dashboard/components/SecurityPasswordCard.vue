<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import { z } from 'zod'
import { CheckCircle2, KeyRound, LoaderCircle, ShieldCheck } from '@lucide/vue'

import type { AccountPasswordPayload } from '@/domains/accounts/contracts'

type PasswordField = 'currentPassword' | 'newPassword' | 'confirmPassword'

const props = withDefaults(
  defineProps<{
    errorMessage?: string
    isPending?: boolean
    requiresCurrentPassword?: boolean
    successMessage?: string
  }>(),
  {
    requiresCurrentPassword: true,
  },
)

const emit = defineEmits<{
  submit: [payload: AccountPasswordPayload]
}>()

const passwordSchema = computed(() =>
  z
    .object({
      currentPassword: props.requiresCurrentPassword
        ? z.string().min(1, 'Confirm your current password first.')
        : z.string(),
      newPassword: z
        .string()
        .min(8, 'Use at least 8 characters.')
        .regex(/[A-Z]/, 'Add at least one uppercase letter.')
        .regex(/[0-9]/, 'Add at least one number.'),
      confirmPassword: z.string().min(1, 'Repeat the new password.'),
    })
    .refine((values) => values.newPassword === values.confirmPassword, {
      message: 'Passwords do not match.',
      path: ['confirmPassword'],
    }),
)

const form = ref({
  currentPassword: '',
  newPassword: '',
  confirmPassword: '',
})
const touchedFields = ref<Partial<Record<PasswordField, boolean>>>({})
const wasSubmitted = ref(false)

const validationResult = computed(() => passwordSchema.value.safeParse(form.value))
const fieldErrors = computed<Partial<Record<PasswordField, string>>>(() => {
  if (validationResult.value.success) {
    return {}
  }

  return validationResult.value.error.issues.reduce<Partial<Record<PasswordField, string>>>(
    (errors, issue) => {
      const field = issue.path[0]

      if (
        (field === 'currentPassword' || field === 'newPassword' || field === 'confirmPassword') &&
        !errors[field]
      ) {
        errors[field] = issue.message
      }

      return errors
    },
    {},
  )
})
const canSubmit = computed(() => validationResult.value.success && !props.isPending)

watch(
  () => props.successMessage,
  (message) => {
    if (!message) {
      return
    }

    form.value = {
      confirmPassword: '',
      currentPassword: '',
      newPassword: '',
    }
    touchedFields.value = {}
    wasSubmitted.value = false
  },
)

function touchField(field: PasswordField) {
  touchedFields.value = {
    ...touchedFields.value,
    [field]: true,
  }
}

function shouldShowError(field: PasswordField) {
  return Boolean((wasSubmitted.value || touchedFields.value[field]) && fieldErrors.value[field])
}

function submitPasswordChange() {
  wasSubmitted.value = true
  touchedFields.value = {
    confirmPassword: true,
    currentPassword: true,
    newPassword: true,
  }
  if (!canSubmit.value) {
    return
  }

  emit('submit', {
    ...(props.requiresCurrentPassword ? { current_password: form.value.currentPassword } : {}),
    new_password: form.value.newPassword,
    password_confirm: form.value.confirmPassword,
  })
}
</script>

<template>
  <form
    class="rounded-3xl bg-white p-2 shadow-[0_0_0_1px_rgb(15_23_42_/_6%),0_10px_28px_rgb(15_23_42_/_5%)]"
    novalidate
    @submit.prevent="submitPasswordChange"
  >
    <div class="rounded-2xl bg-slate-50/80 p-4 sm:p-5 md:p-6">
      <header class="flex flex-col gap-2 sm:flex-row sm:items-start sm:justify-between">
        <div>
          <p class="text-xs leading-4 font-semibold tracking-[0.12em] text-blue-600 uppercase">
            Security
          </p>
          <h2 class="mt-1 text-lg leading-6 font-semibold text-balance text-slate-950">Password</h2>
          <p class="mt-1 max-w-2xl text-sm leading-6 font-medium text-pretty text-slate-500">
            Your password is never displayed. Save a local password before removing your only social
            sign-in.
          </p>
        </div>
        <span
          class="inline-flex min-h-8 w-fit items-center gap-1.5 rounded-lg bg-blue-50 px-2.5 text-xs font-semibold text-blue-700 shadow-[0_0_0_1px_rgb(191_219_254_/_80%)]"
        >
          <ShieldCheck :size="14" :stroke-width="2.3" aria-hidden="true" />
          Protected
        </span>
      </header>

      <div class="mt-6 grid gap-3">
        <label
          v-if="requiresCurrentPassword"
          class="grid gap-4 rounded-2xl bg-white p-4 shadow-[0_0_0_1px_rgb(15_23_42_/_5%)] md:grid-cols-[minmax(0,1fr)_minmax(260px,360px)] md:items-start"
        >
          <span>
            <span class="text-sm leading-5 font-semibold text-slate-800">Current password</span>
            <span class="mt-1 block text-sm leading-5 font-medium text-pretty text-slate-500">
              Required to confirm that this change is being made by you.
            </span>
          </span>
          <span class="grid gap-2">
            <input
              v-model="form.currentPassword"
              class="min-h-11 w-full rounded-xl border bg-white px-3 text-sm font-medium text-slate-950 outline-none transition-[border-color,box-shadow] duration-150 placeholder:text-slate-400 focus:border-blue-300 focus:shadow-[0_0_0_4px_rgb(219_234_254_/_85%)]"
              :class="shouldShowError('currentPassword') ? 'border-red-200' : 'border-slate-200/80'"
              type="password"
              name="currentPassword"
              autocomplete="current-password"
              :aria-invalid="shouldShowError('currentPassword')"
              aria-describedby="current-password-error"
              :disabled="isPending"
              @blur="touchField('currentPassword')"
            />
            <span
              v-if="shouldShowError('currentPassword')"
              id="current-password-error"
              class="text-xs leading-4 font-medium text-red-600"
              role="alert"
            >
              {{ fieldErrors.currentPassword }}
            </span>
          </span>
        </label>

        <label
          class="grid gap-4 rounded-2xl bg-white p-4 shadow-[0_0_0_1px_rgb(15_23_42_/_5%)] md:grid-cols-[minmax(0,1fr)_minmax(260px,360px)] md:items-start"
        >
          <span>
            <span class="text-sm leading-5 font-semibold text-slate-800">New password</span>
            <span class="mt-1 block text-sm leading-5 font-medium text-pretty text-slate-500">
              Use 8+ characters with at least one number and one uppercase letter.
            </span>
          </span>
          <span class="grid gap-2">
            <input
              v-model="form.newPassword"
              class="min-h-11 w-full rounded-xl border bg-white px-3 text-sm font-medium text-slate-950 outline-none transition-[border-color,box-shadow] duration-150 placeholder:text-slate-400 focus:border-blue-300 focus:shadow-[0_0_0_4px_rgb(219_234_254_/_85%)]"
              :class="shouldShowError('newPassword') ? 'border-red-200' : 'border-slate-200/80'"
              type="password"
              name="newPassword"
              autocomplete="new-password"
              :aria-invalid="shouldShowError('newPassword')"
              aria-describedby="new-password-error"
              :disabled="isPending"
              @blur="touchField('newPassword')"
            />
            <span
              v-if="shouldShowError('newPassword')"
              id="new-password-error"
              class="text-xs leading-4 font-medium text-red-600"
              role="alert"
            >
              {{ fieldErrors.newPassword }}
            </span>
          </span>
        </label>

        <label
          class="grid gap-4 rounded-2xl bg-white p-4 shadow-[0_0_0_1px_rgb(15_23_42_/_5%)] md:grid-cols-[minmax(0,1fr)_minmax(260px,360px)] md:items-start"
        >
          <span>
            <span class="text-sm leading-5 font-semibold text-slate-800">Confirm new password</span>
            <span class="mt-1 block text-sm leading-5 font-medium text-pretty text-slate-500">
              Re-enter the new password so it can be checked before saving.
            </span>
          </span>
          <span class="grid gap-2">
            <input
              v-model="form.confirmPassword"
              class="min-h-11 w-full rounded-xl border bg-white px-3 text-sm font-medium text-slate-950 outline-none transition-[border-color,box-shadow] duration-150 placeholder:text-slate-400 focus:border-blue-300 focus:shadow-[0_0_0_4px_rgb(219_234_254_/_85%)]"
              :class="shouldShowError('confirmPassword') ? 'border-red-200' : 'border-slate-200/80'"
              type="password"
              name="confirmPassword"
              autocomplete="new-password"
              :aria-invalid="shouldShowError('confirmPassword')"
              aria-describedby="confirm-password-error"
              :disabled="isPending"
              @blur="touchField('confirmPassword')"
            />
            <span
              v-if="shouldShowError('confirmPassword')"
              id="confirm-password-error"
              class="text-xs leading-4 font-medium text-red-600"
              role="alert"
            >
              {{ fieldErrors.confirmPassword }}
            </span>
          </span>
        </label>
      </div>

      <p
        v-if="errorMessage"
        class="mt-5 rounded-xl border border-red-100 bg-red-50 px-3 py-2.5 text-sm leading-5 font-medium text-red-700"
        role="alert"
      >
        {{ errorMessage }}
      </p>

      <p
        v-if="successMessage"
        class="mt-5 rounded-xl border border-emerald-100 bg-emerald-50 px-3 py-2.5 text-sm leading-5 font-medium text-emerald-700"
        aria-live="polite"
      >
        {{ successMessage }}
      </p>

      <footer class="mt-6 flex justify-end border-t border-slate-200/70 pt-5">
        <button
          class="inline-flex min-h-10 w-full cursor-pointer items-center justify-center gap-2 rounded-xl bg-blue-600 px-4 text-sm font-semibold text-white outline-none transition-[background-color,scale,opacity,box-shadow] duration-150 hover:bg-blue-700 focus-visible:ring-4 focus-visible:ring-blue-100 active:scale-[0.96] disabled:cursor-not-allowed disabled:opacity-50 sm:w-auto sm:min-w-44 motion-reduce:transition-none"
          type="submit"
          :disabled="!canSubmit"
        >
          <LoaderCircle
            v-if="isPending"
            class="size-4 animate-spin"
            :stroke-width="2.2"
            aria-hidden="true"
          />
          <CheckCircle2 v-else-if="canSubmit" :size="15" :stroke-width="2.2" aria-hidden="true" />
          <KeyRound v-else :size="15" :stroke-width="2.2" aria-hidden="true" />
          Save password
        </button>
      </footer>
    </div>
  </form>
</template>
