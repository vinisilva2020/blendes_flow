<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import { z } from 'zod'
import {
  ImagePlus,
  KeyRound,
  LoaderCircle,
  Save,
  ShieldAlert,
  Unlink2,
  UserRound,
  X,
} from '@lucide/vue'

import { useAccountAvatar } from '@/domains/accounts/composables/useAccountAvatar'
import GoogleButton from '@/components/GoogleButton.vue'
import type {
  AccountGoogleSocialAccountPayload,
  AccountPasswordPayload,
  SocialAccount,
} from '@/domains/accounts/contracts'
import googleLogo from '@/assets/img/google.svg'

type ProfileField = 'username' | 'email'
type PasswordSetupField = 'newPassword' | 'confirmPassword'

export type ProfileDetailsFormValues = {
  avatarType: string | null
  email: string
  username: string
}

export type ProfileDetailsFormPayload = {
  avatar_type: string | null
  email: string
  username: string
}

const props = defineProps<{
  errorMessage?: string
  initialValues: ProfileDetailsFormValues
  isLoading?: boolean
  isLinkingGoogle?: boolean
  isPending?: boolean
  isSettingLocalPassword?: boolean
  isUnlinkingGoogle?: boolean
  passwordSetupErrorMessage?: string
  resetKey?: string | number | null
  socialAccounts?: SocialAccount[]
  successMessage?: string
}>()

const emit = defineEmits<{
  linkGoogleAccount: [payload: AccountGoogleSocialAccountPayload]
  openAvatarDialog: []
  setLocalPassword: [payload: AccountPasswordPayload]
  submit: [payload: ProfileDetailsFormPayload]
  unlinkGoogleAccount: []
}>()

const profileSchema = z.object({
  username: z
    .string()
    .trim()
    .min(2, 'Use at least 2 characters for your username.')
    .max(150, 'Keep your username under 150 characters.')
    .regex(/^[\w.@+-]+$/, 'Use only letters, numbers, and @/./+/-/_.'),
  email: z.string().trim().email('Use a valid email address.'),
  avatarType: z.string().nullable(),
})
const passwordSetupSchema = z
  .object({
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
  })

const form = ref<ProfileDetailsFormValues>({ ...props.initialValues })
const initialForm = ref<ProfileDetailsFormValues>({ ...props.initialValues })
const touchedFields = ref<Partial<Record<ProfileField, boolean>>>({})
const wasSubmitted = ref(false)
const isPasswordHelpDialogOpen = ref(false)
const passwordSetupForm = ref({
  confirmPassword: '',
  newPassword: '',
})
const passwordSetupTouchedFields = ref<Partial<Record<PasswordSetupField, boolean>>>({})
const wasPasswordSetupSubmitted = ref(false)
const googleLinkClientError = ref('')

const { avatarUrl } = useAccountAvatar(() => form.value.avatarType)

const validationResult = computed(() => profileSchema.safeParse(form.value))
const fieldErrors = computed<Partial<Record<ProfileField, string>>>(() => {
  if (validationResult.value.success) {
    return {}
  }

  return validationResult.value.error.issues.reduce<Partial<Record<ProfileField, string>>>(
    (errors, issue) => {
      const field = issue.path[0]

      if ((field === 'username' || field === 'email') && !errors[field]) {
        errors[field] = issue.message
      }

      return errors
    },
    {},
  )
})
const passwordSetupValidationResult = computed(() =>
  passwordSetupSchema.safeParse(passwordSetupForm.value),
)
const passwordSetupFieldErrors = computed<Partial<Record<PasswordSetupField, string>>>(() => {
  if (passwordSetupValidationResult.value.success) {
    return {}
  }

  return passwordSetupValidationResult.value.error.issues.reduce<
    Partial<Record<PasswordSetupField, string>>
  >((errors, issue) => {
    const field = issue.path[0]

    if ((field === 'newPassword' || field === 'confirmPassword') && !errors[field]) {
      errors[field] = issue.message
    }

    return errors
  }, {})
})
const hasChanges = computed(
  () =>
    form.value.username !== initialForm.value.username ||
    form.value.email !== initialForm.value.email ||
    form.value.avatarType !== initialForm.value.avatarType,
)
const canSave = computed(
  () => hasChanges.value && validationResult.value.success && !props.isPending && !props.isLoading,
)
const avatarAlt = computed(() =>
  form.value.username.trim() ? `${form.value.username.trim()} avatar` : 'User avatar',
)
const googleAccount = computed(
  () => props.socialAccounts?.find((account) => account.provider === 'google') ?? null,
)
const isGoogleLinked = computed(() => Boolean(googleAccount.value))
const canUnlinkGoogle = computed(() => Boolean(googleAccount.value?.can_unlink))
const googleAccountLabel = computed(() => {
  if (!googleAccount.value) {
    return 'Not connected'
  }

  return googleAccount.value.email || 'Connected'
})
const canSubmitPasswordSetup = computed(
  () => passwordSetupValidationResult.value.success && !props.isSettingLocalPassword,
)

watch(canUnlinkGoogle, (canUnlink) => {
  if (canUnlink) {
    closePasswordHelpDialog()
  }
})

watch(isGoogleLinked, (isLinked) => {
  if (isLinked) {
    googleLinkClientError.value = ''
  }
})

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

function resetForm(values: ProfileDetailsFormValues) {
  form.value = { ...values }
  initialForm.value = { ...values }
  touchedFields.value = {}
  wasSubmitted.value = false
}

function touchField(field: ProfileField) {
  touchedFields.value = {
    ...touchedFields.value,
    [field]: true,
  }
}

function shouldShowError(field: ProfileField) {
  return Boolean((wasSubmitted.value || touchedFields.value[field]) && fieldErrors.value[field])
}

function touchPasswordSetupField(field: PasswordSetupField) {
  passwordSetupTouchedFields.value = {
    ...passwordSetupTouchedFields.value,
    [field]: true,
  }
}

function shouldShowPasswordSetupError(field: PasswordSetupField) {
  return Boolean(
    (wasPasswordSetupSubmitted.value || passwordSetupTouchedFields.value[field]) &&
    passwordSetupFieldErrors.value[field],
  )
}

function setAvatarType(avatarType: string) {
  form.value = {
    ...form.value,
    avatarType,
  }
}

function submitForm() {
  wasSubmitted.value = true
  touchedFields.value = {
    email: true,
    username: true,
  }

  if (!canSave.value) {
    return
  }

  emit('submit', {
    avatar_type: form.value.avatarType,
    email: form.value.email.trim(),
    username: form.value.username.trim(),
  })
}

function requestGoogleUnlink() {
  if (!isGoogleLinked.value || props.isUnlinkingGoogle || props.isPending) {
    return
  }

  if (!canUnlinkGoogle.value) {
    isPasswordHelpDialogOpen.value = true
    return
  }

  emit('unlinkGoogleAccount')
}

function linkGoogleAccount(credential: string) {
  googleLinkClientError.value = ''
  emit('linkGoogleAccount', { credential })
}

function setGoogleLinkClientError(message: string) {
  googleLinkClientError.value = message
}

function closePasswordHelpDialog() {
  if (props.isSettingLocalPassword) {
    return
  }

  isPasswordHelpDialogOpen.value = false
  passwordSetupForm.value = {
    confirmPassword: '',
    newPassword: '',
  }
  passwordSetupTouchedFields.value = {}
  wasPasswordSetupSubmitted.value = false
}

function submitPasswordSetup() {
  wasPasswordSetupSubmitted.value = true
  passwordSetupTouchedFields.value = {
    confirmPassword: true,
    newPassword: true,
  }

  if (!canSubmitPasswordSetup.value) {
    return
  }

  emit('setLocalPassword', {
    new_password: passwordSetupForm.value.newPassword,
    password_confirm: passwordSetupForm.value.confirmPassword,
  })
}

defineExpose({
  getAvatarType: () => form.value.avatarType,
  setAvatarType,
})
</script>

<template>
  <form
    class="rounded-3xl bg-white p-2 shadow-[0_0_0_1px_rgb(15_23_42_/_6%),0_10px_28px_rgb(15_23_42_/_5%)]"
    novalidate
    @submit.prevent="submitForm"
  >
    <div class="rounded-2xl bg-slate-50/80 p-4 sm:p-5 md:p-6">
      <header class="flex flex-col gap-2 sm:flex-row sm:items-start sm:justify-between">
        <div>
          <p class="text-xs leading-4 font-semibold tracking-[0.12em] text-blue-600 uppercase">
            Profile
          </p>
          <h2 class="mt-1 text-lg leading-6 font-semibold text-balance text-slate-950">
            Personal information
          </h2>
          <p class="mt-1 max-w-2xl text-sm leading-6 font-medium text-pretty text-slate-500">
            Keep your workspace identity recognizable for collaborators and activity history.
          </p>
        </div>
      </header>

      <div v-if="isLoading" class="mt-6 grid gap-3" aria-label="Loading profile form">
        <span class="h-20 rounded-2xl bg-white"></span>
        <span class="h-20 rounded-2xl bg-white"></span>
        <span class="h-20 rounded-2xl bg-white"></span>
      </div>

      <div v-else class="mt-6 grid gap-3">
        <div
          class="grid gap-4 rounded-2xl bg-white p-4 shadow-[0_0_0_1px_rgb(15_23_42_/_5%)] md:grid-cols-[minmax(0,1fr)_minmax(260px,360px)] md:items-center"
        >
          <div>
            <span class="text-sm leading-5 font-semibold text-slate-800">Avatar</span>
            <p class="mt-1 text-sm leading-5 font-medium text-pretty text-slate-500">
              Choose a visual marker that makes your account easy to identify.
            </p>
          </div>

          <div class="flex items-center justify-between gap-3 md:justify-end">
            <span
              class="grid size-14 shrink-0 place-items-center overflow-hidden rounded-2xl bg-slate-100 text-slate-500"
            >
              <img
                v-if="avatarUrl"
                class="size-full object-cover outline outline-1 -outline-offset-1 outline-black/10"
                :src="avatarUrl"
                :alt="avatarAlt"
              />
              <UserRound v-else :size="22" :stroke-width="2" aria-hidden="true" />
            </span>

            <button
              class="inline-flex min-h-10 cursor-pointer items-center justify-center gap-2 rounded-xl bg-white px-3.5 text-sm font-semibold text-blue-700 outline-none shadow-[0_0_0_1px_rgb(147_197_253_/_90%)] transition-[background-color,color,scale,box-shadow] duration-150 ease-out hover:bg-blue-50 hover:text-blue-800 hover:shadow-[0_0_0_1px_rgb(96_165_250),0_8px_18px_rgb(37_99_235_/_10%)] focus-visible:ring-4 focus-visible:ring-blue-100 active:scale-[0.96] disabled:cursor-not-allowed disabled:bg-slate-50 disabled:text-slate-400 disabled:opacity-80 disabled:shadow-[0_0_0_1px_rgb(203_213_225_/_90%)] motion-reduce:transition-none"
              type="button"
              :disabled="isPending"
              @click="emit('openAvatarDialog')"
            >
              <ImagePlus :size="15" :stroke-width="2.2" aria-hidden="true" />
              Choose
            </button>
          </div>
        </div>

        <label
          class="grid gap-4 rounded-2xl bg-white p-4 shadow-[0_0_0_1px_rgb(15_23_42_/_5%)] md:grid-cols-[minmax(0,1fr)_minmax(260px,360px)] md:items-start"
        >
          <span>
            <span class="text-sm leading-5 font-semibold text-slate-800">Username</span>
            <span class="mt-1 block text-sm leading-5 font-medium text-pretty text-slate-500">
              This name appears in menus, ownership labels, and workspace activity.
            </span>
          </span>
          <span class="grid gap-2">
            <input
              v-model="form.username"
              class="min-h-11 w-full rounded-xl border bg-white px-3 text-sm font-medium text-slate-950 outline-none transition-[border-color,box-shadow] duration-150 placeholder:text-slate-400 focus:border-blue-300 focus:shadow-[0_0_0_4px_rgb(219_234_254_/_85%)] disabled:cursor-not-allowed disabled:bg-slate-50"
              :class="shouldShowError('username') ? 'border-red-200' : 'border-slate-200/80'"
              type="text"
              name="username"
              autocomplete="username"
              :aria-invalid="shouldShowError('username')"
              aria-describedby="profile-username-error"
              :disabled="isPending"
              @blur="touchField('username')"
            />
            <span
              v-if="shouldShowError('username')"
              id="profile-username-error"
              class="text-xs leading-4 font-medium text-red-600"
              role="alert"
            >
              {{ fieldErrors.username }}
            </span>
          </span>
        </label>

        <label
          class="grid gap-4 rounded-2xl bg-white p-4 shadow-[0_0_0_1px_rgb(15_23_42_/_5%)] md:grid-cols-[minmax(0,1fr)_minmax(260px,360px)] md:items-start"
        >
          <span>
            <span class="text-sm leading-5 font-semibold text-slate-800">Email address</span>
            <span class="mt-1 block text-sm leading-5 font-medium text-pretty text-slate-500">
              Used for authentication, account recovery, and important product notices.
            </span>
          </span>
          <span class="grid gap-2">
            <input
              v-model="form.email"
              class="min-h-11 w-full rounded-xl border bg-white px-3 text-sm font-medium text-slate-950 outline-none transition-[border-color,box-shadow] duration-150 placeholder:text-slate-400 focus:border-blue-300 focus:shadow-[0_0_0_4px_rgb(219_234_254_/_85%)] disabled:cursor-not-allowed disabled:bg-slate-50"
              :class="shouldShowError('email') ? 'border-red-200' : 'border-slate-200/80'"
              type="email"
              name="email"
              autocomplete="email"
              :aria-invalid="shouldShowError('email')"
              aria-describedby="profile-email-error"
              :disabled="isPending"
              @blur="touchField('email')"
            />
            <span
              v-if="shouldShowError('email')"
              id="profile-email-error"
              class="text-xs leading-4 font-medium text-red-600"
              role="alert"
            >
              {{ fieldErrors.email }}
            </span>
          </span>
        </label>

        <section
          class="grid gap-4 rounded-2xl bg-white p-4 shadow-[0_0_0_1px_rgb(15_23_42_/_5%)] md:grid-cols-[minmax(0,1fr)_minmax(260px,360px)] md:items-center"
          aria-labelledby="linked-accounts-title"
        >
          <div>
            <span id="linked-accounts-title" class="text-sm leading-5 font-semibold text-slate-800">
              Linked accounts
            </span>
            <p class="mt-1 text-sm leading-5 font-medium text-pretty text-slate-500">
              Google sign-in access for this profile.
            </p>
          </div>

          <div class="grid gap-3">
            <div
              class="flex min-w-0 items-center justify-between gap-3 rounded-2xl bg-slate-50 p-2 shadow-[inset_0_0_0_1px_rgb(15_23_42_/_5%)] sm:p-2.5"
            >
              <div class="flex min-w-0 items-center gap-3">
                <span
                  class="grid size-10 shrink-0 place-items-center rounded-xl bg-white shadow-[0_0_0_1px_rgb(15_23_42_/_7%)]"
                >
                  <img class="size-5" :src="googleLogo" alt="" aria-hidden="true" />
                </span>
                <span class="min-w-0">
                  <span class="block text-sm leading-5 font-semibold text-slate-900">Google</span>
                  <span
                    class="block truncate text-xs leading-4 font-medium"
                    :class="isGoogleLinked ? 'text-emerald-600' : 'text-slate-500'"
                    aria-live="polite"
                  >
                    {{ googleAccountLabel }}
                  </span>
                </span>
              </div>

              <button
                v-if="isGoogleLinked"
                class="inline-flex min-h-10 shrink-0 cursor-pointer items-center justify-center gap-2 rounded-xl border-0 bg-white px-3 text-sm font-semibold text-red-700 shadow-[0_0_0_1px_rgb(254_202_202_/_95%)] outline-none transition-[background-color,color,scale,opacity,box-shadow] duration-150 ease-out hover:bg-red-50 hover:text-red-800 hover:shadow-[0_0_0_1px_rgb(248_113_113),0_8px_18px_rgb(220_38_38_/_10%)] focus-visible:ring-4 focus-visible:ring-red-100 active:scale-[0.96] disabled:cursor-not-allowed disabled:opacity-70 motion-reduce:transition-none"
                type="button"
                :disabled="isUnlinkingGoogle || isPending"
                @click="requestGoogleUnlink"
              >
                <LoaderCircle
                  v-if="isUnlinkingGoogle"
                  class="size-4 animate-spin"
                  :stroke-width="2.2"
                  aria-hidden="true"
                />
                <Unlink2 v-else :size="15" :stroke-width="2.2" aria-hidden="true" />
                {{ isUnlinkingGoogle ? 'Disconnecting' : 'Disconnect' }}
              </button>

              <GoogleButton
                v-else
                class="max-w-40 shrink-0"
                label="Connect"
                :is-pending="isLinkingGoogle || isPending"
                @credential="linkGoogleAccount"
                @error="setGoogleLinkClientError"
              />
            </div>

            <p
              v-if="googleLinkClientError"
              class="rounded-xl border border-red-100 bg-red-50 px-3 py-2.5 text-sm leading-5 font-medium text-red-700"
              role="alert"
            >
              {{ googleLinkClientError }}
            </p>
          </div>
        </section>
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

      <footer class="mt-6 flex justify-end border-t border-slate-200/70 pt-5">
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
          Save profile
        </button>
      </footer>
    </div>

    <Teleport to="body">
      <Transition name="password-help-dialog">
        <div
          v-if="isPasswordHelpDialogOpen"
          class="fixed inset-0 z-50 grid place-items-center bg-slate-950/35 px-4 py-6 backdrop-blur-sm"
          role="presentation"
          @click.self="closePasswordHelpDialog"
        >
          <section
            class="w-full max-w-lg rounded-3xl bg-white p-2 shadow-[0_22px_70px_rgb(15_23_42_/_24%),0_0_0_1px_rgb(15_23_42_/_8%)]"
            role="dialog"
            aria-modal="true"
            aria-labelledby="password-help-title"
            aria-describedby="password-help-description"
          >
            <form
              class="rounded-2xl bg-slate-50/80 p-4 sm:p-5"
              novalidate
              @submit.prevent="submitPasswordSetup"
            >
              <header class="flex items-start justify-between gap-4">
                <div class="min-w-0">
                  <span
                    class="inline-flex size-10 items-center justify-center rounded-xl bg-amber-50 text-amber-700 shadow-[0_0_0_1px_rgb(253_230_138_/_95%)]"
                  >
                    <ShieldAlert :size="19" :stroke-width="2.2" aria-hidden="true" />
                  </span>
                  <h2
                    id="password-help-title"
                    class="mt-4 text-lg leading-6 font-semibold text-balance text-slate-950"
                  >
                    Add a password before disconnecting Google
                  </h2>
                  <p
                    id="password-help-description"
                    class="mt-2 text-sm leading-6 font-medium text-pretty text-slate-600"
                  >
                    Google is currently your only sign-in method. Create a local password first;
                    after it is saved, you can disconnect Google without losing access.
                  </p>
                </div>

                <button
                  class="inline-flex min-h-10 min-w-10 shrink-0 cursor-pointer items-center justify-center rounded-xl bg-white text-slate-500 outline-none shadow-[0_0_0_1px_rgb(203_213_225_/_90%)] transition-[background-color,color,scale,box-shadow] duration-150 hover:bg-slate-100 hover:text-slate-800 focus-visible:ring-4 focus-visible:ring-blue-100 active:scale-[0.96] disabled:cursor-not-allowed disabled:opacity-60 motion-reduce:transition-none"
                  type="button"
                  :disabled="isSettingLocalPassword"
                  aria-label="Close password help"
                  @click="closePasswordHelpDialog"
                >
                  <X :size="16" :stroke-width="2.3" aria-hidden="true" />
                </button>
              </header>

              <div class="mt-5 grid gap-3">
                <label class="grid gap-2" for="google-unlink-new-password">
                  <span class="text-sm leading-5 font-semibold text-slate-800">New password</span>
                  <input
                    id="google-unlink-new-password"
                    v-model="passwordSetupForm.newPassword"
                    class="min-h-11 w-full rounded-xl border bg-white px-3 text-sm font-medium text-slate-950 outline-none transition-[border-color,box-shadow] duration-150 placeholder:text-slate-400 focus:border-blue-300 focus:shadow-[0_0_0_4px_rgb(219_234_254_/_85%)] disabled:cursor-not-allowed disabled:bg-slate-50"
                    :class="
                      shouldShowPasswordSetupError('newPassword')
                        ? 'border-red-200'
                        : 'border-slate-200/80'
                    "
                    type="password"
                    name="newPassword"
                    autocomplete="new-password"
                    placeholder="Create a secure password"
                    :aria-invalid="shouldShowPasswordSetupError('newPassword')"
                    aria-describedby="google-unlink-new-password-help google-unlink-new-password-error"
                    :disabled="isSettingLocalPassword"
                    @blur="touchPasswordSetupField('newPassword')"
                  />
                  <span
                    v-if="!shouldShowPasswordSetupError('newPassword')"
                    id="google-unlink-new-password-help"
                    class="text-xs leading-4 font-medium text-slate-500"
                  >
                    Use at least 8 characters, one uppercase letter, and one number.
                  </span>
                  <span
                    v-if="shouldShowPasswordSetupError('newPassword')"
                    id="google-unlink-new-password-error"
                    class="text-xs leading-4 font-medium text-red-600"
                    role="alert"
                  >
                    {{ passwordSetupFieldErrors.newPassword }}
                  </span>
                </label>

                <label class="grid gap-2" for="google-unlink-confirm-password">
                  <span class="text-sm leading-5 font-semibold text-slate-800">
                    Confirm password
                  </span>
                  <input
                    id="google-unlink-confirm-password"
                    v-model="passwordSetupForm.confirmPassword"
                    class="min-h-11 w-full rounded-xl border bg-white px-3 text-sm font-medium text-slate-950 outline-none transition-[border-color,box-shadow] duration-150 placeholder:text-slate-400 focus:border-blue-300 focus:shadow-[0_0_0_4px_rgb(219_234_254_/_85%)] disabled:cursor-not-allowed disabled:bg-slate-50"
                    :class="
                      shouldShowPasswordSetupError('confirmPassword')
                        ? 'border-red-200'
                        : 'border-slate-200/80'
                    "
                    type="password"
                    name="confirmPassword"
                    autocomplete="new-password"
                    placeholder="Repeat the password"
                    :aria-invalid="shouldShowPasswordSetupError('confirmPassword')"
                    aria-describedby="google-unlink-confirm-password-error"
                    :disabled="isSettingLocalPassword"
                    @blur="touchPasswordSetupField('confirmPassword')"
                  />
                  <span
                    v-if="shouldShowPasswordSetupError('confirmPassword')"
                    id="google-unlink-confirm-password-error"
                    class="text-xs leading-4 font-medium text-red-600"
                    role="alert"
                  >
                    {{ passwordSetupFieldErrors.confirmPassword }}
                  </span>
                </label>
              </div>

              <p
                v-if="passwordSetupErrorMessage"
                class="mt-4 rounded-xl border border-red-100 bg-red-50 px-3 py-2.5 text-sm leading-5 font-medium text-red-700"
                role="alert"
              >
                {{ passwordSetupErrorMessage }}
              </p>

              <footer
                class="mt-5 flex flex-col-reverse gap-2 border-t border-slate-200/70 pt-4 sm:flex-row sm:justify-end"
              >
                <button
                  class="inline-flex min-h-10 cursor-pointer items-center justify-center rounded-xl bg-white px-4 text-sm font-semibold text-slate-600 outline-none shadow-[0_0_0_1px_rgb(203_213_225_/_90%)] transition-[background-color,color,scale,box-shadow] duration-150 hover:bg-slate-100 hover:text-slate-900 focus-visible:ring-4 focus-visible:ring-blue-100 active:scale-[0.96] disabled:cursor-not-allowed disabled:opacity-60 motion-reduce:transition-none"
                  type="button"
                  :disabled="isSettingLocalPassword"
                  @click="closePasswordHelpDialog"
                >
                  Cancel
                </button>
                <button
                  class="inline-flex min-h-10 cursor-pointer items-center justify-center gap-2 rounded-xl bg-blue-600 px-4 text-sm font-semibold text-white outline-none transition-[background-color,scale,opacity,box-shadow] duration-150 hover:bg-blue-700 focus-visible:ring-4 focus-visible:ring-blue-100 active:scale-[0.96] disabled:cursor-not-allowed disabled:opacity-50 motion-reduce:transition-none"
                  type="submit"
                  :disabled="!canSubmitPasswordSetup"
                >
                  <LoaderCircle
                    v-if="isSettingLocalPassword"
                    class="size-4 animate-spin"
                    :stroke-width="2.2"
                    aria-hidden="true"
                  />
                  <KeyRound v-else :size="15" :stroke-width="2.2" aria-hidden="true" />
                  Save password
                </button>
              </footer>
            </form>
          </section>
        </div>
      </Transition>
    </Teleport>
  </form>
</template>

<style scoped>
.password-help-dialog-enter-active,
.password-help-dialog-leave-active {
  transition:
    opacity 160ms ease-out,
    transform 160ms ease-out;
}

.password-help-dialog-enter-from,
.password-help-dialog-leave-to {
  opacity: 0;
  transform: translateY(8px);
}

@media (prefers-reduced-motion: reduce) {
  .password-help-dialog-enter-active,
  .password-help-dialog-leave-active {
    transition: none;
  }
}
</style>
