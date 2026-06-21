<script setup lang="ts">
import {
  ArrowLeft,
  Blend,
  Check,
  CheckCircle2,
  Eye,
  EyeOff,
  LockKeyhole,
  ShieldCheck,
} from '@lucide/vue'
import { computed, shallowRef } from 'vue'
import heroImage from '@/assets/img/hero.png'

const password = shallowRef('')
const passwordConfirmation = shallowRef('')
const showPassword = shallowRef(false)
const showPasswordConfirmation = shallowRef(false)
const wasUpdated = shallowRef(false)

const passwordRules = computed(() => [
  {
    label: 'At least 8 characters',
    isValid: password.value.length >= 8,
  },
  {
    label: 'One uppercase letter',
    isValid: /[A-Z]/.test(password.value),
  },
  {
    label: 'One number',
    isValid: /\d/.test(password.value),
  },
])

const passwordsMatch = computed(
  () => passwordConfirmation.value.length > 0 && password.value === passwordConfirmation.value,
)

const canSubmit = computed(
  () => passwordRules.value.every((rule) => rule.isValid) && passwordsMatch.value,
)

function updatePassword() {
  if (!canSubmit.value) return

  wasUpdated.value = true
}
</script>

<template>
  <main class="min-h-screen bg-[#fbfeff] text-[#172224]" aria-label="Create a new password">
    <section
      class="grid min-h-screen grid-cols-[minmax(300px,43vw)_minmax(0,1fr)] overflow-hidden bg-[#fbfeff] max-[860px]:grid-cols-1"
    >
      <aside
        class="relative flex min-h-screen flex-col justify-between overflow-hidden bg-cover bg-center px-[clamp(28px,5vw,68px)] py-[clamp(30px,6vh,62px)] text-white max-[860px]:hidden"
        :style="{
          backgroundImage: `radial-gradient(ellipse at 62% 14%, rgb(174 238 255 / 18%) 0%, transparent 44%), linear-gradient(160deg, rgb(7 12 14 / 94%) 0%, rgb(15 28 32 / 88%) 48%, rgb(0 0 0 / 90%) 100%), url(${heroImage})`,
        }"
      >
        <div
          class="pointer-events-none absolute inset-0 bg-[linear-gradient(180deg,rgb(255_255_255_/_5%)_0_1px,transparent_1px_100%),linear-gradient(90deg,rgb(255_255_255_/_4%)_0_1px,transparent_1px_100%)] bg-[length:72px_72px] opacity-70"
          aria-hidden="true"
        ></div>

        <div class="relative z-10 flex items-center gap-3">
          <div
            class="flex size-12 items-center justify-center rounded-[16px] border border-white/15 bg-white/10 shadow-[0_18px_44px_rgb(0_0_0_/_38%),inset_0_1px_0_rgb(255_255_255_/_12%)] backdrop-blur-xl"
          >
            <Blend class="text-[#aeeeff]" :size="26" :stroke-width="2.4" aria-hidden="true" />
          </div>
          <span class="text-sm font-black tracking-wide text-white/90">Blendes Flow</span>
        </div>

        <div class="relative z-10 mx-auto w-full max-w-[430px]">
          <p class="mb-4 text-xs font-black uppercase tracking-[0.12em] text-[#aeeeff]">
            Final recovery step
          </p>
          <h1
            class="m-0 text-balance text-[clamp(1.85rem,2.6vw,2.9rem)] font-extrabold leading-[1.04] text-white"
          >
            Create a password that keeps your account protected.
          </h1>

          <div class="mt-8 grid gap-3" aria-label="New password guidance">
            <div
              class="grid grid-cols-[auto_1fr] gap-3 rounded-lg border border-white/10 bg-white/10 p-4 shadow-[0_18px_42px_rgb(0_0_0_/_22%),inset_0_1px_0_rgb(255_255_255_/_10%)] backdrop-blur-xl"
            >
              <CheckCircle2
                class="mt-0.5 text-[#aeeeff]"
                :size="19"
                :stroke-width="2.3"
                aria-hidden="true"
              />
              <div>
                <strong class="block text-sm font-black leading-none text-white">
                  Code already confirmed
                </strong>
                <span class="mt-1.5 block text-pretty text-xs font-bold leading-5 text-white/62">
                  This screen appears after the OTP step is complete.
                </span>
              </div>
            </div>

            <div
              class="grid grid-cols-[auto_1fr] gap-3 rounded-lg border border-white/10 bg-white/[0.07] p-4"
            >
              <LockKeyhole
                class="mt-0.5 text-white/58"
                :size="19"
                :stroke-width="2.3"
                aria-hidden="true"
              />
              <div>
                <strong class="block text-sm font-black leading-none text-white/86">
                  Set a new password
                </strong>
                <span class="mt-1.5 block text-pretty text-xs font-bold leading-5 text-white/56">
                  Use a password you have not used before.
                </span>
              </div>
            </div>

            <div
              class="grid grid-cols-[auto_1fr] gap-3 rounded-lg border border-white/10 bg-white/[0.07] p-4"
            >
              <ShieldCheck
                class="mt-0.5 text-white/58"
                :size="19"
                :stroke-width="2.3"
                aria-hidden="true"
              />
              <div>
                <strong class="block text-sm font-black leading-none text-white/86">
                  Sign in again
                </strong>
                <span class="mt-1.5 block text-pretty text-xs font-bold leading-5 text-white/56">
                  After saving, use the new password on the login screen.
                </span>
              </div>
            </div>
          </div>
        </div>

        <p
          class="relative z-10 m-0 max-w-[360px] text-pretty text-xs font-bold leading-5 text-white/54"
        >
          For your safety, avoid names, birthdays, repeated numbers, or passwords used in other
          tools.
        </p>
      </aside>

      <section
        class="relative flex min-h-screen flex-col border-l border-[#dbe8eb] bg-[#fbfeff] text-[#172224] shadow-[-18px_0_48px_rgb(18_33_36_/_6%)]"
      >
        <header class="flex items-center justify-between gap-4 px-7 py-6 max-[520px]:px-5">
          <RouterLink
            class="inline-flex items-center gap-2 text-sm font-extrabold text-[#172224] no-underline"
            to="/"
            aria-label="Blendes Flow home"
          >
            <span
              class="inline-flex size-9 items-center justify-center rounded-full border border-[#d8e6e9] bg-white shadow-[0_10px_26px_rgb(18_33_36_/_8%)]"
            >
              <Blend class="text-[#246b78]" :size="20" :stroke-width="2.4" aria-hidden="true" />
            </span>
            <span class="max-[520px]:hidden">Blendes Flow</span>
          </RouterLink>

          <RouterLink
            class="inline-flex min-h-9 items-center gap-2 rounded-full px-3 text-xs font-extrabold text-[#4f666c] no-underline transition duration-180 hover:bg-[#eef7f9] hover:text-[#172224] focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#aeeeff] motion-reduce:transition-none"
            to="/confirm-otp"
          >
            <ArrowLeft :size="15" :stroke-width="2.5" aria-hidden="true" />
            Back to code
          </RouterLink>
        </header>

        <div class="flex flex-1 items-center justify-center px-6 py-8 max-[520px]:px-5">
          <div class="w-full max-w-[430px]">
            <div
              class="mb-6 inline-flex size-12 items-center justify-center rounded-[14px] border border-[#d8e6e9] bg-white text-[#246b78] shadow-[0_14px_32px_rgb(18_33_36_/_8%),inset_0_1px_0_rgb(255_255_255_/_92%)]"
              aria-hidden="true"
            >
              <LockKeyhole :size="23" :stroke-width="2.35" />
            </div>

            <Transition mode="out-in" name="password-panel">
              <div v-if="!wasUpdated" key="form">
                <div class="mb-6">
                  <p class="mb-3 text-xs font-black uppercase tracking-[0.12em] text-[#246b78]">
                    New password
                  </p>
                  <h2
                    class="m-0 text-balance text-[1.7rem] font-extrabold leading-tight text-[#172224]"
                  >
                    Choose and confirm your new password.
                  </h2>
                  <p class="mt-3 text-pretty text-sm font-semibold leading-6 text-[#6c8085]">
                    Type your new password twice. We will show whether the passwords match before
                    you save the change.
                  </p>
                </div>

                <form class="grid gap-4" @submit.prevent="updatePassword">
                  <label class="grid gap-2" for="new-password">
                    <span class="text-xs font-extrabold leading-none text-[#172224]">
                      New password
                    </span>
                    <span class="relative block">
                      <input
                        id="new-password"
                        v-model="password"
                        class="password-input min-h-11 w-full rounded-lg border border-[#d8e6e9] bg-white px-3.5 pr-11 text-sm font-bold text-[#172224] shadow-[0_8px_18px_rgb(18_33_36_/_5%),inset_0_1px_0_rgb(255_255_255_/_92%)] outline-none transition duration-180 placeholder:text-[#9aaeb2] focus:border-[#8adff3] focus:shadow-[0_0_0_4px_rgb(174_238_255_/_26%),0_10px_24px_rgb(18_33_36_/_7%)]"
                        name="password"
                        :type="showPassword ? 'text' : 'password'"
                        autocomplete="new-password"
                        placeholder="Create a secure password"
                        required
                      />
                      <button
                        class="absolute right-2 top-1/2 inline-flex size-8 -translate-y-1/2 cursor-pointer items-center justify-center rounded-md border-0 bg-transparent text-[#7a8f94] transition duration-180 hover:bg-[#eef7f9] hover:text-[#246b78] focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#aeeeff] active:scale-[0.96] motion-reduce:transition-none motion-reduce:active:scale-100"
                        type="button"
                        :aria-label="showPassword ? 'Hide password' : 'Show password'"
                        :aria-pressed="showPassword"
                        @click="showPassword = !showPassword"
                      >
                        <EyeOff
                          v-if="showPassword"
                          :size="17"
                          :stroke-width="2.2"
                          aria-hidden="true"
                        />
                        <Eye v-else :size="17" :stroke-width="2.2" aria-hidden="true" />
                      </button>
                    </span>
                  </label>

                  <div
                    class="grid gap-2 rounded-lg border border-[#d8e6e9] bg-[#f4fafb] px-4 py-3"
                    aria-label="Password requirements"
                  >
                    <div
                      v-for="rule in passwordRules"
                      :key="rule.label"
                      class="flex min-h-5 items-center gap-2 text-xs font-bold text-[#62777d]"
                    >
                      <span
                        class="inline-flex size-5 flex-none items-center justify-center rounded-full transition duration-180"
                        :class="
                          rule.isValid
                            ? 'bg-[#ecfbf8] text-[#0f5753]'
                            : 'bg-white text-[#9aaeb2] shadow-[inset_0_0_0_1px_rgb(216_230_233)]'
                        "
                      >
                        <Check :size="13" :stroke-width="3" aria-hidden="true" />
                      </span>
                      {{ rule.label }}
                    </div>
                  </div>

                  <label class="grid gap-2" for="confirm-new-password">
                    <span class="text-xs font-extrabold leading-none text-[#172224]">
                      Confirm new password
                    </span>
                    <span class="relative block">
                      <input
                        id="confirm-new-password"
                        v-model="passwordConfirmation"
                        class="password-input min-h-11 w-full rounded-lg border border-[#d8e6e9] bg-white px-3.5 pr-11 text-sm font-bold text-[#172224] shadow-[0_8px_18px_rgb(18_33_36_/_5%),inset_0_1px_0_rgb(255_255_255_/_92%)] outline-none transition duration-180 placeholder:text-[#9aaeb2] focus:border-[#8adff3] focus:shadow-[0_0_0_4px_rgb(174_238_255_/_26%),0_10px_24px_rgb(18_33_36_/_7%)]"
                        name="passwordConfirmation"
                        :type="showPasswordConfirmation ? 'text' : 'password'"
                        autocomplete="new-password"
                        placeholder="Type the same password again"
                        required
                      />
                      <button
                        class="absolute right-2 top-1/2 inline-flex size-8 -translate-y-1/2 cursor-pointer items-center justify-center rounded-md border-0 bg-transparent text-[#7a8f94] transition duration-180 hover:bg-[#eef7f9] hover:text-[#246b78] focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#aeeeff] active:scale-[0.96] motion-reduce:transition-none motion-reduce:active:scale-100"
                        type="button"
                        :aria-label="
                          showPasswordConfirmation
                            ? 'Hide password confirmation'
                            : 'Show password confirmation'
                        "
                        :aria-pressed="showPasswordConfirmation"
                        @click="showPasswordConfirmation = !showPasswordConfirmation"
                      >
                        <EyeOff
                          v-if="showPasswordConfirmation"
                          :size="17"
                          :stroke-width="2.2"
                          aria-hidden="true"
                        />
                        <Eye v-else :size="17" :stroke-width="2.2" aria-hidden="true" />
                      </button>
                    </span>
                  </label>

                  <p
                    v-if="passwordConfirmation"
                    class="m-0 text-xs font-bold leading-5"
                    :class="passwordsMatch ? 'text-[#0f5753]' : 'text-[#9a4a1d]'"
                  >
                    {{ passwordsMatch ? 'Passwords match.' : 'Passwords do not match yet.' }}
                  </p>

                  <button
                    class="mt-1 inline-flex min-h-11 w-full cursor-pointer items-center justify-center rounded-lg border border-[#2b7f8f] bg-[#246b78] text-sm font-black leading-none text-white shadow-[0_16px_30px_rgb(18_33_36_/_18%),0_0_24px_rgb(174_238_255_/_18%),inset_0_1px_0_rgb(255_255_255_/_14%)] transition duration-180 hover:-translate-y-px hover:border-[#236575] hover:bg-[#1f5f6d] hover:shadow-[0_18px_36px_rgb(18_33_36_/_22%),0_0_28px_rgb(174_238_255_/_22%),inset_0_1px_0_rgb(255_255_255_/_16%)] focus-visible:outline focus-visible:outline-3 focus-visible:outline-offset-3 focus-visible:outline-[#aeeeff]/70 disabled:cursor-not-allowed disabled:border-[#b9d9de] disabled:bg-[#9ab9c0] disabled:shadow-none disabled:hover:translate-y-0 active:scale-[0.96] motion-reduce:transition-none motion-reduce:hover:translate-y-0 motion-reduce:active:scale-100"
                    type="submit"
                    :disabled="!canSubmit"
                  >
                    Save new password
                  </button>
                </form>
              </div>

              <div v-else key="updated">
                <div
                  class="mb-6 inline-flex min-h-11 items-center gap-2 rounded-full border border-[#ccefed] bg-[#ecfbf8] px-4 text-xs font-black text-[#0f5753]"
                >
                  <CheckCircle2 :size="17" :stroke-width="2.4" aria-hidden="true" />
                  Password updated
                </div>

                <h2
                  class="m-0 text-balance text-[1.7rem] font-extrabold leading-tight text-[#172224]"
                >
                  Your new password is ready.
                </h2>
                <p class="mt-3 text-pretty text-sm font-semibold leading-6 text-[#6c8085]">
                  Use it the next time you sign in to Blendes. Your previous password should no
                  longer be used.
                </p>

                <RouterLink
                  class="mt-6 inline-flex min-h-11 w-full items-center justify-center rounded-lg border border-[#2b7f8f] bg-[#246b78] text-sm font-black leading-none text-white no-underline shadow-[0_16px_30px_rgb(18_33_36_/_18%),0_0_24px_rgb(174_238_255_/_18%),inset_0_1px_0_rgb(255_255_255_/_14%)] transition duration-180 hover:-translate-y-px hover:border-[#236575] hover:bg-[#1f5f6d] focus-visible:outline focus-visible:outline-3 focus-visible:outline-offset-3 focus-visible:outline-[#aeeeff]/70 active:scale-[0.96] motion-reduce:transition-none motion-reduce:hover:translate-y-0 motion-reduce:active:scale-100"
                  to="/auth"
                >
                  Back to login
                </RouterLink>
              </div>
            </Transition>
          </div>
        </div>

        <footer
          class="flex items-center justify-between gap-4 px-7 py-5 text-[0.7rem] font-bold text-[#7a8f94] max-[520px]:px-5"
        >
          <span>&copy; 2026 Blendes</span>
          <div class="flex gap-4">
            <a class="text-[#62777d] no-underline hover:text-[#172224]" href="#privacy">
              Privacy
            </a>
            <a class="text-[#62777d] no-underline hover:text-[#172224]" href="#support">
              Support
            </a>
          </div>
        </footer>
      </section>
    </section>
  </main>
</template>

<style scoped>
.password-input::-ms-reveal,
.password-input::-ms-clear {
  display: none;
}

.password-input::-webkit-credentials-auto-fill-button,
.password-input::-webkit-caps-lock-indicator,
.password-input::-webkit-clear-button {
  display: none;
  visibility: hidden;
  pointer-events: none;
}

.password-panel-enter-active,
.password-panel-leave-active {
  transition:
    opacity 180ms ease,
    transform 180ms ease;
}

.password-panel-enter-from,
.password-panel-leave-to {
  opacity: 0;
  transform: translateY(8px);
}

@media (prefers-reduced-motion: reduce) {
  .password-panel-enter-active,
  .password-panel-leave-active {
    transition: opacity 140ms ease;
  }

  .password-panel-enter-from,
  .password-panel-leave-to {
    transform: none;
  }
}
</style>
