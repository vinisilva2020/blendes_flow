import { computed, shallowRef } from 'vue'
import { defineStore } from 'pinia'

import { refreshAuthentication } from '@/domains/auth/requests'
import { clearAccessToken, setAccessToken } from '@/lib/http/access-token'
import {
  clearStoredRefreshToken,
  getStoredRefreshToken,
  saveRefreshToken,
} from '@/lib/http/refresh-token'
import type { AuthenticationTokens } from '@/domains/auth/contracts'

export const useAuthenticationStore = defineStore('authentication', () => {
  const tokens = shallowRef<AuthenticationTokens | null>(null)
  const isRestoringSession = shallowRef(false)

  const isAuthenticated = computed(() => tokens.value !== null)
  const accessToken = computed(() => tokens.value?.access_token ?? null)
  const sessionId = computed(() => tokens.value?.session_id ?? null)

  function startSession(nextTokens: AuthenticationTokens) {
    tokens.value = nextTokens
    setAccessToken(nextTokens.access_token)
    saveRefreshToken({
      expiresAt: nextTokens.refresh_expires_at,
      refreshToken: nextTokens.refresh_token,
    })
  }

  function endSession() {
    tokens.value = null
    clearAccessToken()
    clearStoredRefreshToken()
  }

  async function restoreSession() {
    const storedRefreshToken = getStoredRefreshToken()

    if (!storedRefreshToken) {
      endSession()
      return false
    }

    isRestoringSession.value = true

    try {
      const nextTokens = await refreshAuthentication({
        refresh_token: storedRefreshToken.refreshToken,
      })

      startSession(nextTokens)
      return true
    } catch {
      endSession()
      return false
    } finally {
      isRestoringSession.value = false
    }
  }

  return {
    accessToken,
    endSession,
    isAuthenticated,
    isRestoringSession,
    restoreSession,
    sessionId,
    startSession,
    tokens,
  }
})
