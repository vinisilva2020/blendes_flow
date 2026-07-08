import { request } from '@/lib/http/client'

import type {
  Account,
  AccountGoogleSocialAccountPayload,
  AccountPasswordPayload,
  AccountRegistrationPayload,
  AccountUpdatePayload,
} from './contracts'

export function createAccount(payload: AccountRegistrationPayload) {
  return request<Account>({
    data: payload,
    method: 'POST',
    url: '/v1/accounts/',
  })
}

export function getCurrentAccount() {
  return request<Account>({
    method: 'GET',
    url: '/v1/accounts/me/',
  })
}

export function updateCurrentAccount(payload: AccountUpdatePayload) {
  return request<Account>({
    data: payload,
    method: 'PATCH',
    url: '/v1/accounts/me/',
  })
}

export function updateCurrentAccountPassword(payload: AccountPasswordPayload) {
  return request<void>({
    data: payload,
    method: 'PUT',
    url: '/v1/accounts/me/password/',
  })
}

export function linkCurrentGoogleSocialAccount(payload: AccountGoogleSocialAccountPayload) {
  return request<Account>({
    data: payload,
    method: 'POST',
    url: '/v1/accounts/me/social-accounts/google/',
  })
}

export function unlinkCurrentGoogleSocialAccount() {
  return request<void>({
    method: 'DELETE',
    url: '/v1/accounts/me/social-accounts/google/',
  })
}
