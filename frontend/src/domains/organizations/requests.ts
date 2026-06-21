import { request } from '@/lib/http/client'

import type { NewOrganization, Organization, OrganizationChanges } from './contracts'

export function listOrganizations() {
  return request<Organization[]>({
    method: 'GET',
    url: '/v1/organizations/',
  })
}

export function createOrganization(payload: NewOrganization) {
  return request<Organization>({
    data: payload,
    method: 'POST',
    url: '/v1/organizations/',
  })
}

export function getOrganization(organizationId: number) {
  return request<Organization>({
    method: 'GET',
    url: `/v1/organizations/${organizationId}/`,
  })
}

export function updateOrganization(organizationId: number, payload: OrganizationChanges) {
  return request<Organization>({
    data: payload,
    method: 'PATCH',
    url: `/v1/organizations/${organizationId}/`,
  })
}

export function deleteOrganization(organizationId: number) {
  return request<void>({
    method: 'DELETE',
    url: `/v1/organizations/${organizationId}/`,
  })
}
