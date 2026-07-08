import { useMutation, useQuery, useQueryClient } from '@tanstack/vue-query'
import { computed, toValue, type MaybeRefOrGetter } from 'vue'

import type { Blave, NewBlave, UpdateBlave } from './contracts'
import { createBlave, deleteBlave, listBlaves, updateBlave } from './requests'

export const blaveKeys = {
  all: ['blaves'] as const,
  lists: () => [...blaveKeys.all, 'list'] as const,
  list: (organizationId: number) => [...blaveKeys.lists(), organizationId] as const,
}

export function useBlaves(
  organizationId: MaybeRefOrGetter<number | null>,
  enabled: MaybeRefOrGetter<boolean> = true,
) {
  const resolvedOrganizationId = computed(() => toValue(organizationId))

  return useQuery({
    enabled: computed(() => toValue(enabled) && resolvedOrganizationId.value !== null),
    queryKey: computed(() =>
      resolvedOrganizationId.value === null
        ? [...blaveKeys.lists(), 'current']
        : blaveKeys.list(resolvedOrganizationId.value),
    ),
    queryFn: () => listBlaves(resolvedOrganizationId.value!),
  })
}

export function useCreateBlaveMutation(organizationId: MaybeRefOrGetter<number | null>) {
  const queryClient = useQueryClient()
  const resolvedOrganizationId = computed(() => toValue(organizationId))

  return useMutation({
    mutationFn: (payload: NewBlave) => {
      if (resolvedOrganizationId.value === null) {
        throw new Error('Select a workspace before creating a flow.')
      }

      return createBlave(resolvedOrganizationId.value, payload)
    },
    onSuccess: () => {
      if (resolvedOrganizationId.value !== null) {
        void queryClient.invalidateQueries({
          queryKey: blaveKeys.list(resolvedOrganizationId.value),
        })
      }
    },
  })
}

export function useUpdateBlaveMutation(organizationId: MaybeRefOrGetter<number | null>) {
  const queryClient = useQueryClient()
  const resolvedOrganizationId = computed(() => toValue(organizationId))

  function updateCachedBlave(updatedBlave: Blave) {
    if (resolvedOrganizationId.value === null) {
      return
    }

    queryClient.setQueryData<Blave[]>(blaveKeys.list(resolvedOrganizationId.value), (current) =>
      current?.map((blave) => (blave.id === updatedBlave.id ? updatedBlave : blave)),
    )
  }

  return useMutation({
    mutationFn: ({ blaveId, payload }: { blaveId: number; payload: UpdateBlave }) =>
      updateBlave(blaveId, payload),
    onSuccess: (updatedBlave) => {
      updateCachedBlave(updatedBlave)

      if (resolvedOrganizationId.value !== null) {
        void queryClient.invalidateQueries({
          queryKey: blaveKeys.list(resolvedOrganizationId.value),
        })
      }
    },
  })
}

export function useDeleteBlaveMutation(organizationId: MaybeRefOrGetter<number | null>) {
  const queryClient = useQueryClient()
  const resolvedOrganizationId = computed(() => toValue(organizationId))

  function removeCachedBlave(blaveId: number) {
    if (resolvedOrganizationId.value === null) {
      return
    }

    queryClient.setQueryData<Blave[]>(blaveKeys.list(resolvedOrganizationId.value), (current) =>
      current?.filter((blave) => blave.id !== blaveId),
    )
  }

  return useMutation({
    mutationFn: (blaveId: number) => deleteBlave(blaveId),
    onSuccess: (_data, blaveId) => {
      removeCachedBlave(blaveId)

      if (resolvedOrganizationId.value !== null) {
        void queryClient.invalidateQueries({
          queryKey: blaveKeys.list(resolvedOrganizationId.value),
        })
      }
    },
  })
}
