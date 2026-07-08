import { request } from '@/lib/http/client'

import type { Blave, NewBlave, UpdateBlave } from './contracts'

export function listBlaves(organizationId: number) {
  return request<Blave[]>({
    method: 'GET',
    url: `/v1/organizations/${organizationId}/blaves/`,
  })
}

export function createBlave(organizationId: number, payload: NewBlave) {
  return request<Blave>({
    data: payload,
    method: 'POST',
    url: `/v1/organizations/${organizationId}/blaves/`,
  })
}

export function updateBlave(blaveId: number, payload: UpdateBlave) {
  return request<Blave>({
    data: payload,
    method: 'PATCH',
    url: `/v1/blaves/${blaveId}/`,
  })
}

export function deleteBlave(blaveId: number) {
  return request<void>({
    method: 'DELETE',
    url: `/v1/blaves/${blaveId}/`,
  })
}
