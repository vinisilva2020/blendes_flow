import type { components } from '@/shared/api/schema'

export type LoginCredentials = components['schemas']['LoginInputSerializerV1']
export type AuthenticationTokens = components['schemas']['AuthenticationOutputSerializerV1']
export type AuthenticationSession = components['schemas']['AuthenticationSessionOutputSerializerV1']
export type RefreshTokenPayload = components['schemas']['RefreshTokenInputSerializerV1']
export type ApiErrorEnvelope = components['schemas']['APIErrorSerializerV1']
