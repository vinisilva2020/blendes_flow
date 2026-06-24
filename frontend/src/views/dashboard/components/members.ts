export type MemberStatus = 'active' | 'pending'
export type MemberRole = 'Admin' | 'Manager' | 'Member'

export type OrganizationMember = {
  email: string
  id: number
  initials: string
  joinedAt: string
  lastActive: string
  name: string
  role: MemberRole
  status: MemberStatus
  team: string
  username: string
}
