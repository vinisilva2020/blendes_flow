import type { components } from '@/shared/api/schema'

export type BlaveMovement = components['schemas']['BlaveMovementOutputSerializerV1']
export type BlaveMovementName = components['schemas']['MovementEnum']
export type BlaveMovementStatus = components['schemas']['BlaveMovementOutputSerializerV1StatusEnum']
export type NewBlave = components['schemas']['BlaveInputSerializerV1']
export type UpdateBlave = components['schemas']['PatchedBlavePartialInputSerializerV1']

type GeneratedBlave = components['schemas']['BlaveOutputSerializerV1']

export type Blave = Omit<GeneratedBlave, 'description' | 'movement_statuses'> & {
  created_by_user?: number
  description?: string | null
  movement_statuses?: BlaveMovement[]
  movements?: BlaveMovement[]
  organization?: number
}

export function getBlaveMovements(blave: Blave) {
  return blave.movement_statuses ?? blave.movements ?? []
}
