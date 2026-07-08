import { computed, toValue, type MaybeRefOrGetter } from 'vue'

const avatarModules = import.meta.glob<string>('@/assets/img/avatar/*.{png,jpg,jpeg,webp,svg}', {
  eager: true,
  import: 'default',
  query: '?url',
})

const avatarByType = Object.fromEntries(
  Object.entries(avatarModules).map(([path, src]) => {
    const fileName = path.split('/').pop() ?? ''
    const avatarType = fileName.replace(/\.[^.]+$/, '')

    return [avatarType, src]
  }),
)

export const accountAvatarOptions = Object.entries(avatarByType)
  .map(([type, src]) => ({ src, type }))
  .sort((first, second) => first.type.localeCompare(second.type))

function normalizeAvatarType(avatarType: string | null | undefined) {
  const value = avatarType?.trim()

  if (!value) {
    return null
  }

  return /^\d+$/.test(value) ? value.padStart(2, '0') : value
}

export function resolveAccountAvatarUrl(avatarType: string | null | undefined) {
  const normalizedAvatarType = normalizeAvatarType(avatarType)

  return normalizedAvatarType ? avatarByType[normalizedAvatarType] : undefined
}

export function useAccountAvatar(avatarType: MaybeRefOrGetter<string | null | undefined>) {
  const avatarUrl = computed(() => resolveAccountAvatarUrl(toValue(avatarType)))

  return {
    avatarUrl,
  }
}

export function useAccountAvatarOptions() {
  return accountAvatarOptions
}
