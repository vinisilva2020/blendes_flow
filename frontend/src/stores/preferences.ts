import { computed, shallowRef, watch } from 'vue'
import { defineStore } from 'pinia'

const preferencesStorageKey = 'blendes.preferences'

const colorSchemePreferences = ['light', 'dark'] as const
const languagePreferences = ['pt-BR', 'es-ES', 'en-US'] as const

export type ColorSchemePreference = (typeof colorSchemePreferences)[number]
export type LanguagePreference = (typeof languagePreferences)[number]

export interface UserPreferences {
  colorScheme: ColorSchemePreference
  enableFloatingTips: boolean
  isFavoritesOpen: boolean
  isSidebarCollapsed: boolean
  language: LanguagePreference
  prefersReducedMotion: boolean
}

const defaultPreferences: UserPreferences = {
  colorScheme: 'light',
  enableFloatingTips: true,
  isFavoritesOpen: true,
  isSidebarCollapsed: false,
  language: 'pt-BR',
  prefersReducedMotion: false,
}

export const usePreferencesStore = defineStore('preferences', () => {
  const preferences = shallowRef<UserPreferences>(restorePreferences())

  const colorScheme = computed(() => preferences.value.colorScheme)
  const enableFloatingTips = computed(() => preferences.value.enableFloatingTips)
  const isFavoritesOpen = computed(() => preferences.value.isFavoritesOpen)
  const isSidebarCollapsed = computed(() => preferences.value.isSidebarCollapsed)
  const language = computed(() => preferences.value.language)
  const prefersReducedMotion = computed(() => preferences.value.prefersReducedMotion)

  function updatePreferences(nextPreferences: Partial<UserPreferences>) {
    preferences.value = {
      ...preferences.value,
      ...nextPreferences,
    }

    savePreferences(preferences.value)
  }

  function setColorScheme(colorSchemePreference: ColorSchemePreference) {
    updatePreferences({ colorScheme: colorSchemePreference })
  }

  function setLanguage(languagePreference: LanguagePreference) {
    updatePreferences({ language: languagePreference })
  }

  function setPrefersReducedMotion(shouldReduceMotion: boolean) {
    updatePreferences({ prefersReducedMotion: shouldReduceMotion })
  }

  function setEnableFloatingTips(shouldEnableFloatingTips: boolean) {
    updatePreferences({ enableFloatingTips: shouldEnableFloatingTips })
  }

  function setFavoritesOpen(isOpen: boolean) {
    updatePreferences({ isFavoritesOpen: isOpen })
  }

  function setSidebarCollapsed(isCollapsed: boolean) {
    updatePreferences({ isSidebarCollapsed: isCollapsed })
  }

  function toggleFavorites() {
    setFavoritesOpen(!preferences.value.isFavoritesOpen)
  }

  function toggleSidebar() {
    setSidebarCollapsed(!preferences.value.isSidebarCollapsed)
  }

  function resetPreferences() {
    preferences.value = { ...defaultPreferences }
    savePreferences(preferences.value)
  }

  watch(colorScheme, applyColorSchemePreference, { immediate: true })

  return {
    colorScheme,
    enableFloatingTips,
    isFavoritesOpen,
    isSidebarCollapsed,
    language,
    preferences,
    prefersReducedMotion,
    resetPreferences,
    setColorScheme,
    setEnableFloatingTips,
    setFavoritesOpen,
    setLanguage,
    setPrefersReducedMotion,
    setSidebarCollapsed,
    toggleFavorites,
    toggleSidebar,
    updatePreferences,
  }
})

function restorePreferences() {
  try {
    const value = localStorage.getItem(preferencesStorageKey)

    if (!value) {
      return { ...defaultPreferences }
    }

    return normalizePreferences(JSON.parse(value) as unknown)
  } catch {
    clearStoredPreferences()
    return { ...defaultPreferences }
  }
}

function normalizePreferences(value: unknown): UserPreferences {
  if (!isRecord(value)) {
    return { ...defaultPreferences }
  }

  return {
    colorScheme: isColorSchemePreference(value.colorScheme)
      ? value.colorScheme
      : defaultPreferences.colorScheme,
    enableFloatingTips:
      typeof value.enableFloatingTips === 'boolean'
        ? value.enableFloatingTips
        : defaultPreferences.enableFloatingTips,
    isFavoritesOpen:
      typeof value.isFavoritesOpen === 'boolean'
        ? value.isFavoritesOpen
        : defaultPreferences.isFavoritesOpen,
    isSidebarCollapsed:
      typeof value.isSidebarCollapsed === 'boolean'
        ? value.isSidebarCollapsed
        : defaultPreferences.isSidebarCollapsed,
    language: isLanguagePreference(value.language) ? value.language : defaultPreferences.language,
    prefersReducedMotion:
      typeof value.prefersReducedMotion === 'boolean'
        ? value.prefersReducedMotion
        : defaultPreferences.prefersReducedMotion,
  }
}

function savePreferences(preferences: UserPreferences) {
  try {
    localStorage.setItem(preferencesStorageKey, JSON.stringify(preferences))
  } catch {
    // Preferences remain available in memory when browser storage is unavailable.
  }
}

function clearStoredPreferences() {
  try {
    localStorage.removeItem(preferencesStorageKey)
  } catch {
    // Nothing to clear when browser storage is unavailable.
  }
}

function applyColorSchemePreference(colorSchemePreference: ColorSchemePreference) {
  if (typeof document === 'undefined') {
    return
  }

  const isDarkMode = colorSchemePreference === 'dark'

  document.documentElement.classList.toggle('dark', isDarkMode)
  document.documentElement.dataset.theme = colorSchemePreference
  document.documentElement.style.colorScheme = colorSchemePreference
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null && !Array.isArray(value)
}

function isColorSchemePreference(value: unknown): value is ColorSchemePreference {
  return colorSchemePreferences.includes(value as ColorSchemePreference)
}

function isLanguagePreference(value: unknown): value is LanguagePreference {
  return languagePreferences.includes(value as LanguagePreference)
}
