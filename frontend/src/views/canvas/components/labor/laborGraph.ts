import { Position, type Connection, type Styles } from '@vue-flow/core'

import type { LaborEdge, LaborExecutionType, LaborNode, LaborNodeKind } from './types'

const EXECUTOR_KINDS: LaborNodeKind[] = ['role', 'group']

export const initialLaborNodes: LaborNode[] = [
  {
    id: 'team-manager',
    type: 'labor-node',
    position: { x: 42, y: 18 },
    width: 132,
    height: 104,
    sourcePosition: Position.Bottom,
    data: {
      kind: 'role',
      label: 'Team Manager',
    },
    draggable: false,
    selectable: false,
    connectable: true,
    focusable: false,
  },
  {
    id: 'retrospective',
    type: 'labor-node',
    position: { x: 100, y: 176 },
    width: 248,
    height: 118,
    targetPosition: Position.Top,
    data: {
      kind: 'schapter',
      label: 'Conducao de retrospectiva',
    },
    draggable: false,
    selectable: false,
    connectable: true,
    focusable: false,
  },
  {
    id: 'team',
    type: 'labor-node',
    position: { x: 304, y: 374 },
    width: 124,
    height: 96,
    sourcePosition: Position.Top,
    data: {
      kind: 'group',
      label: 'Team',
    },
    draggable: false,
    selectable: false,
    connectable: true,
    focusable: false,
  },
]

export const getLaborEdgeStyle = (executionType: LaborExecutionType): Styles => ({
  stroke: 'var(--labor-edge)',
  strokeDasharray: executionType === 'indirect' ? '8 8' : undefined,
  strokeLinecap: 'round' as const,
  strokeWidth: 2.35,
})

export const createLaborEdge = (
  connection: Connection,
  executionType: LaborExecutionType,
): LaborEdge => ({
  ...connection,
  id: `${connection.source}-${connection.target}-${executionType}-${Date.now()}`,
  type: 'smoothstep',
  data: {
    executionType,
  },
  deletable: true,
  focusable: false,
  interactionWidth: 16,
  pathOptions: {
    borderRadius: 24,
    offset: 28,
  },
  selectable: true,
  style: getLaborEdgeStyle(executionType),
})

export const initialLaborEdges: LaborEdge[] = [
  createLaborEdge(
    {
      source: 'team-manager',
      target: 'retrospective',
      sourceHandle: 'executor-source-bottom',
      targetHandle: 'schapter-target-top',
    },
    'direct',
  ),
  createLaborEdge(
    {
      source: 'team',
      target: 'retrospective',
      sourceHandle: 'executor-source-top',
      targetHandle: 'schapter-target-bottom',
    },
    'indirect',
  ),
].map((edge, index) => ({
  ...edge,
  id: index === 0 ? 'team-manager-direct-retrospective' : 'team-indirect-retrospective',
}))

export const isExecutorKind = (kind: LaborNodeKind) => EXECUTOR_KINDS.includes(kind)

export const isValidLaborConnection = (connection: Connection, nodes: LaborNode[]): boolean => {
  if (!connection.source || !connection.target || connection.source === connection.target) {
    return false
  }

  const sourceNode = nodes.find((node) => node.id === connection.source)
  const targetNode = nodes.find((node) => node.id === connection.target)

  if (!sourceNode?.data || !targetNode?.data) {
    return false
  }

  return isExecutorKind(sourceNode.data.kind) && targetNode.data.kind === 'schapter'
}

export const getNextExecutionType = (executionType: LaborExecutionType): LaborExecutionType =>
  executionType === 'direct' ? 'indirect' : 'direct'

export const withExecutionType = (
  edge: LaborEdge,
  executionType: LaborExecutionType,
): LaborEdge => ({
  ...edge,
  data: {
    ...edge.data,
    executionType,
  },
  style: getLaborEdgeStyle(executionType),
})
