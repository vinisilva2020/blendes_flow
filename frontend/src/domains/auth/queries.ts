import { useMutation, useQuery } from '@tanstack/vue-query'

import {
  listAuthenticationSessions,
  revokeAuthenticationSession,
  signIn,
  signInWithGoogle,
  signOut,
} from './requests'

export const authenticationKeys = {
  all: ['authentication'] as const,
  sessions: () => [...authenticationKeys.all, 'sessions'] as const,
}

export function useSignInMutation() {
  return useMutation({
    mutationFn: signIn,
  })
}

export function useGoogleSignInMutation() {
  return useMutation({
    mutationFn: signInWithGoogle,
  })
}

export function useSignOutMutation() {
  return useMutation({
    mutationFn: signOut,
  })
}

export function useAuthenticationSessions(enabled: boolean) {
  return useQuery({
    enabled,
    queryKey: authenticationKeys.sessions(),
    queryFn: listAuthenticationSessions,
  })
}

export function useRevokeAuthenticationSessionMutation() {
  return useMutation({
    mutationFn: revokeAuthenticationSession,
  })
}
