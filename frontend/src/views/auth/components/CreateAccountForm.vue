<script setup lang="ts">
import { computed, ref, shallowRef } from 'vue'
import { Check, Eye, EyeOff, Loader2, UserRound, X } from '@lucide/vue'
import { z } from 'zod'

import type { AccountRegistrationPayload } from '@/domains/accounts/contracts'

defineProps<{
  errorMessage?: string
  isPending?: boolean
  successMessage?: string
}>()

const emit = defineEmits<{
  submit: [payload: AccountRegistrationPayload]
}>()

const avatarModules = import.meta.glob<string>('@/assets/img/avatar/*.{png,jpg,jpeg,webp,svg}', {
  eager: true,
  import: 'default',
  query: '?url',
})

const avatars = Object.entries(avatarModules)
  .map(([path, src]) => {
    const fileName = path.split('/').pop() ?? ''
    const id = fileName.replace(/\.[^.]+$/, '')

    return {
      id,
      label: `Avatar ${id}`,
      src,
    }
  })
  .sort((current, next) => current.id.localeCompare(next.id, undefined, { numeric: true }))

const formSchema = z
  .object({
    username: z
      .string()
      .trim()
      .min(1, 'Enter a username to continue.')
      .max(150, 'Use 150 characters or fewer.')
      .regex(/^[\w.@+-]+$/u, 'Use letters, numbers, and @ . + - _ only.'),
    email: z
      .string()
      .trim()
      .min(1, 'Enter an email address to continue.')
      .email('Enter a valid email address.'),
    password: z
      .string()
      .min(8, 'Use at least 8 characters.')
      .regex(/[^\w\s]/u, 'Use at least one special character.'),
    confirmPassword: z.string().min(1, 'Confirm your password to continue.'),
    avatarType: z.string().optional(),
  })
  .refine((data) => data.password === data.confirmPassword, {
    path: ['confirmPassword'],
    message: 'Passwords do not match.',
  })

type FieldName = 'username' | 'email' | 'password' | 'confirmPassword'
type FormValues = z.input<typeof formSchema>

const values = ref<FormValues>({
  username: '',
  email: '',
  password: '',
  confirmPassword: '',
  avatarType: '',
})
const wasSubmitted = ref(false)
const showPassword = ref(false)
const showConfirmPassword = ref(false)
const isAvatarDialogOpen = shallowRef(false)

const selectedAvatar = computed(() =>
  avatars.find((avatar) => avatar.id === values.value.avatarType),
)

const validationResult = computed(() => formSchema.safeParse(values.value))

const fieldErrors = computed<Record<FieldName, string>>(() => {
  const errors: Record<FieldName, string> = {
    username: '',
    email: '',
    password: '',
    confirmPassword: '',
  }

  if (validationResult.value.success) {
    return errors
  }

  for (const issue of validationResult.value.error.issues) {
    const fieldName = issue.path[0]

    if (typeof fieldName === 'string' && isFieldName(fieldName) && !errors[fieldName]) {
      errors[fieldName] = issue.message
    }
  }

  return errors
})

const visibleFieldErrors = computed<Record<FieldName, string>>(() => ({
  username: shouldShowError('username') ? fieldErrors.value.username : '',
  email: shouldShowError('email') ? fieldErrors.value.email : '',
  password: shouldShowError('password') ? fieldErrors.value.password : '',
  confirmPassword: shouldShowError('confirmPassword') ? fieldErrors.value.confirmPassword : '',
}))

function isFieldName(value: string): value is FieldName {
  return ['username', 'email', 'password', 'confirmPassword'].includes(value)
}

function shouldShowError(fieldName: FieldName) {
  return wasSubmitted.value && Boolean(fieldErrors.value[fieldName])
}

function selectAvatar(avatarId: string) {
  values.value.avatarType = avatarId
  isAvatarDialogOpen.value = false
}

function clearAvatar() {
  values.value.avatarType = ''
  isAvatarDialogOpen.value = false
}

function submitForm() {
  wasSubmitted.value = true

  const result = formSchema.safeParse(values.value)

  if (!result.success) {
    return
  }

  emit('submit', {
    username: result.data.username,
    email: result.data.email.toLowerCase(),
    password: result.data.password,
    password_confirm: result.data.confirmPassword,
    avatar_type: result.data.avatarType || null,
  })
}
</script>

<template>
  <form class="grid gap-4" novalidate @submit.prevent="submitForm">
    <section class="flex items-center gap-3 border-b border-slate-200 pb-4 max-[520px]:flex-wrap">
      <button
        class="grid size-16 shrink-0 cursor-pointer place-items-center overflow-hidden rounded-2xl border border-slate-200 bg-white text-[#62777d] outline outline-1 outline-black/10 transition-[border-color,box-shadow,transform] duration-180 hover:border-[#8adff3] hover:shadow-[0_0_0_4px_rgb(174_238_255_/_18%)] active:scale-[0.96] focus-visible:outline focus-visible:outline-3 focus-visible:outline-offset-3 focus-visible:outline-[#aeeeff]/70 motion-reduce:transition-none"
        type="button"
        aria-haspopup="dialog"
        :aria-expanded="isAvatarDialogOpen"
        :aria-label="selectedAvatar ? 'Change selected avatar' : 'Choose profile avatar'"
        @click="isAvatarDialogOpen = true"
      >
        <img
          v-if="selectedAvatar"
          class="size-full object-cover"
          :src="selectedAvatar.src"
          :alt="selectedAvatar.label"
        />
        <UserRound v-else :size="24" :stroke-width="1.9" aria-hidden="true" />
      </button>

      <div class="min-w-0 flex-1">
        <div class="flex flex-wrap items-center gap-x-2 gap-y-1">
          <p class="m-0 text-sm font-extrabold leading-5 text-[#172224]">Profile avatar</p>
          <span class="text-xs font-bold leading-4 text-[#7a8f94]">Optional</span>
        </div>
        <p class="m-0 text-xs font-bold leading-4 text-[#62777d]">
          {{ selectedAvatar ? selectedAvatar.label : 'No avatar selected' }}
        </p>
      </div>

      <div class="flex shrink-0 items-center gap-2 max-[520px]:ml-[76px]">
        <button
          class="inline-flex min-h-9 cursor-pointer items-center justify-center rounded-xl border border-slate-200 bg-white px-3 text-xs font-black text-[#172224] transition-[border-color,color,transform] duration-180 hover:border-[#8adff3] hover:text-[#246b78] active:scale-[0.96] focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#aeeeff] motion-reduce:transition-none"
          type="button"
          @click="isAvatarDialogOpen = true"
        >
          {{ selectedAvatar ? 'Change' : 'Choose' }}
        </button>
        <button
          v-if="selectedAvatar"
          class="inline-flex min-h-9 cursor-pointer items-center justify-center rounded-xl border border-transparent bg-white px-2.5 text-xs font-black text-[#7a8f94] transition-[color,transform] duration-180 hover:text-[#9f2f25] active:scale-[0.96] focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#aeeeff] motion-reduce:transition-none"
          type="button"
          @click="clearAvatar"
        >
          Remove
        </button>
      </div>
    </section>

    <div class="grid gap-4">
      <div class="grid grid-cols-2 gap-x-3 gap-y-4 max-[620px]:grid-cols-1">
        <label class="grid gap-1.5" for="username">
          <span class="text-xs font-extrabold leading-none text-[#172224]">
            Username <span class="text-[#9f2f25]" aria-hidden="true">*</span>
          </span>
          <input
            id="username"
            v-model="values.username"
            class="min-h-10 w-full rounded-xl border bg-white px-3 text-sm font-bold text-[#172224] outline-none transition-[border-color,box-shadow] duration-180 placeholder:text-[#9aaeb2] focus:border-[#8adff3] focus:shadow-[0_0_0_3px_rgb(174_238_255_/_18%)] motion-reduce:transition-none"
            :class="visibleFieldErrors.username ? 'border-[#d7786f]' : 'border-slate-200'"
            name="username"
            type="text"
            autocomplete="username"
            placeholder="marina.silva"
            required
            :aria-invalid="Boolean(visibleFieldErrors.username)"
            aria-describedby="username-error"
          />
          <p
            v-if="visibleFieldErrors.username"
            id="username-error"
            class="m-0 text-xs font-bold leading-4 text-[#9f2f25]"
            role="alert"
          >
            {{ visibleFieldErrors.username }}
          </p>
        </label>

        <label class="grid gap-1.5" for="email">
          <span class="text-xs font-extrabold leading-none text-[#172224]">
            Email <span class="text-[#9f2f25]" aria-hidden="true">*</span>
          </span>
          <input
            id="email"
            v-model="values.email"
            class="min-h-10 w-full rounded-xl border bg-white px-3 text-sm font-bold text-[#172224] outline-none transition-[border-color,box-shadow] duration-180 placeholder:text-[#9aaeb2] focus:border-[#8adff3] focus:shadow-[0_0_0_3px_rgb(174_238_255_/_18%)] motion-reduce:transition-none"
            :class="visibleFieldErrors.email ? 'border-[#d7786f]' : 'border-slate-200'"
            name="email"
            type="email"
            autocomplete="email"
            placeholder="you@example.com"
            required
            :aria-invalid="Boolean(visibleFieldErrors.email)"
            aria-describedby="email-error"
          />
          <p
            v-if="visibleFieldErrors.email"
            id="email-error"
            class="m-0 text-xs font-bold leading-4 text-[#9f2f25]"
            role="alert"
          >
            {{ visibleFieldErrors.email }}
          </p>
        </label>

        <label class="grid gap-1.5" for="password">
          <span class="text-xs font-extrabold leading-none text-[#172224]">
            Password <span class="text-[#9f2f25]" aria-hidden="true">*</span>
          </span>
          <span class="relative block">
            <input
              id="password"
              v-model="values.password"
              class="min-h-10 w-full rounded-xl border bg-white px-3 pr-11 text-sm font-bold text-[#172224] outline-none transition-[border-color,box-shadow] duration-180 placeholder:text-[#9aaeb2] focus:border-[#8adff3] focus:shadow-[0_0_0_3px_rgb(174_238_255_/_18%)] motion-reduce:transition-none"
              :class="visibleFieldErrors.password ? 'border-[#d7786f]' : 'border-slate-200'"
              name="password"
              :type="showPassword ? 'text' : 'password'"
              autocomplete="new-password"
              placeholder="Strong password"
              required
              :aria-invalid="Boolean(visibleFieldErrors.password)"
              aria-describedby="password-help password-error"
            />
            <button
              class="absolute right-1.5 top-1/2 inline-flex size-8 -translate-y-1/2 cursor-pointer items-center justify-center rounded-lg border-0 bg-transparent text-[#7a8f94] transition-[background-color,color,transform] duration-180 hover:bg-[#eef7f9] hover:text-[#246b78] active:scale-[0.96] focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#aeeeff] motion-reduce:transition-none"
              type="button"
              :aria-label="showPassword ? 'Hide password' : 'Show password'"
              :aria-pressed="showPassword"
              @click="showPassword = !showPassword"
            >
              <EyeOff v-if="showPassword" :size="16" :stroke-width="2.2" aria-hidden="true" />
              <Eye v-else :size="16" :stroke-width="2.2" aria-hidden="true" />
            </button>
          </span>
          <p
            v-if="!visibleFieldErrors.password"
            id="password-help"
            class="m-0 text-xs font-bold leading-4 text-[#62777d]"
          >
            Use 8+ characters and one special character.
          </p>
          <p
            v-if="visibleFieldErrors.password"
            id="password-error"
            class="m-0 text-xs font-bold leading-4 text-[#9f2f25]"
            role="alert"
          >
            {{ visibleFieldErrors.password }}
          </p>
        </label>

        <label class="grid gap-1.5 content-start" for="confirmPassword">
          <span class="text-xs font-extrabold leading-none text-[#172224]">
            Confirm password <span class="text-[#9f2f25]" aria-hidden="true">*</span>
          </span>
          <span class="relative block">
            <input
              id="confirmPassword"
              v-model="values.confirmPassword"
              class="min-h-10 w-full rounded-xl border bg-white px-3 pr-11 text-sm font-bold text-[#172224] outline-none transition-[border-color,box-shadow] duration-180 placeholder:text-[#9aaeb2] focus:border-[#8adff3] focus:shadow-[0_0_0_3px_rgb(174_238_255_/_18%)] motion-reduce:transition-none"
              :class="visibleFieldErrors.confirmPassword ? 'border-[#d7786f]' : 'border-slate-200'"
              name="confirmPassword"
              :type="showConfirmPassword ? 'text' : 'password'"
              autocomplete="new-password"
              placeholder="Repeat password"
              required
              :aria-invalid="Boolean(visibleFieldErrors.confirmPassword)"
              aria-describedby="confirm-password-error"
            />
            <button
              class="absolute right-1.5 top-1/2 inline-flex size-8 -translate-y-1/2 cursor-pointer items-center justify-center rounded-lg border-0 bg-transparent text-[#7a8f94] transition-[background-color,color,transform] duration-180 hover:bg-[#eef7f9] hover:text-[#246b78] active:scale-[0.96] focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#aeeeff] motion-reduce:transition-none"
              type="button"
              :aria-label="
                showConfirmPassword ? 'Hide password confirmation' : 'Show password confirmation'
              "
              :aria-pressed="showConfirmPassword"
              @click="showConfirmPassword = !showConfirmPassword"
            >
              <EyeOff
                v-if="showConfirmPassword"
                :size="16"
                :stroke-width="2.2"
                aria-hidden="true"
              />
              <Eye v-else :size="16" :stroke-width="2.2" aria-hidden="true" />
            </button>
          </span>
          <p
            v-if="visibleFieldErrors.confirmPassword"
            id="confirm-password-error"
            class="m-0 text-xs font-bold leading-4 text-[#9f2f25]"
            role="alert"
          >
            {{ visibleFieldErrors.confirmPassword }}
          </p>
        </label>
      </div>
    </div>

    <p
      v-if="errorMessage"
      class="m-0 rounded-xl bg-[#fff1f0] px-3.5 py-3 text-sm font-bold leading-5 text-[#9f2f25] shadow-[inset_0_0_0_1px_rgb(159_47_37_/_14%)]"
      role="alert"
    >
      {{ errorMessage }}
    </p>

    <p
      v-if="successMessage"
      class="m-0 inline-flex items-start gap-2 rounded-xl bg-[#effaf4] px-3.5 py-3 text-sm font-bold leading-5 text-[#166534] shadow-[inset_0_0_0_1px_rgb(22_101_52_/_14%)]"
      role="status"
    >
      <Check class="mt-0.5 shrink-0" :size="16" :stroke-width="2.4" aria-hidden="true" />
      {{ successMessage }}
    </p>

    <button
      class="inline-flex min-h-10 w-full cursor-pointer items-center justify-center gap-2 rounded-xl border border-[#2b7f8f] bg-[#246b78] px-4 text-sm font-black leading-none text-white shadow-[0_12px_24px_rgb(18_33_36_/_14%),inset_0_1px_0_rgb(255_255_255_/_14%)] transition-[transform,border-color,background-color,box-shadow,opacity] duration-180 hover:-translate-y-px hover:border-[#236575] hover:bg-[#1f5f6d] hover:shadow-[0_14px_28px_rgb(18_33_36_/_18%),inset_0_1px_0_rgb(255_255_255_/_16%)] active:scale-[0.96] disabled:cursor-not-allowed disabled:opacity-60 disabled:hover:translate-y-0 focus-visible:outline focus-visible:outline-3 focus-visible:outline-offset-3 focus-visible:outline-[#aeeeff]/70 motion-reduce:transition-none motion-reduce:hover:translate-y-0"
      type="submit"
      :disabled="isPending"
    >
      <Loader2
        v-if="isPending"
        class="animate-spin"
        :size="16"
        :stroke-width="2.4"
        aria-hidden="true"
      />
      {{ isPending ? 'Creating account...' : 'Create account' }}
    </button>
  </form>

  <Teleport to="body">
    <div
      v-if="isAvatarDialogOpen"
      class="fixed inset-0 z-50 grid place-items-center bg-[#071113]/42 px-5 py-8 backdrop-blur-[6px]"
      role="presentation"
      @click.self="isAvatarDialogOpen = false"
      @keydown.esc="isAvatarDialogOpen = false"
    >
      <section
        class="w-full max-w-[520px] rounded-2xl border border-slate-200 bg-white p-5 text-left shadow-[0_28px_80px_rgb(7_17_19_/_22%)]"
        role="dialog"
        aria-modal="true"
        aria-labelledby="avatar-dialog-title"
      >
        <header class="flex items-start justify-between gap-4">
          <div>
            <h2 id="avatar-dialog-title" class="m-0 text-xl font-black text-[#071113]">
              Choose avatar
            </h2>
            <p class="mt-2 text-sm font-bold leading-5 text-[#62777d]">
              Pick a profile image for this account.
            </p>
          </div>

          <button
            class="inline-flex size-10 cursor-pointer items-center justify-center rounded-xl border border-slate-200 bg-white text-[#62777d] transition-[border-color,color,transform] duration-180 hover:border-[#8adff3] hover:text-[#246b78] active:scale-[0.96] focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#aeeeff] motion-reduce:transition-none"
            type="button"
            aria-label="Close avatar dialog"
            @click="isAvatarDialogOpen = false"
          >
            <X :size="17" :stroke-width="2.4" aria-hidden="true" />
          </button>
        </header>

        <div class="mt-5 grid grid-cols-5 gap-3 max-[520px]:grid-cols-3" role="list">
          <button
            class="group grid min-h-24 cursor-pointer justify-items-center gap-2 rounded-xl border bg-white p-2.5 text-xs font-black text-[#62777d] transition-[border-color,box-shadow,transform,color] duration-180 hover:border-[#8adff3] hover:text-[#172224] hover:shadow-[0_0_0_4px_rgb(174_238_255_/_18%)] active:scale-[0.96] focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#aeeeff] motion-reduce:transition-none"
            :class="
              !values.avatarType
                ? 'border-[#246b78] shadow-[0_0_0_4px_rgb(174_238_255_/_22%)]'
                : 'border-slate-200'
            "
            type="button"
            role="listitem"
            :aria-pressed="!values.avatarType"
            @click="clearAvatar"
          >
            <span
              class="grid size-14 place-items-center rounded-xl bg-[#f7fbfc] text-[#62777d] outline outline-1 outline-black/10"
            >
              <UserRound :size="24" :stroke-width="1.9" aria-hidden="true" />
            </span>
            <span>None</span>
          </button>

          <button
            v-for="avatar in avatars"
            :key="avatar.id"
            class="group grid min-h-24 cursor-pointer justify-items-center gap-2 rounded-xl border bg-white p-2.5 text-xs font-black text-[#62777d] transition-[border-color,box-shadow,transform,color] duration-180 hover:border-[#8adff3] hover:text-[#172224] hover:shadow-[0_0_0_4px_rgb(174_238_255_/_18%)] active:scale-[0.96] focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#aeeeff] motion-reduce:transition-none"
            :class="
              values.avatarType === avatar.id
                ? 'border-[#246b78] shadow-[0_0_0_4px_rgb(174_238_255_/_22%)]'
                : 'border-slate-200'
            "
            type="button"
            role="listitem"
            :aria-pressed="values.avatarType === avatar.id"
            @click="selectAvatar(avatar.id)"
          >
            <img
              class="size-14 rounded-xl object-cover outline outline-1 outline-black/10"
              :src="avatar.src"
              :alt="avatar.label"
            />
            <span>{{ avatar.id }}</span>
          </button>
        </div>
      </section>
    </div>
  </Teleport>
</template>
