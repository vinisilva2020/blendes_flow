<script setup lang="ts">
import { shallowRef } from 'vue'
import { VueFlow, type Connection, type EdgeMouseEvent, type VueFlowStore } from '@vue-flow/core'

import LaborGraphNode from './labor/LaborGraphNode.vue'
import {
  createLaborEdge,
  getNextExecutionType,
  initialLaborEdges,
  initialLaborNodes,
  isValidLaborConnection,
  withExecutionType,
} from './labor/laborGraph'
import type { LaborEdge, LaborNode } from './labor/types'

const nodes = shallowRef<LaborNode[]>(initialLaborNodes)
const edges = shallowRef<LaborEdge[]>(initialLaborEdges)

const fitLaborMap = (flow: VueFlowStore) => {
  requestAnimationFrame(() => {
    flow.fitView({
      duration: 260,
      maxZoom: 0.95,
      minZoom: 0.35,
      padding: 0.16,
    })
  })
}

const isValidConnection = (connection: Connection) =>
  isValidLaborConnection(connection, nodes.value)

const onConnect = (connection: Connection) => {
  if (!isValidConnection(connection)) {
    return
  }

  const connectionAlreadyExists = edges.value.some(
    (edge) => edge.source === connection.source && edge.target === connection.target,
  )

  if (connectionAlreadyExists) {
    return
  }

  edges.value = [...edges.value, createLaborEdge(connection, 'direct')]
}

const toggleEdgeExecution = (edgeId: string) => {
  edges.value = edges.value.map((edge) => {
    if (edge.id !== edgeId) {
      return edge
    }

    const nextExecutionType = getNextExecutionType(edge.data?.executionType ?? 'direct')
    return withExecutionType(edge, nextExecutionType)
  })
}

const onEdgeDoubleClick = ({ edge }: EdgeMouseEvent) => {
  toggleEdgeExecution(edge.id)
}
</script>

<template>
  <VueFlow
    id="labor-execution-map"
    v-model:nodes="nodes"
    v-model:edges="edges"
    class="labor-map"
    :fit-view-on-init="true"
    :min-zoom="0.28"
    :max-zoom="1.25"
    :pan-on-drag="true"
    :zoom-on-scroll="true"
    :zoom-on-pinch="true"
    :zoom-on-double-click="false"
    :prevent-scrolling="true"
    :nodes-draggable="false"
    :nodes-connectable="true"
    :elements-selectable="false"
    :select-nodes-on-drag="false"
    :auto-pan-on-node-drag="false"
    :edges-focusable="false"
    :nodes-focusable="false"
    :disable-keyboard-a11y="true"
    :auto-connect="false"
    :is-valid-connection="isValidConnection"
    @connect="onConnect"
    @edge-double-click="onEdgeDoubleClick"
    @init="fitLaborMap"
  >
    <template #node-labor-node="{ data, selected }">
      <LaborGraphNode :data="data" :selected="selected" />
    </template>
  </VueFlow>
</template>

<style scoped>
.labor-map {
  --labor-bg: #f8f8f6;
  --labor-grid-major: rgb(0 0 0 / 5%);
  --labor-grid-minor: rgb(0 0 0 / 3.2%);
  --labor-edge: #272727;

  width: 100%;
  height: 100%;
  min-width: 0;
  min-height: 0;
  background:
    linear-gradient(var(--labor-grid-major) 1px, transparent 1px),
    linear-gradient(90deg, var(--labor-grid-major) 1px, transparent 1px),
    linear-gradient(var(--labor-grid-minor) 1px, transparent 1px),
    linear-gradient(90deg, var(--labor-grid-minor) 1px, transparent 1px), var(--labor-bg);
  background-position:
    -1px -1px,
    -1px -1px,
    -1px -1px,
    -1px -1px;
  background-size:
    80px 80px,
    80px 80px,
    20px 20px,
    20px 20px;
  color: #1f1f1f;
}

.labor-map :deep(.vue-flow__pane) {
  cursor: grab;
}

.labor-map :deep(.vue-flow__pane:active) {
  cursor: grabbing;
}

.labor-map :deep(.vue-flow__renderer),
.labor-map :deep(.vue-flow__pane) {
  width: 100%;
  height: 100%;
}

.labor-map :deep(.vue-flow__node) {
  border: 0;
  background: transparent;
  box-shadow: none;
  color: inherit;
  padding: 0;
}

.labor-map :deep(.vue-flow__node.selected) {
  box-shadow: none;
}

.labor-map :deep(.vue-flow__edge-path),
.labor-map :deep(.vue-flow__connection-path) {
  stroke-linecap: round;
}

.labor-map :deep(.vue-flow__edge.selected .vue-flow__edge-path) {
  stroke-width: 3;
}
</style>
