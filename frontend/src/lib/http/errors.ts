import axios from 'axios'

import type { ApiErrorEnvelope } from '@/domains/auth/contracts'

type ApiErrorBody = ApiErrorEnvelope['error']

export class ApiRequestError extends Error {
  readonly status: number | null
  readonly code: string
  readonly details: unknown

  constructor(error: ApiErrorBody, status: number | null) {
    super(error.message)
    this.name = 'ApiRequestError'
    this.status = status
    this.code = error.code
    this.details = error.details
  }
}

export function normalizeApiError(error: unknown) {
  if (axios.isAxiosError<ApiErrorEnvelope>(error)) {
    const apiError = error.response?.data?.error

    if (apiError) {
      return new ApiRequestError(apiError, error.response?.status ?? null)
    }

    return new ApiRequestError(
      {
        code: 'http_error',
        message: error.message || 'Request failed.',
        details: error.response?.data ?? null,
      },
      error.response?.status ?? null,
    )
  }

  return new ApiRequestError(
    {
      code: 'unexpected_error',
      message: 'An unexpected error occurred.',
      details: error,
    },
    null,
  )
}
