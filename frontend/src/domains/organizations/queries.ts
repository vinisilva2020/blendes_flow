import { useMutation, useQuery, useQueryClient } from '@tanstack/vue-query'

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

export function useOrganization(organizationId: number, enabled = true) {
  return useQuery({
    enabled,
    queryKey: organizationKeys.detail(organizationId),
    queryFn: () => getOrganization(organizationId),
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
    mutationFn: ({ organizationId, data }: { organizationId: number; data: Parameters<typeof updateOrganization>[1] }) =>
      updateOrganization(organizationId, data),
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
