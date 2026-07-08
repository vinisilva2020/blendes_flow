<script setup lang="ts">
import { shallowRef } from 'vue'
import { VueFlow, type Edge, type Node, type VueFlowStore } from '@vue-flow/core'

import CanvasActionsMenu from './components/CanvasActionsMenu.vue'
import CanvasBoardCard, { type CanvasBoardCardVariant } from './components/CanvasBoardCard.vue'

import '@vue-flow/core/dist/style.css'
import '@vue-flow/core/dist/theme-default.css'

type BoardNodeData = {
  content?: 'boundground' | 'labor'
  title: string
  variant: CanvasBoardCardVariant
}

type BoardNode = Node<BoardNodeData, any, 'board'>

const flowId = 'blendes-canvas'

function createBoardNode(
  id: string,
  position: { x: number; y: number },
  size: { width: number; height: number },
  data: BoardNodeData,
): BoardNode {
  return {
    id,
    type: 'board',
    position,
    width: size.width,
    height: size.height,
    data,
    draggable: false,
    connectable: false,
  }
}

const nodes = shallowRef<BoardNode[]>([
  createBoardNode(
    'gathering-phase',
    { x: 0, y: 0 },
    { width: 595, height: 60 },
    { title: 'Gathering', variant: 'phase' },
  ),
  createBoardNode(
    'analysis-phase',
    { x: 605, y: 0 },
    { width: 1190, height: 60 },
    { title: 'Analysis', variant: 'phase' },
  ),
  createBoardNode(
    'boundground',
    { x: 0, y: 80 },
    { width: 185, height: 170 },
    { title: 'B - Boundground', variant: 'section', content: 'boundground' },
  ),
  createBoardNode(
    'labor',
    { x: 0, y: 260 },
    { width: 260, height: 360 },
    { title: 'L - Labor', variant: 'section', content: 'labor' },
  ),
  createBoardNode(
    'echo',
    { x: 270, y: 80 },
    { width: 320, height: 500 },
    { title: 'E - Echo', variant: 'section' },
  ),
  createBoardNode(
    'noisecatch',
    { x: 605, y: 80 },
    { width: 485, height: 500 },
    { title: 'N - Noisecatch', variant: 'section' },
  ),
  createBoardNode(
    'drawbridge',
    { x: 1100, y: 80 },
    { width: 165, height: 500 },
    { title: 'D - Drawbridge', variant: 'section' },
  ),
  createBoardNode(
    'enhance',
    { x: 1275, y: 80 },
    { width: 360, height: 500 },
    { title: 'E - Enhance', variant: 'section' },
  ),
  createBoardNode(
    'sightline',
    { x: 1645, y: 80 },
    { width: 140, height: 500 },
    { title: 'S - Sightline', variant: 'section' },
  ),
])
const edges = shallowRef<Edge[]>([])

function fitCanvasOnInit(flow: VueFlowStore) {
  requestAnimationFrame(() => {
    void flow.fitView({
      maxZoom: 1,
      minZoom: 0.3,
      padding: 0.12,
    })
  })
}
</script>

<template>
  <main class="fixed inset-0 overflow-hidden bg-white" aria-label="Canvas workspace">
    <VueFlow
      :id="flowId"
      class="miro-canvas"
      :nodes="nodes"
      :edges="edges"
      :default-viewport="{ x: 0, y: 0, zoom: 1 }"
      :min-zoom="0.25"
      :max-zoom="2"
      :pan-on-drag="true"
      :zoom-on-scroll="true"
      :zoom-on-pinch="true"
      :zoom-on-double-click="false"
      :pan-on-scroll="false"
      :prevent-scrolling="true"
      :nodes-draggable="false"
      :nodes-connectable="false"
      :elements-selectable="false"
      :select-nodes-on-drag="false"
      :edges-focusable="false"
      :nodes-focusable="false"
      :disable-keyboard-a11y="true"
      @init="fitCanvasOnInit"
    >
      <template #node-board="{ data, dimensions }">
        <CanvasBoardCard
          :content="data.content"
          :height="dimensions.height"
          :title="data.title"
          :variant="data.variant"
          :width="dimensions.width"
        />
      </template>
    </VueFlow>

    <CanvasActionsMenu :flow-id="flowId" />
  </main>
</template>

<style scoped>
.miro-canvas {
  width: 100%;
  height: 100%;
  background-color: #ffffff;
  background-image: radial-gradient(circle, rgb(22 33 38 / 36%) 1.25px, transparent 1.25px);
  background-size: 24px 24px;
  cursor: grab;
}

.miro-canvas:active {
  cursor: grabbing;
}

.miro-canvas :deep(.vue-flow__pane) {
  cursor: inherit;
}

.miro-canvas :deep(.vue-flow__selectionpane) {
  cursor: inherit;
}

.miro-canvas :deep(.vue-flow__renderer) {
  width: 100%;
  height: 100%;
}

.miro-canvas :deep(.vue-flow__node) {
  cursor: inherit;
}

.miro-canvas :deep(.vue-flow__node-board) {
  background: transparent;
  border: 0;
  box-shadow: none;
  padding: 0;
}
</style>
