<script setup>
import { Blend, Eye } from '@lucide/vue'
import { useRouter } from 'vue-router'
import heroImage from '@/assets/img/hero.png'
import GoogleAuthButton from '@/components/buttons/GoogleButton.vue'

const router = useRouter()

function goToOrganizations() {
  router.push({ name: 'organizations' })
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
            Uma plataforma para entender e melhorar fluxos.
          </h1>

          <p class="mx-auto mt-4 max-w-[360px] text-sm font-semibold leading-6 text-white/62">
            O Blendes transforma sinais, rotinas e indicadores em uma leitura clara para evoluir com
            mais precisão.
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
          <a
            class="inline-flex items-center gap-2 text-sm font-extrabold text-[#172224] no-underline"
            href="/"
            aria-label="Blendes Flow home"
          >
            <span
              class="inline-flex size-9 items-center justify-center rounded-full border border-[#d8e6e9] bg-white shadow-[0_10px_26px_rgb(18_33_36_/_8%)]"
            >
              <Blend class="text-[#246b78]" :size="20" :stroke-width="2.4" aria-hidden="true" />
            </span>
            <span class="max-[520px]:hidden">Blendes Flow</span>
          </a>

          <p class="m-0 text-xs font-bold text-[#4f666c]">
            Não tem conta?
            <RouterLink
              class="font-extrabold text-[#172224] underline decoration-[#aeeeff] decoration-2 underline-offset-4"
              to="/register"
              >Criar conta</RouterLink
            >
          </p>
        </header>

        <div class="flex flex-1 items-center justify-center px-6 py-8 max-[520px]:px-5">
          <div class="w-full max-w-[390px]">
            <div class="mb-6 text-center">
              <h2 class="m-0 text-[1.55rem] font-extrabold leading-tight text-[#172224]">
                Bem-vindo de volta ao Blendes
              </h2>
              <p class="mt-2 text-sm font-semibold leading-5 text-[#6c8085]">
                Entre com seus dados para continuar acompanhando seus fluxos.
              </p>
            </div>

            <div class="grid gap-3">
              <GoogleAuthButton />
            </div>

            <div class="my-5 grid grid-cols-[1fr_auto_1fr] items-center gap-3" aria-hidden="true">
              <span class="h-px bg-[#dce8eb]"></span>
              <p class="m-0 text-xs font-extrabold uppercase leading-none text-[#7a8f94]">
                ou entre com
              </p>
              <span class="h-px bg-[#dce8eb]"></span>
            </div>

            <form class="grid gap-4" @submit.prevent="goToOrganizations">
              <label class="grid gap-2" for="email">
                <span class="text-xs font-extrabold leading-none text-[#172224]">Email</span>
                <input
                  id="email"
                  class="min-h-11 w-full rounded-lg border border-[#d8e6e9] bg-white px-3.5 text-sm font-bold text-[#172224] shadow-[0_8px_18px_rgb(18_33_36_/_5%),inset_0_1px_0_rgb(255_255_255_/_92%)] outline-none transition duration-180 placeholder:text-[#9aaeb2] focus:border-[#8adff3] focus:shadow-[0_0_0_4px_rgb(174_238_255_/_26%),0_10px_24px_rgb(18_33_36_/_7%)]"
                  name="email"
                  type="email"
                  autocomplete="email"
                  placeholder="seu@email.com"
                />
              </label>

              <label class="grid gap-2" for="password">
                <span class="text-xs font-extrabold leading-none text-[#172224]">Password</span>
                <span class="relative block">
                  <input
                    id="password"
                    class="min-h-11 w-full rounded-lg border border-[#d8e6e9] bg-white px-3.5 pr-11 text-sm font-bold text-[#172224] shadow-[0_8px_18px_rgb(18_33_36_/_5%),inset_0_1px_0_rgb(255_255_255_/_92%)] outline-none transition duration-180 placeholder:text-[#9aaeb2] focus:border-[#8adff3] focus:shadow-[0_0_0_4px_rgb(174_238_255_/_26%),0_10px_24px_rgb(18_33_36_/_7%)]"
                    name="password"
                    type="password"
                    autocomplete="current-password"
                    placeholder="Mínimo 8 caracteres"
                  />
                  <Eye
                    class="pointer-events-none absolute right-3.5 top-1/2 -translate-y-1/2 text-[#7a8f94]"
                    :size="17"
                    :stroke-width="2.2"
                    aria-hidden="true"
                  />
                </span>
              </label>

              <button
                class="mt-1 inline-flex min-h-11 w-full cursor-pointer items-center justify-center rounded-lg border border-[#2b7f8f] bg-[#246b78] text-sm font-black leading-none text-white shadow-[0_16px_30px_rgb(18_33_36_/_18%),0_0_24px_rgb(174_238_255_/_18%),inset_0_1px_0_rgb(255_255_255_/_14%)] transition duration-180 hover:-translate-y-px hover:border-[#236575] hover:bg-[#1f5f6d] hover:shadow-[0_18px_36px_rgb(18_33_36_/_22%),0_0_28px_rgb(174_238_255_/_22%),inset_0_1px_0_rgb(255_255_255_/_16%)] focus-visible:outline focus-visible:outline-3 focus-visible:outline-offset-3 focus-visible:outline-[#aeeeff]/70 motion-reduce:transition-none motion-reduce:hover:translate-y-0"
                type="submit"
              >
                Entrar
              </button>
            </form>

            <RouterLink
              class="mt-4 block text-center text-xs font-extrabold text-[#172224] underline decoration-[#aeeeff] decoration-2 underline-offset-4"
              to="/forgot-password"
            >
              Esqueceu sua senha?
            </RouterLink>
          </div>
        </div>

        <footer
          class="flex items-center justify-between gap-4 px-7 py-5 text-[0.7rem] font-bold text-[#7a8f94] max-[520px]:px-5"
        >
          <span>© 2026 Blendes</span>
          <div class="flex gap-4">
            <a class="text-[#62777d] no-underline hover:text-[#172224]" href="#privacy"
              >Privacidade</a
            >
            <a class="text-[#62777d] no-underline hover:text-[#172224]" href="#support">Suporte</a>
          </div>
        </footer>
      </section>
    </section>
  </main>
</template>
