import { request } from '@/lib/http/client'
import { getMockAccount, isMockDataEnabled } from '@/lib/mock/data'

import type { Account, AccountChanges } from './contracts'

export function getCurrentAccount() {
  if (isMockDataEnabled) {
    return getMockAccount()
  }

  return request<Account>({
    method: 'GET',
    url: '/v1/accounts/me/',
  })
}

export async function updateCurrentAccount(payload: AccountChanges) {
  if (isMockDataEnabled) {
    const account = await getMockAccount()

    return {
      ...account,
      ...payload,
    } satisfies Account
  }

  return request<Account>({
    data: payload,
    method: 'PATCH',
    url: '/v1/accounts/me/',
  })
}

export function deleteCurrentAccount() {
  if (isMockDataEnabled) {
    return Promise.resolve()
  }

  return request<void>({
    method: 'DELETE',
    url: '/v1/accounts/me/',
  })
}
