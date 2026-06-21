<script setup lang="ts">
import { ArrowLeft, Blend, CheckCircle2, Clock3, Mail, ShieldCheck } from '@lucide/vue'
import { shallowRef } from 'vue'
import heroImage from '@/assets/img/hero.png'

const email = shallowRef('')
const wasSent = shallowRef(false)

function requestPasswordRecovery() {
  wasSent.value = true
}
</script>

<template>
  <main class="min-h-screen bg-[#fbfeff] text-[#172224]" aria-label="Password recovery">
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
            Secure recovery
          </p>
          <h1
            class="m-0 text-[clamp(1.85rem,2.6vw,2.9rem)] font-extrabold leading-[1.04] text-white"
          >
            Get back into your account with a code sent by email.
          </h1>

          <div class="mt-8 grid gap-3" aria-label="Password recovery steps">
            <div
              class="grid grid-cols-[auto_1fr] gap-3 rounded-lg border border-white/10 bg-white/10 p-4 shadow-[0_18px_42px_rgb(0_0_0_/_22%),inset_0_1px_0_rgb(255_255_255_/_10%)] backdrop-blur-xl"
            >
              <Mail
                class="mt-0.5 text-[#aeeeff]"
                :size="19"
                :stroke-width="2.3"
                aria-hidden="true"
              />
              <div>
                <strong class="block text-sm font-black leading-none text-white"
                  >Enter your email</strong
                >
                <span class="mt-1.5 block text-xs font-bold leading-5 text-white/62">
                  Use the same address registered with Blendes.
                </span>
              </div>
            </div>

            <div
              class="grid grid-cols-[auto_1fr] gap-3 rounded-lg border border-white/10 bg-white/[0.07] p-4"
            >
              <Clock3
                class="mt-0.5 text-white/58"
                :size="19"
                :stroke-width="2.3"
                aria-hidden="true"
              />
              <div>
                <strong class="block text-sm font-black leading-none text-white/86"
                  >Receive your code</strong
                >
                <span class="mt-1.5 block text-xs font-bold leading-5 text-white/56">
                  The 6-digit code should arrive in your Gmail in a few moments.
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
                <strong class="block text-sm font-black leading-none text-white/86"
                  >Confirm the digits</strong
                >
                <span class="mt-1.5 block text-xs font-bold leading-5 text-white/56">
                  Type only the code numbers to continue securely.
                </span>
              </div>
            </div>
          </div>
        </div>

        <p class="relative z-10 m-0 max-w-[360px] text-xs font-bold leading-5 text-white/54">
          For security, we do not reveal whether an email exists on the platform. If an account is
          found, we will send a verification code.
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
            to="/auth"
          >
            <ArrowLeft :size="15" :stroke-width="2.5" aria-hidden="true" />
            Back to login
          </RouterLink>
        </header>

        <div class="flex flex-1 items-center justify-center px-6 py-8 max-[520px]:px-5">
          <div class="w-full max-w-[410px]">
            <div
              class="mb-6 inline-flex size-12 items-center justify-center rounded-[14px] border border-[#d8e6e9] bg-white text-[#246b78] shadow-[0_14px_32px_rgb(18_33_36_/_8%),inset_0_1px_0_rgb(255_255_255_/_92%)]"
              aria-hidden="true"
            >
              <Mail :size="23" :stroke-width="2.35" />
            </div>

            <Transition mode="out-in" name="recovery-panel">
              <div v-if="!wasSent" key="form">
                <div class="mb-6">
                  <p class="mb-3 text-xs font-black uppercase tracking-[0.12em] text-[#246b78]">
                    Forgot your password?
                  </p>
                  <h2 class="m-0 text-[1.7rem] font-extrabold leading-tight text-[#172224]">
                    We will send a 6-digit code to help you reset your access.
                  </h2>
                  <p class="mt-3 text-sm font-semibold leading-6 text-[#6c8085]">
                    Enter the email used for your account. If it is registered, you will receive a
                    code in your Gmail with the next step to create a new password.
                  </p>
                </div>

                <form class="grid gap-4" @submit.prevent="requestPasswordRecovery">
                  <label class="grid gap-2" for="recovery-email">
                    <span class="text-xs font-extrabold leading-none text-[#172224]">Email</span>
                    <input
                      id="recovery-email"
                      v-model.trim="email"
                      class="min-h-11 w-full rounded-lg border border-[#d8e6e9] bg-white px-3.5 text-sm font-bold text-[#172224] shadow-[0_8px_18px_rgb(18_33_36_/_5%),inset_0_1px_0_rgb(255_255_255_/_92%)] outline-none transition duration-180 placeholder:text-[#9aaeb2] focus:border-[#8adff3] focus:shadow-[0_0_0_4px_rgb(174_238_255_/_26%),0_10px_24px_rgb(18_33_36_/_7%)]"
                      name="email"
                      type="email"
                      autocomplete="email"
                      placeholder="you@company.com"
                      required
                    />
                  </label>

                  <button
                    class="mt-1 inline-flex min-h-11 w-full cursor-pointer items-center justify-center rounded-lg border border-[#2b7f8f] bg-[#246b78] text-sm font-black leading-none text-white shadow-[0_16px_30px_rgb(18_33_36_/_18%),0_0_24px_rgb(174_238_255_/_18%),inset_0_1px_0_rgb(255_255_255_/_14%)] transition duration-180 hover:-translate-y-px hover:border-[#236575] hover:bg-[#1f5f6d] hover:shadow-[0_18px_36px_rgb(18_33_36_/_22%),0_0_28px_rgb(174_238_255_/_22%),inset_0_1px_0_rgb(255_255_255_/_16%)] focus-visible:outline focus-visible:outline-3 focus-visible:outline-offset-3 focus-visible:outline-[#aeeeff]/70 motion-reduce:transition-none motion-reduce:hover:translate-y-0"
                    type="submit"
                  >
                    Send recovery code
                  </button>
                </form>

                <div
                  class="mt-5 rounded-lg border border-[#d8e6e9] bg-[#f4fafb] px-4 py-3 text-xs font-bold leading-5 text-[#4f666c]"
                >
                  Also check your spam or junk folder if the email takes a while to arrive.
                </div>
              </div>

              <div v-else key="sent">
                <div
                  class="mb-6 inline-flex min-h-11 items-center gap-2 rounded-full border border-[#ccefed] bg-[#ecfbf8] px-4 text-xs font-black text-[#0f5753]"
                >
                  <CheckCircle2 :size="17" :stroke-width="2.4" aria-hidden="true" />
                  Request received
                </div>

                <h2 class="m-0 text-[1.7rem] font-extrabold leading-tight text-[#172224]">
                  Check your email to continue.
                </h2>
                <p class="mt-3 text-sm font-semibold leading-6 text-[#6c8085]">
                  If there is an account linked to
                  <strong class="font-extrabold text-[#172224]">{{ email }}</strong
                  >, we will send a 6-digit code to recover your password.
                </p>

                <div
                  class="mt-6 grid gap-3 rounded-lg border border-[#d8e6e9] bg-white p-4 shadow-[0_14px_34px_rgb(18_33_36_/_7%)]"
                >
                  <div class="flex items-start gap-3">
                    <Clock3
                      class="mt-0.5 flex-none text-[#246b78]"
                      :size="18"
                      :stroke-width="2.3"
                      aria-hidden="true"
                    />
                    <p class="m-0 text-xs font-bold leading-5 text-[#62777d]">
                      Delivery can take a few minutes. The code will expire after a limited time to
                      keep your account protected.
                    </p>
                  </div>
                </div>

                <div class="mt-5 grid gap-3">
                  <button
                    class="inline-flex min-h-11 w-full cursor-pointer items-center justify-center rounded-lg border border-[#d8e6e9] bg-white text-sm font-black leading-none text-[#172224] shadow-[0_10px_24px_rgb(18_33_36_/_7%),inset_0_1px_0_rgb(255_255_255_/_92%)] transition duration-180 hover:-translate-y-px hover:border-[#b9d9de] hover:bg-[#f6fbfc] focus-visible:outline focus-visible:outline-3 focus-visible:outline-offset-3 focus-visible:outline-[#aeeeff]/70 motion-reduce:transition-none motion-reduce:hover:translate-y-0"
                    type="button"
                    @click="wasSent = false"
                  >
                    Use another email
                  </button>

                  <RouterLink
                    class="inline-flex min-h-11 w-full items-center justify-center rounded-lg border border-[#2b7f8f] bg-[#246b78] text-sm font-black leading-none text-white no-underline shadow-[0_16px_30px_rgb(18_33_36_/_18%),0_0_24px_rgb(174_238_255_/_18%),inset_0_1px_0_rgb(255_255_255_/_14%)] transition duration-180 hover:-translate-y-px hover:border-[#236575] hover:bg-[#1f5f6d] focus-visible:outline focus-visible:outline-3 focus-visible:outline-offset-3 focus-visible:outline-[#aeeeff]/70 motion-reduce:transition-none motion-reduce:hover:translate-y-0"
                    to="/confirm-otp"
                  >
                    Enter the 6-digit code
                  </RouterLink>
                </div>
              </div>
            </Transition>
          </div>
        </div>

        <footer
          class="flex items-center justify-between gap-4 px-7 py-5 text-[0.7rem] font-bold text-[#7a8f94] max-[520px]:px-5"
        >
          <span>© 2026 Blendes</span>
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
.recovery-panel-enter-active,
.recovery-panel-leave-active {
  transition:
    opacity 180ms ease,
    transform 180ms ease;
}

.recovery-panel-enter-from,
.recovery-panel-leave-to {
  opacity: 0;
  transform: translateY(8px);
}

@media (prefers-reduced-motion: reduce) {
  .recovery-panel-enter-active,
  .recovery-panel-leave-active {
    transition: opacity 140ms ease;
  }

  .recovery-panel-enter-from,
  .recovery-panel-leave-to {
    transform: none;
  }
}
</style>
