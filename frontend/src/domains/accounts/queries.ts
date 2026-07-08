import { useMutation, useQuery, useQueryClient } from '@tanstack/vue-query'

import {
  createAccount,
  getCurrentAccount,
  linkCurrentGoogleSocialAccount,
  unlinkCurrentGoogleSocialAccount,
  updateCurrentAccount,
  updateCurrentAccountPassword,
} from './requests'

export const accountKeys = {
  all: ['accounts'] as const,
  current: () => [...accountKeys.all, 'current'] as const,
}

export function useCreateAccountMutation() {
  return useMutation({
    mutationFn: createAccount,
  })
}

export function useCurrentAccount(enabled = true) {
  return useQuery({
    enabled,
    queryKey: accountKeys.current(),
    queryFn: getCurrentAccount,
  })
}

export function useUpdateCurrentAccountMutation() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: updateCurrentAccount,
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: accountKeys.current() })
    },
  })
}

export function useUpdateCurrentAccountPasswordMutation() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: updateCurrentAccountPassword,
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: accountKeys.current() })
    },
  })
}

export function useLinkCurrentGoogleSocialAccountMutation() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: linkCurrentGoogleSocialAccount,
    onSuccess: (account) => {
      queryClient.setQueryData(accountKeys.current(), account)
    },
  })
}

export function useUnlinkCurrentGoogleSocialAccountMutation() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: unlinkCurrentGoogleSocialAccount,
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: accountKeys.current() })
    },
  })
}
