const refreshTokenStorageKey = 'blendes.refreshToken'
const refreshTokenExpiresAtStorageKey = 'blendes.refreshTokenExpiresAt'

export type StoredRefreshToken = {
  expiresAt: string
  refreshToken: string
}

export function saveRefreshToken(payload: StoredRefreshToken) {
  try {
    sessionStorage.setItem(refreshTokenStorageKey, payload.refreshToken)
    sessionStorage.setItem(refreshTokenExpiresAtStorageKey, payload.expiresAt)
  } catch {
    // Session restore is best-effort. The in-memory session remains active.
  }
}

export function getStoredRefreshToken(): StoredRefreshToken | null {
  try {
    const refreshToken = sessionStorage.getItem(refreshTokenStorageKey)
    const expiresAt = sessionStorage.getItem(refreshTokenExpiresAtStorageKey)

    if (!refreshToken || !expiresAt) {
      return null
    }

    if (Number.isNaN(Date.parse(expiresAt)) || Date.parse(expiresAt) <= Date.now()) {
      clearStoredRefreshToken()
      return null
    }

    return {
      expiresAt,
      refreshToken,
    }
  } catch {
    return null
  }
}

export function clearStoredRefreshToken() {
  try {
    sessionStorage.removeItem(refreshTokenStorageKey)
    sessionStorage.removeItem(refreshTokenExpiresAtStorageKey)
  } catch {
    // Nothing to clear when browser storage is unavailable.
  }
}
