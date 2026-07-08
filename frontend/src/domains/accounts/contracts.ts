import type { components } from '@/shared/api/schema'

export type Account = components['schemas']['AccountOutputSerializerV1']
export type AccountGoogleSocialAccountPayload =
  components['schemas']['AccountGoogleSocialAccountInputSerializerV1']
export type AccountRegistrationPayload =
  components['schemas']['AccountRegistrationInputSerializerV1']
export type AccountUpdatePayload = components['schemas']['PatchedAccountPartialInputSerializerV1']
export type AccountPasswordPayload = components['schemas']['AccountPasswordInputSerializerV1']
export type SocialAccount = components['schemas']['SocialAccountOutputSerializerV1']
