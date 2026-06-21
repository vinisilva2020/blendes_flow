import type { components } from '@/shared/api/schema'

export type Organization = components['schemas']['OrganizationOutputSerializerV1']
export type NewOrganization = components['schemas']['OrganizationInputSerializerV1']
export type OrganizationChanges =
  components['schemas']['PatchedOrganizationPartialInputSerializerV1']
