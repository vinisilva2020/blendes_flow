<script setup lang="ts">
import { nextTick, onMounted, shallowRef } from 'vue'
import { LocateFixed, Minus, Plus } from '@lucide/vue'
import { MarkerType, Position, VueFlow, useVueFlow, type Edge, type Node } from '@vue-flow/core'
import '@vue-flow/core/dist/style.css'
import '@vue-flow/core/dist/theme-default.css'

import OrganizationFlowNode from './OrganizationFlowNode.vue'
import { organizationMap, type OrganizationNode } from './organization-map'

type FlowNodeData = {
  kind: OrganizationNode['kind']
  label: string
  owner?: string
}

const flowId = 'organization-flow-map'
const container = shallowRef<HTMLElement>()
const { fitView, zoomIn, zoomOut } = useVueFlow({ id: flowId })

function buildGraph(root: OrganizationNode) {
  const nodes: Node<FlowNodeData>[] = []
  const edges: Edge[] = []
  const departments = root.children ?? []
  const nodeWidth = 224
  const operationGap = 52
  const operationStep = nodeWidth + operationGap
  const departmentGap = operationStep * 2 + 8
  const totalWidth = Math.max(0, (departments.length - 1) * departmentGap)

  nodes.push({
    id: root.id,
    type: 'organization-node',
    position: { x: totalWidth / 2, y: 0 },
    sourcePosition: Position.Bottom,
    data: { kind: root.kind, label: root.name, owner: root.owner },
  })

  departments.forEach((department, departmentIndex) => {
    const departmentX = departmentIndex * departmentGap
    nodes.push({
      id: department.id,
      type: 'organization-node',
      position: { x: departmentX, y: 190 },
      sourcePosition: Position.Bottom,
      targetPosition: Position.Top,
      data: { kind: department.kind, label: department.name, owner: department.owner },
    })
    edges.push(createEdge(root.id, department.id, department.kind))

    const operations = department.children ?? []
    operations.forEach((operation, operationIndex) => {
      const offset = (operationIndex - (operations.length - 1) / 2) * operationStep
      nodes.push({
        id: operation.id,
        type: 'organization-node',
        position: { x: departmentX + offset, y: 390 },
        targetPosition: Position.Top,
        data: { kind: operation.kind, label: operation.name, owner: operation.owner },
      })
      edges.push(createEdge(department.id, operation.id, operation.kind))
    })
  })

  return { nodes, edges }
}

function createEdge(source: string, target: string, targetKind: OrganizationNode['kind']): Edge {
  return {
    id: `${source}-${target}`,
    source,
    target,
    type: 'smoothstep',
    animated: false,
    focusable: false,
    selectable: false,
    pathOptions: { borderRadius: 22, offset: 34 },
    markerEnd: { type: MarkerType.ArrowClosed, width: 14, height: 14, color: targetKind === 'operation' ? '#8b5cf6' : '#0891b2' },
    style: {
      stroke: targetKind === 'operation' ? '#8b5cf6' : '#0891b2',
      strokeWidth: 2,
    },
  }
}

const graph = buildGraph(organizationMap)
const nodes = shallowRef(graph.nodes)
const edges = shallowRef(graph.edges)

async function realign() {
  await nextTick()
  await fitView({ duration: 320, padding: 0.12, minZoom: 0.24, maxZoom: 1 })
}

onMounted(realign)
</script>

<template>
  <div ref="container" class="organization-flow-map">
    <VueFlow
      :id="flowId"
      v-model:nodes="nodes"
      v-model:edges="edges"
      :fit-view-on-init="true"
      :min-zoom="0.2"
      :max-zoom="1.8"
      :pan-on-drag="true"
      :zoom-on-scroll="true"
      :zoom-on-pinch="true"
      :zoom-on-double-click="true"
      :prevent-scrolling="true"
      :nodes-draggable="false"
      :nodes-connectable="false"
      :elements-selectable="false"
      :nodes-focusable="false"
      :edges-focusable="false"
      :disable-keyboard-a11y="true"
      @init="realign"
    >
      <template #node-organization-node="{ data }">
        <OrganizationFlowNode :data="data" />
      </template>
    </VueFlow>

    <div class="organization-flow-map__controls" aria-label="Map controls">
      <button type="button" aria-label="Zoom in" title="Zoom in" @click="zoomIn({ duration: 180 })">
        <Plus :size="17" :stroke-width="2.2" aria-hidden="true" />
      </button>
      <button type="button" aria-label="Zoom out" title="Zoom out" @click="zoomOut({ duration: 180 })">
        <Minus :size="17" :stroke-width="2.2" aria-hidden="true" />
      </button>
      <button type="button" aria-label="Reposition organization map" title="Reposition map" @click="realign">
        <LocateFixed :size="17" :stroke-width="2.2" aria-hidden="true" />
      </button>
    </div>

    <p class="organization-flow-map__hint">Drag to move · Scroll or pinch to zoom</p>
  </div>
</template>

<style scoped>
.organization-flow-map {
  position: relative;
  width: 100%;
  height: 100%;
  min-width: 0;
  min-height: 0;
  overflow: hidden;
  background-color: #f8fafc;
  background-image: radial-gradient(circle, rgb(148 163 184 / 32%) 1px, transparent 1px);
  background-size: 20px 20px;
}

.organization-flow-map :deep(.vue-flow),
.organization-flow-map :deep(.vue-flow__renderer),
.organization-flow-map :deep(.vue-flow__pane) {
  width: 100%;
  height: 100%;
}

.organization-flow-map :deep(.vue-flow__pane) {
  cursor: grab;
}

.organization-flow-map :deep(.vue-flow__pane:active) {
  cursor: grabbing;
}

.organization-flow-map :deep(.vue-flow__node) {
  border: 0;
  background: transparent;
  padding: 0;
  box-shadow: none;
}

.organization-flow-map :deep(.vue-flow__edge-path) {
  stroke-linecap: round;
  stroke-linejoin: round;
}

.organization-flow-map__controls {
  position: absolute;
  right: 16px;
  bottom: 16px;
  z-index: 10;
  display: flex;
  gap: 4px;
  padding: 4px;
  border-radius: 16px;
  background: rgb(255 255 255 / 92%);
  box-shadow: 0 8px 26px rgb(15 23 42 / 14%);
  backdrop-filter: blur(10px);
}

.organization-flow-map__controls button {
  display: grid;
  width: 40px;
  height: 40px;
  cursor: pointer;
  place-items: center;
  border: 0;
  border-radius: 12px;
  background: transparent;
  color: #475569;
  outline: none;
  transition-property: background-color, color, transform, box-shadow;
  transition-duration: 150ms;
}

.organization-flow-map__controls button:hover {
  background: #eff6ff;
  color: #1d4ed8;
}

.organization-flow-map__controls button:focus-visible {
  box-shadow: 0 0 0 4px rgb(219 234 254 / 90%);
}

.organization-flow-map__controls button:active {
  transform: scale(0.96);
}

.organization-flow-map__hint {
  position: absolute;
  bottom: 21px;
  left: 16px;
  z-index: 10;
  margin: 0;
  padding: 8px 11px;
  border-radius: 10px;
  background: rgb(255 255 255 / 88%);
  box-shadow: 0 3px 12px rgb(15 23 42 / 8%);
  color: #64748b;
  font-size: 11px;
  font-weight: 600;
  backdrop-filter: blur(8px);
}

:global(.dark) .organization-flow-map {
  background-color: #020617;
  background-image: radial-gradient(circle, rgb(100 116 139 / 28%) 1px, transparent 1px);
}

:global(.dark) .organization-flow-map__controls,
:global(.dark) .organization-flow-map__hint {
  background: rgb(15 23 42 / 90%);
  color: #94a3b8;
  box-shadow: 0 8px 28px rgb(0 0 0 / 30%);
}

:global(.dark) .organization-flow-map__controls button {
  color: #cbd5e1;
}

:global(.dark) .organization-flow-map__controls button:hover {
  background: rgb(59 130 246 / 12%);
  color: #93c5fd;
}

@media (max-width: 640px) {
  .organization-flow-map__controls {
    right: 10px;
    bottom: 10px;
  }

  .organization-flow-map__hint {
    top: 10px;
    bottom: auto;
    left: 10px;
  }
}

@media (prefers-reduced-motion: reduce) {
  .organization-flow-map__controls button {
    transition: none;
  }
}
</style>
