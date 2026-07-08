import type { Edge, Node } from '@vue-flow/core'

export type LaborExecutionType = 'direct' | 'indirect'

export type LaborNodeKind = 'role' | 'group' | 'schapter'

export type LaborNodeData = {
  kind: LaborNodeKind
  label: string
}

export type LaborEdgeData = {
  executionType: LaborExecutionType
}

export type LaborNode = Node<LaborNodeData, any, 'labor-node'>

export type LaborEdge = Edge<LaborEdgeData>
