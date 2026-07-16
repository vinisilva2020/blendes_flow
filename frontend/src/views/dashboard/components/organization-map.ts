export type OrganizationNodeKind = 'organization' | 'department' | 'operation'

export type OrganizationNode = {
  id: string
  name: string
  kind: OrganizationNodeKind
  owner?: string
  children?: OrganizationNode[]
}

export const organizationMap: OrganizationNode = {
  id: 'blendes',
  name: 'Blendes',
  kind: 'organization',
  owner: 'Executive office',
  children: [
    {
      id: 'operations',
      name: 'Operations',
      kind: 'department',
      owner: 'Marina Costa',
      children: [
        { id: 'fulfillment', name: 'Order fulfillment', kind: 'operation', owner: '8 mapped steps' },
        { id: 'quality', name: 'Quality assurance', kind: 'operation', owner: '5 mapped steps' },
      ],
    },
    {
      id: 'customer',
      name: 'Customer experience',
      kind: 'department',
      owner: 'Rafael Lima',
      children: [
        { id: 'onboarding', name: 'Customer onboarding', kind: 'operation', owner: '6 mapped steps' },
        { id: 'support', name: 'Service recovery', kind: 'operation', owner: '4 mapped steps' },
      ],
    },
    {
      id: 'finance',
      name: 'Finance & strategy',
      kind: 'department',
      owner: 'Camila Rocha',
      children: [
        { id: 'planning', name: 'Quarterly planning', kind: 'operation', owner: '7 mapped steps' },
        { id: 'procurement', name: 'Strategic procurement', kind: 'operation', owner: '5 mapped steps' },
      ],
    },
  ],
}
