<script setup lang="ts">
import { computed, ref } from 'vue'
import { Eye, EyeOff } from '@lucide/vue'

import type { LoginCredentials } from '@/domains/auth/contracts'

defineProps<{
  errorMessage?: string
  isPending?: boolean
}>()

const emit = defineEmits<{
  submit: [credentials: LoginCredentials]
}>()

const showPassword = ref(false)
const identifier = ref('')
const password = ref('')
const wasSubmitted = ref(false)

const fieldErrors = computed(() => ({
  identifier: identifier.value.trim() ? '' : 'Enter your email to continue.',
  password: password.value ? '' : 'Enter your password to continue.',
}))

const visibleFieldErrors = computed(() => {
  if (!wasSubmitted.value) {
    return {
      identifier: '',
      password: '',
    }
  }

  return fieldErrors.value
})

function submitForm() {
  wasSubmitted.value = true

  if (fieldErrors.value.identifier || fieldErrors.value.password) {
    return
  }

  emit('submit', {
    identifier: identifier.value.trim(),
    password: password.value,
  })
}
</script>

<template>
  <form class="grid gap-4" novalidate @submit.prevent="submitForm">
    <label class="grid gap-2" for="identifier">
      <span class="text-xs font-extrabold leading-none text-[#172224]">Email</span>
      <input
        id="identifier"
        v-model.trim="identifier"
        class="min-h-11 w-full rounded-lg border border-[#d8e6e9] bg-white px-3.5 text-sm font-bold text-[#172224] shadow-[0_8px_18px_rgb(18_33_36_/_5%),inset_0_1px_0_rgb(255_255_255_/_92%)] outline-none transition-[border-color,box-shadow] duration-180 placeholder:text-[#9aaeb2] focus:border-[#8adff3] focus:shadow-[0_0_0_4px_rgb(174_238_255_/_26%),0_10px_24px_rgb(18_33_36_/_7%)]"
        name="identifier"
        type="email"
        autocomplete="email"
        placeholder="you@example.com"
        :aria-invalid="Boolean(visibleFieldErrors.identifier)"
        aria-describedby="identifier-error"
      />
      <p
        v-if="visibleFieldErrors.identifier"
        id="identifier-error"
        class="m-0 text-xs font-bold leading-4 text-[#9f2f25]"
        role="alert"
      >
        {{ visibleFieldErrors.identifier }}
      </p>
    </label>

    <label class="grid gap-2" for="password">
      <span class="text-xs font-extrabold leading-none text-[#172224]">Password</span>
      <span class="relative block">
        <input
          id="password"
          v-model="password"
          class="auth-password-input min-h-11 w-full rounded-lg border border-[#d8e6e9] bg-white px-3.5 pr-11 text-sm font-bold text-[#172224] shadow-[0_8px_18px_rgb(18_33_36_/_5%),inset_0_1px_0_rgb(255_255_255_/_92%)] outline-none transition-[border-color,box-shadow] duration-180 placeholder:text-[#9aaeb2] focus:border-[#8adff3] focus:shadow-[0_0_0_4px_rgb(174_238_255_/_26%),0_10px_24px_rgb(18_33_36_/_7%)]"
          name="password"
          :type="showPassword ? 'text' : 'password'"
          autocomplete="current-password"
          placeholder="Minimum 8 characters"
          :aria-invalid="Boolean(visibleFieldErrors.password)"
          aria-describedby="password-error"
        />
        <button
          class="absolute right-2 top-1/2 inline-flex size-8 -translate-y-1/2 cursor-pointer items-center justify-center rounded-md border-0 bg-transparent text-[#7a8f94] transition-[background-color,color] duration-180 hover:bg-[#eef7f9] hover:text-[#246b78] focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#aeeeff] motion-reduce:transition-none"
          type="button"
          :aria-label="showPassword ? 'Hide password' : 'Show password'"
          :aria-pressed="showPassword"
          @click="showPassword = !showPassword"
        >
          <EyeOff v-if="showPassword" :size="17" :stroke-width="2.2" aria-hidden="true" />
          <Eye v-else :size="17" :stroke-width="2.2" aria-hidden="true" />
        </button>
      </span>
      <p
        v-if="visibleFieldErrors.password"
        id="password-error"
        class="m-0 text-xs font-bold leading-4 text-[#9f2f25]"
        role="alert"
      >
        {{ visibleFieldErrors.password }}
      </p>
    </label>

    <p
      v-if="errorMessage"
      class="rounded-lg bg-[#fff1f0] px-3.5 py-3 text-sm font-bold leading-5 text-[#9f2f25] shadow-[inset_0_0_0_1px_rgb(159_47_37_/_14%)]"
      role="alert"
    >
      {{ errorMessage }}
    </p>

    <button
      class="mt-1 inline-flex min-h-11 w-full cursor-pointer items-center justify-center rounded-lg border border-[#2b7f8f] bg-[#246b78] text-sm font-black leading-none text-white shadow-[0_16px_30px_rgb(18_33_36_/_18%),0_0_24px_rgb(174_238_255_/_18%),inset_0_1px_0_rgb(255_255_255_/_14%)] transition-[transform,border-color,background-color,box-shadow,opacity] duration-180 hover:-translate-y-px hover:border-[#236575] hover:bg-[#1f5f6d] hover:shadow-[0_18px_36px_rgb(18_33_36_/_22%),0_0_28px_rgb(174_238_255_/_22%),inset_0_1px_0_rgb(255_255_255_/_16%)] active:scale-[0.96] disabled:cursor-not-allowed disabled:opacity-60 disabled:hover:translate-y-0 focus-visible:outline focus-visible:outline-3 focus-visible:outline-offset-3 focus-visible:outline-[#aeeeff]/70 motion-reduce:transition-none motion-reduce:hover:translate-y-0"
      type="submit"
      :disabled="isPending"
    >
      {{ isPending ? 'Signing in...' : 'Sign in' }}
    </button>
  </form>
</template>

<style scoped>
.auth-password-input::-ms-reveal,
.auth-password-input::-ms-clear {
  display: none;
}

.auth-password-input::-webkit-credentials-auto-fill-button,
.auth-password-input::-webkit-caps-lock-indicator,
.auth-password-input::-webkit-clear-button {
  display: none;
  visibility: hidden;
  pointer-events: none;
}
</style>
