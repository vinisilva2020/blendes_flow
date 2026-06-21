import axios, { AxiosHeaders, type AxiosRequestConfig } from 'axios'

import { getAccessToken } from './access-token'
import { normalizeApiError } from './errors'

const defaultApiBaseUrl = import.meta.env.DEV ? 'http://127.0.0.1:8000/api' : '/api'

export const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL ?? defaultApiBaseUrl,
  headers: {
    Accept: 'application/json',
    'Content-Type': 'application/json',
  },
  withCredentials: true,
})

apiClient.interceptors.request.use((config) => {
  const token = getAccessToken()

  // Mantem o token em memoria e injeta o Bearer em um unico lugar.
  if (token) {
    config.headers = AxiosHeaders.from(config.headers)
    config.headers.set('Authorization', `Bearer ${token}`)
  }

  return config
})

export async function request<T>(config: AxiosRequestConfig): Promise<T> {
  try {
    const response = await apiClient.request<T>(config)

    if (response.status === 204) {
      return undefined as T
    }

    return response.data
  } catch (error) {
    throw normalizeApiError(error)
  }
}
