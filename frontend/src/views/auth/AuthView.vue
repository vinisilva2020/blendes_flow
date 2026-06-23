<script setup lang="ts">
import { computed, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Blend } from '@lucide/vue'

import heroImage from '@/assets/img/hero.png'
import GoogleAuthButton from '@/components/GoogleButton.vue'
import type { LoginCredentials } from '@/domains/auth/contracts'
import { useGoogleSignInMutation, useSignInMutation } from '@/domains/auth/queries'
import { ApiRequestError } from '@/lib/http/errors'
import { useAuthenticationStore } from '@/stores/authentication'

import AuthSignInForm from './components/AuthSignInForm.vue'

const router = useRouter()
const route = useRoute()
const authenticationStore = useAuthenticationStore()
const signInMutation = useSignInMutation()
const googleSignInMutation = useGoogleSignInMutation()
const googleClientError = ref('')

const errorMessage = computed(() => {
  const error = googleSignInMutation.error.value ?? signInMutation.error.value

  if (error instanceof ApiRequestError) {
    return error.message
  }

  if (error) {
    return 'Unable to sign in. Check your details and try again.'
  }

  return googleClientError.value
})

async function submitSignIn(credentials: LoginCredentials) {
  googleClientError.value = ''
  const tokens = await signInMutation.mutateAsync(credentials).catch(() => null)

  if (!tokens) {
    return
  }

  authenticationStore.startSession(tokens)
  await router.push(getPostSignInLocation())
}

async function submitGoogleSignIn(credential: string) {
  googleClientError.value = ''
  const tokens = await googleSignInMutation
    .mutateAsync({ credential })
    .catch(() => null)

  if (!tokens) {
    return
  }

  authenticationStore.startSession(tokens)
  await router.push(getPostSignInLocation())
}

function setGoogleClientError(message: string) {
  googleSignInMutation.reset()
  signInMutation.reset()
  googleClientError.value = message
}

function getPostSignInLocation() {
  const redirectPath = route.query.redirect

  if (typeof redirectPath === 'string' && redirectPath.startsWith('/')) {
    return redirectPath
  }

  return { name: 'organizations' }
}
</script>

<template>
  <main class="min-h-screen bg-[#fbfeff] text-[#172224]" aria-label="Blendes authentication">
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
            A platform to understand and improve flows.
          </h1>

          <p class="mx-auto mt-4 max-w-[360px] text-sm font-semibold leading-6 text-white/62">
            Blendes turns signals, routines, and metrics into clear insights so you can improve with
            greater precision.
          </p>

          <div class="mt-8 flex justify-center gap-2" aria-hidden="true">
            <span class="size-2 rounded-full bg-[#aeeeff]"></span>
            <span class="size-2 rounded-full bg-white/25"></span>
            <span class="size-2 rounded-full bg-white/25"></span>
          </div>
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
            Don't have an account?
            <RouterLink
              class="font-extrabold text-[#172224] underline decoration-[#aeeeff] decoration-2 underline-offset-4"
              to="/register"
              >Create account</RouterLink
            >
          </p>
        </header>

        <div class="flex flex-1 items-center justify-center px-6 py-8 max-[520px]:px-5">
          <div class="w-full max-w-[390px]">
            <div class="mb-6 text-center">
              <h2 class="m-0 text-[1.55rem] font-extrabold leading-tight text-[#172224]">
                Welcome back to Blendes
              </h2>
              <p class="mt-2 text-sm font-semibold leading-5 text-[#6c8085]">
                Sign in with your details to keep tracking your flows.
              </p>
            </div>

            <div class="grid gap-3">
              <GoogleAuthButton
                :is-pending="googleSignInMutation.isPending.value"
                @credential="submitGoogleSignIn"
                @error="setGoogleClientError"
              />
            </div>

            <div class="my-5 grid grid-cols-[1fr_auto_1fr] items-center gap-3" aria-hidden="true">
              <span class="h-px bg-[#dce8eb]"></span>
              <p class="m-0 text-xs font-extrabold uppercase leading-none text-[#7a8f94]">
                or sign in with
              </p>
              <span class="h-px bg-[#dce8eb]"></span>
            </div>

            <AuthSignInForm
              :error-message="errorMessage"
              :is-pending="signInMutation.isPending.value"
              @submit="submitSignIn"
            />

            <RouterLink
              class="mt-4 block text-center text-xs font-extrabold text-[#172224] underline decoration-[#aeeeff] decoration-2 underline-offset-4"
              to="/forgot-password"
            >
              Forgot your password?
            </RouterLink>
          </div>
        </div>

        <footer
          class="flex items-center justify-between gap-4 px-7 py-5 text-[0.7rem] font-bold text-[#7a8f94] max-[520px]:px-5"
        >
          <span>2026 Blendes</span>
          <div class="flex gap-4">
            <a class="text-[#62777d] no-underline hover:text-[#172224]" href="#privacy">Privacy</a>
            <a class="text-[#62777d] no-underline hover:text-[#172224]" href="#support">Support</a>
          </div>
        </footer>
      </section>
    </section>
  </main>
</template>
