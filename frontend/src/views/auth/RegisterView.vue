<script setup lang="ts">
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'
import { Blend } from '@lucide/vue'

import heroImage from '@/assets/img/hero.png'
import type { AccountRegistrationPayload } from '@/domains/accounts/contracts'
import { useCreateAccountMutation } from '@/domains/accounts/queries'
import { ApiRequestError } from '@/lib/http/errors'

import CreateAccountForm from './components/CreateAccountForm.vue'

const router = useRouter()
const createAccountMutation = useCreateAccountMutation()
const successMessage = ref('')

const errorMessage = computed(() => {
  const error = createAccountMutation.error.value

  if (error instanceof ApiRequestError) {
    return error.message
  }

  if (error) {
    return 'Unable to create this account. Check the details and try again.'
  }

  return ''
})

async function submitCreateAccount(payload: AccountRegistrationPayload) {
  successMessage.value = ''
  createAccountMutation.reset()

  const account = await createAccountMutation.mutateAsync(payload).catch(() => null)

  if (!account) {
    return
  }

  successMessage.value = 'Account created. Redirecting to sign in...'
  window.setTimeout(() => {
    void router.push({ name: 'auth' })
  }, 900)
}
</script>

<template>
  <main class="min-h-screen bg-[#fbfeff] text-[#172224]" aria-label="Create Blendes account">
    <section
      class="grid min-h-screen grid-cols-[minmax(300px,43vw)_minmax(0,1fr)] overflow-hidden bg-[#fbfeff] max-[860px]:grid-cols-1"
    >
      <aside
        class="relative flex min-h-screen flex-col justify-end overflow-hidden bg-cover bg-center px-[clamp(28px,5vw,68px)] py-[clamp(30px,6vh,62px)] text-white max-[860px]:hidden"
        :style="{
          backgroundImage: `radial-gradient(ellipse at 62% 14%, rgb(174 238 255 / 16%) 0%, transparent 44%), linear-gradient(160deg, rgb(7 12 14 / 94%) 0%, rgb(15 28 32 / 88%) 48%, rgb(0 0 0 / 90%) 100%), url(${heroImage})`,
        }"
      >
        <div
          class="pointer-events-none absolute inset-0 bg-[linear-gradient(180deg,rgb(255_255_255_/_5%)_0_1px,transparent_1px_100%),linear-gradient(90deg,rgb(255_255_255_/_4%)_0_1px,transparent_1px_100%)] bg-[length:72px_72px] opacity-70"
          aria-hidden="true"
        ></div>

        <div class="relative z-10 mb-[clamp(54px,12vh,128px)] flex justify-center">
          <div
            class="flex size-16 items-center justify-center rounded-[18px] border border-white/15 bg-white/10 shadow-[0_18px_44px_rgb(0_0_0_/_42%),inset_0_1px_0_rgb(255_255_255_/_12%)] backdrop-blur-xl"
          >
            <Blend class="text-[#aeeeff]" :size="34" :stroke-width="2.4" aria-hidden="true" />
          </div>
        </div>

        <div class="relative z-10 mx-auto w-full max-w-[430px] text-center">
          <h1
            class="m-0 text-[clamp(1.75rem,2.4vw,2.7rem)] font-extrabold leading-[1.06] text-white"
          >
            Start with a clearer account setup.
          </h1>

          <p class="mx-auto mt-4 max-w-[360px] text-sm font-semibold leading-6 text-white/62">
            Create your Blendes account with validated details before entering your workspace.
          </p>
        </div>
      </aside>

      <section
        class="relative flex min-h-screen flex-col border-l border-[#dbe8eb] bg-[#fbfeff] text-[#172224] shadow-[-18px_0_48px_rgb(18_33_36_/_6%)]"
      >
        <header class="flex items-center justify-between gap-4 px-7 py-6 max-[520px]:px-5">
          <RouterLink
            class="inline-flex items-center gap-2 text-sm font-extrabold text-[#172224] no-underline"
            :to="{ name: 'home' }"
            aria-label="Blendes Flow home"
          >
            <span
              class="inline-flex size-9 items-center justify-center rounded-full border border-[#d8e6e9] bg-white shadow-[0_10px_26px_rgb(18_33_36_/_8%)]"
            >
              <Blend class="text-[#246b78]" :size="20" :stroke-width="2.4" aria-hidden="true" />
            </span>
            <span class="max-[520px]:hidden">Blendes Flow</span>
          </RouterLink>

          <p class="m-0 text-xs font-bold text-[#4f666c]">
            Already have an account?
            <RouterLink
              class="font-extrabold text-[#172224] underline decoration-[#aeeeff] decoration-2 underline-offset-4"
              to="/auth"
              >Sign in</RouterLink
            >
          </p>
        </header>

        <div class="flex flex-1 items-center justify-center px-6 py-5 max-[520px]:px-4">
          <div
            class="w-full max-w-[600px] rounded-2xl border border-slate-200 bg-white p-5 shadow-[0_12px_30px_rgb(18_33_36_/_5%)] max-[520px]:p-4"
          >
            <div class="mb-4 text-center">
              <h2 class="m-0 text-[1.35rem] font-extrabold leading-tight text-[#172224]">
                Create your account
              </h2>
              <p class="mt-1.5 text-sm font-semibold leading-5 text-[#6c8085]">
                Add secure credentials and choose an optional avatar.
              </p>
            </div>

            <CreateAccountForm
              :error-message="errorMessage"
              :is-pending="createAccountMutation.isPending.value"
              :success-message="successMessage"
              @submit="submitCreateAccount"
            />
          </div>
        </div>
      </section>
    </section>
  </main>
</template>
