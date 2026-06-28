import { useMutation, useQuery, useQueryClient } from '@tanstack/vue-query'

import { deleteCurrentAccount, getCurrentAccount, updateCurrentAccount } from './requests'

export const accountKeys = {
  all: ['accounts'] as const,
  current: () => [...accountKeys.all, 'current'] as const,
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
    onSuccess: (account) => {
      queryClient.setQueryData(accountKeys.current(), account)
    },
  })
}

export function useDeleteCurrentAccountMutation() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: deleteCurrentAccount,
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: accountKeys.all })
    },
  })
}
