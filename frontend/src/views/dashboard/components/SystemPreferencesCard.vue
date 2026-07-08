<script setup lang="ts">
import { computed } from 'vue'
import { Check, Languages, MessageCircleQuestion, Moon, Sun } from '@lucide/vue'

import {
  usePreferencesStore,
  type ColorSchemePreference,
  type LanguagePreference,
} from '@/stores/preferences'

type ThemeOption = {
  icon: typeof Sun
  label: string
  value: ColorSchemePreference
}

type LanguageOption = {
  label: string
  value: LanguagePreference
}

const preferencesStore = usePreferencesStore()

const themeOptions: ThemeOption[] = [
  { icon: Sun, label: 'Light', value: 'light' },
  { icon: Moon, label: 'Dark', value: 'dark' },
]

const languageOptions: LanguageOption[] = [
  { label: 'Português (Brasil)', value: 'pt-BR' },
  { label: 'Español', value: 'es-ES' },
  { label: 'English', value: 'en-US' },
]

const selectedLanguage = computed({
  get: () => preferencesStore.language,
  set: (language: LanguagePreference) => {
    preferencesStore.setLanguage(language)
  },
})

function selectColorScheme(colorScheme: ColorSchemePreference) {
  preferencesStore.setColorScheme(colorScheme)
}

function toggleFloatingTips() {
  preferencesStore.setEnableFloatingTips(!preferencesStore.enableFloatingTips)
}
</script>

<template>
  <section
    class="rounded-3xl bg-white p-2 shadow-[0_0_0_1px_rgb(15_23_42_/_6%),0_10px_28px_rgb(15_23_42_/_5%)] transition-[background-color,box-shadow] duration-200 dark:bg-slate-900 dark:shadow-[0_0_0_1px_rgb(51_65_85_/_70%),0_18px_42px_rgb(0_0_0_/_24%)]"
    aria-labelledby="system-preferences-title"
  >
    <div
      class="rounded-2xl bg-slate-50/80 p-4 transition-colors duration-200 sm:p-5 md:p-6 dark:bg-slate-950/70"
    >
      <header class="flex flex-col gap-2 sm:flex-row sm:items-start sm:justify-between">
        <div>
          <p
            class="text-xs leading-4 font-semibold tracking-[0.12em] text-blue-600 uppercase dark:text-blue-300"
          >
            Settings
          </p>
          <h2
            id="system-preferences-title"
            class="mt-1 text-lg leading-6 font-semibold text-balance text-slate-950 dark:text-slate-50"
          >
            System preferences
          </h2>
          <p
            class="mt-1 max-w-2xl text-sm leading-6 font-medium text-pretty text-slate-500 dark:text-slate-400"
          >
            Adjust how the workspace looks and how much contextual guidance appears while you work.
          </p>
        </div>
      </header>

      <div class="mt-6 grid gap-3">
        <section
          class="grid gap-4 rounded-2xl bg-white p-4 shadow-[0_0_0_1px_rgb(15_23_42_/_5%)] transition-[background-color,box-shadow] duration-200 md:grid-cols-[minmax(0,1fr)_minmax(260px,360px)] md:items-center dark:bg-slate-900 dark:shadow-[0_0_0_1px_rgb(51_65_85_/_58%)]"
          aria-labelledby="settings-theme-label"
        >
          <div class="min-w-0">
            <span
              id="settings-theme-label"
              class="block text-sm leading-5 font-semibold text-slate-800 dark:text-slate-100"
            >
              Theme
            </span>
            <p
              class="mt-1 text-sm leading-5 font-medium text-pretty text-slate-500 dark:text-slate-400"
            >
              Choose the visual mode used across the application interface.
            </p>
          </div>

          <div
            class="grid grid-cols-2 gap-1 rounded-2xl bg-slate-100 p-1 shadow-[inset_0_0_0_1px_rgb(15_23_42_/_6%)] transition-colors duration-200 dark:bg-slate-800 dark:shadow-[inset_0_0_0_1px_rgb(51_65_85_/_65%)]"
            role="group"
            aria-labelledby="settings-theme-label"
          >
            <button
              v-for="option in themeOptions"
              :key="option.value"
              class="inline-flex min-h-10 cursor-pointer items-center justify-center gap-2 rounded-xl px-3 text-sm font-semibold outline-none transition-[background-color,color,scale,box-shadow] duration-150 ease-out focus-visible:ring-4 focus-visible:ring-blue-100 active:scale-[0.96] motion-reduce:transition-none"
              :class="
                preferencesStore.colorScheme === option.value
                  ? 'bg-white text-blue-700 shadow-[0_0_0_1px_rgb(147_197_253_/_75%),0_6px_14px_rgb(37_99_235_/_8%)] dark:bg-blue-400/15 dark:text-blue-200 dark:shadow-[0_0_0_1px_rgb(96_165_250_/_32%)]'
                  : 'text-slate-600 hover:bg-white/70 hover:text-slate-950 dark:text-slate-300 dark:hover:bg-slate-700 dark:hover:text-slate-50'
              "
              type="button"
              :aria-pressed="preferencesStore.colorScheme === option.value"
              @click="selectColorScheme(option.value)"
            >
              <component :is="option.icon" :size="15" :stroke-width="2.2" aria-hidden="true" />
              {{ option.label }}
            </button>
          </div>
        </section>

        <label
          class="grid gap-4 rounded-2xl bg-white p-4 shadow-[0_0_0_1px_rgb(15_23_42_/_5%)] transition-[background-color,box-shadow] duration-200 md:grid-cols-[minmax(0,1fr)_minmax(260px,360px)] md:items-center dark:bg-slate-900 dark:shadow-[0_0_0_1px_rgb(51_65_85_/_58%)]"
          for="settings-language"
        >
          <span class="min-w-0">
            <span
              class="flex items-center gap-2 text-sm leading-5 font-semibold text-slate-800 dark:text-slate-100"
            >
              <Languages
                class="size-4 text-slate-500 dark:text-slate-400"
                :stroke-width="2.2"
                aria-hidden="true"
              />
              Language
            </span>
            <span
              class="mt-1 block text-sm leading-5 font-medium text-pretty text-slate-500 dark:text-slate-400"
            >
              Select the default language for navigation, labels, and system messages.
            </span>
          </span>

          <select
            id="settings-language"
            v-model="selectedLanguage"
            class="min-h-11 w-full cursor-pointer rounded-xl border border-slate-200/80 bg-white px-3 text-sm font-semibold text-slate-900 outline-none transition-[background-color,border-color,color,box-shadow] duration-150 focus:border-blue-300 focus:shadow-[0_0_0_4px_rgb(219_234_254_/_85%)] dark:border-slate-700 dark:bg-slate-950 dark:text-slate-100 dark:focus:border-blue-400/50 dark:focus:shadow-[0_0_0_4px_rgb(30_64_175_/_35%)]"
            name="settingsLanguage"
          >
            <option v-for="option in languageOptions" :key="option.value" :value="option.value">
              {{ option.label }}
            </option>
          </select>
        </label>

        <section
          class="grid gap-4 rounded-2xl bg-white p-4 shadow-[0_0_0_1px_rgb(15_23_42_/_5%)] transition-[background-color,box-shadow] duration-200 md:grid-cols-[minmax(0,1fr)_minmax(260px,360px)] md:items-center dark:bg-slate-900 dark:shadow-[0_0_0_1px_rgb(51_65_85_/_58%)]"
          aria-labelledby="settings-floating-tips-label"
        >
          <div class="min-w-0">
            <span
              id="settings-floating-tips-label"
              class="flex items-center gap-2 text-sm leading-5 font-semibold text-slate-800 dark:text-slate-100"
            >
              <MessageCircleQuestion
                class="size-4 text-slate-500 dark:text-slate-400"
                :stroke-width="2.2"
                aria-hidden="true"
              />
              Floating tips
            </span>
            <p
              class="mt-1 text-sm leading-5 font-medium text-pretty text-slate-500 dark:text-slate-400"
            >
              Show compact helper tips on controls that benefit from extra context.
            </p>
          </div>

          <div
            class="flex items-center justify-between gap-3 rounded-2xl bg-slate-50 p-2.5 transition-colors duration-200 dark:bg-slate-950"
          >
            <span
              class="text-sm leading-5 font-semibold text-slate-700 dark:text-slate-200"
              aria-live="polite"
            >
              {{ preferencesStore.enableFloatingTips ? 'Enabled' : 'Disabled' }}
            </span>

            <button
              class="relative inline-flex min-h-10 w-16 cursor-pointer items-center rounded-full p-1 outline-none transition-[background-color,scale,box-shadow] duration-150 ease-out focus-visible:ring-4 focus-visible:ring-blue-100 active:scale-[0.96] motion-reduce:transition-none"
              :class="
                preferencesStore.enableFloatingTips
                  ? 'bg-blue-600 shadow-[0_6px_14px_rgb(37_99_235_/_18%)] dark:bg-blue-500'
                  : 'bg-slate-200 shadow-[inset_0_0_0_1px_rgb(15_23_42_/_7%)] dark:bg-slate-700 dark:shadow-[inset_0_0_0_1px_rgb(148_163_184_/_12%)]'
              "
              type="button"
              role="switch"
              :aria-checked="preferencesStore.enableFloatingTips"
              aria-labelledby="settings-floating-tips-label"
              @click="toggleFloatingTips"
            >
              <span
                class="grid size-8 place-items-center rounded-full bg-white text-blue-700 shadow-[0_2px_7px_rgb(15_23_42_/_16%)] transition-[transform,color] duration-150 ease-out motion-reduce:transition-none dark:bg-slate-100"
                :class="
                  preferencesStore.enableFloatingTips
                    ? 'translate-x-6 text-blue-700'
                    : 'translate-x-0 text-slate-400'
                "
              >
                <Check :size="14" :stroke-width="2.4" aria-hidden="true" />
              </span>
            </button>
          </div>
        </section>
      </div>
    </div>
  </section>
</template>
