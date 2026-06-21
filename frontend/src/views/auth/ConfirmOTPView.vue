<script setup lang="ts">
import { ArrowLeft, Blend, CheckCircle2, Clock3, KeyRound, Mail, ShieldCheck } from '@lucide/vue'
import { computed, nextTick, shallowRef } from 'vue'
import heroImage from '@/assets/img/hero.png'

const otpDigits = shallowRef<string[]>(Array(6).fill(''))
const isVerified = shallowRef(false)

const otpCode = computed(() => otpDigits.value.join(''))
const isOtpComplete = computed(() => otpCode.value.length === 6)

function updateDigit(index: number, event: Event) {
  const target = event.target as HTMLInputElement
  const cleanValue = target.value.replace(/\D/g, '').slice(-1)

  otpDigits.value = otpDigits.value.map((digit, digitIndex) =>
    digitIndex === index ? cleanValue : digit,
  )
  target.value = cleanValue

  if (cleanValue && index < otpDigits.value.length - 1) {
    focusOtpInput(index + 1)
  }
}

function handleKeydown(index: number, event: KeyboardEvent) {
  if (event.key === 'Backspace' && !otpDigits.value[index] && index > 0) {
    focusOtpInput(index - 1)
  }
}

function handlePaste(event: ClipboardEvent) {
  event.preventDefault()

  const pastedCode = event.clipboardData?.getData('text').replace(/\D/g, '').slice(0, 6) ?? ''

  if (!pastedCode) return

  otpDigits.value = Array.from({ length: 6 }, (_, index) => pastedCode[index] ?? '')
  focusOtpInput(Math.min(pastedCode.length, 5))
}

function focusOtpInput(index: number) {
  nextTick(() => {
    const input = document.querySelector<HTMLInputElement>(`[data-otp-index="${index}"]`)
    input?.focus()
    input?.select()
  })
}

function confirmOtp() {
  if (!isOtpComplete.value) return

  isVerified.value = true
}
</script>

<template>
  <main
    class="min-h-screen bg-[#fbfeff] text-[#172224]"
    aria-label="Confirm password recovery code"
  >
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
            Account verification
          </p>
          <h1
            class="m-0 text-[clamp(1.85rem,2.6vw,2.9rem)] font-extrabold leading-[1.04] text-white"
          >
            Six digits are enough to prove this recovery is yours.
          </h1>

          <div class="mt-8 grid gap-3" aria-label="Code confirmation steps">
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
                  >Open your Gmail</strong
                >
                <span class="mt-1.5 block text-xs font-bold leading-5 text-white/62">
                  Use the latest recovery email from Blendes.
                </span>
              </div>
            </div>

            <div
              class="grid grid-cols-[auto_1fr] gap-3 rounded-lg border border-white/10 bg-white/[0.07] p-4"
            >
              <KeyRound
                class="mt-0.5 text-white/58"
                :size="19"
                :stroke-width="2.3"
                aria-hidden="true"
              />
              <div>
                <strong class="block text-sm font-black leading-none text-white/86"
                  >Copy only the code</strong
                >
                <span class="mt-1.5 block text-xs font-bold leading-5 text-white/56">
                  Enter the 6 digits. No spaces, links, or extra text.
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
                  >Create a new password</strong
                >
                <span class="mt-1.5 block text-xs font-bold leading-5 text-white/56">
                  After confirmation, you can safely update your access.
                </span>
              </div>
            </div>
          </div>
        </div>

        <p class="relative z-10 m-0 max-w-[360px] text-xs font-bold leading-5 text-white/54">
          The code expires after a short time. If it does not work, request a new recovery email and
          use the most recent code.
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
            to="/forgot-password"
          >
            <ArrowLeft :size="15" :stroke-width="2.5" aria-hidden="true" />
            Change email
          </RouterLink>
        </header>

        <div class="flex flex-1 items-center justify-center px-6 py-8 max-[520px]:px-5">
          <div class="w-full max-w-[430px]">
            <div
              class="mb-6 inline-flex size-12 items-center justify-center rounded-[14px] border border-[#d8e6e9] bg-white text-[#246b78] shadow-[0_14px_32px_rgb(18_33_36_/_8%),inset_0_1px_0_rgb(255_255_255_/_92%)]"
              aria-hidden="true"
            >
              <KeyRound :size="23" :stroke-width="2.35" />
            </div>

            <Transition mode="out-in" name="otp-panel">
              <div v-if="!isVerified" key="form">
                <div class="mb-6">
                  <p class="mb-3 text-xs font-black uppercase tracking-[0.12em] text-[#246b78]">
                    Password recovery
                  </p>
                  <h2 class="m-0 text-[1.7rem] font-extrabold leading-tight text-[#172224]">
                    Enter the 6-digit code sent to your Gmail.
                  </h2>
                  <p class="mt-3 text-sm font-semibold leading-6 text-[#6c8085]">
                    You only need to type the numbers from the email. Each digit goes in one box,
                    and we will move you forward automatically as you fill them in.
                  </p>
                </div>

                <form class="grid gap-5" @submit.prevent="confirmOtp">
                  <fieldset class="m-0 border-0 p-0">
                    <legend class="mb-3 text-xs font-extrabold leading-none text-[#172224]">
                      Recovery code
                    </legend>

                    <div class="grid grid-cols-6 gap-2.5 max-[420px]:gap-2" @paste="handlePaste">
                      <input
                        v-for="(_, index) in otpDigits"
                        :key="index"
                        :aria-label="`Digit ${index + 1} of 6`"
                        :data-otp-index="index"
                        :value="otpDigits[index]"
                        class="otp-digit-input aspect-square min-h-[52px] w-full rounded-lg border border-[#d8e6e9] bg-white text-center text-[1.35rem] font-black leading-none text-[#172224] shadow-[0_10px_22px_rgb(18_33_36_/_6%),inset_0_1px_0_rgb(255_255_255_/_92%)] outline-none transition duration-180 placeholder:text-[#9aaeb2] focus:border-[#8adff3] focus:shadow-[0_0_0_4px_rgb(174_238_255_/_26%),0_12px_26px_rgb(18_33_36_/_8%)] max-[420px]:min-h-[46px] max-[420px]:text-[1.1rem]"
                        inputmode="numeric"
                        maxlength="1"
                        pattern="[0-9]*"
                        type="text"
                        autocomplete="one-time-code"
                        @input="updateDigit(index, $event)"
                        @keydown="handleKeydown(index, $event)"
                      />
                    </div>
                  </fieldset>

                  <div
                    class="grid grid-cols-[auto_1fr] gap-3 rounded-lg border border-[#d8e6e9] bg-[#f4fafb] px-4 py-3 text-xs font-bold leading-5 text-[#4f666c]"
                  >
                    <Clock3
                      class="mt-0.5 text-[#246b78]"
                      :size="17"
                      :stroke-width="2.35"
                      aria-hidden="true"
                    />
                    <p class="m-0">
                      If you requested more than one email, use the newest code in your inbox.
                    </p>
                  </div>

                  <button
                    class="inline-flex min-h-11 w-full cursor-pointer items-center justify-center rounded-lg border border-[#2b7f8f] bg-[#246b78] text-sm font-black leading-none text-white shadow-[0_16px_30px_rgb(18_33_36_/_18%),0_0_24px_rgb(174_238_255_/_18%),inset_0_1px_0_rgb(255_255_255_/_14%)] transition duration-180 hover:-translate-y-px hover:border-[#236575] hover:bg-[#1f5f6d] hover:shadow-[0_18px_36px_rgb(18_33_36_/_22%),0_0_28px_rgb(174_238_255_/_22%),inset_0_1px_0_rgb(255_255_255_/_16%)] focus-visible:outline focus-visible:outline-3 focus-visible:outline-offset-3 focus-visible:outline-[#aeeeff]/70 disabled:cursor-not-allowed disabled:border-[#b9d9de] disabled:bg-[#9ab9c0] disabled:shadow-none disabled:hover:translate-y-0 motion-reduce:transition-none motion-reduce:hover:translate-y-0"
                    type="submit"
                    :disabled="!isOtpComplete"
                  >
                    Confirm code
                  </button>
                </form>

                <p class="mt-5 text-center text-xs font-bold leading-5 text-[#6c8085]">
                  Did not receive it?
                  <RouterLink
                    class="font-extrabold text-[#172224] underline decoration-[#aeeeff] decoration-2 underline-offset-4"
                    to="/forgot-password"
                  >
                    Send another code
                  </RouterLink>
                </p>
              </div>

              <div v-else key="confirmed">
                <div
                  class="mb-6 inline-flex min-h-11 items-center gap-2 rounded-full border border-[#ccefed] bg-[#ecfbf8] px-4 text-xs font-black text-[#0f5753]"
                >
                  <CheckCircle2 :size="17" :stroke-width="2.4" aria-hidden="true" />
                  Code confirmed
                </div>

                <h2 class="m-0 text-[1.7rem] font-extrabold leading-tight text-[#172224]">
                  Your recovery code is valid.
                </h2>
                <p class="mt-3 text-sm font-semibold leading-6 text-[#6c8085]">
                  Now you can create a new password for your Blendes account. Keep this browser tab
                  open while you finish the recovery.
                </p>

                <RouterLink
                  class="mt-6 inline-flex min-h-11 w-full items-center justify-center rounded-lg border border-[#2b7f8f] bg-[#246b78] text-sm font-black leading-none text-white no-underline shadow-[0_16px_30px_rgb(18_33_36_/_18%),0_0_24px_rgb(174_238_255_/_18%),inset_0_1px_0_rgb(255_255_255_/_14%)] transition duration-180 hover:-translate-y-px hover:border-[#236575] hover:bg-[#1f5f6d] focus-visible:outline focus-visible:outline-3 focus-visible:outline-offset-3 focus-visible:outline-[#aeeeff]/70 motion-reduce:transition-none motion-reduce:hover:translate-y-0"
                  to="/new-password"
                >
                  Continue
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
.otp-digit-input::-webkit-outer-spin-button,
.otp-digit-input::-webkit-inner-spin-button {
  margin: 0;
  appearance: none;
}

.otp-panel-enter-active,
.otp-panel-leave-active {
  transition:
    opacity 180ms ease,
    transform 180ms ease;
}

.otp-panel-enter-from,
.otp-panel-leave-to {
  opacity: 0;
  transform: translateY(8px);
}

@media (prefers-reduced-motion: reduce) {
  .otp-panel-enter-active,
  .otp-panel-leave-active {
    transition: opacity 140ms ease;
  }

  .otp-panel-enter-from,
  .otp-panel-leave-to {
    transform: none;
  }
}
</style>
