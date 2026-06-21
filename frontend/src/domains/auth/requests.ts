import { request } from '@/lib/http/client'

import type {
  AuthenticationSession,
  AuthenticationTokens,
  LoginCredentials,
  RefreshTokenPayload,
} from './contracts'

export function signIn(credentials: LoginCredentials) {
  return request<AuthenticationTokens>({
    data: credentials,
    method: 'POST',
    url: '/v1/authentication/login/',
  })
}

export function refreshAuthentication(payload: RefreshTokenPayload) {
  return request<AuthenticationTokens>({
    data: payload,
    method: 'POST',
    url: '/v1/authentication/refresh/',
  })
}

export function signOut() {
  return request<void>({
    method: 'POST',
    url: '/v1/authentication/logout/',
  })
}

export function listAuthenticationSessions() {
  return request<AuthenticationSession[]>({
    method: 'GET',
    url: '/v1/authentication/sessions/',
  })
}

export function revokeAuthenticationSession(sessionId: string) {
  return request<void>({
    method: 'DELETE',
    url: `/v1/authentication/sessions/${sessionId}/`,
  })
}
