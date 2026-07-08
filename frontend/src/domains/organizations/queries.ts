import { useMutation, useQuery, useQueryClient } from '@tanstack/vue-query'
import { computed, toValue, type MaybeRefOrGetter } from 'vue'

import {
  createOrganization,
  deleteOrganization,
  getOrganization,
  listOrganizations,
  updateOrganization,
} from './requests'

export const organizationKeys = {
  all: ['organizations'] as const,
  lists: () => [...organizationKeys.all, 'list'] as const,
  detail: (organizationId: number) => [...organizationKeys.all, 'detail', organizationId] as const,
}

export function useOrganizations(enabled = true) {
  return useQuery({
    enabled,
    queryKey: organizationKeys.lists(),
    queryFn: listOrganizations,
  })
}

export function useOrganization(
  organizationId: MaybeRefOrGetter<number | null>,
  enabled: MaybeRefOrGetter<boolean> = true,
) {
  const resolvedOrganizationId = computed(() => toValue(organizationId))

  return useQuery({
    enabled: computed(() => toValue(enabled) && resolvedOrganizationId.value !== null),
    queryKey: computed(() =>
      resolvedOrganizationId.value === null
        ? [...organizationKeys.all, 'detail', 'current']
        : organizationKeys.detail(resolvedOrganizationId.value),
    ),
    queryFn: () => getOrganization(resolvedOrganizationId.value!),
  })
}

export function useCreateOrganizationMutation() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: createOrganization,
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: organizationKeys.lists() })
    },
  })
}

export function useUpdateOrganizationMutation() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: ({
      organizationId,
      data,
    }: {
      organizationId: number
      data: Parameters<typeof updateOrganization>[1]
    }) => updateOrganization(organizationId, data),
    onSuccess: (organization) => {
      void queryClient.invalidateQueries({ queryKey: organizationKeys.lists() })
      void queryClient.invalidateQueries({ queryKey: organizationKeys.detail(organization.id) })
    },
  })
}

export function useDeleteOrganizationMutation() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: deleteOrganization,
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: organizationKeys.lists() })
    },
  })
}
